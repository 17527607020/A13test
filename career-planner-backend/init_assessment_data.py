"""
初始化测评数据 - MBTI和霍兰德题目
"""
import asyncio
from sqlalchemy import select
from app.core.config import AsyncSessionLocal, engine, Base
from app.models.assessment import Assessment, AssessmentQuestion
from app.models.user import User  # 导入User模型以建立外键关系


# MBTI题目数据
MBTI_QUESTIONS = [
    # E/I 维度
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
    # S/N 维度
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
    # T/F 维度
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
    # J/P 维度
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

# 霍兰德题目数据
HOLLAND_QUESTIONS = [
    {"text": "我喜欢拆卸和组装机械装置", "dimension": "R", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢户外活动和体育运动", "dimension": "R", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢使用工具修理物品", "dimension": "R", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢研究科学问题", "dimension": "I", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢阅读科技类书籍", "dimension": "I", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢分析复杂的问题", "dimension": "I", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢绘画、音乐或写作", "dimension": "A", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢参加文艺活动", "dimension": "A", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢创造新事物", "dimension": "A", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢帮助他人解决问题", "dimension": "S", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢从事教育工作", "dimension": "S", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我关心社会公益问题", "dimension": "S", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢领导团队完成目标", "dimension": "E", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢销售和谈判", "dimension": "E", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我有创业的想法", "dimension": "E", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢有条理、有规律的工作", "dimension": "C", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我喜欢处理数据和文档", "dimension": "C", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
    {"text": "我注重细节和准确性", "dimension": "C", "options": [
        {"text": "非常符合", "value": "A", "score": 2},
        {"text": "比较符合", "value": "B", "score": 1},
        {"text": "不太符合", "value": "C", "score": 0}
    ]},
]


# 职业技能测评题目数据
SKILL_QUESTIONS = [
    # 沟通能力
    {"text": "我能够清晰、准确地表达自己的想法和观点", "dimension": "communication", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够认真倾听他人的意见并给予反馈", "dimension": "communication", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够根据不同对象调整沟通方式", "dimension": "communication", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    # 团队协作
    {"text": "我能够与不同性格的人合作共事", "dimension": "teamwork", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "在团队中，我愿意承担自己的责任", "dimension": "teamwork", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够在团队冲突中寻求共识", "dimension": "teamwork", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    # 问题解决
    {"text": "面对复杂问题时，我能够系统分析", "dimension": "problem_solving", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够提出创新的解决方案", "dimension": "problem_solving", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够在压力下保持冷静并做出决策", "dimension": "problem_solving", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    # 学习能力
    {"text": "我能够快速学习新知识和技能", "dimension": "learning", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我会主动寻找学习机会提升自己", "dimension": "learning", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够将学到的知识应用到实践中", "dimension": "learning", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    # 时间管理
    {"text": "我能够合理安排时间，按时完成任务", "dimension": "time_management", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够区分任务的优先级", "dimension": "time_management", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够避免拖延，保持高效工作", "dimension": "time_management", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    # 适应能力
    {"text": "我能够适应新的工作环境和变化", "dimension": "adaptability", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "面对挫折时，我能够快速调整心态", "dimension": "adaptability", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
    {"text": "我能够接受批评并从中学习", "dimension": "adaptability", "options": [
        {"text": "总是如此", "value": "A", "score": 4},
        {"text": "经常如此", "value": "B", "score": 3},
        {"text": "有时如此", "value": "C", "score": 2},
        {"text": "很少如此", "value": "D", "score": 1}
    ]},
]


async def init_assessments():
    """初始化测评数据"""
    async with AsyncSessionLocal() as db:
        # 检查是否已有数据
        result = await db.execute(select(Assessment))
        existing = result.scalars().first()
        if existing:
            print("测评数据已存在，跳过初始化")
            return

        # 创建MBTI测评
        mbti = Assessment(
            code="mbti",
            name="MBTI职业性格测评",
            description="了解你的性格类型，找到适合的职业方向。MBTI将人的性格分为16种类型，帮助你更好地认识自己。",
            icon="User",
            color="#6B5CE7",
            duration=15,
            question_count=len(MBTI_QUESTIONS)
        )
        db.add(mbti)
        await db.flush()

        # 添加MBTI题目
        for i, q in enumerate(MBTI_QUESTIONS):
            question = AssessmentQuestion(
                assessment_id=mbti.id,
                question_text=q["text"],
                question_order=i + 1,
                dimension=q["dimension"],
                options=q["options"]
            )
            db.add(question)

        # 创建霍兰德测评
        holland = Assessment(
            code="holland",
            name="霍兰德职业兴趣测评",
            description="基于兴趣倾向，推荐适合的职业领域。霍兰德理论将职业兴趣分为六种类型，帮助你找到最适合的职业方向。",
            icon="TrendCharts",
            color="#E95CBF",
            duration=10,
            question_count=len(HOLLAND_QUESTIONS)
        )
        db.add(holland)
        await db.flush()

        # 添加霍兰德题目
        for i, q in enumerate(HOLLAND_QUESTIONS):
            question = AssessmentQuestion(
                assessment_id=holland.id,
                question_text=q["text"],
                question_order=i + 1,
                dimension=q["dimension"],
                options=q["options"]
            )
            db.add(question)

        # 创建职业技能测评
        skill = Assessment(
            code="skill",
            name="职业技能测评",
            description="评估你的核心职业技能水平，包括沟通能力、团队协作、问题解决、学习能力等关键职场技能。",
            icon="Collection",
            color="#54A0FF",
            duration=20,
            question_count=len(SKILL_QUESTIONS)
        )
        db.add(skill)
        await db.flush()

        # 添加职业技能题目
        for i, q in enumerate(SKILL_QUESTIONS):
            question = AssessmentQuestion(
                assessment_id=skill.id,
                question_text=q["text"],
                question_order=i + 1,
                dimension=q["dimension"],
                options=q["options"]
            )
            db.add(question)

        await db.commit()
        print("测评数据初始化完成！")
        print(f"- MBTI测评：{len(MBTI_QUESTIONS)}题")
        print(f"- 霍兰德测评：{len(HOLLAND_QUESTIONS)}题")
        print(f"- 职业技能测评：{len(SKILL_QUESTIONS)}题")


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
