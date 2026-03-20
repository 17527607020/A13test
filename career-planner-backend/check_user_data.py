import psycopg2

def check_user_data():
    """检查用户数据"""
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
        
        # 查询用户数据
        cursor.execute("""
            SELECT id, username, email, role, created_at 
            FROM users 
            WHERE username = 'test_user'
        """)
        user = cursor.fetchone()
        
        if user:
            print(f"用户数据:")
            print(f"  ID: {user[0]}")
            print(f"  用户名: {user[1]}")
            print(f"  邮箱: {user[2]}")
            print(f"  角色: {user[3]}")
            print(f"  创建时间: {user[4]}")
            print(f"  创建时间类型: {type(user[4])}")
        else:
            print("未找到用户数据")
        
        # 查询所有用户
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"\n总用户数: {count}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"查询用户数据失败: {e}")

if __name__ == "__main__":
    check_user_data()