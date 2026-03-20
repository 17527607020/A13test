"""
扩展面试题目数据
为每个岗位添加更多题目
"""
import asyncio
from sqlalchemy import select, func
from app.core.config import AsyncSessionLocal
from app.models.interview import InterviewQuestion, JobPosition


# 扩展的各岗位面试题目
EXTENDED_QUESTIONS = {
    "java": [
        {
            "question_text": "请解释Java中的HashMap底层实现原理？",
            "reference_answer": "HashMap底层是数组+链表+红黑树（JDK8）。当链表长度超过8且数组长度超过64时，链表会转换为红黑树。put流程：1) 计算key的hash值；2) 定位数组位置；3) 处理冲突（链表/红黑树）；4) 插入或更新节点。扩容因子0.75，扩容为原来的2倍。",
            "difficulty": "hard",
            "tags": ["Java", "HashMap", "数据结构"],
            "category": "technical"
        },
        {
            "question_text": "请解释Java中的异常处理机制？",
            "reference_answer": "Java异常分为Error和Exception。Error是程序无法处理的错误，如OutOfMemoryError。Exception分为受检异常（必须处理）和非受检异常（RuntimeException）。处理方式：try-catch-finally、throws声明、throw抛出。最佳实践：不要用异常控制流程，及时关闭资源。",
            "difficulty": "medium",
            "tags": ["Java", "异常处理", "基础"],
            "category": "technical"
        },
        {
            "question_text": "请解释Java中的反射机制？有什么应用场景？",
            "reference_answer": "反射是在运行时获取类的信息并操作类的属性和方法。核心类：Class、Field、Method、Constructor。应用场景：1) 框架设计（Spring IOC）；2) 动态代理；3) 注解处理；4) 序列化/反序列化。缺点：性能较低，破坏封装性。",
            "difficulty": "medium",
            "tags": ["Java", "反射", "高级特性"],
            "category": "technical"
        },
        {
            "question_text": "请解释Java内存模型(JMM)和volatile关键字？",
            "reference_answer": "JMM定义了线程和主内存之间的抽象关系。volatile保证可见性和禁止指令重排序，但不保证原子性。适用场景：状态标志位、双重检查锁定单例。与synchronized区别：volatile轻量级，只保证可见性；synchronized保证原子性和可见性。",
            "difficulty": "hard",
            "tags": ["Java", "JMM", "多线程"],
            "category": "technical"
        },
        {
            "question_text": "请解释Spring Boot的自动配置原理？",
            "reference_answer": "Spring Boot自动配置基于条件注解实现。核心：@EnableAutoConfiguration导入META-INF/spring.factories中的配置类，通过@Conditional系列注解判断是否生效。常用条件：@ConditionalOnClass、@ConditionalOnMissingBean、@ConditionalOnProperty。可通过exclude排除特定配置。",
            "difficulty": "hard",
            "tags": ["Spring Boot", "自动配置", "原理"],
            "category": "technical"
        },
        {
            "question_text": "请解释MyBatis的一级缓存和二级缓存？",
            "reference_answer": "一级缓存是SqlSession级别，默认开启，同一SqlSession中相同查询返回缓存数据。二级缓存是Mapper级别，需要配置开启，跨SqlSession共享。缓存失效场景：执行insert/update/delete、手动clearCache、事务提交/回滚。生产环境建议使用Redis等分布式缓存。",
            "difficulty": "medium",
            "tags": ["MyBatis", "缓存", "数据库"],
            "category": "technical"
        },
        {
            "question_text": "请解释Java中的设计模式，举例说明？",
            "reference_answer": "常用设计模式：1) 单例模式：确保类只有一个实例；2) 工厂模式：创建对象不暴露创建逻辑；3) 策略模式：定义算法族，使它们可以相互替换；4) 观察者模式：对象间一对多依赖；5) 代理模式：控制对象访问。Spring中大量使用代理模式实现AOP。",
            "difficulty": "medium",
            "tags": ["Java", "设计模式", "架构"],
            "category": "technical"
        },
        {
            "question_text": "请解释JVM的垃圾回收算法和垃圾收集器？",
            "reference_answer": "垃圾回收算法：1) 标记-清除：效率低，有碎片；2) 复制算法：适合新生代，无碎片但浪费空间；3) 标记-整理：适合老年代。常用收集器：Serial（单线程）、Parallel Scavenge（吞吐量优先）、CMS（低延迟）、G1（分区收集，JDK9默认）、ZGC（超低延迟）。",
            "difficulty": "hard",
            "tags": ["JVM", "GC", "性能优化"],
            "category": "technical"
        },
        {
            "question_text": "请解释MySQL索引的数据结构？为什么使用B+树？",
            "reference_answer": "MySQL InnoDB使用B+树作为索引结构。选择B+树原因：1) 层级少，查询效率稳定；2) 叶子节点形成链表，范围查询高效；3) 单节点存储更多key，减少磁盘IO。聚簇索引叶子节点存储完整行数据，非聚簇索引存储主键值，需要回表查询。",
            "difficulty": "hard",
            "tags": ["MySQL", "索引", "数据库"],
            "category": "technical"
        },
        {
            "question_text": "请解释Redis的数据类型和应用场景？",
            "reference_answer": "Redis数据类型：1) String：缓存、计数器；2) Hash：对象存储；3) List：消息队列、时间线；4) Set：标签、社交关系；5) ZSet：排行榜、延时队列。高级：Bitmap、HyperLogLog、Geo。持久化：RDB快照、AOF日志。集群：主从复制、哨兵、Cluster。",
            "difficulty": "medium",
            "tags": ["Redis", "缓存", "数据库"],
            "category": "technical"
        }
    ],
    "frontend": [
        {
            "question_text": "请解释浏览器渲染原理？从输入URL到页面展示的过程？",
            "reference_answer": "过程：1) DNS解析；2) TCP连接；3) 发送HTTP请求；4) 接收响应；5) 解析HTML构建DOM树；6) 解析CSS构建CSSOM树；7) 合并生成渲染树；8) 布局计算；9) 绘制。优化点：减少HTTP请求、压缩资源、使用CDN、开启浏览器缓存、避免阻塞渲染。",
            "difficulty": "hard",
            "tags": ["前端", "浏览器", "性能"],
            "category": "technical"
        },
        {
            "question_text": "请解释HTTP和HTTPS的区别？HTTPS如何保证安全？",
            "reference_answer": "HTTP是明文传输，HTTPS是加密传输。HTTPS通过SSL/TLS协议保证安全：1) 对称加密传输数据；2) 非对称加密交换密钥；3) 数字证书验证服务器身份。HTTPS默认端口443，HTTP端口80。HTTPS需要CA证书，有一定性能开销。",
            "difficulty": "medium",
            "tags": ["前端", "HTTP", "网络安全"],
            "category": "technical"
        },
        {
            "question_text": "请解释前端跨域问题及解决方案？",
            "reference_answer": "跨域是浏览器同源策略限制。解决方案：1) CORS：服务端设置Access-Control-Allow-Origin；2) JSONP：利用script标签，只支持GET；3) 代理服务器：Nginx反向代理；4) postMessage：跨窗口通信；5) WebSocket：不受同源策略限制。推荐使用CORS。",
            "difficulty": "medium",
            "tags": ["前端", "跨域", "网络"],
            "category": "technical"
        },
        {
            "question_text": "请解释TypeScript中interface和type的区别？",
            "reference_answer": "interface：1) 可以声明合并；2) 可以extends继承；3) 适合定义对象形状。type：1) 可以定义联合类型、交叉类型；2) 可以使用typeof获取类型；3) 更灵活。选择：对象形状用interface，复杂类型用type。实际开发中两者可以互换使用。",
            "difficulty": "medium",
            "tags": ["TypeScript", "类型系统", "前端"],
            "category": "technical"
        },
        {
            "question_text": "请解释Webpack的构建流程？",
            "reference_answer": "Webpack构建流程：1) 初始化参数，合并配置；2) 创建Compiler对象；3) 加载所有插件；4) 执行run方法；5) 编译模块：从入口开始，递归解析依赖；6) 完成编译，生成chunk；7) 输出资源到dist目录。优化：tree-shaking、code-splitting、缓存、多线程构建。",
            "difficulty": "hard",
            "tags": ["Webpack", "工程化", "前端"],
            "category": "technical"
        },
        {
            "question_text": "请解释前端状态管理（Vuex/Redux）的核心概念？",
            "reference_answer": "核心概念：1) State：单一状态树，存储应用数据；2) Getters/Selectors：派生状态；3) Mutations/Reducers：同步修改状态；4) Actions：异步操作，提交mutation；5) Modules：模块化拆分。原则：单向数据流，状态不可直接修改，通过mutation修改。",
            "difficulty": "medium",
            "tags": ["前端", "状态管理", "架构"],
            "category": "technical"
        },
        {
            "question_text": "请解释前端路由的实现原理？",
            "reference_answer": "前端路由两种模式：1) Hash模式：URL中#后面的部分变化触发hashchange事件，不需要服务器支持；2) History模式：使用pushState和replaceState API，URL更美观，需要服务器配置支持。Vue Router和React Router都支持这两种模式。",
            "difficulty": "medium",
            "tags": ["前端", "路由", "SPA"],
            "category": "technical"
        },
        {
            "question_text": "请解释Promise的原理和常用方法？",
            "reference_answer": "Promise是异步编程解决方案，有pending、fulfilled、rejected三种状态。常用方法：then()、catch()、finally()、Promise.all()、Promise.race()、Promise.allSettled()。特点：状态一旦改变就不可逆，支持链式调用。async/await是Promise的语法糖。",
            "difficulty": "medium",
            "tags": ["JavaScript", "Promise", "异步"],
            "category": "technical"
        },
        {
            "question_text": "请解释WebSocket的使用场景和实现方式？",
            "reference_answer": "WebSocket是全双工通信协议，适合实时场景：聊天应用、在线协作、实时数据推送、游戏。实现：new WebSocket(url)，监听onopen、onmessage、onclose、onerror事件。与HTTP区别：WebSocket持久连接，服务器可主动推送，开销小。",
            "difficulty": "medium",
            "tags": ["前端", "WebSocket", "实时通信"],
            "category": "technical"
        },
        {
            "question_text": "请解释前端安全问题和防范措施？",
            "reference_answer": "常见安全问题：1) XSS：跨站脚本攻击，防范：转义HTML、CSP策略；2) CSRF：跨站请求伪造，防范：Token验证、SameSite Cookie；3) SQL注入：防范：参数化查询；4) 点击劫持：防范：X-Frame-Options头。开发中要注意输入验证和输出编码。",
            "difficulty": "hard",
            "tags": ["前端", "安全", "防护"],
            "category": "technical"
        }
    ],
    "product": [
        {
            "question_text": "请解释产品路线图如何制定？",
            "reference_answer": "产品路线图制定：1) 明确产品愿景和战略目标；2) 收集需求：用户反馈、市场分析、竞品研究；3) 需求优先级排序：KANO模型、RICE评分；4) 规划版本：MVP、迭代计划；5) 资源评估：技术可行性、人力投入；6) 时间规划：里程碑节点。定期复盘调整。",
            "difficulty": "medium",
            "tags": ["产品经理", "产品规划", "路线图"],
            "category": "technical"
        },
        {
            "question_text": "请解释用户画像的概念和构建方法？",
            "reference_answer": "用户画像是目标用户的虚拟代表，包含人口属性、行为特征、心理特征等。构建方法：1) 数据收集：用户调研、行为数据；2) 标签提取：基础标签、行为标签、偏好标签；3) 聚类分析：相似用户分组；4) 画像可视化：标签云、雷达图。用于精准营销和产品优化。",
            "difficulty": "medium",
            "tags": ["产品经理", "用户研究", "用户画像"],
            "category": "technical"
        },
        {
            "question_text": "请解释A/B测试的原理和实施步骤？",
            "reference_answer": "A/B测试是对比两个版本效果的方法。实施步骤：1) 确定测试目标和假设；2) 设计实验方案；3) 确定样本量和测试周期；4) 分流实现：随机分配用户；5) 数据收集和分析；6) 得出结论并决策。注意事项：确保样本代表性、避免辛普森悖论、一次只测一个变量。",
            "difficulty": "medium",
            "tags": ["产品经理", "A/B测试", "数据分析"],
            "category": "technical"
        },
        {
            "question_text": "请解释PRD文档应该包含哪些内容？",
            "reference_answer": "PRD文档内容：1) 文档信息：版本、修改记录；2) 项目背景和目标；3) 用户范围和场景；4) 功能需求：功能列表、流程图、原型图；5) 非功能需求：性能、安全、兼容性；6) 数据埋点需求；7) 验收标准；8) 风险评估。好的PRD要清晰、完整、可执行。",
            "difficulty": "easy",
            "tags": ["产品经理", "PRD", "文档"],
            "category": "technical"
        },
        {
            "question_text": "请解释如何进行用户调研？",
            "reference_answer": "用户调研方法：1) 定性调研：用户访谈、焦点小组、可用性测试；2) 定量调研：问卷调查、数据分析、A/B测试。调研流程：明确目标 -> 选择方法 -> 设计方案 -> 执行调研 -> 分析结果 -> 输出洞察。注意样本代表性和调研者偏见。",
            "difficulty": "medium",
            "tags": ["产品经理", "用户调研", "方法论"],
            "category": "technical"
        },
        {
            "question_text": "请解释B端产品和C端产品的区别？",
            "reference_answer": "B端vs C端：1) 用户：B端是企业用户，C端是个人用户；2) 决策：B端理性决策，C端感性决策；3) 目标：B端提效降本，C端满足需求；4) 付费：B端企业付费，C端用户付费或广告；5) 迭代：B端稳定优先，C端快速迭代。产品设计思路不同。",
            "difficulty": "medium",
            "tags": ["产品经理", "B端", "C端"],
            "category": "technical"
        },
        {
            "question_text": "请解释如何评估产品功能的价值？",
            "reference_answer": "功能价值评估方法：1) RICE模型：Reach（覆盖面）、Impact（影响）、Confidence（信心）、Effort（投入）；2) KANO模型：基本型、期望型、兴奋型；3) ROI分析：投入产出比；4) 用户价值：解决用户痛点程度。综合考虑业务价值和开发成本。",
            "difficulty": "hard",
            "tags": ["产品经理", "需求评估", "方法论"],
            "category": "technical"
        },
        {
            "question_text": "请解释产品经理如何与技术团队协作？",
            "reference_answer": "协作要点：1) 需求评审：提前沟通，确保理解一致；2) 文档质量：PRD清晰完整，减少反复确认；3) 优先级沟通：说明业务价值，帮助技术做决策；4) 验收把关：对照需求验收，及时反馈；5) 进度跟进：每日站会、周报。建立信任，尊重技术专业性。",
            "difficulty": "medium",
            "tags": ["产品经理", "团队协作", "沟通"],
            "category": "technical"
        },
        {
            "question_text": "请解释产品迭代的原则和方法？",
            "reference_answer": "迭代原则：1) 小步快跑，快速验证；2) 数据驱动决策；3) 用户反馈闭环；4) 持续优化。迭代方法：敏捷开发、看板管理、持续集成。每次迭代包含：需求评审、开发测试、上线发布、数据复盘。保持节奏，避免过度迭代。",
            "difficulty": "medium",
            "tags": ["产品经理", "迭代", "敏捷"],
            "category": "technical"
        },
        {
            "question_text": "请解释如何做竞品分析报告？",
            "reference_answer": "竞品分析报告结构：1) 背景和目的；2) 竞品选择：直接竞品、间接竞品；3) 分析维度：产品定位、功能对比、用户体验、商业模式、运营策略；4) SWOT分析；5) 总结和启示。工具：体验产品、用户评价、数据平台。输出可执行的产品建议。",
            "difficulty": "medium",
            "tags": ["产品经理", "竞品分析", "报告"],
            "category": "technical"
        }
    ],
    "data": [
        {
            "question_text": "请解释数据仓库和数据湖的区别？",
            "reference_answer": "数据仓库：结构化数据，预定义schema，适合BI分析，查询性能高。数据湖：原始数据存储，支持结构化/半结构化/非结构化，schema-on-read，适合机器学习和探索性分析。现代架构：湖仓一体（Lakehouse），结合两者优势。",
            "difficulty": "hard",
            "tags": ["数据分析", "数据仓库", "架构"],
            "category": "technical"
        },
        {
            "question_text": "请解释ETL的概念和流程？",
            "reference_answer": "ETL是数据抽取、转换、加载的过程。流程：1) Extract：从源系统抽取数据；2) Transform：清洗、转换、聚合、计算；3) Load：加载到目标系统。工具：Informatica、Talend、DataX、Airflow。现代趋势：ELT，先加载后转换，利用目标系统算力。",
            "difficulty": "medium",
            "tags": ["数据分析", "ETL", "数据处理"],
            "category": "technical"
        },
        {
            "question_text": "请解释数据可视化的重要性和常用工具？",
            "reference_answer": "数据可视化将数据转化为图形，帮助发现规律、传递信息。常用工具：1) Excel：基础图表；2) Tableau：商业智能，交互式仪表盘；3) Power BI：微软生态，集成度高；4) Python：Matplotlib、Seaborn、Plotly；5) ECharts：Web可视化。选择依据：数据量、交互需求、团队技能。",
            "difficulty": "easy",
            "tags": ["数据分析", "可视化", "工具"],
            "category": "technical"
        },
        {
            "question_text": "请解释机器学习在数据分析中的应用？",
            "reference_answer": "应用场景：1) 预测分析：销售预测、需求预测；2) 分类：用户分层、风险评估；3) 聚类：客户分群、异常检测；4) 推荐系统：个性化推荐；5) 自然语言处理：文本分析、情感分析。常用算法：线性回归、决策树、随机森林、K-means、神经网络。",
            "difficulty": "hard",
            "tags": ["数据分析", "机器学习", "AI"],
            "category": "technical"
        },
        {
            "question_text": "请解释A/B测试的统计学原理？",
            "reference_answer": "A/B测试基于假设检验：1) 建立原假设和备择假设；2) 选择显著性水平α（通常0.05）；3) 计算检验统计量；4) 计算p值；5) 做出结论。关键概念：样本量计算、统计功效、置信区间、第一类错误、第二类错误。确保结果统计显著且业务显著。",
            "difficulty": "hard",
            "tags": ["数据分析", "统计学", "A/B测试"],
            "category": "technical"
        },
        {
            "question_text": "请解释数据清洗的常见方法和步骤？",
            "reference_answer": "数据清洗步骤：1) 缺失值处理：删除、填充（均值/中位数/众数/插值）；2) 异常值处理：删除、替换、分箱；3) 重复值处理：去重；4) 数据类型转换；5) 格式统一：日期、字符串；6) 逻辑校验：业务规则验证。Python工具：Pandas的dropna、fillna、duplicated等方法。",
            "difficulty": "medium",
            "tags": ["数据分析", "数据清洗", "Python"],
            "category": "technical"
        },
        {
            "question_text": "请解释用户行为分析的方法和指标？",
            "reference_answer": "分析方法：1) 漏斗分析：转化路径分析；2) 留存分析：用户粘性；3) 路径分析：用户行为路径；4) 分群分析：用户分层。关键指标：PV/UV、访问时长、跳出率、转化率、留存率、活跃度。工具：Google Analytics、神策数据、Mixpanel。",
            "difficulty": "medium",
            "tags": ["数据分析", "用户行为", "指标"],
            "category": "technical"
        },
        {
            "question_text": "请解释SQL窗口函数的使用场景？",
            "reference_answer": "窗口函数对一组行进行计算，不减少行数。常用函数：ROW_NUMBER、RANK、DENSE_RANK、SUM、AVG、LEAD、LAG。使用场景：1) 排名问题；2) 累计计算；3) 同比环比；4) 移动平均；5) 分组取Top N。语法：函数名() OVER(PARTITION BY ... ORDER BY ...)。",
            "difficulty": "medium",
            "tags": ["SQL", "窗口函数", "数据库"],
            "category": "technical"
        },
        {
            "question_text": "请解释数据质量管理的维度？",
            "reference_answer": "数据质量维度：1) 完整性：数据是否完整；2) 准确性：数据是否正确；3) 一致性：数据是否一致；4) 及时性：数据是否及时更新；5) 唯一性：数据是否重复；6) 有效性：数据是否符合规则。管理方法：数据质量监控、异常告警、数据治理流程。",
            "difficulty": "medium",
            "tags": ["数据分析", "数据质量", "治理"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中NumPy和Pandas的区别？",
            "reference_answer": "NumPy：多维数组ndarray，数值计算，底层C实现，性能高。Pandas：基于NumPy，提供Series和DataFrame，适合表格数据处理。NumPy适合矩阵运算、科学计算；Pandas适合数据清洗、分析、处理。实际使用中经常配合使用，Pandas底层依赖NumPy。",
            "difficulty": "medium",
            "tags": ["Python", "NumPy", "Pandas"],
            "category": "technical"
        }
    ],
    "python": [
        {
            "question_text": "请解释Python中的深拷贝和浅拷贝？",
            "reference_answer": "浅拷贝：创建新对象，但内部引用仍指向原对象。方法：copy()、切片、list()。深拷贝：递归复制所有对象。方法：copy.deepcopy()。区别在于嵌套对象的处理。浅拷贝修改嵌套对象会影响原对象，深拷贝完全独立。",
            "difficulty": "medium",
            "tags": ["Python", "拷贝", "基础"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的上下文管理器和with语句？",
            "reference_answer": "上下文管理器定义了__enter__和__exit__方法，用于资源管理。with语句自动调用这两个方法，确保资源正确释放。应用场景：文件操作、数据库连接、锁管理。也可以用contextlib.contextmanager装饰器简化实现。好处：代码简洁、异常安全。",
            "difficulty": "medium",
            "tags": ["Python", "上下文管理器", "高级特性"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的元类(metaclass)？",
            "reference_answer": "元类是创建类的类，类是元类的实例。默认元类是type。用途：1) 类创建时自动注册；2) 属性检查和修改；3) 单例模式实现；4) ORM框架实现。理解：类->实例对象，元类->类对象。实际开发中较少使用，主要用于框架开发。",
            "difficulty": "hard",
            "tags": ["Python", "元类", "高级特性"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的协程和asyncio？",
            "reference_answer": "协程是轻量级线程，用户态调度，单线程内实现并发。asyncio是Python异步编程框架。关键字：async定义协程，await等待协程执行。优势：IO密集型任务效率高，无线程切换开销。适用场景：网络请求、数据库操作、文件IO。注意：CPU密集型任务不适合。",
            "difficulty": "hard",
            "tags": ["Python", "协程", "异步"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的内存管理机制？",
            "reference_answer": "Python内存管理：1) 引用计数：主要方式，引用为0时回收；2) 垃圾回收：循环引用处理，分代回收策略；3) 内存池：小对象使用PyMalloc。手动干预：gc模块控制垃圾回收。优化：避免循环引用、使用生成器、及时释放大对象。",
            "difficulty": "hard",
            "tags": ["Python", "内存管理", "性能"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的描述符(descriptor)？",
            "reference_answer": "描述符是实现了__get__、__set__、__delete__方法的对象。用于控制属性访问。数据描述符：同时实现__get__和__set__。非数据描述符：只实现__get__。应用：property装饰器、类方法、静态方法、ORM字段定义。是Python实现属性绑定的核心机制。",
            "difficulty": "hard",
            "tags": ["Python", "描述符", "高级特性"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的多进程和多线程选择？",
            "reference_answer": "选择依据：CPU密集型用多进程，IO密集型用多线程或协程。原因：GIL限制多线程不能利用多核。多进程：multiprocessing模块，独立内存空间，开销大。多线程：threading模块，共享内存，开销小。协程：asyncio，单线程并发，适合IO密集型。",
            "difficulty": "medium",
            "tags": ["Python", "多进程", "多线程"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的类型注解？",
            "reference_answer": "类型注解是Python 3.5+引入的特性，用于标注变量和函数的类型。语法：name: type = value。工具：mypy进行静态类型检查。优点：代码更清晰、IDE支持更好、提前发现错误。typing模块提供List、Dict、Optional等复杂类型。运行时不强制检查。",
            "difficulty": "medium",
            "tags": ["Python", "类型注解", "typing"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的迭代器和可迭代对象？",
            "reference_answer": "可迭代对象：实现__iter__方法，返回迭代器。迭代器：实现__iter__和__next__方法。for循环原理：调用iter()获取迭代器，循环调用next()直到StopIteration。生成器是特殊的迭代器，使用yield实现。区别：可迭代对象可以重复迭代，迭代器只能迭代一次。",
            "difficulty": "medium",
            "tags": ["Python", "迭代器", "生成器"],
            "category": "technical"
        },
        {
            "question_text": "请解释Python中的魔法方法及常见用途？",
            "reference_answer": "魔法方法是以双下划线开头和结尾的方法。常见：__init__初始化、__str__字符串表示、__repr__调试表示、__len__长度、__getitem__索引访问、__call__可调用、__eq__相等比较、__hash__哈希值。用于自定义类的行为，实现运算符重载、上下文管理等。",
            "difficulty": "medium",
            "tags": ["Python", "魔法方法", "面向对象"],
            "category": "technical"
        }
    ],
    "ui": [
        {
            "question_text": "请解释响应式设计的原理和方法？",
            "reference_answer": "响应式设计使网页适应不同屏幕尺寸。方法：1) 媒体查询@media；2) 弹性布局flex/grid；3) 相对单位rem/em/vw；4) 图片自适应max-width:100%；5) 移动优先设计。断点设置：手机<768px，平板768-1024px，桌面>1024px。测试：Chrome DevTools设备模拟。",
            "difficulty": "medium",
            "tags": ["UI设计", "响应式", "前端"],
            "category": "technical"
        },
        {
            "question_text": "请解释设计规范文档应该包含哪些内容？",
            "reference_answer": "设计规范文档内容：1) 品牌规范：Logo使用、品牌色；2) 色彩系统：主色、辅色、功能色；3) 字体规范：字体族、字号、行高；4) 间距系统：栅格、边距、间距；5) 组件规范：按钮、表单、卡片等；6) 图标规范；7) 动效规范。确保设计一致性和团队协作效率。",
            "difficulty": "medium",
            "tags": ["UI设计", "设计规范", "文档"],
            "category": "technical"
        },
        {
            "question_text": "请解释交互设计的原则？",
            "reference_answer": "交互设计原则：1) 可视性：操作结果可见；2) 反馈：及时响应用户操作；3) 约束：限制用户输入；4) 映射：控件与结果对应；5) 一致性：交互方式统一；6) 可撤销：允许用户犯错；7) 减少记忆负担。尼尔森可用性原则是经典参考。",
            "difficulty": "medium",
            "tags": ["UI设计", "交互设计", "用户体验"],
            "category": "technical"
        },
        {
            "question_text": "请解释设计稿交付开发的标准流程？",
            "reference_answer": "交付流程：1) 设计稿完成并自检；2) 标注关键尺寸、颜色、字体；3) 切图导出：不同倍率、格式；4) 整理资源文件；5) 编写设计说明文档；6) 设计评审会议；7) 开发过程答疑；8) 验收检查。工具：Figma、蓝湖、Zeplin提高协作效率。",
            "difficulty": "easy",
            "tags": ["UI设计", "设计交付", "协作"],
            "category": "technical"
        },
        {
            "question_text": "请解释用户研究的方法有哪些？",
            "reference_answer": "用户研究方法：1) 定性研究：用户访谈、焦点小组、可用性测试、实地观察；2) 定量研究：问卷调查、A/B测试、数据分析、眼动追踪。研究流程：确定目标 -> 选择方法 -> 设计方案 -> 执行研究 -> 分析结果 -> 输出洞察。研究驱动设计决策。",
            "difficulty": "medium",
            "tags": ["UI设计", "用户研究", "方法论"],
            "category": "technical"
        },
        {
            "question_text": "请解释动效设计的作用和原则？",
            "reference_answer": "动效作用：1) 引导用户注意力；2) 提供操作反馈；3) 解释界面变化；4) 增强品牌感。原则：1) 有目的性，不为动效而动效；2) 自然流畅，符合物理规律；3) 时长适中，200-500ms；4) 不影响性能；5) 可关闭选项。工具：Lottie、After Effects、Principle。",
            "difficulty": "medium",
            "tags": ["UI设计", "动效设计", "交互"],
            "category": "technical"
        },
        {
            "question_text": "请解释信息架构(IA)的设计方法？",
            "reference_answer": "信息架构设计：1) 内容盘点：梳理所有内容；2) 用户研究：了解用户需求；3) 分类组织：逻辑分组；4) 导航设计：全局导航、局部导航；5) 标签系统：命名规范；6) 搜索系统：检索方式。方法：卡片分类法、用户路径分析。目标是让用户快速找到信息。",
            "difficulty": "hard",
            "tags": ["UI设计", "信息架构", "UX"],
            "category": "technical"
        },
        {
            "question_text": "请解释设计评审的流程和要点？",
            "reference_answer": "设计评审流程：1) 准备：整理设计稿、标注说明；2) 参与者：产品、开发、设计、测试；3) 演示：讲解设计思路；4) 讨论：收集反馈、解决问题；5) 确认：达成一致、记录修改点。要点：提前沟通、聚焦问题、控制时间、明确结论。避免设计反复修改。",
            "difficulty": "medium",
            "tags": ["UI设计", "设计评审", "协作"],
            "category": "technical"
        },
        {
            "question_text": "请解释可访问性设计的重要性？",
            "reference_answer": "可访问性设计让所有用户都能使用产品，包括残障人士。要点：1) 颜色对比度足够；2) 支持键盘操作；3) 屏幕阅读器兼容；4) 图片替代文字；5) 表单标签清晰；6) 焦点状态可见。标准：WCAG 2.1。好处：扩大用户群、提升SEO、法律合规。",
            "difficulty": "medium",
            "tags": ["UI设计", "可访问性", "无障碍"],
            "category": "technical"
        },
        {
            "question_text": "请解释设计系统的维护和迭代方法？",
            "reference_answer": "设计系统维护：1) 版本管理：语义化版本号；2) 变更日志：记录每次更新；3) 文档完善：使用指南、示例代码；4) 定期评审：检查一致性；5) 收集反馈：用户问题追踪；6) 团队协作：设计+开发共同维护。原则：稳定性优先、向后兼容、渐进式升级。",
            "difficulty": "hard",
            "tags": ["UI设计", "设计系统", "维护"],
            "category": "technical"
        }
    ],
    "operation": [
        {
            "question_text": "请解释用户增长模型有哪些？",
            "reference_answer": "用户增长模型：1) AARRR模型：获取、激活、留存、变现、推荐；2) RARRA模型：留存优先；3) 增长黑客：数据驱动快速实验；4) 北极星指标：核心增长指标。实施：明确增长目标 -> 搭建增长团队 -> 设计增长实验 -> 数据分析优化。持续迭代。",
            "difficulty": "medium",
            "tags": ["运营", "用户增长", "方法论"],
            "category": "technical"
        },
        {
            "question_text": "请解释用户分层运营的方法？",
            "reference_answer": "用户分层方法：1) RFM模型：最近消费、消费频次、消费金额；2) 生命周期分层：新用户、活跃用户、沉默用户、流失用户；3) 价值分层：高价值、中价值、低价值；4) 行为分层：根据用户行为特征。分层后制定差异化运营策略，提高运营效率。",
            "difficulty": "medium",
            "tags": ["运营", "用户分层", "精细化运营"],
            "category": "technical"
        },
        {
            "question_text": "请解释社群运营的核心要素？",
            "reference_answer": "社群运营要素：1) 定位：明确社群价值和目标用户；2) 规则：入群门槛、群规；3) 内容：持续输出价值内容；4) 互动：话题引导、活动策划；5) 氛围：维护良好讨论环境；6) 转化：引导商业价值。关键：找到核心用户，培养KOC，形成社群文化。",
            "difficulty": "medium",
            "tags": ["运营", "社群运营", "用户粘性"],
            "category": "technical"
        },
        {
            "question_text": "请解释活动运营的数据分析方法？",
            "reference_answer": "活动数据分析：1) 核心指标：参与率、转化率、ROI；2) 漏斗分析：各环节转化；3) 用户分群：不同用户表现；4) 时间分析：高峰时段；5) 对比分析：与历史活动对比。复盘要点：数据呈现、问题分析、经验总结、优化建议。数据驱动活动优化。",
            "difficulty": "medium",
            "tags": ["运营", "活动运营", "数据分析"],
            "category": "technical"
        },
        {
            "question_text": "请解释内容营销的策略和方法？",
            "reference_answer": "内容营销策略：1) 内容定位：目标用户、内容调性；2) 内容矩阵：图文、视频、直播；3) 内容规划：选题库、发布计划；4) 分发渠道：自有媒体、付费媒体、赢得媒体；5) 数据追踪：阅读量、互动率、转化率。核心：持续输出有价值的内容，建立品牌信任。",
            "difficulty": "medium",
            "tags": ["运营", "内容营销", "策略"],
            "category": "technical"
        },
        {
            "question_text": "请解释用户召回的方法？",
            "reference_answer": "用户召回方法：1) Push推送：个性化内容；2) 短信触达：优惠信息；3) 邮件营销：产品更新；4) 电话回访：高价值用户；5) 广告投放：精准定向。策略：分析流失原因 -> 制定召回方案 -> 选择触达渠道 -> 设计召回诱饵 -> 效果追踪。注意频率控制。",
            "difficulty": "medium",
            "tags": ["运营", "用户召回", "流失挽回"],
            "category": "technical"
        },
        {
            "question_text": "请解释运营活动策划的完整流程？",
            "reference_answer": "活动策划流程：1) 需求分析：目标、预算、时间；2) 创意策划：主题、玩法、规则；3) 方案设计：流程图、原型图；4) 资源协调：技术、设计、推广；5) 上线准备：测试、埋点；6) 活动执行：监控、调整；7) 数据复盘：效果分析、经验总结。文档化沉淀。",
            "difficulty": "medium",
            "tags": ["运营", "活动策划", "流程"],
            "category": "technical"
        },
        {
            "question_text": "请解释如何搭建数据运营体系？",
            "reference_answer": "数据运营体系：1) 指标体系：北极星指标、过程指标、结果指标；2) 数据采集：埋点设计、数据接入；3) 数据分析：报表、看板、分析报告；4) 数据应用：用户画像、个性化推荐、预警机制；5) 数据驱动决策：实验、优化、迭代。工具：神策、GrowingIO、Tableau。",
            "difficulty": "hard",
            "tags": ["运营", "数据运营", "体系搭建"],
            "category": "technical"
        },
        {
            "question_text": "请解释新媒体运营的核心能力？",
            "reference_answer": "新媒体运营能力：1) 内容创作：文案、图片、视频；2) 平台运营：微信公众号、抖音、小红书；3) 数据分析：阅读量、互动率、转化率；4) 活动策划：涨粉、促活、转化；5) 用户运营：粉丝互动、社群管理。趋势：短视频、直播、私域流量。持续学习平台规则。",
            "difficulty": "medium",
            "tags": ["运营", "新媒体", "内容"],
            "category": "technical"
        },
        {
            "question_text": "请解释品牌运营的方法？",
            "reference_answer": "品牌运营方法：1) 品牌定位：目标用户、差异化价值；2) 品牌形象：视觉识别、品牌故事；3) 内容传播：公关、广告、自媒体；4) 用户口碑：产品体验、服务口碑；5) 品牌活动：发布会、跨界合作。衡量指标：品牌知名度、美誉度、忠诚度。长期投入，持续积累。",
            "difficulty": "hard",
            "tags": ["运营", "品牌运营", "营销"],
            "category": "technical"
        }
    ],
    "qa": [
        {
            "question_text": "请解释测试金字塔模型？",
            "reference_answer": "测试金字塔：底层单元测试（数量最多）、中层集成测试、顶层UI测试（数量最少）。原因：底层测试执行快、成本低、定位准。实践：70%单元测试、20%集成测试、10%UI测试。避免倒金字塔，UI测试维护成本高、执行慢。",
            "difficulty": "medium",
            "tags": ["测试", "测试策略", "测试金字塔"],
            "category": "technical"
        },
        {
            "question_text": "请解释持续集成(CI)的概念和流程？",
            "reference_answer": "持续集成是频繁集成代码并自动构建测试。流程：1) 开发提交代码；2) 自动拉取代码；3) 自动构建；4) 自动运行测试；5) 反馈结果。工具：Jenkins、GitLab CI、GitHub Actions。好处：早发现问题、减少集成风险、提高开发效率。配合代码审查使用。",
            "difficulty": "medium",
            "tags": ["测试", "CI/CD", "DevOps"],
            "category": "technical"
        },
        {
            "question_text": "请解释接口测试的方法和工具？",
            "reference_answer": "接口测试验证API功能正确性。方法：1) 功能测试：正常场景、异常场景；2) 边界测试：参数边界值；3) 性能测试：响应时间、并发；4) 安全测试：鉴权、注入。工具：Postman、JMeter、RestAssured、pytest+requests。自动化：集成到CI/CD流程。",
            "difficulty": "medium",
            "tags": ["测试", "接口测试", "API"],
            "category": "technical"
        },
        {
            "question_text": "请解释测试环境管理的方法？",
            "reference_answer": "测试环境管理：1) 环境分类：开发环境、测试环境、预发布环境、生产环境；2) 环境隔离：独立数据库、配置管理；3) 数据管理：测试数据准备、数据隔离；4) 版本控制：代码版本、配置版本；5) 环境监控：服务状态、日志收集。使用Docker容器化部署提高效率。",
            "difficulty": "medium",
            "tags": ["测试", "环境管理", "DevOps"],
            "category": "technical"
        },
        {
            "question_text": "请解释移动端测试的要点？",
            "reference_answer": "移动端测试要点：1) 兼容性测试：不同设备、系统版本、分辨率；2) 安装卸载测试；3) 网络测试：弱网、断网；4) 电量消耗测试；5) 性能测试：启动时间、内存占用；6) 安全测试：数据加密、权限管理；7) 用户体验测试。工具：Appium、Monkey、PerfDog。",
            "difficulty": "medium",
            "tags": ["测试", "移动测试", "App"],
            "category": "technical"
        },
        {
            "question_text": "请解释安全测试的类型和方法？",
            "reference_answer": "安全测试类型：1) 漏洞扫描：自动化工具扫描；2) 渗透测试：模拟攻击；3) 代码审计：源码分析；4) 配置审计：服务器配置检查。常见漏洞：SQL注入、XSS、CSRF、越权访问。工具：OWASP ZAP、Burp Suite、SonarQube。遵循安全测试标准如OWASP Top 10。",
            "difficulty": "hard",
            "tags": ["测试", "安全测试", "网络安全"],
            "category": "technical"
        },
        {
            "question_text": "请解释测试数据管理的方法？",
            "reference_answer": "测试数据管理：1) 数据准备：手动创建、数据生成工具、生产数据脱敏；2) 数据隔离：每个测试用例独立数据；3) 数据清理：测试后清理数据；4) 数据版本：基线数据管理；5) 敏感数据：脱敏处理。工具：Faker生成假数据、数据库快照。确保数据安全和可重复性。",
            "difficulty": "medium",
            "tags": ["测试", "测试数据", "数据管理"],
            "category": "technical"
        },
        {
            "question_text": "请解释探索性测试的方法？",
            "reference_answer": "探索性测试是边学习边测试的方法。方法：1) 自由探索：无计划探索；2) 基于场景：用户场景模拟；3) 基于风险：高风险区域重点测试；4) 基于会话：时间盒测试。优点：发现未知问题、灵活应对变化。缺点：不可重复、依赖测试人员经验。与脚本测试结合使用。",
            "difficulty": "medium",
            "tags": ["测试", "探索性测试", "测试方法"],
            "category": "technical"
        },
        {
            "question_text": "请解释测试报告的内容和结构？",
            "reference_answer": "测试报告结构：1) 概述：测试目的、范围、时间；2) 测试环境：硬件、软件配置；3) 测试内容：功能点、测试用例；4) 测试结果：通过率、Bug统计；5) 风险评估：遗留问题、风险点；6) 结论建议：是否上线、改进建议。清晰、客观、有数据支撑。使用图表可视化。",
            "difficulty": "easy",
            "tags": ["测试", "测试报告", "文档"],
            "category": "technical"
        },
        {
            "question_text": "请解释测试左移的概念和实践？",
            "reference_answer": "测试左移是在开发早期介入测试。实践：1) 参与需求评审，提前发现问题；2) 测试用例提前设计；3) 开发自测，单元测试；4) 持续集成，快速反馈；5) 静态代码分析。好处：降低修复成本、提高质量、缩短周期。需要开发和测试紧密协作，测试前置。",
            "difficulty": "medium",
            "tags": ["测试", "测试左移", "敏捷"],
            "category": "technical"
        }
    ]
}

# 更多通用行为面试题
MORE_BEHAVIORAL_QUESTIONS = [
    {
        "question_text": "请描述一次你解决复杂问题的经历？",
        "reference_answer": "应该使用STAR法则：情境(Situation)、任务(Task)、行动(Action)、结果(Result)。描述问题背景、你的职责、采取的具体步骤、最终取得的成果。体现分析能力、解决问题的思路和执行力。",
        "difficulty": "medium",
        "tags": ["问题解决", "能力展示"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "你如何处理工作中的压力？",
        "reference_answer": "应该展示积极的压力管理方式：1) 分析压力来源；2) 合理规划时间；3) 分解任务优先级；4) 寻求团队支持；5) 保持工作生活平衡。举例说明具体方法，体现成熟的工作态度。",
        "difficulty": "easy",
        "tags": ["压力管理", "自我调节"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "请描述一次你主动学习新技能的经历？",
        "reference_answer": "应该说明：1) 学习动机：为什么学；2) 学习方法：怎么学；3) 应用场景：如何应用；4) 学习成果：取得什么效果。体现学习能力和主动性，展示持续成长的态度。",
        "difficulty": "easy",
        "tags": ["学习能力", "主动性"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "你如何保持对行业趋势的了解？",
        "reference_answer": "应该展示持续学习的习惯：1) 关注行业媒体和博客；2) 参加技术会议和社区；3) 阅读专业书籍；4) 参与开源项目；5) 与同行交流。举例说明最近学到的新知识或趋势。",
        "difficulty": "easy",
        "tags": ["行业认知", "学习习惯"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "请描述一次你失败的经历，你学到了什么？",
        "reference_answer": "选择一个真实的失败案例，重点放在反思和成长上：1) 描述失败情况；2) 分析失败原因；3) 采取的补救措施；4) 学到的教训；5) 如何避免再次发生。展示诚实、自省和成长能力。",
        "difficulty": "medium",
        "tags": ["失败经历", "自我反思"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "你期望的薪资是多少？",
        "reference_answer": "回答策略：1) 提前调研市场行情；2) 给出合理范围而非具体数字；3) 表明可以协商；4) 强调价值贡献。如：根据我的经验和市场调研，期望范围是X-Y，具体可以根据岗位职责和福利待遇协商。",
        "difficulty": "easy",
        "tags": ["薪资谈判", "求职技巧"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "你有什么问题想问我们吗？",
        "reference_answer": "应该提出有深度的问题：1) 关于岗位：团队结构、工作内容、成长空间；2) 关于公司：发展方向、企业文化；3) 关于业务：产品规划、市场策略。避免问薪资福利，展示对岗位的真正兴趣。",
        "difficulty": "easy",
        "tags": ["提问技巧", "求职态度"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "请描述你理想的工作环境？",
        "reference_answer": "应该描述积极的工作环境特征：1) 团队协作氛围；2) 学习成长机会；3) 开放沟通文化；4) 认可和激励机制。同时表达适应不同环境的能力，展示灵活性和团队意识。",
        "difficulty": "easy",
        "tags": ["工作环境", "团队文化"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "你如何管理自己的时间？",
        "reference_answer": "应该展示时间管理方法：1) 任务清单和优先级；2) 时间块管理；3) 避免多任务并行；4) 定期复盘优化；5) 工具辅助（日历、待办）。举例说明如何高效完成多个任务。",
        "difficulty": "easy",
        "tags": ["时间管理", "工作效率"],
        "category": "behavioral",
        "job_type": None
    },
    {
        "question_text": "请描述一次你超出预期完成工作的经历？",
        "reference_answer": "使用STAR法则描述：1) 任务背景和预期目标；2) 你的额外付出；3) 具体行动和方法；4) 最终成果和影响。体现主动性、责任感和追求卓越的态度。",
        "difficulty": "medium",
        "tags": ["工作表现", "主动性"],
        "category": "behavioral",
        "job_type": None
    }
]


async def extend_interview_questions():
    """扩展面试题目"""
    async with AsyncSessionLocal() as db:
        print("开始扩展面试题目...")

        total_added = 0

        # 1. 为各岗位添加更多技术题目
        for job_code, questions in EXTENDED_QUESTIONS.items():
            result = await db.execute(
                select(JobPosition).where(JobPosition.code == job_code)
            )
            job = result.scalar_one_or_none()

            if not job:
                continue

            # 检查是否已有这些题目
            existing_result = await db.execute(
                select(func.count(InterviewQuestion.id)).where(
                    InterviewQuestion.job_type == job_code
                )
            )
            existing_count = existing_result.scalar() or 0

            # 添加新题目
            added = 0
            for i, q in enumerate(questions):
                # 检查题目是否已存在
                check_result = await db.execute(
                    select(InterviewQuestion).where(
                        InterviewQuestion.question_text == q["question_text"]
                    )
                )
                if check_result.scalar_one_or_none():
                    continue

                question = InterviewQuestion(
                    category=q["category"],
                    job_type=job_code,
                    question_text=q["question_text"],
                    reference_answer=q["reference_answer"],
                    difficulty=q["difficulty"],
                    tags=q["tags"],
                    question_order=existing_count + i,
                    is_active=True
                )
                db.add(question)
                added += 1
                total_added += 1

            # 更新岗位题目数量
            if added > 0:
                job.question_count = existing_count + added
                print(
                    f"  为岗位 {job.name} 新增 {added} 道题目，共 {job.question_count} 道")

        # 2. 添加更多行为面试题
        for q in MORE_BEHAVIORAL_QUESTIONS:
            check_result = await db.execute(
                select(InterviewQuestion).where(
                    InterviewQuestion.question_text == q["question_text"]
                )
            )
            if check_result.scalar_one_or_none():
                continue

            question = InterviewQuestion(
                category=q["category"],
                job_type=q["job_type"],
                question_text=q["question_text"],
                reference_answer=q["reference_answer"],
                difficulty=q["difficulty"],
                tags=q["tags"],
                is_active=True
            )
            db.add(question)
            total_added += 1

        print(f"  新增 {len(MORE_BEHAVIORAL_QUESTIONS)} 道行为面试题")

        await db.commit()
        print(f"\n题目扩展完成！本次新增 {total_added} 道题目")


if __name__ == "__main__":
    asyncio.run(extend_interview_questions())
