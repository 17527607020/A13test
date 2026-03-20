"""
首页相关的请求/响应模型
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProgressItem(BaseModel):
    """进度项"""
    title: str
    value: int
    description: str


class LearningResource(BaseModel):
    """学习资源"""
    id: int
    title: str
    description: str
    logo: str
    color: str
    tag: str
    tag_type: str
    content: Optional[str] = None  # 文章内容
    link: Optional[str] = None


class AIRecommendation(BaseModel):
    """AI推荐"""
    title: str
    subtitle: str
    content: str
    avatar_icon: str = "ChatDotRound"


class QuickAction(BaseModel):
    """快速操作"""
    label: str
    icon: str
    route: str
    button_type: str


class HomeDataResponse(BaseModel):
    """首页数据响应"""
    # 用户信息
    username: str
    greeting: str

    # 进度数据
    progress_items: List[ProgressItem]

    # AI推荐
    ai_recommendation: AIRecommendation

    # 学习资源
    learning_resources: List[LearningResource]

    # 快速操作
    quick_actions: List[QuickAction]

    # 统计数据
    total_assessments: int = 0
    total_interviews: int = 0
    total_plans: int = 0
