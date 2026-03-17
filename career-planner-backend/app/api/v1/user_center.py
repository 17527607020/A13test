from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

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


@router.get("/profile", response_model=UserProfileResponse)
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
    
    if profile:
        return UserProfileResponse(
            success=True,
            data={
                "id": profile.id,
                "user_id": profile.user_id,
                "nickname": profile.nickname,
                "phone": profile.phone,
                "avatar_url": profile.avatar_url,
                "bio": profile.bio,
                "location": profile.location,
                "website": profile.website,
                "created_at": profile.created_at,
                "updated_at": profile.updated_at
            }
        )
    else:
        return UserProfileResponse(
            success=True,
            data={
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
        )


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
    
    return UserProfileResponse(
        success=True,
        data={
            "id": profile.id,
            "user_id": profile.user_id,
            "nickname": profile.nickname,
            "phone": profile.phone,
            "avatar_url": profile.avatar_url,
            "bio": profile.bio,
            "location": profile.location,
            "website": profile.website,
            "created_at": profile.created_at,
            "updated_at": profile.updated_at
        },
        message="用户资料更新成功"
    )


@router.post("/change-password", response_model=PasswordChangeResponse)
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
    
    return PasswordChangeResponse(
        success=True,
        message="密码修改成功"
    )


@router.get("/history", response_model=UserHistoryResponse)
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
    
    history_items = [
        UserHistoryItem(
            id=h.id,
            action_type=h.action_type,
            action_data=h.action_data,
            description=h.description,
            created_at=h.created_at
        )
        for h in histories
    ]
    
    return UserHistoryResponse(
        success=True,
        data=history_items
    )