from fastapi import APIRouter, Depends, HTTPException, Response, Request
from schemas import LoginUserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from utils.user_utils import user_login
import logging
from utils.time_setting import get_access_cookie_expire, get_refresh_cookie_expire
from auth.dependencies import get_current_user
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

        response.set_cookie(key='access_token', value=access_token, httponly=True, path='/', expires=access_cookie_expire, domain='127.0.0.1')

        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, path='/', expires=refresh_cookie_expire, domain='127.0.0.1')

        return {'message': 'Login Successful'}

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown Error in Login Endpoint {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')


@router.post('/logout')
async def logout(request: Request, response: Response, user: dict = Depends(get_current_user)):

    return user