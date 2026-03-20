"""
初始化面试题目数据
为每个岗位添加面试题目
"""
import asyncio
from sqlalchemy import select, update
from app.core.config import AsyncSessionLocal
from app.models.interview import InterviewQuestion, JobPosition


# 各岗位的面试题目
JOB_QUESTIONS = {
    "java": [
        {
            "question_text": "请介绍一下Java的基本数据类型，以及它们和包装类的区别？",
            "reference_answer": "Java有8种基本数据类型：byte、short、int、long、float、double、char、boolean。包装类是对基本数据类型的封装，提供了更多方法和功能。主要区别：1) 基本类型存储在栈中，包装类对象存储在堆中；2) 包装类可以为null，基本类型不能；3) 包装类提供了类型转换等方法；4) Java 5之后支持自动装箱和拆箱。",
            "difficulty": "easy",
            "tags": ["Java基础", "数据类型"],
            "category": "technical"
        },
        {
            "question_text": "请解释Java中的多态是什么？如何实现多态？",
            "reference_answer": "多态是指同一个行为具有多个不同表现形式的能力。实现多态的三个条件：1) 继承；2) 方法重写；3) 父类引用指向子类对象。多态的好处：提高代码的扩展性和可维护性，降低耦合度。",
            "difficulty": "medium",
            "tags": ["Java", "面向对象", "多态"],
            "category": "technical"
        },
        {
            "question_text": "请解释Java中的集合框架，ArrayList和LinkedList的区别？",
            "reference_answer": "ArrayList基于动态数组实现，LinkedList基于双向链表实现。区别：1) ArrayList随机访问效率高O(1)，插入删除效率低O(n)；2) LinkedList插入删除效率高O(1)，随机访问效率低O(n)；3) ArrayList更节省内存；4) 根据使用场景选择合适的集合。",
            "difficulty": "medium",
            "tags": ["Java", "集合", "数据结构"],
            "category": "technical"
        },
        {
            "question_text": "请解释Java中的线程池，以及如何合理配置线程池参数？",
            "reference_answer": "线程池是管理线程的容器，可以复用线程、控制并发数。核心参数：corePoolSize（核心线程数）、maximumPoolSize（最大线程数）、workQueue（工作队列）、keepAliveTime（空闲线程存活时间）。配置建议：CPU密集型任务线程数=CPU核心数+1，IO密集型任务线程数=CPU核心数*2。",
            "difficulty": "hard",
            "tags": ["Java", "多线程", "线程池"],
            "category": "technical"
        },
        {
            "question_text": "请解释Spring框架的IOC和AOP是什么？",
            "reference_answer": "IOC（控制反转）是将对象的创建和管理交给Spring容器，通过依赖注入实现解耦。AOP（面向切面编程）是将与业务无关的逻辑（如日志、事务）抽取出来，通过代理模式实现。好处：降低耦合、提高代码复用、便于维护。",
            "difficulty": "medium",
            "tags": ["Spring", "IOC", "AOP"],
            "category": "technical"
        }
    ],
    "frontend": [
        {
            "question_text": "请解释Vue的生命周期有哪些？分别在什么时候调用？",
            "reference_answer": "Vue2生命周期：beforeCreate、created、beforeMount、mounted、beforeUpdate、updated、beforeDestroy、destroyed。Vue3使用setup替代了beforeCreate和created。mounted阶段DOM已挂载，适合发起请求；beforeDestroy适合清理定时器和事件监听。",
            "difficulty": "medium",
            "tags": ["Vue", "生命周期", "前端"],
            "category": "technical"
        },
        {
            "question_text": "请解释JavaScript中的闭包是什么？有什么应用场景？",
            "reference_answer": "闭包是指函数能够访问其词法作用域外的变量，即使外部函数已经执行完毕。应用场景：1) 数据私有化；2) 柯里化函数；3) 模块模式；4) 防抖节流函数。注意事项：闭包会导致内存不能及时释放，需要注意内存泄漏。",
            "difficulty": "medium",
            "tags": ["JavaScript", "闭包", "前端"],
            "category": "technical"
        },
        {
            "question_text": "请解释CSS盒模型，以及box-sizing属性的作用？",
            "reference_answer": "CSS盒模型包含content、padding、border、margin四部分。标准盒模型width只包含content，IE盒模型width包含content+padding+border。box-sizing: border-box使用IE盒模型，布局更方便计算。",
            "difficulty": "easy",
            "tags": ["CSS", "盒模型", "前端"],
            "category": "technical"
        },
        {
            "question_text": "请解释React中的虚拟DOM是什么？有什么优势？",
            "reference_answer": "虚拟DOM是用JavaScript对象模拟真实DOM结构。优势：1) 减少DOM操作次数，提高性能；2) 跨平台能力；3) 声明式编程。Diff算法比较新旧虚拟DOM差异，只更新变化的部分到真实DOM。",
            "difficulty": "medium",
            "tags": ["React", "虚拟DOM", "前端"],
            "category": "technical"
        },
        {
            "question_text": "请解释前端性能优化的方法有哪些？",
            "reference_answer": "性能优化方法：1) 资源压缩合并；2) 图片懒加载、CDN加速；3) 代码分割、按需加载；4) 浏览器缓存策略；5) 防抖节流；6) 虚拟列表；7) Web Worker处理复杂计算；8) 服务端渲染SSR。",
            "difficulty": "hard",
            "tags": ["前端", "性能优化", "工程化"],
            "category": "technical"
        }
    ],
    "product": [
        {
            "question_text": "请介绍一下产品经理的主要职责是什么？",
            "reference_answer": "产品经理的主要职责：1) 市场调研和需求分析；2) 产品规划和设计；3) 需求文档撰写；4) 项目跟进和协调；5) 产品上线和迭代；6) 数据分析和优化。核心是发现用户需求，设计解决方案，推动产品落地。",
            "difficulty": "easy",
            "tags": ["产品经理", "职责", "基础"],
            "category": "technical"
        },
        {
            "question_text": "请解释你如何进行需求分析？",
            "reference_answer": "需求分析步骤：1) 收集需求：用户访谈、问卷调查、数据分析；2) 需求分类：功能性需求、非功能性需求；3) 需求优先级排序：KANO模型、四象限法则；4) 需求验证：原型测试、A/B测试；5) 输出需求文档：PRD、用户故事。",
            "difficulty": "medium",
            "tags": ["产品经理", "需求分析", "方法论"],
            "category": "technical"
        },
        {
            "question_text": "请解释什么是MVP？如何设计MVP？",
            "reference_answer": "MVP（Minimum Viable Product）最小可行产品，是用最小成本验证产品假设的方法。设计步骤：1) 明确核心假设；2) 定义关键指标；3) 确定最小功能集；4) 快速开发上线；5) 收集反馈迭代。目的是快速验证想法，降低试错成本。",
            "difficulty": "medium",
            "tags": ["产品经理", "MVP", "产品思维"],
            "category": "technical"
        },
        {
            "question_text": "请解释如何进行竞品分析？",
            "reference_answer": "竞品分析步骤：1) 确定竞品：直接竞品、间接竞品、潜在竞品；2) 分析维度：产品功能、用户体验、商业模式、运营策略；3) 收集信息：官网、应用商店、用户评价；4) SWOT分析：优势、劣势、机会、威胁；5) 输出分析报告和改进建议。",
            "difficulty": "medium",
            "tags": ["产品经理", "竞品分析", "方法论"],
            "category": "technical"
        },
        {
            "question_text": "请解释如何用数据驱动产品决策？",
            "reference_answer": "数据驱动决策：1) 确定关键指标：DAU、留存率、转化率等；2) 建立数据埋点体系；3) 数据采集和分析；4) 发现问题和机会；5) 提出假设并验证；6) 持续迭代优化。常用工具：Google Analytics、神策数据、GrowingIO。",
            "difficulty": "hard",
            "tags": ["产品经理", "数据分析", "决策"],
            "category": "technical"
        }
    ],
    "data": [
        {
            "question_text": "请解释数据分析的基本流程是什么？",
            "reference_answer": "数据分析流程：1) 明确分析目标；2) 数据收集：数据库、API、爬虫等；3) 数据清洗：处理缺失值、异常值、重复值；4) 数据探索：描述性统计、可视化；5) 数据分析：统计分析、机器学习；6) 结果呈现：报告、仪表盘。",
            "difficulty": "easy",
            "tags": ["数据分析", "流程", "基础"],
            "category": "technical"
        },
        {
            "question_text": "请解释SQL中的JOIN有哪些类型？有什么区别？",
            "reference_answer": "SQL JOIN类型：1) INNER JOIN：返回两表匹配的记录；2) LEFT JOIN：返回左表所有记录，右表不匹配则为NULL；3) RIGHT JOIN：返回右表所有记录，左表不匹配则为NULL；4) FULL JOIN：返回两表所有记录。根据业务需求选择合适的JOIN类型。",
            "difficulty": "medium",
            "tags": ["SQL", "数据库", "数据分析"],
            "category": "technical"
        },
        {
            "question_text": "请解释常用的统计分析方法有哪些？",
            "reference_answer": "常用统计分析方法：1) 描述性统计：均值、中位数、标准差；2) 假设检验：t检验、卡方检验；3) 相关分析：皮尔逊相关系数；4) 回归分析：线性回归、逻辑回归；5) 聚类分析：K-means；6) 时间序列分析：ARIMA。",
            "difficulty": "medium",
            "tags": ["统计学", "分析方法", "数据分析"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中Pandas库的主要功能和数据结构？",
            "reference_answer": "Pandas主要数据结构：Series（一维）、DataFrame（二维）。主要功能：1) 数据读取：read_csv、read_excel等；2) 数据清洗：处理缺失值、重复值；3) 数据筛选：条件过滤、索引操作；4) 数据聚合：groupby、pivot_table；5) 数据可视化：plot方法。",
            "difficulty": "medium",
            "tags": ["Python", "Pandas", "数据分析"],
            "category": "technical"
        },
        {
            "question_text": "请解释如何设计一个数据指标体系？",
            "reference_answer": "数据指标体系设计：1) 明确业务目标；2) 拆解关键指标：北极星指标、过程指标、结果指标；3) 指标分层：一级指标、二级指标、三级指标；4) 定义指标口径：计算公式、数据来源；5) 建立监控体系：看板、预警机制。如OSM模型：目标-策略-度量。",
            "difficulty": "hard",
            "tags": ["数据分析", "指标体系", "方法论"],
            "category": "technical"
        }
    ],
    "python": [
        {
            "question_text": "请解释Python中的装饰器是什么？有什么应用场景？",
            "reference_answer": "装饰器是一个函数，用于修改其他函数的行为，在不改变原函数代码的情况下增加功能。应用场景：1) 日志记录；2) 性能测试；3) 权限验证；4) 缓存；5) 重试机制。本质是高阶函数，接收函数作为参数，返回新函数。",
            "difficulty": "medium",
            "tags": ["Python", "装饰器", "高级特性"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的生成器是什么？和列表有什么区别？",
            "reference_answer": "生成器是一种迭代器，使用yield关键字返回值，惰性计算。区别：1) 内存占用：生成器更小，按需生成；2) 计算方式：生成器惰性计算，列表立即计算；3) 可重复性：列表可重复遍历，生成器只能遍历一次。适合处理大数据集。",
            "difficulty": "medium",
            "tags": ["Python", "生成器", "迭代器"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的GIL是什么？对多线程有什么影响？",
            "reference_answer": "GIL（全局解释器锁）是CPython中的互斥锁，确保同一时刻只有一个线程执行Python字节码。影响：1) 多线程无法利用多核CPU；2) IO密集型任务影响不大；3) CPU密集型任务建议使用多进程。解决方案：multiprocessing、协程asyncio。",
            "difficulty": "hard",
            "tags": ["Python", "GIL", "多线程"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的面向对象编程，类和对象的区别？",
            "reference_answer": "类是对象的模板，定义了属性和方法；对象是类的实例。面向对象三大特性：1) 封装：隐藏内部实现；2) 继承：代码复用，子类继承父类；3) 多态：同一方法不同实现。Python支持多继承，使用MRO（方法解析顺序）处理冲突。",
            "difficulty": "medium",
            "tags": ["Python", "面向对象", "OOP"],
            "category": "technical"
        },
        {
            "question_text": "请解释Django和Flask框架的区别？",
            "reference_answer": "Django是全功能框架，内置ORM、Admin、认证系统等，适合快速开发大型项目。Flask是微框架，核心简单，扩展灵活，适合小型项目和API开发。选择依据：项目规模、开发速度、定制需求。Django开箱即用，Flask需要自己组装。",
            "difficulty": "medium",
            "tags": ["Python", "Web框架", "Django", "Flask"],
            "category": "technical"
        }
    ],
    "ui": [
        {
            "question_text": "请解释UI设计的基本原则有哪些？",
            "reference_answer": "UI设计基本原则：1) 一致性：风格、颜色、字体统一；2) 简洁性：去除冗余元素；3) 可用性：操作简单直观；4) 反馈性：及时响应用户操作；5) 容错性：防止用户犯错；6) 层次性：信息分级展示。遵循用户认知习惯，降低学习成本。",
            "difficulty": "easy",
            "tags": ["UI设计", "设计原则", "基础"],
            "category": "technical"
        },
        {
            "question_text": "请解释色彩搭配的基本原则？",
            "reference_answer": "色彩搭配原则：1) 60-30-10法则：主色60%、辅色30%、强调色10%；2) 色彩对比：冷暖对比、明暗对比；3) 色彩和谐：同类色、邻近色、互补色；4) 品牌一致性：符合品牌调性；5) 可访问性：考虑色盲用户。工具：Adobe Color、Coolors。",
            "difficulty": "medium",
            "tags": ["UI设计", "色彩", "视觉设计"],
            "category": "technical"
        },
        {
            "question_text": "请解释移动端和PC端设计的区别？",
            "reference_answer": "移动端vs PC端：1) 屏幕尺寸：移动端小，信息精简；PC端大，信息丰富；2) 交互方式：移动端触控，PC端鼠标键盘；3) 使用场景：移动端碎片化，PC端专注；4) 导航设计：移动端底部导航，PC端顶部导航；5) 响应式设计适配多端。",
            "difficulty": "medium",
            "tags": ["UI设计", "移动端", "PC端"],
            "category": "technical"
        },
        {
            "question_text": "请解释设计系统的概念和作用？",
            "reference_answer": "设计系统是一套完整的设计规范，包含设计原则、组件库、样式指南、交互规范等。作用：1) 保证设计一致性；2) 提高设计效率；3) 便于团队协作；4) 降低沟通成本。知名案例：Material Design、Ant Design、Apple HIG。",
            "difficulty": "hard",
            "tags": ["UI设计", "设计系统", "组件库"],
            "category": "technical"
        },
        {
            "question_text": "请解释用户体验(UX)和用户界面(UI)的区别？",
            "reference_answer": "UX关注用户使用产品的整体体验，包括需求分析、用户研究、信息架构、交互设计等。UI关注产品的视觉表现，包括界面设计、视觉元素、动效设计等。UX是骨架，UI是皮肤。两者相辅相成，共同打造优秀产品。",
            "difficulty": "medium",
            "tags": ["UI设计", "UX设计", "用户体验"],
            "category": "technical"
        }
    ],
    "operation": [
        {
            "question_text": "请解释运营的主要工作内容是什么？",
            "reference_answer": "运营主要工作：1) 用户运营：拉新、促活、留存、转化；2) 内容运营：内容策划、生产、分发；3) 活动运营：活动策划、执行、复盘；4) 产品运营：数据分析、用户反馈、产品优化；5) 渠道运营：渠道拓展、合作推广。核心目标是增长。",
            "difficulty": "easy",
            "tags": ["运营", "工作内容", "基础"],
            "category": "technical"
        },
        {
            "question_text": "请解释用户运营的核心指标有哪些？",
            "reference_answer": "用户运营核心指标：1) 获客指标：新增用户数、获客成本(CAC)；2) 活跃指标：DAU、MAU、用户活跃度；3) 留存指标：次日留存、7日留存、30日留存；4) 转化指标：转化率、ARPU、LTV；5) 传播指标：K因子、分享率。关注用户全生命周期。",
            "difficulty": "medium",
            "tags": ["运营", "用户运营", "数据分析"],
            "category": "technical"
        },
        {
            "question_text": "请解释如何策划一场运营活动？",
            "reference_answer": "活动策划步骤：1) 明确目标：拉新、促活、转化；2) 确定主题和玩法；3) 设计活动流程和规则；4) 制定推广方案；5) 准备物料和技术支持；6) 执行和监控；7) 数据复盘：ROI、参与率、转化率。关注用户体验和风险控制。",
            "difficulty": "medium",
            "tags": ["运营", "活动运营", "策划"],
            "category": "technical"
        },
        {
            "question_text": "请解释内容运营的策略有哪些？",
            "reference_answer": "内容运营策略：1) 内容定位：目标用户、内容调性；2) 内容生产：PGC、UGC、PUGC；3) 内容分发：多渠道布局、算法推荐；4) 内容运营：热点追踪、专题策划；5) 数据分析：阅读量、互动率、转化率。打造内容矩阵，形成传播闭环。",
            "difficulty": "medium",
            "tags": ["运营", "内容运营", "策略"],
            "category": "technical"
        },
        {
            "question_text": "请解释私域运营的概念和方法？",
            "reference_answer": "私域运营是在自有渠道（微信、APP、社群）进行用户运营，可反复触达。方法：1) 引流：公域转私域；2) 用户分层：标签化管理；3) 内容运营：持续输出价值；4) 活动运营：促销、互动；5) 社群运营：建立用户粘性。优势：成本低、可控性强。",
            "difficulty": "hard",
            "tags": ["运营", "私域运营", "用户增长"],
            "category": "technical"
        }
    ],
    "qa": [
        {
            "question_text": "请解释软件测试的主要类型有哪些？",
            "reference_answer": "软件测试类型：1) 按阶段分：单元测试、集成测试、系统测试、验收测试；2) 按方法分：黑盒测试、白盒测试、灰盒测试；3) 按目的分：功能测试、性能测试、安全测试、兼容性测试；4) 按方式分：手动测试、自动化测试。根据项目需求选择合适的测试策略。",
            "difficulty": "easy",
            "tags": ["测试", "测试类型", "基础"],
            "category": "technical"
        },
        {
            "question_text": "请解释测试用例设计的方法有哪些？",
            "reference_answer": "测试用例设计方法：1) 等价类划分：有效等价类、无效等价类；2) 边界值分析：边界上、边界附近；3) 错误推测法：经验判断可能的问题；4) 因果图法：输入条件组合；5) 正交实验法：多因素组合优化；6) 场景法：业务流程测试。",
            "difficulty": "medium",
            "tags": ["测试", "测试用例", "测试设计"],
            "category": "technical"
        },
        {
            "question_text": "请解释Bug的生命周期是什么？",
            "reference_answer": "Bug生命周期：新建 -> 打开 -> 修复 -> 验证 -> 关闭。状态流转：1) 新建：发现Bug；2) 打开：确认Bug；3) 修复：开发修复；4) 验证：测试验证；5) 关闭：验证通过。可能还有：重新打开、拒绝、延期等状态。使用Bug管理工具跟踪。",
            "difficulty": "medium",
            "tags": ["测试", "Bug管理", "流程"],
            "category": "technical"
        },
        {
            "question_text": "请解释自动化测试框架有哪些？如何选择？",
            "reference_answer": "常用自动化测试框架：Web端：Selenium、Playwright、Cypress；API端：Postman、JMeter、RestAssured；移动端：Appium、Espresso。选择依据：1) 项目类型和技术栈；2) 团队技能；3) 维护成本；4) 社区支持。建议从核心功能开始，逐步扩大覆盖。",
            "difficulty": "medium",
            "tags": ["测试", "自动化测试", "框架"],
            "category": "technical"
        },
        {
            "question_text": "请解释性能测试的类型和指标？",
            "reference_answer": "性能测试类型：1) 负载测试：正常负载下的性能；2) 压力测试：极限负载下的表现；3) 并发测试：多用户同时访问；4) 容量测试：系统最大承载能力。关键指标：响应时间、吞吐量(TPS)、并发用户数、错误率、资源利用率(CPU、内存)。",
            "difficulty": "hard",
            "tags": ["测试", "性能测试", "指标"],
            "category": "technical"
        }
    ]
}

# 通用行为面试题
BEHAVIORAL_QUESTIONS = [
    {
        "question_text": "请介绍一下你自己，包括你的教育背景和工作经历。",
        "reference_answer": "应该简洁明了地介绍个人背景，突出与应聘岗位相关的经历，展示自己的优势和特点。控制在2-3分钟内。",
        "difficulty": "easy",
        "tags": ["自我介绍", "沟通能力"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "描述一次团队合作的经历，你在其中扮演了什么角色？",
        "reference_answer": "应该具体描述团队目标、个人职责、协作过程和最终成果。体现沟通协调能力和团队精神。",
        "difficulty": "medium",
        "tags": ["团队合作", "沟通能力"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "你遇到过与同事意见不合的情况吗？你是如何处理的？",
        "reference_answer": "应该体现沟通协调能力，说明如何理性分析问题、尊重他人意见、寻求共识。展示成熟的工作态度。",
        "difficulty": "medium",
        "tags": ["沟通协调", "冲突处理"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "你认为自己最大的优点和缺点是什么？",
        "reference_answer": "优点应该与岗位相关，举例说明；缺点应该诚实但可控，并说明改进措施。避免说'没有缺点'或致命缺点。",
        "difficulty": "easy",
        "tags": ["自我认知", "诚实"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "你对未来3-5年的职业规划是什么？",
        "reference_answer": "应该有清晰的职业目标，与应聘岗位和公司发展相结合。展示上进心和学习意愿。",
        "difficulty": "medium",
        "tags": ["职业规划", "目标感"],
        "category": "behavioral",
        "job_type": None
    }
]


async def init_interview_questions():
    """初始化面试题目"""
    async with AsyncSessionLocal() as db:
        print("开始初始化面试题目...")

        total_questions = 0

        # 1. 添加各岗位的技术面试题
        for job_code, questions in JOB_QUESTIONS.items():
            # 获取岗位
            result = await db.execute(
                select(JobPosition).where(JobPosition.code == job_code)
            )
            job = result.scalar_one_or_none()

            if not job:
                print(f"  岗位 {job_code} 不存在，跳过")
                continue

            # 检查是否已有该岗位的题目
            existing_result = await db.execute(
                select(func.count(InterviewQuestion.id)).where(
                    InterviewQuestion.job_type == job_code
                )
            )
            existing_count = existing_result.scalar() or 0

            if existing_count > 0:
                print(f"  岗位 {job.name} 已有 {existing_count} 道题目，跳过")
                continue

            # 添加题目
            for i, q in enumerate(questions):
                question = InterviewQuestion(
                    category=q["category"],
                    job_type=job_code,
                    question_text=q["question_text"],
                    reference_answer=q["reference_answer"],
                    difficulty=q["difficulty"],
                    tags=q["tags"],
                    question_order=i,
                    is_active=True
                )
                db.add(question)
                total_questions += 1

            # 更新岗位的题目数量
            job.question_count = len(questions)
            print(f"  为岗位 {job.name} 添加了 {len(questions)} 道题目")

        # 2. 添加通用行为面试题
        for i, q in enumerate(BEHAVIORAL_QUESTIONS):
            # 检查是否已存在
            existing_result = await db.execute(
                select(InterviewQuestion).where(
                    InterviewQuestion.question_text == q["question_text"]
                )
            )
            if existing_result.scalar_one_or_none():
                continue

            question = InterviewQuestion(
                category=q["category"],
                job_type=q["job_type"],
                question_text=q["question_text"],
                reference_answer=q["reference_answer"],
                difficulty=q["difficulty"],
                tags=q["tags"],
                question_order=i,
                is_active=True
            )
            db.add(question)
            total_questions += 1

        print(f"  添加了 {len(BEHAVIORAL_QUESTIONS)} 道通用行为面试题")

        await db.commit()
        print(f"\n面试题目初始化完成！共添加 {total_questions} 道题目")


if __name__ == "__main__":
    from sqlalchemy import func
    asyncio.run(init_interview_questions())
