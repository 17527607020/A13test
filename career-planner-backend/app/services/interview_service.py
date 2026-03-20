"""
模拟面试服务层
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
import random
import json

from app.models.interview import (
    InterviewQuestion,
    InterviewSession,
    InterviewAnswer,
    JobPosition
)
from app.schemas.interview import (
    InterviewQuestionResponse,
    InterviewSessionCreate,
    AnswerFeedback,
    InterviewRecordItem
)


class InterviewService:
    """面试服务"""

    # 面试模式映射
    MODE_MAP = {
        "ai": "AI智能面试",
        "behavior": "行为面试",
        "technical": "技术面试"
    }

    @staticmethod
    async def get_job_positions(db: AsyncSession, hot_only: bool = False) -> List[JobPosition]:
        """获取岗位列表"""
        query = select(JobPosition).where(JobPosition.is_active == True)
        if hot_only:
            query = query.where(JobPosition.is_hot == True)
        query = query.order_by(JobPosition.id)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_job_by_code(db: AsyncSession, code: str) -> Optional[JobPosition]:
        """根据代码获取岗位"""
        query = select(JobPosition).where(JobPosition.code == code)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_questions_for_interview(
        db: AsyncSession,
        interview_mode: str,
        job_type: Optional[str] = None,
        count: int = 5
    ) -> List[InterviewQuestion]:
        """获取面试题目"""
        # 构建查询条件
        conditions = [InterviewQuestion.is_active == True]

        # 根据面试模式确定题目分类
        if interview_mode == "technical":
            conditions.append(InterviewQuestion.category == "technical")
            if job_type:
                conditions.append(InterviewQuestion.job_type == job_type)
        elif interview_mode == "behavior":
            conditions.append(InterviewQuestion.category == "behavioral")
        else:  # ai模式 - 混合题目
            # AI模式可以包含各类题目
            pass

        query = select(InterviewQuestion).where(and_(*conditions))
        # 纯随机排序，每次出题都不一样
        query = query.order_by(func.random())
        query = query.limit(count)

        result = await db.execute(query)
        questions = list(result.scalars().all())

        # 如果题目不够，补充通用题目
        if len(questions) < count:
            general_query = select(InterviewQuestion).where(
                and_(
                    InterviewQuestion.is_active == True,
                    InterviewQuestion.category == "general"
                )
            ).limit(count - len(questions))
            general_result = await db.execute(general_query)
            questions.extend(general_result.scalars().all())

        return questions

    @staticmethod
    async def start_interview(
        db: AsyncSession,
        user_id: int,
        interview_mode: str,
        target_job: Optional[str] = None,
        question_count: int = 5
    ) -> InterviewSessionCreate:
        """开始面试"""
        # 获取题目
        questions = await InterviewService.get_questions_for_interview(
            db, interview_mode, target_job, question_count
        )

        if not questions:
            # 如果没有题目，创建默认题目
            questions = await InterviewService.create_default_questions(db, interview_mode, target_job)

        # 创建面试会话
        session = InterviewSession(
            user_id=user_id,
            interview_mode=interview_mode,
            target_job=target_job,
            status="in_progress",
            started_at=datetime.utcnow()
        )
        db.add(session)
        await db.flush()

        # 为每个题目创建空的回答记录
        for i, question in enumerate(questions):
            answer = InterviewAnswer(
                session_id=session.id,
                question_id=question.id,
                user_answer="",
                score=0
            )
            db.add(answer)

        await db.commit()

        return InterviewSessionCreate(
            session_id=session.id,
            questions=[
                InterviewQuestionResponse(
                    id=q.id,
                    category=q.category,
                    job_type=q.job_type,
                    question_text=q.question_text,
                    difficulty=q.difficulty,
                    tags=q.tags,
                    question_order=i
                )
                for i, q in enumerate(questions)
            ],
            total_questions=len(questions),
            started_at=session.started_at
        )

    @staticmethod
    async def create_default_questions(
        db: AsyncSession,
        interview_mode: str,
        job_type: Optional[str] = None
    ) -> List[InterviewQuestion]:
        """创建默认面试题目"""
        default_questions = [
            # 技术类题目
            {
                "category": "technical",
                "job_type": job_type or "general",
                "question_text": "请介绍一下你最熟悉的技术栈，并说明你在项目中是如何运用的？",
                "reference_answer": "应该清晰描述技术栈的组成部分，并结合具体项目说明应用场景和解决的问题。",
                "difficulty": "medium",
                "tags": ["技术栈", "项目经验"]
            },
            {
                "category": "technical",
                "job_type": job_type or "general",
                "question_text": "请描述一个你遇到过的技术难题，你是如何解决的？",
                "reference_answer": "应该包含问题描述、分析过程、解决方案和结果总结。",
                "difficulty": "hard",
                "tags": ["问题解决", "技术能力"]
            },
            # 行为类题目
            {
                "category": "behavioral",
                "job_type": None,
                "question_text": "请介绍一下你自己，包括你的教育背景和工作经历。",
                "reference_answer": "应该简洁明了地介绍个人背景，突出与应聘岗位相关的经历。",
                "difficulty": "easy",
                "tags": ["自我介绍", "沟通能力"]
            },
            {
                "category": "behavioral",
                "job_type": None,
                "question_text": "描述一次团队合作的经历，你在其中扮演了什么角色？",
                "reference_answer": "应该具体描述团队目标、个人职责、协作过程和最终成果。",
                "difficulty": "medium",
                "tags": ["团队合作", "沟通能力"]
            },
            {
                "category": "behavioral",
                "job_type": None,
                "question_text": "你遇到过与同事意见不合的情况吗？你是如何处理的？",
                "reference_answer": "应该体现沟通协调能力，说明如何理性分析问题并达成共识。",
                "difficulty": "medium",
                "tags": ["沟通协调", "冲突处理"]
            },
            {
                "category": "behavioral",
                "job_type": None,
                "question_text": "你认为自己最大的优点和缺点是什么？",
                "reference_answer": "优点应该与岗位相关，缺点应该诚实但可控，并说明改进措施。",
                "difficulty": "easy",
                "tags": ["自我认知", "诚实"]
            },
            {
                "category": "behavioral",
                "job_type": None,
                "question_text": "你对未来3-5年的职业规划是什么？",
                "reference_answer": "应该有清晰的职业目标，并与公司发展相结合。",
                "difficulty": "medium",
                "tags": ["职业规划", "目标感"]
            },
            # 通用题目
            {
                "category": "general",
                "job_type": None,
                "question_text": "你为什么选择我们公司？你对我们公司有什么了解？",
                "reference_answer": "应该展示对公司的调研和了解，说明个人与公司的匹配度。",
                "difficulty": "easy",
                "tags": ["求职动机", "公司了解"]
            },
            {
                "category": "general",
                "job_type": None,
                "question_text": "你有什么问题想问我们的吗？",
                "reference_answer": "应该提出有深度的问题，展示对岗位和公司的关注。",
                "difficulty": "easy",
                "tags": ["提问能力", "主动性"]
            }
        ]

        questions = []
        for i, q_data in enumerate(default_questions):
            question = InterviewQuestion(
                category=q_data["category"],
                job_type=q_data.get("job_type"),
                question_text=q_data["question_text"],
                reference_answer=q_data.get("reference_answer"),
                difficulty=q_data.get("difficulty", "medium"),
                tags=q_data.get("tags", []),
                question_order=i
            )
            db.add(question)
            questions.append(question)

        await db.commit()
        return questions

    @staticmethod
    async def get_session(db: AsyncSession, session_id: int) -> Optional[InterviewSession]:
        """获取面试会话"""
        query = select(InterviewSession).options(
            selectinload(InterviewSession.answers).selectinload(
                InterviewAnswer.question)
        ).where(InterviewSession.id == session_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def submit_answer(
        db: AsyncSession,
        session_id: int,
        question_id: int,
        user_answer: str,
        answer_duration: int = 0
    ) -> AnswerFeedback:
        """提交回答并获取评分"""
        # 获取会话
        session = await InterviewService.get_session(db, session_id)
        if not session:
            raise ValueError("面试会话不存在")

        # 获取问题
        question_query = select(InterviewQuestion).where(
            InterviewQuestion.id == question_id)
        question_result = await db.execute(question_query)
        question = question_result.scalar_one_or_none()
        if not question:
            raise ValueError("面试题目不存在")

        # 查找或创建回答记录
        answer_query = select(InterviewAnswer).where(
            and_(
                InterviewAnswer.session_id == session_id,
                InterviewAnswer.question_id == question_id
            )
        )
        answer_result = await db.execute(answer_query)
        answer = answer_result.scalar_one_or_none()

        if not answer:
            answer = InterviewAnswer(
                session_id=session_id,
                question_id=question_id
            )
            db.add(answer)

        # AI评分逻辑
        score, score_details, feedback, suggestions = await InterviewService.evaluate_answer(
            question, user_answer
        )

        # 更新回答
        answer.user_answer = user_answer
        answer.score = score
        answer.score_details = score_details
        answer.feedback = feedback
        answer.suggestions = suggestions
        answer.answer_duration = answer_duration

        await db.commit()
        await db.refresh(answer)

        return AnswerFeedback(
            id=answer.id,
            question_id=question_id,
            question_text=question.question_text,
            user_answer=user_answer,
            reference_answer=question.reference_answer,
            score=score,
            score_details=score_details,
            feedback=feedback,
            suggestions=suggestions,
            answer_duration=answer_duration
        )

    @staticmethod
    async def evaluate_answer(
        question: InterviewQuestion,
        user_answer: str
    ) -> tuple[float, Dict[str, float], str, str]:
        """评估回答（模拟AI评分）"""
        # 这里实现一个简单的评分逻辑
        # 实际项目中可以接入AI模型进行评分

        score = 0.0
        score_details = {
            "relevance": 0.0,  # 相关性
            "depth": 0.0,     # 深度
            "clarity": 0.0,   # 清晰度
            "completeness": 0.0  # 完整性
        }

        # 基础分数（回答了就有基础分）
        base_score = 40.0

        # 字数相关评分
        answer_length = len(user_answer.strip())
        if answer_length >= 200:
            score_details["completeness"] = 25.0
        elif answer_length >= 100:
            score_details["completeness"] = 20.0
        elif answer_length >= 50:
            score_details["completeness"] = 15.0
        else:
            score_details["completeness"] = 10.0

        # 相关性评分（检查关键词）
        if question.tags:
            matched_tags = sum(
                1 for tag in question.tags if tag.lower() in user_answer.lower())
            relevance_ratio = matched_tags / \
                len(question.tags) if question.tags else 0
            score_details["relevance"] = min(25.0, relevance_ratio * 25.0)
        else:
            score_details["relevance"] = 20.0

        # 深度评分（基于回答结构和内容）
        depth_indicators = ["因为", "所以", "首先",
                            "其次", "最后", "例如", "比如", "总结", "结果"]
        depth_count = sum(
            1 for indicator in depth_indicators if indicator in user_answer)
        score_details["depth"] = min(25.0, depth_count * 5.0)

        # 清晰度评分
        clarity_indicators = ["。", "，", "；", "第一", "第二", "一方面", "另一方面"]
        clarity_count = sum(
            1 for indicator in clarity_indicators if indicator in user_answer)
        score_details["clarity"] = min(25.0, clarity_count * 3.0 + 10.0)

        # 计算总分
        score = base_score + sum(score_details.values()) / 4

        # 限制在0-100
        score = min(100.0, max(0.0, score))

        # 生成反馈
        if score >= 85:
            feedback = "回答非常出色！内容充实、逻辑清晰，展现了良好的专业素养和表达能力。"
        elif score >= 70:
            feedback = "回答较好。内容较为完整，表达也比较清晰，可以适当增加一些具体案例来支撑观点。"
        elif score >= 60:
            feedback = "回答基本合格。建议在回答时更加详细地阐述观点，并提供具体的例子来增强说服力。"
        else:
            feedback = "回答需要改进。建议更深入地理解问题，提供更完整、更有条理的回答。"

        # 生成建议
        suggestions_list = []
        if score_details["completeness"] < 20:
            suggestions_list.append("建议提供更详细的回答，充分展示你的经验和能力")
        if score_details["depth"] < 15:
            suggestions_list.append("建议使用结构化的方式组织回答，如'首先...其次...最后...'")
        if score_details["relevance"] < 15:
            suggestions_list.append("建议更紧密地围绕问题核心进行回答")
        if score_details["clarity"] < 15:
            suggestions_list.append("建议使用更清晰的表达方式，适当使用标点和分段")

        if not suggestions_list:
            suggestions_list.append("继续保持，可以尝试用更多具体案例来丰富回答")

        suggestions = "；".join(suggestions_list)

        return score, score_details, feedback, suggestions

    @staticmethod
    async def complete_interview(db: AsyncSession, session_id: int) -> InterviewSession:
        """完成面试"""
        session = await InterviewService.get_session(db, session_id)
        if not session:
            raise ValueError("面试会话不存在")

        # 计算总分和生成报告
        total_score = 0.0
        all_feedback = []
        strengths = []
        improvements = []

        for answer in session.answers:
            total_score += answer.score
            if answer.feedback:
                all_feedback.append(answer.feedback)

        # 平均分
        if session.answers:
            total_score = total_score / len(session.answers)

        # 分析优势和改进点
        if total_score >= 80:
            strengths.append("整体表现优秀")
            strengths.append("回答逻辑清晰")
        elif total_score >= 60:
            strengths.append("基础能力良好")
            improvements.append("可以更深入地阐述观点")
        else:
            improvements.append("需要加强专业知识储备")
            improvements.append("建议提高表达能力")

        # 更新会话
        session.status = "completed"
        session.total_score = round(total_score, 1)
        session.overall_feedback = "；".join(
            all_feedback[:3]) if all_feedback else "面试已完成"
        session.strengths = strengths
        session.improvements = improvements
        session.completed_at = datetime.utcnow()

        if session.started_at:
            duration = (session.completed_at -
                        session.started_at).total_seconds() / 60
            session.duration = int(duration)

        await db.commit()
        await db.refresh(session)

        return session

    @staticmethod
    async def get_user_interviews(
        db: AsyncSession,
        user_id: int,
        limit: int = 10
    ) -> List[InterviewRecordItem]:
        """获取用户面试记录"""
        query = select(InterviewSession).options(
            selectinload(InterviewSession.answers)
        ).where(
            InterviewSession.user_id == user_id
        ).order_by(InterviewSession.created_at.desc()).limit(limit)

        result = await db.execute(query)
        sessions = result.scalars().all()

        records = []
        for session in sessions:
            mode_name = InterviewService.MODE_MAP.get(
                session.interview_mode, session.interview_mode
            )
            records.append(InterviewRecordItem(
                id=session.id,
                interview_mode=session.interview_mode,
                mode_name=mode_name,
                target_job=session.target_job,
                status=session.status,
                total_score=session.total_score,
                question_count=len(session.answers),
                completed_at=session.completed_at,
                created_at=session.created_at
            ))

        return records

    @staticmethod
    async def get_session_detail(
        db: AsyncSession,
        session_id: int,
        user_id: int
    ) -> Optional[InterviewSession]:
        """获取面试详情"""
        query = select(InterviewSession).options(
            selectinload(InterviewSession.answers).selectinload(
                InterviewAnswer.question)
        ).where(
            and_(
                InterviewSession.id == session_id,
                InterviewSession.user_id == user_id
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def init_default_data(db: AsyncSession):
        """初始化默认数据"""
        # 初始化岗位
        positions = [
            {"name": "Java开发工程师", "code": "java", "logo": "JV", "is_hot": True},
            {"name": "前端开发工程师", "code": "frontend", "logo": "FE", "is_hot": True},
            {"name": "产品经理", "code": "product", "logo": "PM", "is_hot": True},
            {"name": "数据分析师", "code": "data", "logo": "DA", "is_hot": True},
            {"name": "UI设计师", "code": "ui", "logo": "UI", "is_hot": False},
            {"name": "运营专员", "code": "operation", "logo": "OP", "is_hot": False},
            {"name": "Python开发工程师", "code": "python", "logo": "PY", "is_hot": True},
            {"name": "测试工程师", "code": "qa", "logo": "QA", "is_hot": False},
        ]

        for pos_data in positions:
            existing = await InterviewService.get_job_by_code(db, pos_data["code"])
            if not existing:
                position = JobPosition(**pos_data)
                db.add(position)

        await db.commit()
