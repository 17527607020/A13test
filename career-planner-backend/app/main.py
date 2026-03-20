from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import user, student, job_graph, assessment, interview, home
from app.api.v1 import user_center as user_center_router
from app.core.config import settings

app = FastAPI(
    title="CareerPlannerAPI",
    description="职业规划智能体后端API服务",
    version="1.0.1"
)

# CORS 配置 - 允许前端跨域访问
origins = [
    "http://localhost:5002",  # 你的前端地址
    "http://127.0.0.1:5002",
    "http://localhost:5003",  # 新的前端地址
    "http://127.0.0.1:5003",
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user.router, prefix=settings.API_V1_STR, tags=["user"])
app.include_router(
    student.router, prefix=settings.API_V1_STR, tags=["student"])
app.include_router(
    job_graph.router, prefix=settings.API_V1_STR, tags=["job_graph"])
app.include_router(user_center_router.router,
                   prefix=settings.API_V1_STR, tags=["user_center"])
app.include_router(assessment.router,
                   prefix=settings.API_V1_STR, tags=["assessment"])
app.include_router(interview.router,
                   prefix=settings.API_V1_STR, tags=["interview"])
app.include_router(home.router,
                   prefix=settings.API_V1_STR, tags=["home"])


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok", "message": "Backend service is running"}


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to Career Planner API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.SERVER_PORT,
        reload=True
    )
