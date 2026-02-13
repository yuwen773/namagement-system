import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourist.settings')
django.setup()

from attractions.models import Attraction

# 检查精确匹配的景点
print('=== 精确匹配景点 ===')
for name in ['故宫', '长城', '西湖', '黄山', '九寨沟']:
    try:
        a = Attraction.objects.get(name=name, is_deleted=False)
        print(f'{name}: {a.cover_image[:60]}...')
        print(f'  images: {len(a.images)} 张')
    except Attraction.DoesNotExist:
        print(f'{name}: 未找到')

# 检查类别匹配的景点
print('\n=== 类别匹配景点 ===')
a = Attraction.objects.filter(category='自然风光', is_deleted=False).exclude(cover_image='').first()
if a:
    print(f'自然风光示例: {a.name}')
    print(f'  cover: {a.cover_image[:60]}...')
    print(f'  images: {len(a.images)} 张')

a = Attraction.objects.filter(category='人文古迹', is_deleted=False).exclude(cover_image='').first()
if a:
    print(f'人文古迹示例: {a.name}')
    print(f'  cover: {a.cover_image[:60]}...')

a = Attraction.objects.filter(category='主题乐园', is_deleted=False).exclude(cover_image='').first()
if a:
    print(f'主题乐园示例: {a.name}')
    print(f'  cover: {a.cover_image[:60]}...')

# 统计
print('\n=== 统计 ===')
total = Attraction.objects.filter(is_deleted=False).count()
with_cover = Attraction.objects.filter(is_deleted=False).exclude(cover_image='').count()
print(f'总景点: {total}')
print(f'有封面图: {with_cover}')
