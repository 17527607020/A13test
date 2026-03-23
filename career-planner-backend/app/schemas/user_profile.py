from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class UserProfileCreate(BaseModel):
    """创建用户资料"""
    nickname: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None


class UserProfileUpdate(BaseModel):
    """更新用户资料"""
    nickname: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None


class UserProfileResponse(BaseModel):
    """用户资料响应"""
    success: bool = True
    data: Optional[dict[str, Any]] = None
    message: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class PasswordChange(BaseModel):
    """修改密码"""
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)
    confirm_password: str = Field(..., min_length=6)


class PasswordChangeResponse(BaseModel):
    """修改密码响应"""
    success: bool
    message: Optional[str] = None


class UserHistoryItem(BaseModel):
    """用户历史记录项"""
    id: int
    action_type: str
    action_data: Optional[dict] = None
    description: Optional[str] = None
    created_at: datetime


class UserHistoryResponse(BaseModel):
    """用户历史记录响应"""
    success: bool
    data: list[UserHistoryItem]
    message: Optional[str] = None
