"""
数据库迁移脚本 - 添加 mtop API 新字段
使用方法: python scripts/migrate_database.py
"""
import os
import sys
import django
from datetime import datetime

# 设置 Django 环境
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')
django.setup()

from django.db import connection
import django.db.migrations.operations as ops


def check_current_fields():
    """检查当前数据库字段"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'tmall_collecting'
            AND TABLE_NAME = 'products'
        """)
        current_fields = [row[0] for row in cursor.fetchall()]
        return current_fields


def migrate_database(auto_confirm=False):
    """执行数据库迁移"""
    print("=" * 60)
    print("数据库迁移 - 添加 mtop API 新字段")
    print("=" * 60)

    # 新增字段列表
    new_fields = [
        ("product_id", "VARCHAR(100)", "天猫商品ID"),
        ("price_unit", "VARCHAR(20)", "价格单位"),
        ("price_desc", "VARCHAR(200)", "价格描述"),
        ("seller_nick", "VARCHAR(100)", "卖家昵称"),
        ("shop_tags", "VARCHAR(500)", "店铺标签"),
        ("region", "VARCHAR(100)", "地区"),
        ("tags", "VARCHAR(500)", "商品标签"),
        ("product_attributes", "JSON", "商品属性"),
    ]

    # 索引列表
    new_indexes = [
        ("idx_product_id", "product_id"),
        ("idx_region", "region"),
    ]

    # 检查当前字段
    print("\n1. 检查当前数据库字段...")
    current_fields = check_current_fields()
    print(f"   当前字段数: {len(current_fields)}")

    # 确定需要添加的字段
    fields_to_add = []
    for field_name, field_type, comment in new_fields:
        if field_name not in current_fields:
            fields_to_add.append((field_name, field_type, comment))

    if not fields_to_add:
        print("   [OK] 所有新字段已存在，无需迁移")
        return True

    print(f"   需要添加 {len(fields_to_add)} 个新字段")

    # 确认执行
    print("\n即将添加以下字段:")
    for field_name, field_type, comment in fields_to_add:
        print(f"   - {field_name}: {field_type} ({comment})")

    if not auto_confirm:
        try:
            confirm = input("\n是否继续? (y/n): ").lower()
            if confirm != 'y':
                print("已取消迁移")
                return False
        except (EOFError, KeyboardInterrupt):
            print("\n检测到非交互式环境，使用自动确认模式")
            auto_confirm = True

    if auto_confirm:
        print("\n自动确认模式，开始迁移...")

    # 执行迁移
    print("\n2. 执行数据库迁移...")
    with connection.cursor() as cursor:
        try:
            # 添加字段
            for field_name, field_type, comment in fields_to_add:
                # 确定字段位置
                after_clause = ""
                if field_name == "product_id":
                    after_clause = "AFTER id"
                elif field_name == "price_unit":
                    after_clause = "AFTER price"
                elif field_name == "price_desc":
                    after_clause = "AFTER price_unit"
                elif field_name == "seller_nick":
                    after_clause = "AFTER shop"
                elif field_name == "shop_tags":
                    after_clause = "AFTER seller_nick"
                elif field_name == "region":
                    after_clause = "AFTER sales"
                elif field_name == "tags":
                    after_clause = "AFTER region"
                elif field_name == "product_attributes":
                    after_clause = "AFTER tags"

                sql = f"""
                    ALTER TABLE products
                    ADD COLUMN {field_name} {field_type} NULL COMMENT '{comment}'
                    {after_clause}
                """
                cursor.execute(sql)
                print(f"   [OK] 添加字段: {field_name}")

            # 添加索引
            for index_name, column_name in new_indexes:
                # 检查索引是否已存在
                cursor.execute(f"""
                    SELECT COUNT(*)
                    FROM INFORMATION_SCHEMA.STATISTICS
                    WHERE TABLE_SCHEMA = 'tmall_collecting'
                    AND TABLE_NAME = 'products'
                    AND INDEX_NAME = '{index_name}'
                """)
                if cursor.fetchone()[0] == 0:
                    sql = f"CREATE INDEX {index_name} ON products({column_name})"
                    cursor.execute(sql)
                    print(f"   [OK] 添加索引: {index_name} ({column_name})")

            # 为现有数据生成 product_id
            cursor.execute("""
                UPDATE products
                SET product_id = CONCAT('legacy_', id)
                WHERE product_id IS NULL
            """)
            updated = cursor.rowcount
            if updated > 0:
                print(f"   [OK] 更新现有数据 product_id: {updated} 条")

            connection.commit()
            print("\n[OK] 迁移成功完成!")

        except Exception as e:
            connection.rollback()
            print(f"\n[ERROR] 迁移失败: {e}")
            return False

    # 验证迁移
    print("\n3. 验证迁移结果...")
    new_fields_list = check_current_fields()
    missing = [f[0] for f in fields_to_add if f[0] not in new_fields_list]

    if missing:
        print(f"   [ERROR] 缺少字段: {missing}")
        return False

    print("   [OK] 所有字段都已正确添加")

    # 显示统计
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM products")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM products WHERE product_id IS NOT NULL")
        with_id = cursor.fetchone()[0]

    print(f"\n数据库统计:")
    print(f"   总商品数: {total}")
    print(f"   有 product_id: {with_id}")

    print("\n" + "=" * 60)
    print("迁移完成!")
    print("=" * 60)

    return True


def rollback_migration():
    """回滚迁移"""
    print("=" * 60)
    print("回滚数据库迁移")
    print("=" * 60)

    fields_to_remove = [
        "product_attributes", "tags", "region", "shop_tags",
        "seller_nick", "price_desc", "price_unit", "product_id"
    ]

    indexes_to_remove = ["idx_product_id", "idx_region"]

    confirm = input(f"\n确定要删除 {len(fields_to_remove)} 个字段? (yes/no): ")
    if confirm.lower() != 'yes':
        print("已取消回滚")
        return False

    print("\n执行回滚...")
    with connection.cursor() as cursor:
        try:
            # 删除索引
            for index_name in indexes_to_remove:
                cursor.execute(f"DROP INDEX IF EXISTS {index_name} ON products")
                print(f"   [OK] 删除索引: {index_name}")

            # 删除字段
            for field_name in fields_to_remove:
                cursor.execute(f"ALTER TABLE products DROP COLUMN {field_name}")
                print(f"   [OK] 删除字段: {field_name}")

            connection.commit()
            print("\n[OK] 回滚完成!")

        except Exception as e:
            connection.rollback()
            print(f"\n[ERROR] 回滚失败: {e}")
            return False

    return True


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='数据库迁移工具')
    parser.add_argument('--rollback', action='store_true', help='回滚迁移')
    parser.add_argument('--yes', '-y', action='store_true', help='自动确认所有提示')
    args = parser.parse_args()

    try:
        if args.rollback:
            rollback_migration()
        else:
            migrate_database(auto_confirm=args.yes)
    except KeyboardInterrupt:
        print("\n\n操作已中断")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
