# 职业规划智能体 - 开发者指南

> 本文档专为AI开发者准备，帮助快速理解项目架构并开始开发

## 🎯 项目核心定位

**职业规划智能体**是一个基于AI的智能职业规划系统，核心价值在于：
- 🤖 **AI驱动**：使用DeepSeek AI进行简历解析和能力评估
- 📊 **知识图谱**：基于Neo4j构建岗位关系图谱
- 🎯 **智能推荐**：基于用户画像和岗位图谱进行职业规划
- 📱 **现代化技术栈**：Vue3 + FastAPI + TypeScript + Python

## 🏗️ 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    用户浏览器 (Vue3前端)                    │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  职业规划智能体前端 (career-planner-frontend)  │  │
│  │  - Vue 3.5+ (Composition API)               │  │
│  │  - TypeScript 5.9+                          │  │
│  │  - Element Plus 2.13+                         │  │
│  │  - Pinia 3.0+ (状态管理)                   │  │
│  │  - ECharts 6.0+ (数据可视化)                │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                           │ HTTP/REST API
                           │
┌──────────────────────────────▼──────────────────────────────────┐
│              FastAPI后端 (career-planner-backend)        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  业务逻辑层 (app/)                              │  │
│  │  ├── api/v1/        # API路由层                 │  │
│  │  ├── services/        # 业务逻辑层                 │  │
│  │  ├── models/          # 数据模型层                 │  │
│  │  ├── schemas/         # 数据验证层                 │  │
│  │  └── core/           # 核心配置层                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  数据存储层                                       │  │
│  │  ├── PostgreSQL (用户数据)                       │  │
│  │  └── Neo4j (岗位关系图谱)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  外部服务层                                       │  │
│  │  └── DeepSeek AI (简历解析、能力评估)            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 数据流向

```
用户操作 → 前端组件 → Pinia Store → API调用 → FastAPI路由
                                                    ↓
                                            业务逻辑层 (Services)
                                                    ↓
                                            数据库层 (PostgreSQL/Neo4j)
                                                    ↓
                                            外部AI服务 (DeepSeek)
                                                    ↓
                                            返回数据 → 前端展示
```

## 📁 项目目录详解

### 前端目录结构

```
career-planner-frontend/
├── src/
│   ├── api/                      # 🌐 API接口层
│   │   ├── index.ts             # 统一导出所有API
│   │   ├── user.ts              # 用户认证API (登录、注册)
│   │   ├── studentProfile.ts     # 学生画像API (简历、画像)
│   │   └── jobGraph.ts          # 岗位图谱API (图谱查询)
│   │
│   ├── components/                # 🧩 可复用组件
│   │   ├── DashboardLayout.vue  # 主布局组件 (侧边栏、顶部栏)
│   │   ├── AbilityRadar.vue      # 能力雷达图组件
│   │   ├── ProfileForm.vue       # 多步骤画像表单
│   │   └── ResumeUpload.vue      # 简历上传组件
│   │
│   ├── views/                    # 📄 页面组件
│   │   ├── Login.vue            # 登录页面
│   │   ├── Home.vue             # 首页
│   │   ├── StudentProfile.vue     # 学生画像页面
│   │   ├── JobGraph.vue          # 岗位图谱页面
│   │   ├── JobExplore.vue        # 岗位探索页面
│   │   ├── CareerPlan.vue        # 职业规划页面
│   │   ├── ReportCenter.vue      # 报告中心页面
│   │   ├── UserCenter.vue        # 个人中心页面
│   │   └── AIAssistant.vue       # AI助手页面
│   │
│   ├── stores/                   # 🗄️ 状态管理 (Pinia)
│   │   ├── index.ts             # Store统一导出
│   │   └── user.ts              # 用户状态 (登录、用户信息)
│   │
│   ├── router/                   # 🛣️ 路由配置
│   │   └── index.ts             # 路由定义、守卫
│   │
│   ├── types/                    # 📝 TypeScript类型定义
│   │   ├── index.ts             # 通用类型
│   │   ├── student.ts           # 学生画像类型
│   │   └── user.ts              # 用户相关类型
│   │
│   ├── utils/                    # 🔧 工具函数
│   │   ├── index.ts             # 工具函数导出
│   │   └── request.ts          # Axios封装 (拦截器、错误处理)
│   │
│   ├── assets/                   # 🎨 静态资源
│   │   ├── main.scss            # 全局样式
│   │   └── vue.svg             # Vue logo
│   │
│   ├── App.vue                   # 📱 应用根组件
│   └── main.ts                   # 🚀 应用入口
│
├── public/                      # 📂 公共静态资源
├── package.json                  # 📦 依赖配置
├── vite.config.ts               # ⚙️ Vite配置
├── tsconfig.json                # 📝 TypeScript配置
└── .eslintrc.js                # 📏 ESLint配置
```

### 后端目录结构

```
career-planner-backend/
├── app/
│   ├── api/                      # 🌐 API路由层
│   │   └── v1/
│   │       ├── user.py           # 用户认证路由
│   │       ├── student.py        # 学生画像路由
│   │       ├── job_graph.py      # 岗位图谱路由
│   │       └── user_center.py   # 个人中心路由
│   │
│   ├── services/                 # 💼 业务逻辑层
│   │   ├── user_service.py     # 用户业务逻辑
│   │   ├── neo4j_service.py  # Neo4j图数据库服务
│   │   └── ability_assessment.py  # 能力评估算法
│   │
│   ├── models/                   # 📊 数据模型层
│   │   ├── user.py            # 用户模型
│   │   ├── student.py         # 学生模型
│   │   ├── user_profile.py    # 用户资料模型
│   │   └── user_history.py    # 历史记录模型
│   │
│   ├── schemas/                  # ✅ 数据验证层
│   │   ├── user.py            # 用户数据验证
│   │   ├── student.py         # 学生数据验证
│   │   ├── user_profile.py    # 用户资料验证
│   │   └── user_center.py   # 个人中心数据验证
│   │
│   ├── core/                     # ⚙️ 核心配置
│   │   └── config.py         # 数据库、Neo4j配置
│   │
│   └── main.py                   # 🚀 FastAPI应用入口
│
├── alembic/                    # 🗃️ 数据库迁移
│   ├── versions/               # 迁移脚本
│   └── env.py                  # Alembic环境配置
│
├── tests/                      # 🧪 测试文件
│   └── test_user_api.py       # 用户API测试
│
├── init_db.py                  # 🗄️ 数据库初始化脚本
├── requirements.txt             # 📦 Python依赖
├── Dockerfile                  # 🐳 Docker配置
└── .env.example                # 🔒 环境变量示例
```

## 🔑 核心技术实现

### 1. 用户认证系统

#### 技术架构
```
前端 (Vue3 + Pinia)
    ↓
登录表单 → user.ts (Store) → user.ts (API)
    ↓
FastAPI后端 → user.py (路由) → user_service.py (业务逻辑)
    ↓
PostgreSQL数据库 → bcrypt密码验证 → JWT Token生成
    ↓
返回Token → 前端存储 → 后续请求自动携带Token
```

#### 关键文件
- **前端**: `src/stores/user.ts`, `src/api/user.ts`, `src/views/Login.vue`
- **后端**: `app/api/v1/user.py`, `app/services/user_service.py`, `app/models/user.py`

#### 认证流程
1. 用户提交登录表单
2. 前端调用 `POST /api/v1/users/login`
3. 后端验证用户名密码 (bcrypt)
4. 生成JWT Token (简单实现: `token_{id}_{username}`)
5. 返回Token和用户信息
6. 前端存储到Pinia + LocalStorage
7. 后续请求自动在Header中携带Token

### 2. 学生画像系统

#### 技术架构
```
用户上传简历
    ↓
前端解析文件 → ResumeUpload.vue → studentProfileApi.uploadResume()
    ↓
FastAPI后端 → student.py路由 → 解析文件内容
    ↓
文件类型判断:
- PDF → PyPDF2提取文本
- Word → python-docx提取文本  
- 图片 → pytesseract OCR识别
    ↓
DeepSeek AI解析 → 提取结构化信息
    ↓
能力评估算法 → ability_assessment.py → 计算能力评分
    ↓
保存到PostgreSQL → student_profiles表
    ↓
返回解析结果 → 前端展示 → ProfileForm.vue编辑
```

#### 关键文件
- **前端**: `src/views/StudentProfile.vue`, `src/components/ProfileForm.vue`, `src/components/ResumeUpload.vue`, `src/api/studentProfile.ts`
- **后端**: `app/api/v1/student.py`, `app/services/ability_assessment.py`, `app/models/student.py`

#### AI解析流程
```python
# 1. 文件解析
if file_type == "application/pdf":
    text = extract_text_from_pdf(content)
elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
    text = extract_text_from_docx(content)
elif file_type in ["image/jpeg", "image/png"]:
    text = extract_text_from_image(content)

# 2. AI解析
prompt = f"""
请从以下简历文本中提取结构化信息，以JSON格式返回：
简历内容：{text}
请提取：基本信息、教育、经历、项目、技能、证书、奖项
只返回JSON，不要其他说明文字。
"""
response = await httpx.AsyncClient().post(
    "https://api.deepseek.com/v1/chat/completions",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个专业的简历解析助手"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 2000
    }
)

# 3. 能力评估
scores = calculate_ability_scores(profile_data)
```

### 3. 岗位图谱系统

#### 技术架构
```
用户访问岗位图谱
    ↓
JobGraph.vue → jobGraphApi.getFullGraph()
    ↓
FastAPI后端 → job_graph.py路由 → neo4j_service.py
    ↓
Neo4j图数据库查询:
- 获取所有岗位节点
- 获取岗位关系 (晋升/换岗)
    ↓
返回图谱数据 → 前端ECharts渲染
```

#### 关键文件
- **前端**: `src/views/JobGraph.vue`, `src/api/jobGraph.ts`
- **后端**: `app/api/v1/job_graph.py`, `app/services/neo4j_service.py`

#### Neo4j数据模型
```
节点类型: Job
- 属性: name, description, salary, type, source

关系类型:
- PROMOTES_TO: 晋升关系 (单向)
- TRANSFERS_TO: 换岗关系 (双向)
```

#### 图谱查询示例
```cypher
# 获取所有岗位
MATCH (j:Job) RETURN j.name, j.description, j.salary, j.type

# 获取晋升路径
MATCH path = (start:Job {name: $job_name})-[:PROMOTES_TO*]->(end:Job)
RETURN path

# 获取换岗路径
MATCH (start:Job {name: $job_name})-[:TRANSFERS_TO*]-(end:Job)
RETURN start, end
```

### 4. 个人中心系统

#### 技术架构
```
用户访问个人中心
    ↓
UserCenter.vue (内联实现，避免组件导入错误)
    ↓
三个功能模块:
1. 个人信息 → localStorage读取 → 表单展示 → 保存到localStorage
2. 账号安全 → 密码表单 → 验证 → 模拟修改
3. 历史记录 → 模拟数据 → 时间线展示
```

#### 关键文件
- **前端**: `src/views/UserCenter.vue` (内联实现)
- **后端**: `app/api/v1/user_center.py`, `app/models/user_profile.py`, `app/models/user_history.py`

#### 内联实现原因
- 避免组件导入错误
- 减少文件依赖
- 简化构建过程
- 提高稳定性

## 🚀 快速开始开发

### 环境准备

#### 1. 安装Node.js和Python
```bash
# 检查Node.js版本 (需要18+)
node --version

# 检查Python版本 (需要3.11+)
python --version
```

#### 2. 克隆项目
```bash
git clone https://github.com/LJD19/A13test03.git
cd A13test03
```

#### 3. 启动后端
```bash
cd career-planner-backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，配置数据库和Neo4j连接

# 初始化数据库
python init_db.py

# 启动后端服务
python -m uvicorn app.main:app --reload --port 8001
```

#### 4. 启动前端
```bash
cd career-planner-frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 开发工具推荐

#### VS Code插件
- **Vue - Official**: Vue语法高亮
- **TypeScript Vue Plugin**: TypeScript支持
- **ESLint**: 代码检查
- **Prettier**: 代码格式化
- **Auto Rename Tag**: Vue组件标签重命名

#### 浏览器插件
- **Vue.js devtools**: Vue调试工具
- **React Developer Tools**: (如果需要调试React相关库)

## 🔧 开发规范

### 前端开发规范

#### 1. 组件开发
```vue
<template>
  <div class="component-name">
    <!-- 模板内容 -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 响应式数据
const data = ref('')

// 生命周期
onMounted(() => {
  // 初始化逻辑
})

// 暴露给父组件
defineExpose({
  data
})
</script>

<style scoped lang="scss">
.component-name {
  // 样式
}
</style>
```

#### 2. API调用
```typescript
import request from '@/utils/request'

export const apiFunction = (params: any) => {
  return request.get('/api/endpoint', { params })
}
```

#### 3. 状态管理
```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  
  const isLoggedIn = computed(() => !!user.value)
  
  const login = async (credentials: any) => {
    // 登录逻辑
  }
  
  return { user, isLoggedIn, login }
})
```

### 后端开发规范

#### 1. 路由定义
```python
from fastapi import APIRouter, Depends
from app.core.config import get_db

router = APIRouter(prefix="/endpoint", tags=["标签"])

@router.get("/")
async def endpoint_function(
    param: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """接口描述"""
    # 业务逻辑
    return {"success": True, "data": result}
```

#### 2. 数据验证
```python
from pydantic import BaseModel, Field

class DataSchema(BaseModel):
    name: str = Field(..., description="字段描述")
    age: int = Field(..., ge=0, le=120)
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+')
```

#### 3. 数据库操作
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_data(db: AsyncSession, id: int):
    result = await db.execute(
        select(Model).where(Model.id == id)
    )
    return result.scalar_one_or_none()
```

## 🐛 常见问题解决

### 1. 前端编译错误

#### 问题：TypeScript类型错误
```
error TS2322: Type 'string' is not assignable to type 'number'
```

**解决**：
```typescript
// 确保类型正确
const value: number = Number(stringValue)
```

#### 问题：组件导入错误
```
error: Failed to resolve component import
```

**解决**：
- 使用内联实现
- 检查文件路径
- 重新安装依赖：`rm -rf node_modules && npm install`

### 2. 后端启动错误

#### 问题：ModuleNotFoundError
```
ModuleNotFoundError: No module named 'xxx'
```

**解决**：
```bash
pip install -r requirements.txt
```

#### 问题：数据库连接失败
```
sqlalchemy.exc.DBAPIError: (psycopg2.OperationalError) could not connect to server
```

**解决**：
- 检查PostgreSQL是否启动
- 检查`.env`文件配置
- 确保数据库已创建

### 3. API调用错误

#### 问题：CORS错误
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**解决**：
- 后端已配置CORS：`allow_origin_regex=".*"`
- 检查后端端口是否正确
- 检查防火墙设置

#### 问题：超时错误
```
AxiosError: timeout of 30000ms exceeded
```

**解决**：
- 检查后端服务是否运行
- 检查数据库查询性能
- 增加超时时间或优化查询

## 📊 数据库设计

### PostgreSQL表关系

```
users (用户表)
    ↓ 1:N
students (学生表)
    ↓ 1:1
student_profiles (学生画像表)

users (用户表)
    ↓ 1:N
user_profiles (用户资料表)

users (用户表)
    ↓ 1:N
user_history (历史记录表)
```

### Neo4j图关系

```
Job (岗位节点)
    ↓ PROMOTES_TO (晋升)
Job (岗位节点)

Job (岗位节点)
    ↓ TRANSFERS_TO (换岗)
Job (岗位节点)
    ↑ TRANSFERS_TO (双向)
Job (岗位节点)
```

## 🎯 核心功能开发指南

### 添加新页面

#### 1. 创建页面组件
```bash
# 在src/views/下创建新页面
touch src/views/NewPage.vue
```

#### 2. 添加路由
```typescript
// src/router/index.ts
{
  path: '/new-page',
  name: 'NewPage',
  component: () => import('@/views/NewPage.vue'),
  meta: { requiresAuth: true }
}
```

#### 3. 添加菜单项
```vue
<!-- src/components/DashboardLayout.vue -->
<router-link to="/new-page">新页面</router-link>
```

### 添加新API

#### 1. 创建API接口
```typescript
// src/api/newApi.ts
import request from '@/utils/request'

export interface DataType {
  id: number
  name: string
}

export const newApi = {
  getData(): Promise<DataType[]> {
    return request.get('/api/endpoint')
  }
}
```

#### 2. 导出API
```typescript
// src/api/index.ts
export * from './newApi'
```

#### 3. 创建后端路由
```python
# app/api/v1/new_api.py
from fastapi import APIRouter

router = APIRouter(prefix="/new-api", tags=["新API"])

@router.get("/")
async def get_data():
    return {"success": True, "data": []}
```

#### 4. 注册路由
```python
# app/main.py
from app.api.v1 import new_api

app.include_router(new_api.router, prefix=settings.API_V1_STR, tags=["new_api"])
```

## 🚢 部署准备

### 生产环境检查清单

- [ ] 修改所有环境变量 (数据库、Neo4j、API密钥)
- [ ] 配置HTTPS
- [ ] 限制CORS允许的域名
- [ ] 启用数据库连接池
- [ ] 配置Redis缓存
- [ ] 优化静态资源加载
- [ ] 配置CDN
- [ ] 启用日志记录
- [ ] 配置监控和告警

### Docker部署

#### 后端Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 前端构建
```bash
npm run build
# 将dist目录部署到Web服务器
```

## 📝 开发注意事项

### 1. 代码质量
- 遵循TypeScript严格模式
- 使用ESLint检查代码
- 使用Prettier格式化代码
- 编写单元测试
- 添加代码注释

### 2. 性能优化
- 使用虚拟滚动处理长列表
- 图片懒加载
- 路由懒加载
- API响应缓存
- 数据库查询优化

### 3. 安全考虑
- 验证所有用户输入
- 使用HTTPS
- 敏感数据加密存储
- 定期更新依赖
- 实施速率限制

### 4. 用户体验
- 添加加载状态
- 错误提示友好
- 响应式设计
- 无障碍访问
- 国际化支持

## 🎓 学习资源

### 官方文档
- [Vue 3文档](https://vuejs.org/)
- [TypeScript文档](https://www.typescriptlang.org/)
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [Element Plus文档](https://element-plus.org/)
- [ECharts文档](https://echarts.apache.org/)

### 推荐教程
- [Vue 3组合式API](https://vuejs.org/guide/introduction.html)
- [Pinia状态管理](https://pinia.vuejs.org/)
- [FastAPI用户指南](https://fastapi.tiangolo.com/tutorial/)
- [Neo4j图数据库](https://neo4j.com/docs/)

## 🤝 贡献指南

### 提交代码
```bash
git add .
git commit -m "feat: 添加新功能"
git push origin main
```

### 代码审查
- 确保代码通过ESLint检查
- 确保所有测试通过
- 确保文档已更新
- 确保没有敏感信息

## 📞 获取帮助

- 项目地址: https://github.com/LJD19/A13test03
- 问题反馈: GitHub Issues
- 技术讨论: GitHub Discussions

---

**祝开发顺利！🚀**