# Generated manually for employee unassigned placeholder data

from django.db import migrations


def create_unassigned_placeholder(apps, schema_editor):
    """创建待分配部门和岗位占位数据"""
    Department = apps.get_model('organization', 'Department')
    Post = apps.get_model('organization', 'Post')

    # 创建待分配部门
    unassigned_dept, _ = Department.objects.get_or_create(
        code='UNASSIGNED',
        defaults={
            'name': '待分配部门',
            'parent': None,
            'is_active': True,
            'sort_order': 999
        }
    )

    # 创建待分配岗位
    Post.objects.get_or_create(
        code='UNASSIGNED',
        defaults={
            'name': '待分配岗位',
            'department': unassigned_dept,
            'is_active': True,
            'sort_order': 999
        }
    )


def rollback_unassigned_placeholder(apps, schema_editor):
    """回滚：删除占位数据"""
    Department = apps.get_model('organization', 'Department')
    Post = apps.get_model('organization', 'Post')

    Post.objects.filter(code='UNASSIGNED').delete()
    Department.objects.filter(code='UNASSIGNED').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('employee', '0001_initial'),
        ('organization', '0002_post'),
    ]

    operations = [
        migrations.RunPython(create_unassigned_placeholder, rollback_unassigned_placeholder)
    ]
