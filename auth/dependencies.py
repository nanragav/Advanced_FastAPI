from fastapi import HTTPException, Request, Depends, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from datetime import datetime, UTC
from .token import decode_user_access_token, decode_user_refresh_token, decode_blog_access_token, decode_blog_refresh_token, create_user_access_token, create_blog_access_token
from sqlalchemy import select
from models import User
from uuid import UUID, uuid4
from sqlalchemy.exc import SQLAlchemyError
import logging
from utils.time_setting import get_access_cookie_expire

logger = logging.getLogger(__name__)

async def get_user_by_id(id: UUID, db: AsyncSession, response: Response):

    try:

        stmt = select(User).where(User.id == id)

        result = await db.execute(stmt)

        user = result.scalar_one_or_none()

        if not user:

            response.delete_cookie(key='user_access_token', path='/user', domain='127.0.0.1')

            response.delete_cookie(key='user_refresh_token', path='/user', domain='127.0.0.1')

            response.delete_cookie(key='blog_access_token', path='/blog', domain='127.0.0.1')

            response.delete_cookie(key='blog_refresh_token', path='blog', domain='127.0.0.1')

            raise HTTPException(status_code=404, detail='User not found')

        return user

    except SQLAlchemyError as se:

        logger.error(f'Error when getting the user {se}')

        raise HTTPException(status_code=500, detail='Error when getting the user')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error when getting the user by id {e}')

        raise HTTPException(status_code=500, detail='Error when getting the user')

async def generate_new_access_token(data: dict):

    try:

        new_user_access_token = await create_user_access_token(data=data)

        new_blog_access_token = await create_blog_access_token(data=data)

        if not new_user_access_token or not new_blog_access_token:

            raise HTTPException(status_code=500, detail='Error when refreshing the token')

        return new_user_access_token, new_blog_access_token

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error when refreshing access token {e}')

        raise HTTPException(status_code=500, detail='Error when refreshing access token')

async def clear_old_cookies(response: Response):

    try:
        response.delete_cookie(key='user_access_token', path='/user', domain='127.0.0.1')

        response.delete_cookie(key='user_refresh_token', path='/user', domain='127.0.0.1')

        response.delete_cookie(key='blog_access_token', path='/blog', domain='127.0.0.1')

        response.delete_cookie(key='blog_refresh_token', path='/blog', domain='127.0.0.1')

        return True

    except Exception as e:

        raise HTTPException(status_code=500, detail='Cannot remove cookies')

async def get_current_user(response: Response, request: Request, db: AsyncSession = Depends(get_db)):

    try:

        user_access_token = request.cookies.get('user_access_token')

        user_refresh_token = request.cookies.get('user_refresh_token')

        if not user_access_token or not user_refresh_token:

            raise HTTPException(status_code=401, detail='Not authenticated')

        user_access_token_decoded = await decode_user_access_token(user_access_token)

        user_refresh_token_decoded = await decode_user_refresh_token(user_refresh_token)

        if user_refresh_token_decoded is not None:

            user_refresh_token_expire = user_refresh_token_decoded['exp']

            if datetime.fromtimestamp(user_refresh_token_expire, tz=UTC) > datetime.now(UTC):

                if user_access_token_decoded is not None:

                    user_access_token_expire = user_access_token_decoded['exp']

                    if datetime.fromtimestamp(user_access_token_expire, tz=UTC) > datetime.now(UTC):

                        user = await get_user_by_id(id=UUID(user_access_token_decoded['id']), db=db, response=response)

                        return user

                    else:

                        user = await get_user_by_id(id=UUID(user_refresh_token_decoded['id']), db=db, response=response)

                        if user.session_id == UUID(user_refresh_token_decoded['session_id']):

                            user.session_id = uuid4()

                            db.add(user)

                            await db.commit()

                            await db.refresh(user)

                            data = {'id': str(user.id), 'name': user.name, 'session_id': str(user.session_id)}

                            new_user_access_token, new_blog_access_token = await generate_new_access_token(data=data)

                            access_expire = await get_access_cookie_expire()

                            response.set_cookie(key='user_access_token', value=new_user_access_token, path='/user',
                                                domain='127.0.0.1', expires=access_expire)

                            response.set_cookie(key='blog_access_token', value=new_blog_access_token, path='/blog',
                                                domain='127.0.0.1', expires=access_expire)

                            return user

                        else:

                            user.session_id = uuid4()

                            db.add(user)

                            await db.commit()

                            await db.refresh(user)

                            status = await clear_old_cookies(response=response)

                            if not status:
                                raise HTTPException(status_code=500, detail='Unable to remove cookies')

                            raise HTTPException(status_code=401, detail='Invalid Session')


                else:
                    user = await get_user_by_id(id= UUID(user_refresh_token_decoded['id']), db=db, response=response)

                    if user.session_id == UUID(user_refresh_token_decoded['session_id']):

                        user.session_id = uuid4()

                        db.add(user)

                        await db.commit()

                        await db.refresh(user)

                        data = {'id': str(user.id), 'name':user.name, 'session_id': str(user.session_id)}

                        new_user_access_token, new_blog_access_token = await generate_new_access_token(data=data)

                        access_expire = await get_access_cookie_expire()

                        response.set_cookie(key='user_access_token', value=new_user_access_token, path='/user',
                                            domain='127.0.0.1', expires=access_expire)

                        response.set_cookie(key='blog_access_token', value=new_blog_access_token, path='/blog',
                                            domain='127.0.0.1', expires=access_expire)

                        return user

                    else:

                        user.session_id = uuid4()

                        db.add(user)

                        await db.commit()

                        await db.refresh(user)

                        status = await clear_old_cookies(response=response)

                        if not status:

                            raise HTTPException(status_code=500, detail='Unable to remove cookies')

                        raise HTTPException(status_code=401, detail='Invalid Session')

            else:

                status = await clear_old_cookies(response=response)

                if not status:

                    raise HTTPException(status_code=500, detail='Unable to remove cookies')

                raise HTTPException(status_code=401, detail='Access Denied')

        else:

            status = await clear_old_cookies(response=response)

            if not status:

                raise HTTPException(status_code=500, detail='Unable to remove cookies')

            raise HTTPException(status_code=401, detail='Access Denied')

    except SQLAlchemyError as se:

        logger.error(f'Error when analysing the token {se}')

        raise HTTPException(status_code=500, detail='Error when getting the user token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error in current user getting {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')
