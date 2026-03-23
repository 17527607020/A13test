import asyncio
from sqlalchemy import text
from app.core.config import engine, Base, AsyncSessionLocal
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.user_history import UserHistory


async def create_tables():
    async with engine.begin() as conn:
        # 创建 user_profiles 表
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                nickname VARCHAR(50),
                phone VARCHAR(20),
                avatar_url VARCHAR(500),
                bio TEXT,
                location VARCHAR(200),
                website VARCHAR(200),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """))

        # 创建 user_histories 表
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS user_histories (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                action_type VARCHAR(50) NOT NULL,
                action_data JSON,
                description VARCHAR(500),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """))

        print("Tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())
