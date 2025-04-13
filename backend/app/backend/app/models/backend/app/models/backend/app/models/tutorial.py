import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Tutorial(Base):
    __tablename__ = "tutorials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    difficulty = Column(String, nullable=True)  # beginner, intermediate, advanced
    estimated_time = Column(Integer, nullable=True)  # in minutes
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, default=False)
    tags = Column(ARRAY(String), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="tutorials")
    steps = relationship("TutorialStep", back_populates="tutorial", cascade="all, delete-orphan")


class TutorialStep(Base):
    __tablename__ = "tutorial_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tutorial_id = Column(UUID(as_uuid=True), ForeignKey("tutorials.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    code = Column(Text, nullable=True)
    language = Column(String, nullable=True)
    position = Column(Integer, nullable=False)
    expected_output = Column(Text, nullable=True)
    hints = Column(JSON, nullable=True)
    
    # Relationships
    tutorial = relationship("Tutorial", back_populates="steps")
