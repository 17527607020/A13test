"""
模拟面试API路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_db
from app.models.user import User
from app.models.interview import JobPosition
from app.schemas.interview import (
    StartInterviewRequest,
    SubmitAnswerRequest,
    InterviewSessionCreate,
    InterviewSessionResponse,
    InterviewSessionDetail,
    InterviewQuestionResponse,
    AnswerFeedback,
    JobPositionResponse,
    InterviewRecordItem,
    InterviewMode,
    InterviewModesResponse
)
from app.services.interview_service import InterviewService
from app.services.user_service import get_user_by_id

router = APIRouter(prefix="/interview", tags=["模拟面试"])


async def get_current_user(
    user_id: int = Query(..., description="用户ID"),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user


@router.get("/modes", response_model=InterviewModesResponse)
async def get_interview_modes():
    """获取面试模式列表"""
    modes = [
        InterviewMode(
            id="ai",
            title="AI智能面试",
            description="AI根据你的简历和目标岗位，智能生成面试问题",
            icon="Microphone",
            color="#6B5CE7",
            tags=["智能推荐", "个性化"]
        ),
        InterviewMode(
            id="behavior",
            title="行为面试",
            description="针对过往经历，考察你的软技能和综合素质",
            icon="ChatDotRound",
            color="#E95CBF",
            tags=["软技能", "综合素质"]
        ),
        InterviewMode(
            id="technical",
            title="技术面试",
            description="针对专业技能进行深度考察，检验技术能力",
            icon="Document",
            color="#54A0FF",
            tags=["专业技能", "深度考察"]
        )
    ]
    return InterviewModesResponse(modes=modes)


@router.get("/jobs", response_model=List[JobPositionResponse])
async def get_job_positions(
    hot_only: bool = Query(False, description="只获取热门岗位"),
    db: AsyncSession = Depends(get_db)
):
    """获取岗位列表"""
    positions = await InterviewService.get_job_positions(db, hot_only=hot_only)
    return [
        JobPositionResponse(
            id=p.id,
            name=p.name,
            code=p.code,
            logo=p.logo,
            question_count=p.question_count,
            description=p.description,
            is_hot=p.is_hot
        )
        for p in positions
    ]


@router.post("/start", response_model=InterviewSessionCreate)
async def start_interview(
    request: StartInterviewRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """开始面试"""
    try:
        result = await InterviewService.start_interview(
            db,
            current_user.id,
            request.interview_mode,
            request.target_job,
            request.question_count
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"开始面试失败: {str(e)}"
        )


@router.post("/answer", response_model=AnswerFeedback)
async def submit_answer(
    request: SubmitAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """提交回答"""
    try:
        result = await InterviewService.submit_answer(
            db,
            request.session_id,
            request.question_id,
            request.user_answer,
            request.answer_duration
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"提交回答失败: {str(e)}"
        )


@router.post("/{session_id}/complete", response_model=InterviewSessionResponse)
async def complete_interview(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """完成面试"""
    try:
        session = await InterviewService.complete_interview(db, session_id)
        return InterviewSessionResponse(
            id=session.id,
            user_id=session.user_id,
            interview_mode=session.interview_mode,
            target_job=session.target_job,
            status=session.status,
            total_score=session.total_score,
            overall_feedback=session.overall_feedback,
            strengths=session.strengths,
            improvements=session.improvements,
            duration=session.duration,
            started_at=session.started_at,
            completed_at=session.completed_at,
            created_at=session.created_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"完成面试失败: {str(e)}"
        )


@router.get("/records", response_model=List[InterviewRecordItem])
async def get_interview_records(
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50, description="返回记录数量"),
    db: AsyncSession = Depends(get_db)
):
    """获取面试记录列表"""
    records = await InterviewService.get_user_interviews(db, current_user.id, limit)
    return records


@router.get("/session/{session_id}", response_model=InterviewSessionDetail)
async def get_session_detail(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取面试会话详情"""
    session = await InterviewService.get_session_detail(db, session_id, current_user.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="面试记录不存在"
        )

    # 构建回答列表
    answers = []
    for answer in session.answers:
        if answer.question:
            answers.append(AnswerFeedback(
                id=answer.id,
                question_id=answer.question_id,
                question_text=answer.question.question_text,
                user_answer=answer.user_answer or "",
                reference_answer=answer.question.reference_answer,
                score=answer.score,
                score_details=answer.score_details,
                feedback=answer.feedback or "",
                suggestions=answer.suggestions,
                answer_duration=answer.answer_duration
            ))

    return InterviewSessionDetail(
        id=session.id,
        user_id=session.user_id,
        interview_mode=session.interview_mode,
        target_job=session.target_job,
        status=session.status,
        total_score=session.total_score,
        overall_feedback=session.overall_feedback,
        strengths=session.strengths,
        improvements=session.improvements,
        duration=session.duration,
        started_at=session.started_at,
        completed_at=session.completed_at,
        created_at=session.created_at,
        answers=answers
    )


@router.post("/init-data")
async def init_default_data(db: AsyncSession = Depends(get_db)):
    """初始化默认数据（仅用于测试/开发）"""
    try:
        await InterviewService.init_default_data(db)
        # 创建默认题目
        await InterviewService.create_default_questions(db, "general", None)
        return {"success": True, "message": "默认数据初始化成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"初始化失败: {str(e)}"
        )
