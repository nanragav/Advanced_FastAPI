from fastapi import Request, Response, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from .token import decode_access_token, decode_refresh_token, create_access_token
import logging
from utils.time_setting import get_current_time_with_tz, get_access_cookie_expire
from datetime import datetime, UTC
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from uuid import UUID
from sqlalchemy import select
from models import User

logger = logging.getLogger(__name__)

async def clear_cookie(response: Response):

    response.delete_cookie(key='access_token', path='/', domain='127.0.0.1')
    response.delete_cookie(key='refresh_token', path='/', domain='127.0.0.1')
    return JSONResponse(status_code=401, content={'detail': 'Authentication Failed'})

async def get_user_by_id(id: UUID, session_id: UUID, db: AsyncSession, response: Response):

    try:

        stmt = select(User).where(User.id == id)

        result = await db.execute(stmt)

        user = result.scalar_one_or_none()

        if not user:

            return await clear_cookie(response=response)

        if user.session_id != session_id:

            return await clear_cookie(response=response)

        return user

    except SQLAlchemyError as se:

        logger.error(f'Error when getting the user {se}')

        return await clear_cookie(response=response)

    except Exception as e:

        logger.error(f'Unknown Error when getting the user {e}')

        return await clear_cookie(response=response)

async def user_token(request: Request, response: Response):

    try:

        access_token = request.cookies.get('access_token')

        refresh_token = request.cookies.get('refresh_token')

        if not access_token or not refresh_token:

            return await clear_cookie(response=response)

        access_token_decoded = None

        refresh_token_decoded = None

        try:

            access_token_decoded = await decode_access_token(access_token)

        except Exception as e:

            logger.error(f'Error in Access Token Decode {e}')

        try:

            refresh_token_decoded = await decode_refresh_token(refresh_token)

        except Exception as e:

            logger.error(f'Error in Refresh Token Decode')

        now = await get_current_time_with_tz()

        if access_token_decoded:

            expire = datetime.fromtimestamp(access_token_decoded['exp'], tz=UTC)

            if expire > now:

                return ('access', access_token_decoded)

        if refresh_token_decoded:

            expire = datetime.fromtimestamp(refresh_token_decoded['exp'], tz=UTC)

            if expire > now:

                return ('refresh', refresh_token_decoded)

        return await clear_cookie(response=response)

    except Exception as e:

        logger.error(f'Unknown Error in getting the token {e}')

        return await clear_cookie(response=response)

async def get_user(response: Response, db: AsyncSession = Depends(get_db), token = Depends(user_token)):

    user_token = token

    if isinstance(user_token, JSONResponse):

        return user_token

    token_source, decoded_token = token

    user = await get_user_by_id(id=UUID(decoded_token['id']), session_id=UUID(decoded_token['session_id']), db=db, response=response)

    if isinstance(user, JSONResponse):

        return user

    if token_source == 'refresh':

        data = {
            'id': user.id,
            'session_id': user.session_id,
            'name': user.name
        }

        new_access_token = await create_access_token(data=data)

        expire = get_access_cookie_expire()

        response.set_cookie(key='access_token', value=new_access_token, path='/', domain='127.0.0.1', expires=expire)

        return user

    return user



