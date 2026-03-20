from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import get_db
from app.schemas.user import UserLogin, UserRegister, UserResponse, AuthResponse
from app.services.user_service import create_user, authenticate_user, get_user_by_id
from app.models.user import User

router = APIRouter()


async def get_current_user(
    user_id: int = None,
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    获取当前登录用户
    简化版：通过user_id获取用户
    """
    if user_id is None:
        raise HTTPException(status_code=401, detail="未登录")

    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user


@router.post("/login", response_model=AuthResponse)
async def login(
    user_login: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    用户登录接口
    验证用户名和密码，返回用户信息和token
    """
    user = await authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    return AuthResponse(
        success=True,
        data=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            token=f"token_{user.id}_{user.username}"
        )
    )


@router.post("/register", response_model=AuthResponse)
async def register(
    user_register: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    用户注册接口
    创建新用户并返回用户信息和token
    """
    user = await create_user(db, user_register)
    if not user:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")

    return AuthResponse(
        success=True,
        data=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            token=f"token_{user.id}_{user.username}"
        )
    )


@router.get("/me/{user_id}", response_model=UserResponse)
async def get_user_info(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    获取用户信息接口
    根据用户ID查询用户信息
    """
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        token=f"token_{user.id}_{user.username}"
    )
