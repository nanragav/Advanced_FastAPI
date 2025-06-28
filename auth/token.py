from fastapi import HTTPException
from typing import Optional
from utils.time_setting import get_current_time_with_tz
from datetime import timedelta
from dotenv import load_dotenv
import os
from jose import jwt, JWTError
import logging

logger = logging.getLogger(__name__)

load_dotenv()

ACCESS_TOKEN_EXPIRE = int(os.getenv('ACCESS_TOKEN_EXPIRE'))

REFRESH_TOKEN_EXPIRE = int(os.getenv('REFRESH_TOKEN_EXPIRE'))

USER_ACCESS_TOKEN_SECRET = os.getenv('USER_ACCESS_TOKEN_SECRET')

USER_REFRESH_TOKEN_SECRET = os.getenv('USER_REFRESH_TOKEN_SECRET')

BLOG_ACCESS_TOKEN_SECRET = os.getenv('BLOG_ACCESS_TOKEN_SECRET')

BLOG_REFRESH_TOKEN_SECRET = os.getenv('BLOG_REFRESH_TOKEN_SECRET')

ALGORITHM = os.getenv('ALGORITHM')


async def create_user_access_token(data: dict, expires: Optional[int] = None):

    try:

        to_encode = data.copy()

        if not expires:

            expire = await get_current_time_with_tz() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

        else:

            expire = await get_current_time_with_tz() + timedelta(minutes=expires)

        to_encode.update({'exp': expire})

        return jwt.encode(to_encode, key=USER_ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)

    except JWTError as je:

        logger.error(f'Error in user access token creation {je}')

        raise HTTPException(status_code=500, detail='Error while creating the user access token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in user access token creation {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')


async def create_user_refresh_token(data: dict, expires: Optional[int] = None):

    try:

        to_encode = data.copy()

        if not expires:

            expire = await get_current_time_with_tz() + timedelta(days=ACCESS_TOKEN_EXPIRE)

        else:

            expire = await get_current_time_with_tz() + timedelta(days=expires)

        to_encode.update({'exp': expire})

        return jwt.encode(to_encode, key=USER_REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)

    except JWTError as je:

        logger.error(f'Error in user refresh token creation {je}')

        raise HTTPException(status_code=500, detail='Error while creating the user refresh token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in user refresh token creation {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

async def decode_user_access_token(token: str):

    try:

        if not token is None:

            return jwt.decode(token,key=USER_ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])

        else:

            raise HTTPException(status_code=401, detail='Error when getting the user access token')

    except JWTError as je:

        if 'signature has expired' in str(je).lower():

            return None

        logger.error(f'Error in user access token decode {je}')

        raise HTTPException(status_code=500, detail='Error while decoding the user access token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in access token decode {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

async def decode_user_refresh_token(token: str):

    try:

        if not token is None:

            return jwt.decode(token=token, key=USER_REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])

        else:

            raise HTTPException(status_code=401, detail='Error when getting the user refresh token')

    except JWTError as je:

        if 'signature has expired' in str(je).lower():

            return None

        logger.error(f'Error in user refresh token decode {je}')

        raise HTTPException(status_code=500, detail='Error while decoding the user refresh token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in user refresh token decode {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

async def create_blog_access_token(data: dict, expires: Optional[int] = None):

    try:

        to_encode = data.copy()

        if not expires:

            expire = await get_current_time_with_tz() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

        else:

            expire = await get_current_time_with_tz() + timedelta(minutes=expires)

        to_encode.update({'exp': expire})

        return jwt.encode(to_encode, key=BLOG_ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)

    except JWTError as je:

        logger.error(f'Error in blog access token creation {je}')

        raise HTTPException(status_code=500, detail='Error while creating the blog access token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in blog access token creation {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')


async def create_blog_refresh_token(data: dict, expires: Optional[int] = None):

    try:

        to_encode = data.copy()

        if not expires:

            expire = await get_current_time_with_tz() + timedelta(days=ACCESS_TOKEN_EXPIRE)

        else:

            expire = await get_current_time_with_tz() + timedelta(days=expires)

        to_encode.update({'exp': expire})

        return jwt.encode(to_encode, key=BLOG_REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)

    except JWTError as je:

        logger.error(f'Error in blog refresh token creation {je}')

        raise HTTPException(status_code=500, detail='Error while creating the blog refresh token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in blog refresh token creation {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

async def decode_blog_access_token(token: str):

    try:

        if not token is None:

            return jwt.decode(token,key=BLOG_ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])

        else:

            raise HTTPException(status_code=401, detail='Error when getting the blog access token')

    except JWTError as je:

        if 'signature has expired' in str(je).lower():

            return None

        logger.error(f'Error in blog access token decode {je}')

        raise HTTPException(status_code=500, detail='Error while decoding the blog access token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in blog access token decode {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

async def decode_blog_refresh_token(token: str):

    try:

        if not token is None:

            return jwt.decode(token=token, key=BLOG_REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])

        else:

            raise HTTPException(status_code=401, detail='Error when getting the blog refresh token')

    except JWTError as je:

        if 'signature has expired' in str(je).lower():

            return None

        logger.error(f'Error in refresh token decode {je}')

        raise HTTPException(status_code=500, detail='Error while decoding the blog refresh token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in blog refresh token decode {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')