from datetime import datetime, UTC, timedelta
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

async def get_current_ist_time():

    try:

        return datetime.now(UTC).replace(tzinfo=None)

    except Exception as e:

        logger.error(f'Error while getting the current time {e}')

        raise HTTPException(status_code=500, detail='Time Error')

async def get_current_time_with_tz():

    try:

        return datetime.now(UTC)

    except Exception as e:

        logger.error(f'Error while getting the current time {e}')

        raise HTTPException(status_code=500, detail='Time Error')

async def get_access_cookie_expire():

    try:

        return datetime.now(UTC) + timedelta(minutes=60)

    except Exception as e:

        logger.error(f'Error while getting the current time {e}')

        raise HTTPException(status_code=500, detail='Time Error')

async def get_refresh_cookie_expire():

    try:

        return datetime.now(UTC) + timedelta(days=7)

    except Exception as e:

        logger.error(f'Error while getting the current time {e}')

        raise HTTPException(status_code=500, detail='Time Error')