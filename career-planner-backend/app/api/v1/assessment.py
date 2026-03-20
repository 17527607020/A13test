"""
职业测评API路由
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_db
from app.models.assessment import Assessment, AssessmentReport
from app.schemas.assessment import (
    AssessmentResponse,
    AssessmentDetailResponse,
    AssessmentSubmit,
    AssessmentReportResponse,
    AssessmentReportDetailResponse,
    ReportListItem
)
from app.services.assessment_service import AssessmentService
from app.services.user_service import get_user_by_id
from app.models.user import User

router = APIRouter(prefix="/assessment", tags=["职业测评"])


async def get_current_user(
    user_id: int = Query(..., description="用户ID"),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return user


@router.get("/list", response_model=List[AssessmentResponse])
async def get_assessments(db: AsyncSession = Depends(get_db)):
    """获取所有测评类型"""
    assessments = await AssessmentService.get_assessments(db)
    return assessments


@router.get("/{assessment_id}", response_model=AssessmentDetailResponse)
async def get_assessment_detail(
    assessment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取测评详情（包含题目）"""
    assessment = await AssessmentService.get_assessment_by_id(db, assessment_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="测评不存在"
        )

    questions = await AssessmentService.get_questions(db, assessment_id)

    return AssessmentDetailResponse(
        id=assessment.id,
        code=assessment.code,
        name=assessment.name,
        description=assessment.description,
        icon=assessment.icon,
        color=assessment.color,
        duration=assessment.duration,
        question_count=assessment.question_count,
        created_at=assessment.created_at,
        questions=questions
    )


@router.post("/submit", response_model=AssessmentReportResponse)
async def submit_assessment(
    submit_data: AssessmentSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """提交测评答案并生成报告"""
    assessment = await AssessmentService.get_assessment_by_id(db, submit_data.assessment_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="测评不存在"
        )

    report = await AssessmentService.submit_assessment(db, current_user.id, submit_data, assessment)
    return report


@router.get("/reports/my", response_model=List[ReportListItem])
async def get_my_reports(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取我的测评报告列表"""
    reports = await AssessmentService.get_user_reports(db, current_user.id)

    result = []
    for report in reports:
        assessment = await AssessmentService.get_assessment_by_id(db, report.assessment_id)
        result.append(ReportListItem(
            id=report.id,
            assessment_id=report.assessment_id,
            assessment_name=assessment.name if assessment else "未知测评",
            assessment_type=assessment.code if assessment else "unknown",
            result_type=report.result_type,
            result_name=report.result_name,
            completed_at=report.completed_at,
            color=assessment.color if assessment else None
        ))

    return result


@router.get("/report/{report_id}", response_model=AssessmentReportDetailResponse)
async def get_report_detail(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取报告详情"""
    report = await AssessmentService.get_report_by_id(db, report_id, current_user.id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="报告不存在"
        )

    assessment = await AssessmentService.get_assessment_by_id(db, report.assessment_id)

    return AssessmentReportDetailResponse(
        id=report.id,
        user_id=report.user_id,
        assessment_id=report.assessment_id,
        result_type=report.result_type,
        result_name=report.result_name,
        scores=report.scores,
        dimensions=report.dimensions,
        suggestions=report.suggestions,
        total_score=report.total_score,
        completed_at=report.completed_at,
        created_at=report.created_at,
        assessment=AssessmentResponse(
            id=assessment.id,
            code=assessment.code,
            name=assessment.name,
            description=assessment.description,
            icon=assessment.icon,
            color=assessment.color,
            duration=assessment.duration,
            question_count=assessment.question_count,
            created_at=assessment.created_at
        ) if assessment else None
    )
