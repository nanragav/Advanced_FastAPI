from fastapi import HTTPException, status
from typing import Optional
from utils.time_setting import get_current_time_with_tz
from datetime import timedelta
from dotenv import load_dotenv
import os
from jose import jwt, JWTError, ExpiredSignatureError
import logging

logger = logging.getLogger(__name__)

load_dotenv()

ACCESS_TOKEN_EXPIRE = int(os.getenv('ACCESS_TOKEN_EXPIRE'))

REFRESH_TOKEN_EXPIRE = int(os.getenv('REFRESH_TOKEN_EXPIRE'))

ACCESS_TOKEN_SECRET = str(os.getenv('USER_ACCESS_TOKEN_SECRET'))

REFRESH_TOKEN_SECRET = str(os.getenv('USER_REFRESH_TOKEN_SECRET'))

ALGORITHM = str(os.getenv('ALGORITHM'))


async def create_access_token(data: dict, expires: Optional[int] = None):

    try:

        to_encode = data.copy()

        if not expires:

            expire = await get_current_time_with_tz() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)

        else:

            expire = await get_current_time_with_tz() + timedelta(minutes=expires)

        to_encode.update({'exp': expire})

        return jwt.encode(to_encode, key=ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)

    except JWTError as je:

        logger.error(f'Error in access token creation {je}')

        raise HTTPException(status_code=500, detail='Error while creating the access token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in access token creation {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')


async def decode_access_token(token: str):

    try:

        if not token is None:

            return jwt.decode(token,key=ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])

        else:

            raise HTTPException(status_code=401, detail='Error when getting the access token')

    except ExpiredSignatureError:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Access token expired')

    except JWTError as je:

        logger.error(f'Error in access token decode {je}')

        # if 'signature has expired' in je:
        #
        #     return None

        raise HTTPException(status_code=500, detail='Error while decoding the access token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in access token decode {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

async def decode_refresh_token(token: str):

    try:

        if not token is None:

            return jwt.decode(token=token, key=REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])

        else:

            raise HTTPException(status_code=401, detail='Error when getting the refresh token')

    except ExpiredSignatureError:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Access token expired')

    except JWTError as je:

        logger.error(f'Error in refresh token decode {je}')

        # if 'signature has expired' in je:
        #
        #     return None

        raise HTTPException(status_code=500, detail='Error while decoding the refresh token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in refresh token decode {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

async def create_refresh_token(data: dict, expires: Optional[int] = None):

    try:

        to_encode = data.copy()

        if not expires:

            expire = await get_current_time_with_tz() + timedelta(minutes=REFRESH_TOKEN_EXPIRE)

        else:

            expire = await get_current_time_with_tz() + timedelta(days=expires)

        to_encode.update({'exp': expire})

        return jwt.encode(to_encode, key=REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)

    except JWTError as je:

        logger.error(f'Error in refresh token creation {je}')

        raise HTTPException(status_code=500, detail='Error while creating the refresh token')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in refresh token creation {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')
