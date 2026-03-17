import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select, text
from app.core.config import settings, Base
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.user_history import UserHistory
from app.services.user_service import get_password_hash


async def init_db():
    """初始化数据库表"""
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    
    print("数据库表创建成功！")
    await engine.dispose()


async def create_test_user():
    """创建测试用户"""
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.username == 'test_user')
        )
        user = result.scalar_one_or_none()
        
        if user:
            print(f'User exists: {user.username}')
            await session.delete(user)
            await session.commit()
            print(f'Deleted old user')
        
        new_user = User(
            username='test_user',
            email='test@example.com',
            password_hash=get_password_hash('password'),
            role='student'
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        
        print(f'✅ Created test_user:')
        print(f'   User ID: {new_user.id}')
        print(f'   Username: {new_user.username}')
        print(f'   Email: {new_user.email}')
        print(f'   Password hash: {new_user.password_hash[:50]}...')
        
    await session.close()
    await engine.dispose()


async def main():
    """主函数"""
    print("开始初始化数据库...")
    
    await init_db()
    await create_test_user()
    
    print("数据库初始化完成！")


if __name__ == "__main__":
    asyncio.run(main())