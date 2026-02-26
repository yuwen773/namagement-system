#!/usr/bin/env python
"""
传承人数据导入脚本

使用方法:
    python scripts/import_inheritors.py <csv_file_path> [--commit] [--default-country=China]

示例:
    # 预览导入（不提交到数据库）
    python scripts/import_inheritors.py dataSource/inheritors_sample.csv
    
    # 正式导入
    python scripts/import_inheritors.py dataSource/inheritors_sample.csv --commit
"""
import argparse
import sys
from pathlib import Path

# 添加backend目录到Python路径
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "heritage_system.settings")
django.setup()

from apps.importer.services import OfflineImporterService


def main():
    parser = argparse.ArgumentParser(description="导入传承人数据")
    parser.add_argument("file_path", help="CSV文件路径")
    parser.add_argument(
        "--commit",
        action="store_true",
        help="提交到数据库（默认为预览模式）",
    )
    parser.add_argument(
        "--default-country",
        default="China",
        help="默认国家（默认: China）",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="批量处理大小（默认: 100）",
    )
    
    args = parser.parse_args()
    
    file_path = Path(args.file_path)
    if not file_path.exists():
        print(f"错误: 文件不存在 - {file_path}")
        sys.exit(1)
    
    print(f"{'='*80}")
    print(f"传承人数据导入")
    print(f"{'='*80}")
    print(f"文件: {file_path}")
    print(f"模式: {'正式导入' if args.commit else '预览模式（不会写入数据库）'}")
    print(f"默认国家: {args.default_country}")
    print(f"{'='*80}\n")
    
    try:
        service = OfflineImporterService(
            file_path=file_path,
            dataset_type="inheritor",
            commit=args.commit,
            default_country=args.default_country,
            batch_size=args.batch_size,
        )
        
        result = service.run()
        
        print(f"\n{'='*80}")
        print(f"导入结果")
        print(f"{'='*80}")
        print(f"总行数: {result.total_rows}")
        print(f"成功: {result.success_count}")
        print(f"失败: {result.error_count}")
        print(f"新建: {result.created_count}")
        print(f"更新: {result.updated_count}")
        
        if result.error_report:
            print(f"\n错误报告已保存到: {result.error_report}")
        
        if not args.commit:
            print(f"\n提示: 这是预览模式，数据未写入数据库")
            print(f"      使用 --commit 参数进行正式导入")
        
        print(f"{'='*80}\n")
        
        sys.exit(0 if result.error_count == 0 else 1)
        
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
