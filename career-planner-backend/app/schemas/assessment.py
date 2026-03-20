"""
职业测评相关Schema
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


# ==================== 测评题目 ====================
class QuestionOption(BaseModel):
    """题目选项"""
    text: str
    value: str
    score: int = 0


class AssessmentQuestionBase(BaseModel):
    """测评题目基础"""
    question_text: str
    question_order: int
    dimension: Optional[str] = None
    options: List[QuestionOption]


class AssessmentQuestionResponse(AssessmentQuestionBase):
    """测评题目响应"""
    id: int

    class Config:
        from_attributes = True


# ==================== 测评类型 ====================
class AssessmentBase(BaseModel):
    """测评基础"""
    code: str
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    duration: Optional[int] = None
    question_count: Optional[int] = None


class AssessmentResponse(AssessmentBase):
    """测评响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class AssessmentDetailResponse(AssessmentResponse):
    """测评详情响应（包含题目）"""
    questions: List[AssessmentQuestionResponse] = []


# ==================== 测评答案提交 ====================
class AnswerSubmit(BaseModel):
    """单个答案提交"""
    question_id: int
    answer: str  # 选择的选项value


class AssessmentSubmit(BaseModel):
    """测评提交"""
    assessment_id: int
    answers: List[AnswerSubmit]


# ==================== 测评报告 ====================
class DimensionScore(BaseModel):
    """维度得分"""
    dimension: str
    score: int
    max_score: int
    percentage: float


class AssessmentReportBase(BaseModel):
    """测评报告基础"""
    assessment_id: int
    result_type: str
    result_name: str
    scores: Dict[str, Any]
    dimensions: Optional[List[DimensionScore]] = None
    suggestions: Optional[str] = None
    total_score: float = 0


class AssessmentReportResponse(AssessmentReportBase):
    """测评报告响应"""
    id: int
    user_id: int
    completed_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class AssessmentReportDetailResponse(AssessmentReportResponse):
    """测评报告详情"""
    assessment: AssessmentResponse


# ==================== 历史报告列表 ====================
class ReportListItem(BaseModel):
    """报告列表项"""
    id: int
    assessment_id: int
    assessment_name: str
    assessment_type: str
    result_type: str
    result_name: str
    completed_at: datetime
    color: Optional[str] = None

    class Config:
        from_attributes = True
