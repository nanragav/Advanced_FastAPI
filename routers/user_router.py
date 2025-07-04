from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi.responses import JSONResponse
from schemas import LoginUserRequest, CreateUserRequest, DeleteUserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from utils.user_utils import user_login, user_logout, create_new_user, delete_current_user
import logging
from utils.time_setting import get_access_cookie_expire, get_refresh_cookie_expire
from auth.dependencies import get_user
from auth.dependencies import clear_cookie
from models import User

logger = logging.getLogger(__name__)

router = APIRouter(tags=['User'])

@router.post('/login')
async def login(request: LoginUserRequest, response: Response, db: AsyncSession = Depends(get_db)):

    try:

        access_token, refresh_token = await user_login(request=request, db=db)

        if not access_token:

            raise HTTPException(status_code=500, detail='Access Token Creation Failed')

        if not refresh_token:

            raise HTTPException(status_code=500, detail="Refresh Token Creation Failed")

        access_cookie_expire = await get_access_cookie_expire()

        refresh_cookie_expire = await get_refresh_cookie_expire()

        response.set_cookie(key='access_token', value=access_token, httponly=True, path='/', expires=access_cookie_expire, domain='127.0.0.1', secure=True)

        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, path='/', expires=refresh_cookie_expire, domain='127.0.0.1', secure=True)

        return {'message': 'Login Successful'}

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error in Login Endpoint {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')


@router.post('/logout')
async def logout(response: Response, db: AsyncSession = Depends(get_db), user = Depends(get_user)):

    try:

        if isinstance(user, JSONResponse):

            response.status_code = 401

            return {'message': "Not Authenticated"}

        status = await user_logout(response=response, db=db, current_user=user)

        if isinstance(status, JSONResponse):

            await clear_cookie(response=response)

            response.status_code = 401

            return {'message': 'Error, Logged out Forcefully'}

        if status:

            await clear_cookie(response=response)

            return {'message': 'Logged Out Successfully'}

        await clear_cookie(response=response)

        response.status_code = 401

        return {'message': 'Error, Logged out Forcefully'}

    except Exception as e:

        logger.error(f'Unknown Error in Logout Endpoint {e}')

        await clear_cookie(response=response)

        response.status_code = 401

        return {'message': 'Error, Logged out Forcefully'}

@router.post('/create-user')
async def create_user(request: CreateUserRequest, response: Response, db: AsyncSession = Depends(get_db), user = Depends(get_user)):

    try:

        if isinstance(user, JSONResponse):

            response.status_code = 401

            return {'message': 'Unauthorized to access this endpoint'}

        new_user = await create_new_user(request=request, db=db, current_user=user)

        return {f'message': f'User Created Successfully with id: {new_user.id} and name: {new_user.name}'}

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error in Logout Endpoint {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

@router.delete('/delete-user')
async def delete_user(response: Response, db: AsyncSession = Depends(get_db), user = Depends(get_user)):

    try:

        if isinstance(user, JSONResponse):

            response.status_code = 401

            return {'message': 'Unauthorized to access this endpoint'}

        status = await delete_current_user(current_user=user, db=db)

        if status:

            await clear_cookie(response=response)

            return {'message': "Your account deleted"}

        await db.rollback()

        return {'message': 'Deletion Failed'}

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error while deleting the user {e}')

        await db.rollback()

        raise HTTPException(status_code=500, detail='Error when removing your account')

