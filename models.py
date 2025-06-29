from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, String, UUID, DateTime, PrimaryKeyConstraint, Text, ForeignKeyConstraint
from uuid import uuid4
from utils.time_setting import get_current_ist_time

class User(Base):

    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), default=uuid4, index=True)
    name = Column(String(60), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    session_id = Column(UUID(as_uuid=True), nullable=False, default=uuid4)
    created_at = Column(DateTime, nullable=True, default=get_current_ist_time)
    created_by = Column(UUID(as_uuid=True), nullable=True)

    content = relationship('Blog', back_populates='creator')

    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_user_id'),
    )

class Blog(Base):

    __tablename__ = 'blogs'

    id = Column(UUID(as_uuid=True), default=uuid4, index=True)
    title = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    creator = relationship('User', back_populates='content')

    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_blogs_id'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_blog_users_id')
    )