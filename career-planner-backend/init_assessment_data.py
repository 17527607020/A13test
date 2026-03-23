"""
初始化测评数据 - 16型人格职业性格测试、心理健康测评、职场情商测评
"""
import asyncio
from sqlalchemy import select
from app.core.config import AsyncSessionLocal, engine, Base
from app.models.assessment import Assessment, AssessmentQuestion
from app.models.user import User


# 16型人格职业性格测试题目（基于MBTI）
PERSONALITY_QUESTIONS = [
    # E/I 维度 - 外向/内向
    {"text": "在社交聚会中，你通常会：", "dimension": "EI", "options": [
        {"text": "主动与许多人交谈，包括陌生人", "value": "A", "score": 1},
        {"text": "只与几个熟悉的人交谈", "value": "B", "score": 1}
    ]},
    {"text": "当你独处时，你通常感到：", "dimension": "EI", "options": [
        {"text": "精力充沛，享受独处时光", "value": "B", "score": 1},
        {"text": "有些无聊，想找人交流", "value": "A", "score": 1}
    ]},
    {"text": "在团队讨论中，你倾向于：", "dimension": "EI", "options": [
        {"text": "先发言，边说边思考", "value": "A", "score": 1},
        {"text": "先倾听，想好后再发言", "value": "B", "score": 1}
    ]},
    {"text": "周末你更喜欢：", "dimension": "EI", "options": [
        {"text": "参加派对或集体活动", "value": "A", "score": 1},
        {"text": "独自在家看书或看电影", "value": "B", "score": 1}
    ]},
    {"text": "你更喜欢与哪种人共事：", "dimension": "EI", "options": [
        {"text": "外向活跃、充满活力的人", "value": "A", "score": 1},
        {"text": "安静沉稳、深思熟虑的人", "value": "B", "score": 1}
    ]},
    # S/N 维度 - 感觉/直觉
    {"text": "你更重视：", "dimension": "SN", "options": [
        {"text": "当前的现实情况", "value": "A", "score": 1},
        {"text": "未来的可能性", "value": "B", "score": 1}
    ]},
    {"text": "你更信任：", "dimension": "SN", "options": [
        {"text": "经验和事实", "value": "A", "score": 1},
        {"text": "直觉和灵感", "value": "B", "score": 1}
    ]},
    {"text": "阅读时，你更喜欢：", "dimension": "SN", "options": [
        {"text": "具体明确的内容", "value": "A", "score": 1},
        {"text": "富有想象力的描述", "value": "B", "score": 1}
    ]},
    {"text": "你更擅长：", "dimension": "SN", "options": [
        {"text": "处理具体事务", "value": "A", "score": 1},
        {"text": "构思新想法", "value": "B", "score": 1}
    ]},
    {"text": "你认为成功更多来自于：", "dimension": "SN", "options": [
        {"text": "努力工作和实践经验", "value": "A", "score": 1},
        {"text": "创新思维和独特见解", "value": "B", "score": 1}
    ]},
    # T/F 维度 - 思考/情感
    {"text": "做决定时，你更看重：", "dimension": "TF", "options": [
        {"text": "逻辑和客观分析", "value": "A", "score": 1},
        {"text": "人情和价值观", "value": "B", "score": 1}
    ]},
    {"text": "当朋友遇到问题时，你倾向于：", "dimension": "TF", "options": [
        {"text": "提供解决方案", "value": "A", "score": 1},
        {"text": "给予情感支持", "value": "B", "score": 1}
    ]},
    {"text": "你认为更好的领导是：", "dimension": "TF", "options": [
        {"text": "公正客观的", "value": "A", "score": 1},
        {"text": "善解人意的", "value": "B", "score": 1}
    ]},
    {"text": "批评别人时，你会：", "dimension": "TF", "options": [
        {"text": "直言不讳，实事求是", "value": "A", "score": 1},
        {"text": "委婉表达，照顾感受", "value": "B", "score": 1}
    ]},
    {"text": "你更欣赏：", "dimension": "TF", "options": [
        {"text": "理性分析的能力", "value": "A", "score": 1},
        {"text": "同理心的品质", "value": "B", "score": 1}
    ]},
    # J/P 维度 - 判断/知觉
    {"text": "你更喜欢的生活方式是：", "dimension": "JP", "options": [
        {"text": "有计划、有条理的", "value": "A", "score": 1},
        {"text": "灵活、随性的", "value": "B", "score": 1}
    ]},
    {"text": "对于任务，你倾向于：", "dimension": "JP", "options": [
        {"text": "尽早完成，避免拖延", "value": "A", "score": 1},
        {"text": "在压力下更有动力", "value": "B", "score": 1}
    ]},
    {"text": "你的工作环境通常是：", "dimension": "JP", "options": [
        {"text": "整洁有序的", "value": "A", "score": 1},
        {"text": "有些凌乱但自己知道东西在哪", "value": "B", "score": 1}
    ]},
    {"text": "旅行时，你更喜欢：", "dimension": "JP", "options": [
        {"text": "提前规划好行程", "value": "A", "score": 1},
        {"text": "随性而行，临时决定", "value": "B", "score": 1}
    ]},
    {"text": "你认为规则：", "dimension": "JP", "options": [
        {"text": "应该被遵守", "value": "A", "score": 1},
        {"text": "可以根据情况变通", "value": "B", "score": 1}
    ]},
]

# 心理健康测评题目
MENTAL_HEALTH_QUESTIONS = [
    # 情绪状态
    {"text": "最近一个月，我感到心情愉快", "dimension": "emotion", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    {"text": "我能够控制自己的情绪波动", "dimension": "emotion", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    {"text": "我经常感到焦虑或紧张", "dimension": "emotion", "options": [
        {"text": "从不", "value": "A", "score": 4},
        {"text": "偶尔", "value": "B", "score": 3},
        {"text": "经常", "value": "C", "score": 2},
        {"text": "总是", "value": "D", "score": 1}
    ]},
    {"text": "我容易因为小事而感到沮丧", "dimension": "emotion", "options": [
        {"text": "从不", "value": "A", "score": 4},
        {"text": "偶尔", "value": "B", "score": 3},
        {"text": "经常", "value": "C", "score": 2},
        {"text": "总是", "value": "D", "score": 1}
    ]},
    # 压力管理
    {"text": "面对压力时，我能够有效应对", "dimension": "stress", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    {"text": "我有健康的减压方式", "dimension": "stress", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    {"text": "工作和生活的压力让我感到喘不过气", "dimension": "stress", "options": [
        {"text": "从不", "value": "A", "score": 4},
        {"text": "偶尔", "value": "B", "score": 3},
        {"text": "经常", "value": "C", "score": 2},
        {"text": "总是", "value": "D", "score": 1}
    ]},
    {"text": "我能够平衡工作与生活", "dimension": "stress", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    # 睡眠质量
    {"text": "我的睡眠质量很好", "dimension": "sleep", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    {"text": "我入睡困难或易醒", "dimension": "sleep", "options": [
        {"text": "从不", "value": "A", "score": 4},
        {"text": "偶尔", "value": "B", "score": 3},
        {"text": "经常", "value": "C", "score": 2},
        {"text": "总是", "value": "D", "score": 1}
    ]},
    {"text": "我早上醒来感到精力充沛", "dimension": "sleep", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    # 社交关系
    {"text": "我有可以倾诉心事的亲友", "dimension": "social", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    {"text": "我享受与人交往的过程", "dimension": "social", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    {"text": "我感到孤独或被孤立", "dimension": "social", "options": [
        {"text": "从不", "value": "A", "score": 4},
        {"text": "偶尔", "value": "B", "score": 3},
        {"text": "经常", "value": "C", "score": 2},
        {"text": "总是", "value": "D", "score": 1}
    ]},
    # 自我认知
    {"text": "我对自己的未来充满信心", "dimension": "self", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    {"text": "我能够接纳自己的缺点", "dimension": "self", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
    {"text": "我觉得自己有价值", "dimension": "self", "options": [
        {"text": "完全符合", "value": "A", "score": 4},
        {"text": "比较符合", "value": "B", "score": 3},
        {"text": "不太符合", "value": "C", "score": 2},
        {"text": "完全不符合", "value": "D", "score": 1}
    ]},
]

# 职场情商测评题目
EQ_QUESTIONS = [
    # 自我意识
    {"text": "我能够清楚地识别自己当下的情绪", "dimension": "self_awareness", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我了解自己的优势和不足", "dimension": "self_awareness", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我知道什么事情会触发我的负面情绪", "dimension": "self_awareness", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    # 自我管理
    {"text": "当我生气时，能够控制不做出过激行为", "dimension": "self_management", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "面对挫折时，我能够快速调整心态", "dimension": "self_management", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够为自己的错误承担责任", "dimension": "self_management", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够在压力下保持冷静", "dimension": "self_management", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    # 社会意识
    {"text": "我能够察觉他人的情绪变化", "dimension": "social_awareness", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够理解他人话中的言外之意", "dimension": "social_awareness", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够站在他人的角度思考问题", "dimension": "social_awareness", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够感知团队的整体氛围", "dimension": "social_awareness", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    # 关系管理
    {"text": "我能够有效地解决与他人的冲突", "dimension": "relationship", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够激励和影响他人", "dimension": "relationship", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够给予他人建设性的反馈", "dimension": "relationship", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够与不同性格的人建立良好关系", "dimension": "relationship", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够在团队中有效协作", "dimension": "relationship", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
]


async def clear_existing_data(db):
    """清除现有的测评数据"""
    from sqlalchemy import delete
    from app.models.assessment import AssessmentReport
    # 先删除报告数据（因为有外键约束）
    await db.execute(delete(AssessmentReport))
    # 再删除题目数据
    await db.execute(delete(AssessmentQuestion))
    # 最后删除测评类型
    await db.execute(delete(Assessment))
    await db.commit()
    print("已清除现有测评数据")


async def init_assessments():
    """初始化测评数据"""
    async with AsyncSessionLocal() as db:
        # 清除现有数据
        await clear_existing_data(db)

        # 创建16型人格职业性格测试
        personality = Assessment(
            code="personality",
            name="16型人格职业性格测试",
            description="基于MBTI理论，了解你的性格类型，发现适合的职业方向。测试将分析你在四个维度的偏好，帮助你更好地认识自己。",
            icon="User",
            color="#6B5CE7",
            duration=15,
            question_count=len(PERSONALITY_QUESTIONS)
        )
        db.add(personality)
        await db.flush()

        # 添加16型人格题目
        for i, q in enumerate(PERSONALITY_QUESTIONS):
            question = AssessmentQuestion(
                assessment_id=personality.id,
                question_text=q["text"],
                question_order=i + 1,
                dimension=q["dimension"],
                options=q["options"]
            )
            db.add(question)

        # 创建心理健康测评
        mental_health = Assessment(
            code="mental_health",
            name="心理健康测评",
            description="全面评估你的心理健康状况，包括情绪状态、压力管理、睡眠质量、社交关系和自我认知等维度。",
            icon="TrendCharts",
            color="#10B981",
            duration=12,
            question_count=len(MENTAL_HEALTH_QUESTIONS)
        )
        db.add(mental_health)
        await db.flush()

        # 添加心理健康题目
        for i, q in enumerate(MENTAL_HEALTH_QUESTIONS):
            question = AssessmentQuestion(
                assessment_id=mental_health.id,
                question_text=q["text"],
                question_order=i + 1,
                dimension=q["dimension"],
                options=q["options"]
            )
            db.add(question)

        # 创建职场情商测评
        eq = Assessment(
            code="eq",
            name="职场情商测评",
            description="评估你的职场情商水平，包括自我意识、自我管理、社会意识和关系管理四个核心维度，助你提升职场软实力。",
            icon="Collection",
            color="#F59E0B",
            duration=10,
            question_count=len(EQ_QUESTIONS)
        )
        db.add(eq)
        await db.flush()

        # 添加职场情商题目
        for i, q in enumerate(EQ_QUESTIONS):
            question = AssessmentQuestion(
                assessment_id=eq.id,
                question_text=q["text"],
                question_order=i + 1,
                dimension=q["dimension"],
                options=q["options"]
            )
            db.add(question)

        await db.commit()
        print("测评数据初始化完成！")
        print(f"- 16型人格职业性格测试：{len(PERSONALITY_QUESTIONS)}题")
        print(f"- 心理健康测评：{len(MENTAL_HEALTH_QUESTIONS)}题")
        print(f"- 职场情商测评：{len(EQ_QUESTIONS)}题")


async def create_tables():
    """创建数据表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("数据表创建完成")


async def main():
    """主函数"""
    await create_tables()
    await init_assessments()


if __name__ == "__main__":
    asyncio.run(main())
