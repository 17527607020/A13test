"""
职业测评服务
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.assessment import Assessment, AssessmentQuestion, AssessmentReport
from app.schemas.assessment import (
    AssessmentSubmit, AnswerSubmit, DimensionScore
)


class AssessmentService:
    """测评服务"""

    @staticmethod
    async def get_assessments(db: AsyncSession) -> List[Assessment]:
        """获取所有测评类型"""
        result = await db.execute(select(Assessment).order_by(Assessment.id))
        return result.scalars().all()

    @staticmethod
    async def get_assessment_by_id(db: AsyncSession, assessment_id: int) -> Optional[Assessment]:
        """根据ID获取测评"""
        result = await db.execute(select(Assessment).where(Assessment.id == assessment_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_assessment_by_code(db: AsyncSession, code: str) -> Optional[Assessment]:
        """根据code获取测评"""
        result = await db.execute(select(Assessment).where(Assessment.code == code))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_questions(db: AsyncSession, assessment_id: int) -> List[AssessmentQuestion]:
        """获取测评题目"""
        result = await db.execute(
            select(AssessmentQuestion)
            .where(AssessmentQuestion.assessment_id == assessment_id)
            .order_by(AssessmentQuestion.question_order)
        )
        return result.scalars().all()

    @staticmethod
    async def get_user_reports(db: AsyncSession, user_id: int) -> List[AssessmentReport]:
        """获取用户测评报告"""
        result = await db.execute(
            select(AssessmentReport)
            .where(AssessmentReport.user_id == user_id)
            .order_by(AssessmentReport.completed_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_report_by_id(db: AsyncSession, report_id: int, user_id: int) -> Optional[AssessmentReport]:
        """获取报告详情"""
        result = await db.execute(
            select(AssessmentReport)
            .where(AssessmentReport.id == report_id)
            .where(AssessmentReport.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def submit_assessment(
        db: AsyncSession,
        user_id: int,
        submit_data: AssessmentSubmit,
        assessment: Assessment
    ) -> AssessmentReport:
        """提交测评并生成报告"""

        # 获取题目
        questions = await AssessmentService.get_questions(db, submit_data.assessment_id)
        question_map = {q.id: q for q in questions}

        # 计算得分
        if assessment.code == 'mbti':
            result = AssessmentService._calculate_mbti(
                submit_data.answers, question_map)
        elif assessment.code == 'holland':
            result = AssessmentService._calculate_holland(
                submit_data.answers, question_map)
        else:
            result = AssessmentService._calculate_generic(
                submit_data.answers, question_map)

        # 保存原始答案
        raw_answers = {
            ans.question_id: ans.answer for ans in submit_data.answers}

        # 创建报告
        report = AssessmentReport(
            user_id=user_id,
            assessment_id=submit_data.assessment_id,
            result_type=result['result_type'],
            result_name=result['result_name'],
            scores=result['scores'],
            dimensions=result.get('dimensions'),
            suggestions=result['suggestions'],
            raw_answers=raw_answers,
            total_score=result.get('total_score', 0)
        )

        db.add(report)
        await db.commit()
        await db.refresh(report)

        return report

    @staticmethod
    def _calculate_mbti(answers: List[AnswerSubmit], question_map: Dict) -> Dict[str, Any]:
        """计算MBTI结果"""
        # MBTI四个维度
        scores = {'E': 0, 'I': 0, 'S': 0, 'N': 0,
                  'T': 0, 'F': 0, 'J': 0, 'P': 0}

        for answer in answers:
            question = question_map.get(answer.question_id)
            if question and question.dimension:
                # 根据维度和答案计算得分
                dimension = question.dimension
                if answer.answer == 'A':
                    scores[dimension[0]] += 1
                else:
                    scores[dimension[1]] += 1

        # 确定类型
        mbti_type = ''
        mbti_type += 'E' if scores['E'] >= scores['I'] else 'I'
        mbti_type += 'S' if scores['S'] >= scores['N'] else 'N'
        mbti_type += 'T' if scores['T'] >= scores['F'] else 'F'
        mbti_type += 'J' if scores['J'] >= scores['P'] else 'P'

        # MBTI类型描述
        mbti_descriptions = {
            'INTJ': '建筑师 - 富有想象力的战略家',
            'INTP': '逻辑学家 - 创新的发明家',
            'ENTJ': '指挥官 - 大胆的领导者',
            'ENTP': '辩论家 - 聪明的探索者',
            'INFJ': '提倡者 - 安静的理想主义者',
            'INFP': '调停者 - 诗意的理想主义者',
            'ENFJ': '主人公 - 富有魅力的领导者',
            'ENFP': '竞选者 - 热情的探索者',
            'ISTJ': '物流师 - 可靠的实干家',
            'ISFJ': '守卫者 - 忠诚的守护者',
            'ESTJ': '总经理 - 高效的管理者',
            'ESFJ': '执政官 - 关心他人的支持者',
            'ISTP': '鉴赏家 - 大胆的实验者',
            'ISFP': '探险家 - 灵活的艺术家',
            'ESTP': '企业家 - 精明的冒险者',
            'ESFP': '表演者 - 自发的娱乐者'
        }

        # 职业建议
        career_suggestions = {
            'INTJ': '适合从事战略规划、科学研究、系统分析等工作',
            'INTP': '适合从事科学研究、技术开发、数据分析等工作',
            'ENTJ': '适合从事企业管理、项目领导、创业等工作',
            'ENTP': '适合从事创业、咨询、市场营销等工作',
            'INFJ': '适合从事心理咨询、教育、写作、人力资源等工作',
            'INFP': '适合从事创意设计、写作、教育、社会工作等工作',
            'ENFJ': '适合从事教育、培训、人力资源、公共关系等工作',
            'ENFP': '适合从事市场营销、公关、创意设计、媒体等工作',
            'ISTJ': '适合从事会计、审计、项目管理、法律等工作',
            'ISFJ': '适合从事医疗护理、教育、行政助理等工作',
            'ESTJ': '适合从事管理、金融、法律、行政等工作',
            'ESFJ': '适合从事人力资源、客户服务、教育、医疗等工作',
            'ISTP': '适合从事工程、技术支持、质量控制等工作',
            'ISFP': '适合从事艺术设计、室内设计、音乐、美容等工作',
            'ESTP': '适合从事销售、市场营销、体育、金融交易等工作',
            'ESFP': '适合从事演艺、销售、旅游、活动策划等工作'
        }

        # 计算维度百分比
        dimensions = [
            DimensionScore(dimension='外向(E)/内向(I)', score=max(scores['E'], scores['I']), max_score=scores['E'] +
                           scores['I'], percentage=scores['E'] / (scores['E'] + scores['I'] + 0.01) * 100),
            DimensionScore(dimension='感觉(S)/直觉(N)', score=max(scores['S'], scores['N']), max_score=scores['S'] +
                           scores['N'], percentage=scores['S'] / (scores['S'] + scores['N'] + 0.01) * 100),
            DimensionScore(dimension='思考(T)/情感(F)', score=max(scores['T'], scores['F']), max_score=scores['T'] +
                           scores['F'], percentage=scores['T'] / (scores['T'] + scores['F'] + 0.01) * 100),
            DimensionScore(dimension='判断(J)/感知(P)', score=max(scores['J'], scores['P']), max_score=scores['J'] +
                           scores['P'], percentage=scores['J'] / (scores['J'] + scores['P'] + 0.01) * 100),
        ]

        return {
            'result_type': mbti_type,
            'result_name': mbti_descriptions.get(mbti_type, mbti_type),
            'scores': scores,
            'dimensions': [d.model_dump() for d in dimensions],
            'suggestions': career_suggestions.get(mbti_type, '建议根据个人兴趣选择适合的职业方向')
        }

    @staticmethod
    def _calculate_holland(answers: List[AnswerSubmit], question_map: Dict) -> Dict[str, Any]:
        """计算霍兰德结果"""
        # 霍兰德六个类型
        scores = {'R': 0, 'I': 0, 'A': 0, 'S': 0, 'E': 0, 'C': 0}

        for answer in answers:
            question = question_map.get(answer.question_id)
            if question and question.dimension:
                # 根据答案加分
                if answer.answer == 'A':
                    scores[question.dimension] += 1

        # 排序获取前三个类型
        sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_three = sorted_types[:3]
        holland_code = ''.join([t[0] for t in top_three])

        # 霍兰德类型描述
        holland_descriptions = {
            'R': '现实型(Realistic) - 喜欢动手操作，擅长使用工具',
            'I': '研究型(Investigative) - 喜欢思考分析，擅长科学研究',
            'A': '艺术型(Artistic) - 喜欢创意表达，擅长艺术创作',
            'S': '社会型(Social) - 喜欢帮助他人，擅长人际交往',
            'E': '企业型(Enterprising) - 喜欢领导管理，擅长商业活动',
            'C': '常规型(Conventional) - 喜欢有序工作，擅长数据处理'
        }

        # 职业建议
        career_map = {
            'R': '工程师、技术员、机械师、厨师、运动员',
            'I': '科学家、研究员、分析师、医生、程序员',
            'A': '设计师、作家、音乐家、演员、摄影师',
            'S': '教师、咨询师、社工、医护人员、人力资源',
            'E': '企业家、销售经理、律师、政治家、营销人员',
            'C': '会计、审计、秘书、图书管理员、数据分析师'
        }

        result_name = ' + '.join([holland_descriptions.get(t[0], t[0])
                                 for t in top_three])
        suggestions = '推荐职业方向：' + \
            '、'.join([career_map.get(t[0], '') for t in top_three])

        total = sum(scores.values()) or 1
        dimensions = [
            DimensionScore(
                dimension='现实型(R)', score=scores['R'], max_score=total, percentage=scores['R'] / total * 100),
            DimensionScore(
                dimension='研究型(I)', score=scores['I'], max_score=total, percentage=scores['I'] / total * 100),
            DimensionScore(
                dimension='艺术型(A)', score=scores['A'], max_score=total, percentage=scores['A'] / total * 100),
            DimensionScore(
                dimension='社会型(S)', score=scores['S'], max_score=total, percentage=scores['S'] / total * 100),
            DimensionScore(
                dimension='企业型(E)', score=scores['E'], max_score=total, percentage=scores['E'] / total * 100),
            DimensionScore(
                dimension='常规型(C)', score=scores['C'], max_score=total, percentage=scores['C'] / total * 100),
        ]

        return {
            'result_type': holland_code,
            'result_name': result_name,
            'scores': scores,
            'dimensions': [d.model_dump() for d in dimensions],
            'suggestions': suggestions
        }

    @staticmethod
    def _calculate_generic(answers: List[AnswerSubmit], question_map: Dict) -> Dict[str, Any]:
        """通用测评计算（职业技能测评）"""
        # 按维度统计得分
        dimension_scores: Dict[str, Dict[str, int]] = {}

        for answer in answers:
            question = question_map.get(answer.question_id)
            if question and question.dimension:
                dim = question.dimension
                if dim not in dimension_scores:
                    dimension_scores[dim] = {'score': 0, 'max_score': 0}

                # 找到选中选项的分数
                if question.options:
                    for opt in question.options:
                        if opt.get('value') == answer.answer:
                            dimension_scores[dim]['score'] += opt.get(
                                'score', 0)
                        dimension_scores[dim]['max_score'] += opt.get(
                            'score', 0)

        # 计算各维度百分比
        dimension_names = {
            'communication': '沟通能力',
            'teamwork': '团队协作',
            'problem_solving': '问题解决',
            'learning': '学习能力',
            'time_management': '时间管理',
            'adaptability': '适应能力'
        }

        dimensions = []
        total_score = 0
        total_max = 0

        for dim, scores in dimension_scores.items():
            max_score = scores['max_score'] or 1
            percentage = (scores['score'] / max_score) * 100
            total_score += scores['score']
            total_max += max_score

            dimensions.append(DimensionScore(
                dimension=dimension_names.get(dim, dim),
                score=scores['score'],
                max_score=max_score,
                percentage=percentage
            ))

        # 计算总分百分比
        overall_percentage = (total_score / total_max *
                              100) if total_max > 0 else 0

        # 生成技能等级
        if overall_percentage >= 85:
            level = "优秀"
            suggestion = "你的职业技能水平非常出色，建议继续深耕专业领域，可以考虑承担更多领导角色。"
        elif overall_percentage >= 70:
            level = "良好"
            suggestion = "你的职业技能水平良好，建议在薄弱环节加强训练，持续提升综合能力。"
        elif overall_percentage >= 50:
            level = "中等"
            suggestion = "你的职业技能处于中等水平，建议制定系统的提升计划，多参与实践锻炼。"
        else:
            level = "待提升"
            suggestion = "建议你系统学习职业技能相关知识，多参与团队协作和实践项目，逐步提升各项能力。"

        return {
            'result_type': f'{overall_percentage:.0f}分',
            'result_name': f'职业技能水平：{level}',
            'scores': {dim: scores['score'] for dim, scores in dimension_scores.items()},
            'dimensions': [d.model_dump() for d in dimensions],
            'suggestions': suggestion,
            'total_score': total_score
        }
