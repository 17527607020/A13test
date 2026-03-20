"""
模拟面试相关的请求/响应模型
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============ 面试题目相关 ============

class QuestionOption(BaseModel):
    """题目选项"""
    text: str
    value: str


class ScoringCriteria(BaseModel):
    """评分标准"""
    key_points: List[str] = Field(default_factory=list, description="关键得分点")
    max_score: int = Field(default=100, description="满分")
    keywords: List[str] = Field(default_factory=list, description="关键词")


class InterviewQuestionResponse(BaseModel):
    """面试题目响应"""
    id: int
    category: str
    job_type: Optional[str] = None
    question_text: str
    difficulty: str = "medium"
    tags: Optional[List[str]] = None
    question_order: int = 0

    class Config:
        from_attributes = True


class InterviewQuestionDetail(InterviewQuestionResponse):
    """面试题目详情（含参考答案）"""
    reference_answer: Optional[str] = None
    scoring_criteria: Optional[Dict[str, Any]] = None


# ============ 面试会话相关 ============

class StartInterviewRequest(BaseModel):
    """开始面试请求"""
    interview_mode: str = Field(...,
                                description="面试模式: ai, behavior, technical")
    target_job: Optional[str] = Field(None, description="目标岗位")
    question_count: int = Field(default=5, ge=3, le=20, description="题目数量")


class SubmitAnswerRequest(BaseModel):
    """提交回答请求"""
    session_id: int
    question_id: int
    user_answer: str = Field(..., min_length=1, description="用户回答")
    answer_duration: int = Field(default=0, ge=0, description="回答时长(秒)")


class AnswerFeedback(BaseModel):
    """回答反馈"""
    id: int
    question_id: int
    question_text: str
    user_answer: str
    reference_answer: Optional[str] = None
    score: float
    score_details: Optional[Dict[str, float]] = None
    feedback: str
    suggestions: Optional[str] = None
    answer_duration: int = 0

    class Config:
        from_attributes = True


class InterviewSessionResponse(BaseModel):
    """面试会话响应"""
    id: int
    user_id: int
    interview_mode: str
    target_job: Optional[str] = None
    status: str
    total_score: float = 0
    overall_feedback: Optional[str] = None
    strengths: Optional[List[str]] = None
    improvements: Optional[List[str]] = None
    duration: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class InterviewSessionDetail(InterviewSessionResponse):
    """面试会话详情（含回答列表）"""
    answers: List[AnswerFeedback] = Field(default_factory=list)


class InterviewSessionCreate(BaseModel):
    """创建面试会话响应"""
    session_id: int
    questions: List[InterviewQuestionResponse]
    total_questions: int
    started_at: datetime


# ============ 岗位相关 ============

class JobPositionResponse(BaseModel):
    """岗位信息响应"""
    id: int
    name: str
    code: str
    logo: Optional[str] = None
    question_count: int = 0
    description: Optional[str] = None
    is_hot: bool = False

    class Config:
        from_attributes = True


# ============ 面试记录列表 ============

class InterviewRecordItem(BaseModel):
    """面试记录列表项"""
    id: int
    interview_mode: str
    mode_name: str
    target_job: Optional[str] = None
    status: str
    total_score: float
    question_count: int
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ============ 面试模式 ============

class InterviewMode(BaseModel):
    """面试模式"""
    id: str
    title: str
    description: str
    icon: str
    color: str
    tags: List[str] = Field(default_factory=list)


class InterviewModesResponse(BaseModel):
    """面试模式列表响应"""
    modes: List[InterviewMode]
