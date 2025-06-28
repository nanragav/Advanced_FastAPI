from fastapi import APIRouter, Depends, HTTPException, Response, Request
from schemas import LoginUserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from utils.user_utils import user_login, user_logout
import logging
from utils.time_setting import get_access_cookie_expire, get_refresh_cookie_expire
from auth.dependencies import get_current_user
from models import User

logger = logging.getLogger(__name__)

router = APIRouter(tags=['User'])

@router.post('/login')
async def login(request: LoginUserRequest, response: Response, db: AsyncSession = Depends(get_db)):

    try:

        user_access_token, user_refresh_token, blog_access_token, blog_refresh_token  = await user_login(request=request, db=db)

        if not user_access_token:

            raise HTTPException(status_code=500, detail='Access Token Creation Failed')

        if not user_refresh_token:

            raise HTTPException(status_code=500, detail="Refresh Token Creation Failed")

        if not blog_access_token:

            raise HTTPException(status_code=500, detail='Access Token Creation Failed')

        if not blog_refresh_token:

            raise HTTPException(status_code=500, detail="Refresh Token Creation Failed")

        access_cookie_expire = await get_access_cookie_expire()

        refresh_cookie_expire = await get_refresh_cookie_expire()

        response.set_cookie(key='user_access_token', value=user_access_token, httponly=True, path='/user', expires=access_cookie_expire, domain='127.0.0.1')

        response.set_cookie(key='blog_access_token', value=blog_access_token, httponly=True, path='/blog', expires=access_cookie_expire, domain='127.0.0.1')

        response.set_cookie(key='user_refresh_token', value=user_refresh_token, httponly=True, path='/user', expires=refresh_cookie_expire, domain='127.0.0.1')

        response.set_cookie(key='blog_refresh_token', value=blog_refresh_token, httponly=True, path='/blog', expires=refresh_cookie_expire, domain='127.0.0.1')

        return {'message': 'Login Successful'}

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error in Login Endpoint {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

@router.post('/user/logout')
async def logout(response: Response, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    try:

        status = await user_logout(response=response, db=db, current_user=current_user)

        if status:

            return {'message': 'Logged out successfully'}

        else:

            raise HTTPException(status_code=500, detail='Error while removing the cookie')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error in Logout Endpoint {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')




