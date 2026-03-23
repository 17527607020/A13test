from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
from typing import Optional
import os
import uuid
from datetime import datetime

from app.core.config import get_db
from app.schemas.user_profile import (
    UserProfileCreate, UserProfileUpdate, UserProfileResponse,
    PasswordChange, PasswordChangeResponse,
    UserHistoryItem, UserHistoryResponse
)
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.user_history import UserHistory
from app.services.user_service import authenticate_user, get_password_hash

router = APIRouter()

# 头像上传目录
UPLOAD_DIR = "uploads/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/profile")
async def get_user_profile(
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户资料
    """
    username = "test_user"

    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == user.id)
    )
    profile = profile_result.scalar_one_or_none()

    def format_datetime(dt):
        return dt.isoformat() if dt else None

    if profile:
        return {
            "success": True,
            "data": {
                "id": profile.id,
                "user_id": profile.user_id,
                "nickname": profile.nickname,
                "phone": profile.phone,
                "avatar_url": profile.avatar_url,
                "bio": profile.bio,
                "location": profile.location,
                "website": profile.website,
                "created_at": format_datetime(profile.created_at),
                "updated_at": format_datetime(profile.updated_at)
            }
        }
    else:
        return {
            "success": True,
            "data": {
                "id": None,
                "user_id": user.id,
                "nickname": None,
                "phone": None,
                "avatar_url": None,
                "bio": None,
                "location": None,
                "website": None,
                "created_at": None,
                "updated_at": None
            }
        }


@router.post("/profile", response_model=UserProfileResponse)
async def create_or_update_profile(
    profile_data: UserProfileCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建或更新用户资料
    """
    username = "test_user"

    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == user.id)
    )
    profile = profile_result.scalar_one_or_none()

    if profile:
        for field, value in profile_data.dict(exclude_unset=True).items():
            if value is not None:
                setattr(profile, field, value)
        profile.updated_at = func.now()
        await db.commit()
        await db.refresh(profile)
    else:
        profile = UserProfile(
            user_id=user.id,
            **profile_data.dict(exclude_unset=True)
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

    def format_datetime(dt):
        return dt.isoformat() if dt else None

    return {
        "success": True,
        "data": {
            "id": profile.id,
            "user_id": profile.user_id,
            "nickname": profile.nickname,
            "phone": profile.phone,
            "avatar_url": profile.avatar_url,
            "bio": profile.bio,
            "location": profile.location,
            "website": profile.website,
            "created_at": format_datetime(profile.created_at),
            "updated_at": format_datetime(profile.updated_at)
        },
        "message": "用户资料更新成功"
    }


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    db: AsyncSession = Depends(get_db)
):
    """
    修改密码
    """
    username = "test_user"

    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if password_data.new_password != password_data.confirm_password:
        raise HTTPException(status_code=400, detail="两次输入的密码不一致")

    user.password_hash = get_password_hash(password_data.new_password)
    await db.commit()

    return {
        "success": True,
        "message": "密码修改成功"
    }


@router.get("/history")
async def get_user_history(
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户历史记录
    """
    username = "test_user"

    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    history_result = await db.execute(
        select(UserHistory).where(UserHistory.user_id == user.id)
        .order_by(UserHistory.created_at.desc())
        .limit(50)
    )
    histories = history_result.scalars().all()

    def format_datetime(dt):
        return dt.isoformat() if dt else None

    history_items = [
        {
            "id": h.id,
            "action_type": h.action_type,
            "action_data": h.action_data,
            "description": h.description,
            "created_at": format_datetime(h.created_at)
        }
        for h in histories
    ]

    return {
        "success": True,
        "data": history_items
    }


@router.post("/upload-avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    上传头像
    """
    username = "test_user"

    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 验证文件类型
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, detail="不支持的文件格式，仅支持 JPG、PNG、GIF、WEBP")

    # 验证文件大小 (最大 5MB)
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小不能超过 5MB")

    # 生成文件名
    file_ext = file.filename.split(
        ".")[-1] if file.filename and "." in file.filename else "jpg"
    filename = f"{uuid.uuid4().hex}.{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # 保存文件
    with open(filepath, "wb") as f:
        f.write(content)

    # 生成访问URL
    avatar_url = f"/uploads/avatars/{filename}"

    # 更新用户资料
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == user.id)
    )
    profile = profile_result.scalar_one_or_none()

    if profile:
        # 删除旧头像
        if profile.avatar_url:
            old_filename = profile.avatar_url.split("/")[-1]
            old_filepath = os.path.join(UPLOAD_DIR, old_filename)
            if os.path.exists(old_filepath) and "default" not in old_filename:
                try:
                    os.remove(old_filepath)
                except:
                    pass

        profile.avatar_url = avatar_url
        profile.updated_at = func.now()
        await db.commit()
        await db.refresh(profile)
    else:
        profile = UserProfile(
            user_id=user.id,
            avatar_url=avatar_url
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

    return {
        "success": True,
        "data": {
            "avatar_url": avatar_url
        },
        "message": "头像上传成功"
    }


@router.post("/update-profile")
async def update_user_profile(
    nickname: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    """
    更新用户资料
    """
    username = "test_user"

    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 获取或创建用户资料
    profile_result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == user.id)
    )
    profile = profile_result.scalar_one_or_none()

    if profile:
        if nickname is not None:
            profile.nickname = nickname
        if phone is not None:
            profile.phone = phone
        if bio is not None:
            profile.bio = bio
        profile.updated_at = func.now()
        await db.commit()
        await db.refresh(profile)
    else:
        profile = UserProfile(
            user_id=user.id,
            nickname=nickname,
            phone=phone,
            bio=bio
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

    def format_datetime(dt):
        return dt.isoformat() if dt else None

    return {
        "success": True,
        "data": {
            "id": profile.id,
            "user_id": profile.user_id,
            "nickname": profile.nickname,
            "phone": profile.phone,
            "avatar_url": profile.avatar_url,
            "bio": profile.bio,
            "location": profile.location,
            "website": profile.website,
            "created_at": format_datetime(profile.created_at),
            "updated_at": format_datetime(profile.updated_at)
        },
        "message": "资料更新成功"
    }
