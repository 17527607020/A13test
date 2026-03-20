"""
初始化面试数据
运行此脚本创建默认的面试题目和岗位数据
"""
import asyncio
from app.core.config import AsyncSessionLocal
from app.services.interview_service import InterviewService


async def main():
    """初始化面试数据"""
    async with AsyncSessionLocal() as db:
        print("开始初始化面试数据...")

        # 初始化岗位数据
        print("1. 初始化岗位数据...")
        await InterviewService.init_default_data(db)
        print("   岗位数据初始化完成")

        # 初始化默认题目
        print("2. 初始化面试题目...")
        questions = await InterviewService.create_default_questions(db, "general", None)
        print(f"   创建了 {len(questions)} 道默认题目")

        print("\n面试数据初始化完成！")


if __name__ == "__main__":
    asyncio.run(main())
