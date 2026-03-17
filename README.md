# 职业规划智能体 (Career Planner AI)

## 项目概述

职业规划智能体是一个基于AI的智能职业规划系统，帮助大学生和职场新人进行职业发展规划、能力评估、岗位匹配和职业路径规划。

### 核心功能

- **用户认证系统** - 注册、登录、权限管理
- **学生画像** - 简历解析、能力评估、个人资料管理
- **岗位图谱** - 基于Neo4j的岗位关系知识图谱
- **岗位探索** - 岗位搜索、筛选、详情查看
- **职业规划** - 智能职业路径推荐
- **报告中心** - 能力分析报告、职业规划报告
- **个人中心** - 用户信息管理、账号安全、操作历史
- **AI助手** - 智能问答、职业建议

## 技术栈

### 前端技术栈

- **框架**: Vue 3.5+ (Composition API)
- **语言**: TypeScript 5.9+
- **构建工具**: Vite 7.3+
- **UI框架**: Element Plus 2.13+
- **状态管理**: Pinia 3.0+ (支持持久化)
- **路由**: Vue Router 4.6+
- **图表**: ECharts 6.0+
- **HTTP客户端**: Axios 1.13+
- **样式**: SCSS

### 后端技术栈

- **框架**: FastAPI 0.100+
- **语言**: Python 3.11+
- **数据库**: PostgreSQL 15+ (SQLAlchemy异步ORM)
- **图数据库**: Neo4j 5.x (岗位关系图谱)
- **认证**: JWT Token (简单实现)
- **密码加密**: bcrypt
- **AI服务**: DeepSeek API (简历解析、能力评估)
- **文档**: Swagger/OpenAPI

### 开发工具

- **版本控制**: Git
- **数据库迁移**: Alembic
- **容器化**: Docker
- **代码规范**: ESLint + Prettier

## 项目结构

```
career-planner-frontend/          # 前端项目
├── src/
│   ├── api/                   # API接口封装
│   │   ├── index.ts           # 统一导出
│   │   ├── user.ts            # 用户相关API
│   │   ├── studentProfile.ts   # 学生画像API
│   │   └── jobGraph.ts        # 岗位图谱API
│   ├── assets/                 # 静态资源
│   │   └── main.scss          # 全局样式
│   ├── components/             # 通用组件
│   │   ├── DashboardLayout.vue # 布局组件
│   │   ├── AbilityRadar.vue   # 能力雷达图
│   │   ├── ProfileForm.vue    # 画像表单
│   │   └── ResumeUpload.vue   # 简历上传
│   ├── router/                 # 路由配置
│   │   └── index.ts
│   ├── stores/                 # 状态管理
│   │   ├── index.ts
│   │   └── user.ts           # 用户状态
│   ├── types/                  # TypeScript类型定义
│   │   ├── index.ts
│   │   ├── student.ts
│   │   └── user.ts
│   ├── utils/                  # 工具函数
│   │   ├── index.ts
│   │   └── request.ts        # Axios封装
│   ├── views/                  # 页面组件
│   │   ├── Login.vue           # 登录页
│   │   ├── Home.vue            # 首页
│   │   ├── StudentProfile.vue   # 学生画像
│   │   ├── JobGraph.vue        # 岗位图谱
│   │   ├── JobExplore.vue      # 岗位探索
│   │   ├── CareerPlan.vue      # 职业规划
│   │   ├── ReportCenter.vue    # 报告中心
│   │   ├── UserCenter.vue      # 个人中心
│   │   └── AIAssistant.vue     # AI助手
│   ├── App.vue                 # 根组件
│   └── main.ts                 # 入口文件
├── public/                     # 公共资源
├── package.json
├── vite.config.ts
├── tsconfig.json
└── .eslintrc.js

career-planner-backend/           # 后端项目
├── app/
│   ├── api/                   # API路由
│   │   └── v1/
│   │       ├── user.py         # 用户认证
│   │       ├── student.py      # 学生画像
│   │       ├── job_graph.py    # 岗位图谱
│   │       └── user_center.py  # 个人中心
│   ├── core/                   # 核心配置
│   │   └── config.py         # 数据库、Neo4j配置
│   ├── models/                 # 数据模型
│   │   ├── user.py          # 用户模型
│   │   ├── student.py       # 学生模型
│   │   ├── user_profile.py  # 用户资料模型
│   │   └── user_history.py  # 历史记录模型
│   ├── schemas/                # Pydantic数据验证
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── user_profile.py
│   │   └── user_center.py
│   ├── services/               # 业务逻辑
│   │   ├── user_service.py
│   │   ├── neo4j_service.py  # Neo4j服务
│   │   └── ability_assessment.py  # 能力评估
│   └── main.py                # FastAPI应用入口
├── alembic/                   # 数据库迁移
├── tests/                     # 测试文件
├── init_db.py                 # 数据库初始化脚本
├── requirements.txt            # Python依赖
├── Dockerfile
└── .env.example              # 环境变量示例
```

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Neo4j 5.x

### 1. 克隆项目

```bash
git clone https://github.com/LJD19/A13test03.git
cd A13test03
```

### 2. 后端设置

#### 2.1 创建虚拟环境

```bash
cd career-planner-backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

#### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 2.3 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/career_planner
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

#### 2.4 初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head

# 或者运行初始化脚本
python init_db.py
```

#### 2.5 启动后端服务

```bash
python -m uvicorn app.main:app --reload --port 8001
```

后端启动成功后访问：
- API文档：http://localhost:8001/docs
- 健康检查：http://localhost:8001/health

### 3. 前端设置

#### 3.1 安装依赖

```bash
cd career-planner-frontend
npm install
```

#### 3.2 启动开发服务器

```bash
npm run dev
```

前端启动成功后访问：http://localhost:5002

### 4. 访问应用

1. 打开浏览器访问 http://localhost:5002
2. 点击"还没有账号？立即注册"创建测试账号
3. 登录后即可使用所有功能

## 核心功能说明

### 用户认证系统

**技术实现**:
- 基于JWT的简单Token认证
- bcrypt密码加密
- Pinia持久化存储用户状态

**API端点**:
- `POST /api/v1/users/register` - 用户注册
- `POST /api/v1/users/login` - 用户登录
- `GET /api/v1/users/me` - 获取当前用户信息

**前端组件**:
- `Login.vue` - 登录页面
- `user.ts` (store) - 用户状态管理
- `request.ts` - 请求拦截器自动添加Token

### 学生画像系统

**技术实现**:
- DeepSeek AI解析简历（支持PDF、Word、图片）
- 基于规则的能力评估算法
- 多步骤表单（基本信息、教育、经历、项目、技能、证书、奖项）

**API端点**:
- `POST /api/v1/students/resume/upload` - 上传简历并解析
- `POST /api/v1/students/resume/parse` - 解析简历文本
- `GET /api/v1/students/profile` - 获取学生画像
- `POST /api/v1/students/profile` - 保存学生画像

**前端组件**:
- `StudentProfile.vue` - 学生画像页面
- `ProfileForm.vue` - 多步骤画像表单
- `ResumeUpload.vue` - 简历上传组件
- `AbilityRadar.vue` - 能力雷达图展示

**能力评估维度**:
- 专业技能
- 学习能力
- 沟通能力
- 抗压能力
- 创新能力
- 实习能力

### 岗位图谱系统

**技术实现**:
- Neo4j图数据库存储岗位关系
- ECharts力导向图可视化
- 支持晋升路径和换岗路径查询
- 模拟数据降级机制

**API端点**:
- `GET /api/v1/job-graph/jobs` - 获取所有岗位
- `GET /api/v1/job-graph/jobs-with-paths` - 获取有路径的岗位
- `GET /api/v1/job-graph/promotion-paths` - 获取晋升路径
- `GET /api/v1/job-graph/transfer-paths` - 获取换岗路径
- `GET /api/v1/job-graph/full-graph` - 获取完整图谱

**前端组件**:
- `JobGraph.vue` - 岗位图谱页面
- `jobGraph.ts` (API) - 岗位图谱接口

**图谱特性**:
- 节点颜色编码（按岗位类型）
- 关系类型区分（晋升/换岗）
- 交互式节点点击查看详情
- 力导向布局算法
- 响应式设计

### 个人中心系统

**技术实现**:
- 内联组件实现（避免导入错误）
- LocalStorage数据持久化
- 模拟历史数据

**API端点**:
- `GET /api/v1/users/profile` - 获取用户资料
- `POST /api/v1/users/profile` - 更新用户资料
- `POST /api/v1/users/change-password` - 修改密码
- `GET /api/v1/users/history` - 获取操作历史

**前端组件**:
- `UserCenter.vue` - 个人中心页面（内联实现）

**功能模块**:
- 个人信息：头像、昵称、手机号、个人简介
- 账号安全：密码修改（带验证）
- 历史记录：时间线展示操作历史

## 数据库设计

### PostgreSQL表结构

#### users表
```sql
- id: 主键
- username: 用户名（唯一）
- email: 邮箱（唯一）
- password_hash: 密码哈希
- role: 角色（student/admin）
- created_at: 创建时间
```

#### students表
```sql
- id: 主键
- user_id: 用户ID（外键）
- created_at: 创建时间
```

#### student_profiles表
```sql
- id: 主键
- student_id: 学生ID（外键）
- basic_info: 基本信息（JSON）
- education: 教育经历（JSON）
- experience: 工作经历（JSON）
- projects: 项目经验（JSON）
- skills: 技能列表（JSON）
- certificates: 证书列表（JSON）
- awards: 奖项列表（JSON）
- ability_scores: 能力评分（JSON）
- created_at: 创建时间
- updated_at: 更新时间
```

#### user_profiles表
```sql
- id: 主键
- user_id: 用户ID（外键）
- nickname: 昵称
- phone: 手机号
- avatar_url: 头像URL
- bio: 个人简介
- location: 所在地
- website: 个人网站
- created_at: 创建时间
- updated_at: 更新时间
```

#### user_history表
```sql
- id: 主键
- user_id: 用户ID（外键）
- action_type: 操作类型
- action_data: 操作数据（JSON）
- description: 操作描述
- created_at: 创建时间
```

### Neo4j图数据库

#### 节点类型
- `Job`: 岗位节点
  - 属性：name, description, salary, type, source

#### 关系类型
- `PROMOTES_TO`: 晋升关系（单向）
- `TRANSFERS_TO`: 换岗关系（双向）

## API文档

### 认证相关

#### 用户注册
```http
POST /api/v1/users/register
Content-Type: application/json

{
  "username": "test_user",
  "email": "test@example.com",
  "password": "password123"
}

Response:
{
  "success": true,
  "data": {
    "id": 1,
    "username": "test_user",
    "email": "test@example.com"
  }
}
```

#### 用户登录
```http
POST /api/v1/users/login
Content-Type: application/json

{
  "username": "test_user",
  "password": "password123"
}

Response:
{
  "success": true,
  "data": {
    "token": "token_xxx",
    "user": {
      "id": 1,
      "username": "test_user",
      "email": "test@example.com"
    }
  }
}
```

### 学生画像相关

#### 上传简历并解析
```http
POST /api/v1/students/resume/upload
Content-Type: multipart/form-data

file: <resume_file>

Response:
{
  "success": true,
  "data": {
    "basic_info": { ... },
    "education": [ ... ],
    "experience": [ ... ],
    "projects": [ ... ],
    "skills": [ ... ],
    "certificates": [ ... ],
    "awards": [ ... ]
  }
}
```

### 岗位图谱相关

#### 获取完整图谱
```http
GET /api/v1/job-graph/full-graph?graph_type=all

Response:
{
  "success": true,
  "data": {
    "nodes": [
      {
        "id": "1",
        "name": "前端开发",
        "type": "开发",
        "description": "...",
        "salary": "10-15K"
      }
    ],
    "links": [
      {
        "source": "1",
        "target": "2",
        "type": "PROMOTES_TO"
      }
    ]
  }
}
```

## 开发规范

### 前端开发规范

1. **组件命名**: PascalCase (如 `UserProfile.vue`)
2. **文件命名**: kebab-case (如 `user-profile.ts`)
3. **变量命名**: camelCase
4. **常量命名**: UPPER_SNAKE_CASE
5. **类型定义**: 统一放在 `types/` 目录
6. **API调用**: 统一放在 `api/` 目录
7. **样式**: 使用SCSS，组件内使用scoped

### 后端开发规范

1. **路由定义**: 使用APIRouter，按功能模块分组
2. **数据验证**: 使用Pydantic schemas
3. **异步操作**: 所有数据库操作使用async/await
4. **错误处理**: 使用HTTPException，返回统一格式
5. **依赖注入**: 使用FastAPI的Depends

### Git提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具链相关
```

## 常见问题

### 1. 后端启动失败

**问题**: `ModuleNotFoundError: No module named 'xxx'`

**解决**:
```bash
pip install -r requirements.txt
```

### 2. 数据库连接失败

**问题**: `connection to server at "localhost:5432" failed`

**解决**:
- 检查PostgreSQL是否启动
- 检查`.env`文件中的数据库配置
- 确保数据库已创建

### 3. Neo4j连接失败

**问题**: 岗位图谱API超时

**解决**:
- 检查Neo4j是否启动
- 检查Neo4j端口7687是否开放
- 检查用户名密码配置

### 4. 前端编译错误

**问题**: TypeScript类型错误

**解决**:
```bash
npm run build
```

### 5. CORS错误

**问题**: 前端无法访问后端API

**解决**:
- 后端已配置CORS允许所有来源
- 检查后端端口是否正确
- 检查防火墙设置

## 部署指南

### Docker部署

#### 后端部署

```bash
cd career-planner-backend
docker build -t career-planner-backend .
docker run -p 8001:8000 career-planner-backend
```

#### 前端部署

```bash
cd career-planner-frontend
npm run build
# 将dist目录部署到Nginx等Web服务器
```

### 生产环境配置

1. **修改环境变量**:
   - 数据库连接字符串
   - Neo4j连接信息
   - API密钥

2. **安全配置**:
   - 修改CORS允许的域名
   - 配置HTTPS
   - 使用强密码策略

3. **性能优化**:
   - 启用数据库连接池
   - 配置Redis缓存
   - 启用CDN

## 项目特色

1. **AI驱动**: 集成DeepSeek AI实现智能简历解析和能力评估
2. **知识图谱**: 基于Neo4j构建岗位关系图谱
3. **可视化**: ECharts实现丰富的数据可视化
4. **响应式**: 适配不同屏幕尺寸
5. **模块化**: 前后端分离，易于维护和扩展
6. **类型安全**: 全面的TypeScript和Pydantic类型定义

## 后续开发计划

- [ ] 完善AI助手功能
- [ ] 增加更多岗位数据
- [ ] 优化能力评估算法
- [ ] 添加社交分享功能
- [ ] 实现消息通知系统
- [ ] 增加数据导出功能
- [ ] 完善单元测试和集成测试
- [ ] 性能优化和缓存策略

## 联系方式

- 项目地址: https://github.com/LJD19/A13test03
- 问题反馈: GitHub Issues

## 许可证

MIT License