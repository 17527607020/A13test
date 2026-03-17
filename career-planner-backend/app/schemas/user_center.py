from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class UserInfoUpdate(BaseModel):
    """用户信息更新"""
    nickname: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None


class PasswordChange(BaseModel):
    """密码修改"""
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)


class UserHistoryItem(BaseModel):
    """用户历史记录项"""
    id: int
    action_type: str
    action_data: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    created_at: datetime


class UserHistoryResponse(BaseModel):
    """用户历史记录响应"""
    success: bool
    data: list[UserHistoryItem]
    message: Optional[str] = None


class UserInfoResponse(BaseModel):
    """用户信息响应"""
    success: bool
    data: Dict[str, Any]
    message: Optional[str] = None