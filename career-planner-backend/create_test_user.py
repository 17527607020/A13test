import psycopg2
from app.services.user_service import get_password_hash

def create_test_user():
    """创建测试用户"""
    try:
        # 连接到数据库
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="career_planner",
            user="postgres",
            password="123456"
        )
        cursor = conn.cursor()
        
        # 检查是否已存在测试用户
        cursor.execute("SELECT id, username FROM users WHERE username = 'test_user'")
        existing_user = cursor.fetchone()
        
        if existing_user:
            print(f"✅ 测试用户已存在: ID={existing_user[0]}, 用户名={existing_user[1]}")
            # 删除现有用户
            cursor.execute("DELETE FROM users WHERE username = 'test_user'")
            print("✅ 已删除现有测试用户")
        
        # 创建新测试用户
        password_hash = get_password_hash("password123")  # 密码: password123
        
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, role, created_at, updated_at)
            VALUES (%s, %s, %s, %s, NOW(), NOW())
            RETURNING id
        """, ("test_user", "test@example.com", password_hash, "student"))
        
        user_id = cursor.fetchone()[0]
        conn.commit()
        
        print(f"✅ 测试用户创建成功！")
        print(f"   用户名: test_user")
        print(f"   密码: password123")
        print(f"   邮箱: test@example.com")
        print(f"   角色: student")
        print(f"   用户ID: {user_id}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建测试用户失败: {e}")
        return False

if __name__ == "__main__":
    create_test_user()