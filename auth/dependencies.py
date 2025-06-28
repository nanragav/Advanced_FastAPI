from fastapi import Request, Response, Depends, HTTPException
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from .token import decode_access_token, decode_refresh_token, create_access_token
from utils.time_setting import get_access_cookie_expire
import logging
from fastapi.responses import JSONResponse
from datetime import datetime, UTC
from uuid import UUID, uuid4
from models import User
from sqlalchemy import select
from  sqlalchemy.exc import SQLAlchemyError



logger = logging.getLogger(__name__)

async def clear_old_cookies(response: Response):

    try:

        response.delete_cookie(key='access_token', path='/', domain='127.0.0.1')

        response.delete_cookie(key='refresh_token', path='/', domain='127.0.0.1')

    except Exception as e:

        logger.error(f'Error in cookie deletion {e}')

        raise HTTPException(status_code=404, detail='Error while removing cookie')

async def clear_cookie_and_error(response: Response, status_code: int, detail: str):

    await clear_old_cookies(response=response)

    return JSONResponse(status_code=status_code, content={'detail':detail}, headers=response.headers)

async def get_user_by_id(id: UUID, db: AsyncSession, response: Response):

    try:

        stmt = select(User).where(User.id == id)

        result = await db.execute(stmt)

        user = result.scalar_one_or_none()

        if not user:

            return clear_cookie_and_error(status_code=404, response=response, detail='User not found')

        return user

    except SQLAlchemyError as se:

        logger.error(f'Error in getting user {se}')

        return clear_cookie_and_error(response=response, status_code=500, detail='Error while getting user')

    except Exception as e:

        logger.error(f'Unknown error while getting the user {e}')

        return clear_cookie_and_error(response=response, status_code=500, detail='Cant retrive the information')


async def get_current_user(request: Request, response: Response, db: AsyncSession = Depends(get_db)):

    try:

        access_token = request.cookies.get('access_token')

        refresh_token = request.cookies.get('refresh_token')

        if not access_token or not refresh_token:

            return await clear_cookie_and_error(response=response,status_code=401, detail='Not Authenticated')

        try:

            access_token_decoded = await decode_access_token(access_token)

        except HTTPException as he:

            logger.error(f'Error in User access token decoding {he}')

            return await clear_cookie_and_error(response=response, status_code=401, detail='Invalid or Expired Token')

        except Exception as e:

            logger.error(f'Unknown error in user access token decode {e}')

            return await clear_cookie_and_error(response=response, status_code=401, detail='Invalid or Tampered Token')

        try:

            refresh_token_decoded = await decode_refresh_token(refresh_token)

        except HTTPException as he:

            logger.error(f'Error in User access token decoding {he}')

            return await clear_cookie_and_error(response=response, status_code=401, detail='Invalid or Expired Token')

        except Exception as e:

            logger.error(f'Unknown error in user access token decode {e}')

            return await clear_cookie_and_error(response=response, status_code=401, detail='Invalid or Tampered Token')

        access_token_expire = access_token_decoded['exp']

        refresh_token_expire = refresh_token_decoded['exp']

        if datetime.fromtimestamp(refresh_token_expire, tz=UTC) > datetime.now(UTC):

            if datetime.fromtimestamp(access_token_expire, tz=UTC) > datetime.now(UTC):

                user = await get_user_by_id(id=UUID(access_token_decoded['id']), db=db, response=response)

                return user

            else:

                user = await get_user_by_id(id=UUID(refresh_token_decoded['id']), db=db, response=response)

                user.session_id = uuid4()

                db.add(user)

                await db.commit()

                await db.refresh(user)

                data = {'id': str(user.id), 'session_id': str(user.session_id), 'name': user.name}

                new_access_token = await create_access_token(data=data)

                expire = await get_access_cookie_expire()

                response.set_cookie(key='access_token', value=new_access_token, path='/', domain='127.0.0.1', expires=expire)

                return user

        else:

            return await clear_cookie_and_error(response=response, status_code=401, detail='Token Expired')

    except HTTPException as he:

        raise he

    except Exception as e:

        raise HTTPException(status_code=401, detail='Error while getting the user')

