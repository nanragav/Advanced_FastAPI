from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

async_engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(bind=async_engine, class_=AsyncSession, autoflush=False, autocommit=False)

Base = declarative_base()

async def get_db():

    db = None

    try:

        db = async_session()

        yield db

    finally:

        await db.close()

