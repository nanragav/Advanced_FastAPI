from sqlalchemy.util import await_only

from schemas import LoginUserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from fastapi import HTTPException, Response
from auth.security import verify_password, get_hash
from auth.token import create_access_token, create_refresh_token
from sqlalchemy.exc import SQLAlchemyError
import logging
from uuid import uuid4
from auth.dependencies import clear_cookie


logger = logging.getLogger(__name__)


async def user_login(request: LoginUserRequest, db: AsyncSession):

    try:

        stmt = select(User).where(User.name == request.name)

        result = await db.execute(stmt)

        user = result.scalar_one_or_none()

        if not user:

            raise HTTPException(status_code=404, detail='User not found')

        is_pass_crt = await verify_password(plain_password=request.password, hashed_password=user.password)

        if not is_pass_crt:

            raise HTTPException(status_code=401, detail='Username or Password is incorrect')

        user.session_id = uuid4()

        db.add(user)

        await db.commit()

        await db.refresh(user)

        data = {"id": str(user.id), 'name': user.name, 'session_id': str(user.session_id)}

        access_token = await create_access_token(data=data)

        refresh_token = await create_refresh_token(data=data)

        return access_token, refresh_token

    except SQLAlchemyError as se:

        logger.error(f'Error while retriving user {se}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

    except HTTPException as he:

        raise he

    except Exception as e:

        logger.error(f'Unknown error in user login {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')

async def user_logout(current_user: dict, response: Response, db: AsyncSession):

    try:

        if not current_user:

            return await clear_cookie(response=response)

        current_user.session_id = uuid4()

        db.add(current_user)

        await db.commit()

        await db.refresh(current_user)

        return True

    except SQLAlchemyError as se:

        logger.error(f'Error while logging out user {se}')

        return await clear_cookie(response=response)

    except Exception as e:

        logger.error(f'Unknown error in user logout {e}')

        return await clear_cookie(response=response)



