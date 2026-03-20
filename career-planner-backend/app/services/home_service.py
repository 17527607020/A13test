"""
首页服务层
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User
from app.models.assessment import AssessmentReport
from app.models.interview import InterviewSession
from app.schemas.home import (
    HomeDataResponse,
    ProgressItem,
    LearningResource,
    AIRecommendation,
    QuickAction
)


class HomeService:
    """首页服务"""

    # 学习资源数据（可以从数据库或配置文件中获取）
    LEARNING_RESOURCES = [
        {
            "id": 1,
            "title": "职业规划入门",
            "description": "了解如何制定有效的职业规划，包括目标设定、路径规划等核心内容。",
            "logo": "CP",
            "color": "#6B5CE7",
            "tag": "基础",
            "tag_type": "primary",
            "content": """# 职业规划入门指南

## 一、什么是职业规划？

职业规划是指个人根据自身情况、职业环境和职业发展机会，对自己的职业发展道路进行设计和规划的过程。一个好的职业规划可以帮助你明确方向，少走弯路。

## 二、职业规划的五个步骤

### 1. 自我认知
首先要了解自己的性格、兴趣、能力和价值观。可以通过以下方式进行自我认知：
- 完成职业性格测评（如MBTI、霍兰德职业兴趣测试）
- 回顾自己的成功经历和失败经历
- 寻求他人的反馈

### 2. 环境分析
了解外部环境，包括：
- 行业发展趋势
- 岗位需求变化
- 薪资水平
- 发展空间

### 3. 目标设定
根据SMART原则设定职业目标：
- **S**pecific（具体的）：明确你想达到什么职位
- **M**easurable（可衡量的）：设定可量化的指标
- **A**chievable（可实现的）：目标要有挑战但可实现
- **R**elevant（相关的）：与你的职业方向一致
- **T**ime-bound（有时限的）：设定完成时间

### 4. 制定计划
将大目标分解为小目标，制定具体的行动计划：
- 短期目标（1年内）
- 中期目标（1-3年）
- 长期目标（3-5年）

### 5. 执行与调整
- 定期检查进度
- 根据实际情况调整计划
- 保持学习和成长

## 三、常见误区

1. **只看薪资**：职业选择应该综合考虑发展空间、兴趣匹配度等因素
2. **盲目跟风**：不要因为某个行业热门就盲目进入，要考虑是否适合自己
3. **缺乏耐心**：职业发展是一个长期过程，需要持续努力

## 四、开始行动

现在就开始你的职业规划之旅吧！完成职业测评，了解自己的性格特点，然后制定属于你的职业发展计划。
"""
        },
        {
            "id": 2,
            "title": "简历撰写技巧",
            "description": "学习如何打造一份专业的简历，突出个人优势和技能，提高面试邀请率。",
            "logo": "CV",
            "color": "#8A7FE0",
            "tag": "求职",
            "tag_type": "success",
            "content": """# 简历撰写技巧指南

## 一、简历的重要性

简历是求职的"敲门砖"，一份优秀的简历可以让你在众多候选人中脱颖而出，获得宝贵的面试机会。

## 二、简历的基本结构

### 1. 个人信息
- 姓名、联系方式（电话、邮箱）
- 求职意向
- 可选：个人网站、GitHub链接等

### 2. 教育背景
- 学校名称、专业、学历
- 毕业时间
- 可选：GPA、主修课程、荣誉奖项

### 3. 实习/工作经历
- 公司名称、职位、时间
- **重点描述工作内容和成果**
- 使用"动词+工作内容+成果"的格式

### 4. 项目经历
- 项目名称、角色
- 项目描述、使用技术
- 个人贡献和项目成果

### 5. 技能证书
- 专业技能（编程语言、软件工具等）
- 语言能力
- 相关证书

## 三、简历撰写要点

### 突出重点
- 将最重要、最相关的内容放在前面
- 根据应聘岗位调整简历内容

### 量化成果
- ❌ "负责销售工作"
- ✅ "负责华东区销售工作，季度销售额增长30%"

### 使用关键词
- 研读职位描述，提取关键词
- 在简历中自然融入这些关键词

### 排版清晰
- 使用统一的字体和格式
- 合理使用空白和分段
- 控制在1-2页

## 四、常见错误

1. **错别字和语法错误**：仔细检查，请他人帮忙审阅
2. **信息不真实**：诚实是最基本的原则
3. **过于冗长**：HR平均只花6秒看一份简历
4. **格式混乱**：保持简洁专业

## 五、简历模板参考

```
姓名 | 电话 | 邮箱

求职意向：前端开发工程师

教育背景
XX大学 | 计算机科学 | 本科 | 2020-2024

实习经历
XX科技公司 | 前端开发实习生 | 2023.06-2023.09
- 负责公司官网改版，使用Vue3+TypeScript开发
- 优化页面加载速度，首屏加载时间减少40%
- 参与组件库开发，编写10+通用组件

项目经历
个人博客系统 | 独立开发者 | 2023.03-2023.05
- 使用Next.js+MDX搭建个人博客
- 实现文章分类、标签、搜索功能
- 部署在Vercel，日均访问量200+

技能
- 前端：HTML/CSS/JavaScript/TypeScript/Vue/React
- 工具：Git/Webpack/Vite
- 英语：CET-6
```

开始优化你的简历吧！
"""
        },
        {
            "id": 3,
            "title": "面试准备指南",
            "description": "掌握面试技巧，包括常见问题回答、礼仪等方面的准备，助你顺利通过面试。",
            "logo": "IV",
            "color": "#E95CBF",
            "tag": "求职",
            "tag_type": "warning",
            "content": """# 面试准备指南

## 一、面试前准备

### 1. 了解公司
- 公司业务、产品、文化
- 行业地位、竞争对手
- 最新动态和新闻

### 2. 岗位研究
- 岗位职责和要求
- 需要的技能和经验
- 可能的面试问题

### 3. 准备材料
- 多份简历打印件
- 作品集（如适用）
- 笔记本和笔
- 证书原件/复印件

## 二、常见面试问题及回答技巧

### 自我介绍
**问题**：请简单介绍一下自己。

**回答框架**：
1. 基本信息（姓名、教育背景）
2. 相关经历（实习、项目）
3. 为什么应聘这个岗位
4. 个人优势

**示例**：
"您好，我叫XXX，XX大学计算机专业应届毕业生。在校期间参与过多个Web开发项目，熟练使用Vue和React框架。曾在XX公司实习，负责前端开发工作。我对贵公司的产品非常感兴趣，希望能加入团队发挥我的专业技能。"

### 优缺点
**问题**：你的优点和缺点是什么？

**回答技巧**：
- 优点：与岗位相关，举例说明
- 缺点：真实但可控，说明改进措施

### 为什么选择我们公司
**回答要点**：
- 公司的吸引力（产品、文化、发展）
- 与个人职业规划的匹配
- 能为公司带来的价值

### 职业规划
**回答框架**：
- 短期：快速融入团队，提升专业技能
- 中期：成为团队骨干，承担更多责任
- 长期：在专业领域深入发展

## 三、面试礼仪

### 着装
- 商务休闲为主
- 整洁大方
- 避免过于随意或正式

### 时间
- 提前10-15分钟到达
- 如有意外情况及时沟通

### 沟通
- 保持眼神交流
- 语速适中，表达清晰
- 积极倾听，适时提问

### 结束时
- 感谢面试官
- 询问后续流程
- 发送感谢邮件

## 四、技术面试准备

### 编程基础
- 数据结构与算法
- 计算机网络
- 操作系统
- 数据库

### 专业技能
- 根据岗位要求准备
- 复习项目中的技术点
- 了解最新技术趋势

### 代码练习
- LeetCode刷题
- 手写代码练习
- 系统设计题

## 五、面试后跟进

1. 24小时内发送感谢邮件
2. 总结面试中的表现
3. 记录面试问题，查漏补缺
4. 耐心等待结果

祝你面试顺利！
"""
        },
        {
            "id": 4,
            "title": "行业趋势分析",
            "description": "了解当前热门行业的发展趋势和未来前景，为职业选择提供参考依据。",
            "logo": "TR",
            "color": "#54A0FF",
            "tag": "洞察",
            "tag_type": "info",
            "content": """# 行业趋势分析

## 一、科技行业

### 人工智能
**发展趋势**：
- AI大模型应用爆发
- AIGC（AI生成内容）快速发展
- AI+行业深度融合

**热门岗位**：
- 算法工程师
- NLP工程师
- AI产品经理
- 提示词工程师

### 云计算与大数据
**发展趋势**：
- 云原生技术普及
- 数据安全重要性提升
- 边缘计算兴起

**热门岗位**：
- 云架构师
- 数据工程师
- 数据分析师
- DevOps工程师

## 二、互联网行业

### 电商
**发展趋势**：
- 直播电商持续增长
- 跨境电商机会增多
- 私域运营成为重点

**热门岗位**：
- 电商运营
- 直播运营
- 用户增长
- 供应链管理

### 短视频与内容
**发展趋势**：
- 内容创作门槛降低
- 知识付费市场扩大
- AI辅助创作普及

**热门岗位**：
- 内容运营
- 视频剪辑
- 新媒体运营
- 内容策划

## 三、新能源行业

### 新能源汽车
**发展趋势**：
- 电动化加速渗透
- 智能化成为竞争点
- 充电基础设施完善

**热门岗位**：
- 电池工程师
- 自动驾驶算法
- 智能座舱开发
- 充电桩运营

### 储能与光伏
**发展趋势**：
- 储能技术突破
- 分布式光伏发展
- 能源数字化转型

**热门岗位**：
- 储能系统工程师
- 光伏设计师
- 能源管理师

## 四、医疗健康

### 医疗科技
**发展趋势**：
- AI辅助诊断
- 远程医疗普及
- 数字健康管理

**热门岗位**：
- 医疗AI工程师
- 生物信息工程师
- 医疗产品经理

### 医药研发
**发展趋势**：
- 创新药研发加速
- 基因技术应用
- 临床试验数字化

**热门岗位**：
- 药物研发
- 临床监查
- 医学事务

## 五、选择建议

### 评估维度
1. **行业前景**：市场规模、增长速度
2. **个人兴趣**：是否热爱这个领域
3. **能力匹配**：是否具备相关技能
4. **发展空间**：晋升通道、薪资水平

### 建议
- 关注新兴行业，抓住早期机会
- 选择与自己专业相关的领域
- 持续学习，保持竞争力
- 关注行业动态，及时调整方向

选择大于努力，方向决定未来！
"""
        }
    ]

    # 快速操作配置
    QUICK_ACTIONS = [
        {"label": "开始测评", "icon": "Edit",
            "route": "/assessment", "button_type": "primary"},
        {"label": "查看画像", "icon": "User",
            "route": "/student-profile", "button_type": "success"},
        {"label": "制定规划", "icon": "TrendCharts",
            "route": "/plan", "button_type": "warning"},
        {"label": "浏览岗位", "icon": "Search",
            "route": "/jobs/list", "button_type": "default"}
    ]

    @staticmethod
    async def get_user_stats(db: AsyncSession, user_id: int) -> dict:
        """获取用户统计数据"""
        # 测评完成数量
        assessment_count = await db.execute(
            select(func.count(AssessmentReport.id)).where(
                AssessmentReport.user_id == user_id
            )
        )
        total_assessments = assessment_count.scalar() or 0

        # 面试完成数量
        interview_count = await db.execute(
            select(func.count(InterviewSession.id)).where(
                InterviewSession.user_id == user_id,
                InterviewSession.status == "completed"
            )
        )
        total_interviews = interview_count.scalar() or 0

        return {
            "total_assessments": total_assessments,
            "total_interviews": total_interviews
        }

    @staticmethod
    async def get_progress_data(db: AsyncSession, user_id: int) -> List[ProgressItem]:
        """获取进度数据"""
        # 获取测评完成情况
        assessment_count = await db.execute(
            select(func.count(AssessmentReport.id)).where(
                AssessmentReport.user_id == user_id
            )
        )
        total_assessments = assessment_count.scalar() or 0

        # 计算测评进度（假设有3种测评类型）
        assessment_progress = min(100, int((total_assessments / 3) * 100))

        # 获取面试完成情况
        interview_count = await db.execute(
            select(func.count(InterviewSession.id)).where(
                InterviewSession.user_id == user_id,
                InterviewSession.status == "completed"
            )
        )
        total_interviews = interview_count.scalar() or 0

        # 计算面试进度（假设完成5次面试为100%）
        interview_progress = min(100, int((total_interviews / 5) * 100))

        # 规划进度（暂时固定，后续可以添加规划表）
        plan_progress = 25 if total_assessments > 0 else 0

        return [
            ProgressItem(
                title="职业测评",
                value=assessment_progress,
                description=f"已完成 {total_assessments} 项测评"
            ),
            ProgressItem(
                title="模拟面试",
                value=interview_progress,
                description=f"已完成 {total_interviews} 次面试"
            ),
            ProgressItem(
                title="规划进度",
                value=plan_progress,
                description="已设定职业目标" if plan_progress > 0 else "尚未开始规划"
            )
        ]

    @staticmethod
    async def get_ai_recommendation(db: AsyncSession, user_id: int) -> AIRecommendation:
        """获取AI推荐内容"""
        # 获取用户最新的测评结果
        latest_report = await db.execute(
            select(AssessmentReport).where(
                AssessmentReport.user_id == user_id
            ).order_by(AssessmentReport.completed_at.desc()).limit(1)
        )
        report = latest_report.scalar_one_or_none()

        if report and report.result_type:
            # 根据测评结果生成推荐
            result_type = report.result_type
            result_name = report.result_name or result_type

            # MBTI类型推荐
            mbti_recommendations = {
                "INFP": "你可能适合从事创意性工作，如设计、写作或教育。建议你探索相关领域的职业机会。",
                "ENFP": "你具有出色的沟通能力和创造力，适合从事市场营销、公关或创业相关工作。",
                "INFJ": "你具有深刻的洞察力，适合从事咨询、人力资源或社会工作等助人行业。",
                "ENFJ": "你天生具有领导魅力，适合从事管理、培训或教育行业。",
                "INTJ": "你具有战略性思维，适合从事数据分析、战略规划或技术研发工作。",
                "ENTJ": "你具有果断的决策力，适合从事企业管理、金融或法律行业。",
                "INTP": "你具有逻辑分析能力，适合从事软件开发、科研或学术工作。",
                "ENTP": "你具有创新思维，适合从事创业、投资或技术咨询工作。",
                "ISFP": "你具有艺术天赋，适合从事设计、音乐或手工艺等创意行业。",
                "ESFP": "你善于与人交往，适合从事销售、演艺或服务行业。",
                "ISTP": "你具有动手能力，适合从事工程技术、机械或体育行业。",
                "ESTP": "你善于应对挑战，适合从事销售、体育或应急救援工作。",
                "ISFJ": "你具有服务精神，适合从事医疗、教育或行政工作。",
                "ESFJ": "你善于照顾他人，适合从事护理、教育或人力资源工作。",
                "ISTJ": "你具有责任心，适合从事财务、审计或行政管理工作。",
                "ESTJ": "你具有组织能力，适合从事管理、行政或法律工作。"
            }

            content = mbti_recommendations.get(result_type,
                                               f"根据你的测评结果（{result_name}），建议你继续探索适合自己的职业方向。"
                                               )

            return AIRecommendation(
                title="职业顾问",
                subtitle=f"基于你的{result_type}测试结果推荐",
                content=content
            )

        # 默认推荐
        return AIRecommendation(
            title="职业顾问",
            subtitle="完成测评获取个性化推荐",
            content="建议你先完成职业测评，我们将根据你的性格特点和兴趣爱好，为你提供个性化的职业建议。"
        )

    @staticmethod
    def get_learning_resources() -> List[LearningResource]:
        """获取学习资源列表"""
        return [LearningResource(**resource) for resource in HomeService.LEARNING_RESOURCES]

    @staticmethod
    def get_quick_actions() -> List[QuickAction]:
        """获取快速操作列表"""
        return [QuickAction(**action) for action in HomeService.QUICK_ACTIONS]

    @staticmethod
    async def get_home_data(db: AsyncSession, user: User) -> HomeDataResponse:
        """获取首页所有数据"""
        # 获取进度数据
        progress_items = await HomeService.get_progress_data(db, user.id)

        # 获取AI推荐
        ai_recommendation = await HomeService.get_ai_recommendation(db, user.id)

        # 获取学习资源
        learning_resources = HomeService.get_learning_resources()

        # 获取快速操作
        quick_actions = HomeService.get_quick_actions()

        # 获取统计数据
        stats = await HomeService.get_user_stats(db, user.id)

        # 生成问候语
        from datetime import datetime
        hour = datetime.now().hour
        if 5 <= hour < 12:
            greeting = "早上好"
        elif 12 <= hour < 14:
            greeting = "中午好"
        elif 14 <= hour < 18:
            greeting = "下午好"
        else:
            greeting = "晚上好"

        return HomeDataResponse(
            username=user.username,
            greeting=greeting,
            progress_items=progress_items,
            ai_recommendation=ai_recommendation,
            learning_resources=learning_resources,
            quick_actions=quick_actions,
            total_assessments=stats["total_assessments"],
            total_interviews=stats["total_interviews"],
            total_plans=0
        )
