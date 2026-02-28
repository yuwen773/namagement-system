"""
创建反馈测试数据脚本
生成20条2026年的反馈数据
"""
import os
import sys
import django
import random
from datetime import datetime, timedelta

# 设置Django环境
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_project.settings')
django.setup()

from apps.feedbacks.models import Feedback
from apps.accounts.models import User

# 反馈数据模板
FEEDBACK_TEMPLATES = [
    {
        'title': '希望增加数据导出功能',
        'content': '建议在数据中心增加导出Excel和CSV的功能，方便我们进行离线数据分析。',
        'type': 'feature'
    },
    {
        'title': '数据统计图表加载缓慢',
        'content': '在查看数据趋势图表时，页面加载时间超过5秒，希望优化加载速度。',
        'type': 'bug'
    },
    {
        'title': '建议添加关键词订阅功能',
        'content': '希望能够订阅特定关键词，当有新的相关问答时自动推送通知。',
        'type': 'feature'
    },
    {
        'title': '移动端适配问题',
        'content': '在手机上浏览页面时，部分表格显示不全，需要左右滑动才能查看完整内容。',
        'type': 'bug'
    },
    {
        'title': '增加数据对比功能',
        'content': '希望能够选择两个时间段的数据进行对比分析，这样可以更直观地看到数据变化趋势。',
        'type': 'feature'
    },
    {
        'title': '搜索结果不准确',
        'content': '搜索"人工智能"相关的问答时，返回了很多不相关的结果，建议优化搜索算法。',
        'type': 'bug'
    },
    {
        'title': '建议添加夜间模式',
        'content': '长时间使用系统对眼睛负担较重，希望能够添加深色模式的夜间主题。',
        'type': 'feature'
    },
    {
        'title': '登录状态异常退出',
        'content': '在使用过程中，经常会被意外退出登录，需要重新登录，影响使用体验。',
        'type': 'bug'
    },
    {
        'title': '希望支持批量操作',
        'content': '数据管理页面希望支持批量删除和批量修改状态的功能，提高操作效率。',
        'type': 'feature'
    },
    {
        'title': '数据更新不及时',
        'content': '问答数据更新频率较低，希望能够增加数据采集的频率，保持数据新鲜度。',
        'type': 'other'
    },
    {
        'title': '建议添加数据分享功能',
        'content': '希望能够将感兴趣的数据分享给团队成员，或者生成分享链接对外分享。',
        'type': 'feature'
    },
    {
        'title': '页面布局混乱',
        'content': '在1440x900分辨率下，公告管理页面的表格列宽显示不合理，内容被截断。',
        'type': 'bug'
    },
    {
        'title': '希望增加数据预警功能',
        'content': '建议设置数据阈值，当某些指标超过或低于设定值时发送预警通知。',
        'type': 'feature'
    },
    {
        'title': '用户权限管理不够细致',
        'content': '希望能够设置更细致的权限控制，比如只能查看特定分类的数据。',
        'type': 'feature'
    },
    {
        'title': '导出文件中文乱码',
        'content': '从数据中心导出的CSV文件在Excel中打开时中文显示为乱码，需要修复。',
        'type': 'bug'
    },
    {
        'title': '建议增加操作日志',
        'content': '希望能够查看自己的操作历史记录，方便追溯之前做过的事情。',
        'type': 'feature'
    },
    {
        'title': '系统响应时间变慢',
        'content': '近期系统整体响应速度明显变慢，尤其是在高峰时段，请检查服务器性能。',
        'type': 'bug'
    },
    {
        'title': '希望支持自定义仪表盘',
        'content': '建议允许用户自定义首页仪表盘的布局和显示内容，个性化展示常用数据。',
        'type': 'feature'
    },
    {
        'title': '数据同步延迟',
        'content': '爬虫采集的数据有时候需要等待很久才能在系统中看到，同步机制需要优化。',
        'type': 'bug'
    },
    {
        'title': '建议增加帮助文档',
        'content': '系统功能较多，新手不太容易上手，建议添加详细的帮助文档和使用教程。',
        'type': 'feature'
    }
]

# 状态分布
STATUS_CHOICES = ['pending', 'processing', 'resolved', 'ignored']
STATUS_WEIGHTS = [0.4, 0.25, 0.25, 0.1]  # 待处理40%，处理中25%，已完成25%，已忽略10%

def generate_2026_dates(count=20):
    """生成2026年的日期"""
    # 2026年1月1日到2026年12月31日
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 12, 31)

    # 计算总秒数
    total_seconds = int((end_date - start_date).total_seconds())

    # 生成随机日期，确保按时间倒序排列（最新的在前）
    random_dates = []
    for _ in range(count):
        random_seconds = random.randint(0, total_seconds)
        random_date = start_date + timedelta(seconds=random_seconds)
        random_dates.append(random_date)

    # 按日期倒序排列
    return sorted(random_dates, reverse=True)

def create_feedback_data():
    """创建反馈测试数据"""
    # 获取所有用户
    users = User.objects.all()
    if not users.exists():
        print("错误：数据库中没有用户，请先创建用户！")
        return

    print(f"找到 {users.count()} 个用户")
    print("开始创建反馈数据...")

    # 清空现有的反馈数据（可选）
    # Feedback.objects.all().delete()
    # print("已清空现有反馈数据")

    created_count = 0
    dates = generate_2026_dates(20)

    # 首先创建所有反馈对象（不保存）
    feedbacks_to_create = []
    admin_users_list = list(users.filter(role='admin'))

    for i, template in enumerate(FEEDBACK_TEMPLATES):
        user = random.choice(users)
        status = random.choices(STATUS_CHOICES, weights=STATUS_WEIGHTS, k=1)[0]

        feedback = Feedback(
            title=template['title'],
            content=template['content'],
            feedback_type=template['type'],
            status=status,
            user=user,
            created_at=dates[i],
            updated_at=dates[i]
        )

        # 如果状态是"已完成"或"已忽略"，随机添加管理员回复
        if status in ['resolved', 'ignored'] and random.random() > 0.3 and admin_users_list:
            replied_by = random.choice(admin_users_list)
            reply_delay = timedelta(hours=random.randint(1, 72))
            replied_at = dates[i] + reply_delay

            replies = [
                '感谢您的反馈，我们已经处理了这个问题。',
                '收到您的建议，已在开发计划中安排。',
                '这个问题已经修复，请刷新页面重试。',
                '您的建议非常有价值，我们会在下个版本中考虑。',
                '感谢您的反馈，我们会持续优化系统性能。',
                '这是一个很好的建议，已转发给产品团队评估。',
                '问题已定位，正在修复中。',
                '该功能已在开发中，预计下月上线。'
            ]

            feedback.admin_reply = random.choice(replies)
            feedback.replied_at = replied_at
            feedback.replied_by = replied_by

        feedbacks_to_create.append(feedback)

    # 批量创建（绕过auto_now_add）
    Feedback.objects.bulk_create(feedbacks_to_create, ignore_conflicts=True)

    # 由于bulk_create后auto_now_add仍然会触发，需要手动更新时间戳
    # 重新获取所有反馈并更新时间
    all_feedbacks = list(Feedback.objects.all().order_by('id'))
    for i, feedback in enumerate(all_feedbacks):
        feedback.created_at = dates[i]
        feedback.updated_at = dates[i]
        feedback.save()

    for i, feedback in enumerate(feedbacks_to_create):
        print(f"[{i+1}/20] 创建反馈: {feedback.title[:30]}... ({feedback.status})")

    created_count = len(feedbacks_to_create)

    print(f"\n成功创建 {created_count} 条反馈数据")
    print(f"  - 功能建议: {Feedback.objects.filter(feedback_type='feature').count()} 条")
    print(f"  - Bug反馈: {Feedback.objects.filter(feedback_type='bug').count()} 条")
    print(f"  - 其他: {Feedback.objects.filter(feedback_type='other').count()} 条")
    print(f"  - 待处理: {Feedback.objects.filter(status='pending').count()} 条")
    print(f"  - 处理中: {Feedback.objects.filter(status='processing').count()} 条")
    print(f"  - 已完成: {Feedback.objects.filter(status='resolved').count()} 条")
    print(f"  - 已忽略: {Feedback.objects.filter(status='ignored').count()} 条")

if __name__ == '__main__':
    create_feedback_data()
