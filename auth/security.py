from passlib.context import CryptContext
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=['bcrypt'])

async def get_hash(plain_password: str):

    try:

        return pwd_context.hash(plain_password)

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in Password Hashing {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error while hashing the password')

async def verify_password(plain_password: str, hashed_password: str):

    try:

        is_valid =  pwd_context.verify(plain_password, hashed_password)

        return is_valid

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in Password Checking {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error while checking the password')