"""
职业测评相关模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.core.config import Base


class Assessment(Base):
    """测评类型表"""
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    # mbti, holland, skill
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    color = Column(String(20))
    duration = Column(Integer)  # 预计时长（分钟）
    question_count = Column(Integer)  # 题目数量
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship(
        "AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")
    reports = relationship(
        "AssessmentReport", back_populates="assessment", cascade="all, delete-orphan")


class AssessmentQuestion(Base):
    """测评题目表"""
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey(
        "assessments.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_order = Column(Integer)  # 题目顺序
    dimension = Column(String(50))  # 维度（如MBTI的E/I, S/N等）
    # 选项列表 [{"text": "选项A", "value": "A", "score": 1}, ...]
    options = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="questions")


class AssessmentReport(Base):
    """测评报告表"""
    __tablename__ = "assessment_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey(
        "assessments.id"), nullable=False)
    result_type = Column(String(100))  # 结果类型（如INFP）
    result_name = Column(String(200))  # 结果名称（如调停者）
    scores = Column(JSON)  # 各维度得分 {"E": 30, "I": 70, ...}
    dimensions = Column(JSON)  # 维度分析
    suggestions = Column(Text)  # 职业建议
    raw_answers = Column(JSON)  # 原始答案
    total_score = Column(Float, default=0)
    completed_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    assessment = relationship("Assessment", back_populates="reports")
