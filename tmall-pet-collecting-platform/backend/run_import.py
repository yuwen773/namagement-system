#!/usr/bin/env python
"""
便捷数据导入脚本 - 直接运行即可导入data目录下所有CSV文件

使用方法:
    python run_import.py              # 导入所有CSV
    python run_import.py --dir path   # 指定目录
    python run_import.py --dry-run    # 试运行
"""
import os
import sys
import django

# 设置Django环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tmall_project.settings')
django.setup()

from django.core.management import call_command


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='CSV数据导入工具')
    parser.add_argument('--dir', type=str, help='CSV文件目录')
    parser.add_argument('--batch-size', type=int, default=100, help='批量大小')
    parser.add_argument('--dry-run', action='store_true', help='试运行模式')

    args = parser.parse_args()

    # 调用Django管理命令
    kwargs = {
        'batch_size': args.batch_size,
        'dry_run': args.dry_run
    }

    if args.dir:
        kwargs['dir'] = args.dir

    print("🚀 开始导入CSV数据...")
    call_command('import_csv', **kwargs)


if __name__ == '__main__':
    main()
