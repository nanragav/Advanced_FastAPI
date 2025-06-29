from fastapi import APIRouter, Depends, HTTPException, Response, Request
from starlette.responses import JSONResponse

from schemas import LoginUserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from utils.user_utils import user_login, user_logout
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

        response.set_cookie(key='access_token', value=access_token, httponly=True, path='/', expires=access_cookie_expire, domain='127.0.0.1')

        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, path='/', expires=refresh_cookie_expire, domain='127.0.0.1')

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

            return {'message': "Authentication Failed. Logging Out"}

        status = await user_logout(response=response, db=db, current_user=user)

        if isinstance(status, JSONResponse):

            await clear_cookie(response=response)

            return {'message': 'Error, Logged out Forcefully'}

        if status:

            await clear_cookie(response=response)

            return {'message': 'Logged Out Successfully'}

        await clear_cookie(response=response)

        return {'message': 'Error, Logged out Forcefully'}

    except Exception as e:

        logger.error(f'Unknown Error in Logout Endpoint {e}')

        await clear_cookie(response=response)

        return {'message': 'Error, Logged out Forcefully'}