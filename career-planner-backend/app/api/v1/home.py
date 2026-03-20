"""
首页API路由
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_db
from app.models.user import User
from app.schemas.home import HomeDataResponse, LearningResource
from app.services.home_service import HomeService
from app.services.user_service import get_user_by_id

router = APIRouter(prefix="/home", tags=["首页"])


async def get_current_user(
    user_id: int = Query(..., description="用户ID"),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    user = await get_user_by_id(db, user_id)
    if not user:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=401, detail="用户不存在")
    return user


@router.get("/data", response_model=HomeDataResponse)
async def get_home_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取首页所有数据"""
    return await HomeService.get_home_data(db, current_user)


@router.get("/resources", response_model=list[LearningResource])
async def get_learning_resources():
    """获取学习资源列表"""
    return HomeService.get_learning_resources()
