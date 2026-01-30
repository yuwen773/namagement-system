"""
数据库连接测试脚本

用于诊断 MySQL 数据库连接问题。
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_mysql_connection():
    """测试 MySQL 数据库连接"""
    print("=" * 60)
    print("数据库连接测试")
    print("=" * 60)

    # 显示当前配置
    print("\n当前数据库配置:")
    print(f"  数据库名: {os.getenv('DB_NAME', 'recipe_analysis_db')}")
    print(f"  用户名: {os.getenv('DB_USER', 'root')}")
    print(f"  密码: {'*' * len(os.getenv('DB_PASSWORD', ''))}")
    print(f"  主机: {os.getenv('DB_HOST', 'localhost')}")
    print(f"  端口: {os.getenv('DB_PORT', '3306')}")

    try:
        import pymysql

        print("\n正在尝试连接数据库...")

        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'recipe_analysis_db'),
            charset='utf8mb4'
        )

        print("✅ 数据库连接成功!")

        # 检查数据库版本
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"   MySQL 版本: {version[0]}")

            # 检查数据库表
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"   当前表数量: {len(tables)}")
            if tables:
                print("   已存在的表:")
                for table in tables:
                    print(f"     - {table[0]}")

        connection.close()

    except ImportError:
        print("❌ PyMySQL 未安装")
        print("   请运行: pip install PyMySQL")

    except pymysql.err.OperationalError as e:
        error_code = e.args[0]
        error_msg = e.args[1]

        print(f"❌ 数据库连接失败 (错误代码: {error_code})")

        if error_code == 1045:
            print("\n可能的原因:")
            print("  1. MySQL 密码不正确")
            print("  2. 用户 'root' 没有访问权限")
            print("\n解决方法:")
            print("  - 检查 .env 文件中的 DB_PASSWORD 设置")
            print("  - 确保 MySQL 服务正在运行")
            print("  - 尝试使用以下命令重置 root 密码:")
            print("    mysql -u root -p")
            print("    ALTER USER 'root'@'localhost' IDENTIFIED BY '你的密码';")
            print("    FLUSH PRIVILEGES;")

        elif error_code == 2002:
            print("\n可能的原因:")
            print("  1. MySQL 服务未启动")
            print("  2. 端口号不正确")
            print("\n解决方法:")
            print("  - 检查 MySQL 服务是否启动")
            print("  - Windows: 在服务中查找 'MySQL' 服务")
            print("  - Linux: sudo systemctl start mysql")

        elif error_code == 1049:
            print("\n可能的原因:")
            print("  1. 数据库不存在")
            print("\n解决方法:")
            print("  - 创建数据库:")
            print(f"    CREATE DATABASE {os.getenv('DB_NAME', 'recipe_analysis_db')} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

        print(f"\n详细错误信息: {error_msg}")

    except Exception as e:
        print(f"❌ 发生未知错误: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_mysql_connection()
