from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.config import Base


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20))
    avatar_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=datetime.utcnow)

    profiles = relationship("StudentProfile", back_populates="student", cascade="all, delete-orphan")


class StudentProfile(Base):
    __tablename__ = 'student_profiles'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, index=True)
    basic_info = Column(JSON, nullable=False)
    education = Column(JSON, default=[])
    experience = Column(JSON, default=[])
    projects = Column(JSON, default=[])
    skills = Column(JSON, default=[])
    certificates = Column(JSON, default=[])
    awards = Column(JSON, default=[])
    ability_scores = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="profiles")
