from schemas import LoginUserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from fastapi import HTTPException
from auth.security import verify_password, get_hash
from auth.token import create_access_token, create_refresh_token
from sqlalchemy.exc import SQLAlchemyError
import logging
from uuid import uuid4

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

        logger.error(f'Unknown error in access token creation {e}')

        raise HTTPException(status_code=500, detail='Internal Server Error')


