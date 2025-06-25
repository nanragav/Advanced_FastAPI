from datetime import datetime, timedelta, UTC
import logging
from fastapi import HTTPException
from sqlalchemy.sql.ddl import sort_tables_and_constraints

logger = logging.getLogger(__name__)

async def get_current_time():

    try:

        return datetime.now(UTC)

    except Exception as e:

        logger.error(f'Error while getting the current time {e}')

        raise HTTPException(status_code=500, detail='Time Error when creating user')