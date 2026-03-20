"""
模拟面试相关模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from app.core.config import Base


class InterviewQuestion(Base):
    """面试题库表"""
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    # 题目分类: technical(技术), behavioral(行为), ai(智能)
    category = Column(String(50), nullable=False)
    # 岗位类型: java, frontend, product, data等
    job_type = Column(String(50))
    # 题目内容
    question_text = Column(Text, nullable=False)
    # 参考答案
    reference_answer = Column(Text)
    # 评分标准 (JSON格式)
    scoring_criteria = Column(JSON)
    # 难度: easy, medium, hard
    difficulty = Column(String(20), default="medium")
    # 标签
    tags = Column(JSON)  # ["Java", "并发", "多线程"]
    # 题目顺序(用于预设面试)
    question_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class InterviewSession(Base):
    """面试会话表"""
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 面试模式: ai, behavior, technical
    interview_mode = Column(String(50), nullable=False)
    # 目标岗位
    target_job = Column(String(100))
    # 面试状态: pending, in_progress, completed, cancelled
    status = Column(String(20), default="pending")
    # 总分
    total_score = Column(Float, default=0)
    # 综合评价
    overall_feedback = Column(Text)
    # 优势
    strengths = Column(JSON)  # ["技术基础扎实", "表达清晰"]
    # 待改进
    improvements = Column(JSON)  # ["需要加强项目经验表述"]
    # 面试时长(分钟)
    duration = Column(Integer, default=0)
    # 开始时间
    started_at = Column(DateTime)
    # 结束时间
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联
    answers = relationship(
        "InterviewAnswer", back_populates="session", cascade="all, delete-orphan")


class InterviewAnswer(Base):
    """面试回答表"""
    __tablename__ = "interview_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey(
        "interview_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey(
        "interview_questions.id"), nullable=False)
    # 用户回答
    user_answer = Column(Text)
    # 得分 (0-100)
    score = Column(Float, default=0)
    # AI评分详情
    # {"relevance": 80, "depth": 70, "clarity": 85}
    score_details = Column(JSON)
    # AI反馈
    feedback = Column(Text)
    # 改进建议
    suggestions = Column(Text)
    # 回答时长(秒)
    answer_duration = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联
    session = relationship("InterviewSession", back_populates="answers")
    question = relationship("InterviewQuestion")


class JobPosition(Base):
    """岗位信息表"""
    __tablename__ = "job_positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    # 岗位代码
    code = Column(String(50), unique=True, nullable=False)
    # 图标/缩写
    logo = Column(String(10))
    # 题目数量
    question_count = Column(Integer, default=0)
    # 描述
    description = Column(Text)
    # 是否热门
    is_hot = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
