import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class CodeSnippet(Base):
    __tablename__ = "code_snippets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    code = Column(Text, nullable=False)
    language = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_public = Column(Boolean, default=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    tags = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="snippets")
    comments = relationship("Comment", back_populates="snippet", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    snippet_id = Column(UUID(as_uuid=True), ForeignKey("code_snippets.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    snippet = relationship("CodeSnippet", back_populates="comments")
    user = relationship("User")
