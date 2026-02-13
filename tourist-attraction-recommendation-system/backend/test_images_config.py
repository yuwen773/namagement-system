import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourist.settings')
django.setup()

from attractions.images_config import ATTRACTION_IMAGES, CATEGORY_DEFAULT_IMAGES, get_category_default_images

print('景点配置数:', len(ATTRACTION_IMAGES))
print('类别配置数:', len(CATEGORY_DEFAULT_IMAGES))
print('测试获取类别图片:', get_category_default_images('自然风光')['cover'][:50])
print('测试获取人文古迹:', get_category_default_images('人文古迹')['cover'][:50])
print('测试未知类别:', get_category_default_images('未知类别')['cover'][:50])
