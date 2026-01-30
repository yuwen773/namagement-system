"""
Simple test to debug the recipe list API
"""

import os
import sys

# 设置控制台编码为 UTF-8 (Windows 兼容)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目路径到 sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.test import RequestFactory
from recipes.views import recipe_list
from recipes.models import Recipe

# Create a request
factory = RequestFactory()

print("=" * 60)
print("Simple Recipe List API Test")
print("=" * 60)

# Check database
recipe_count = Recipe.objects.count()
print(f"Recipe count in database: {recipe_count}")

# Test the view directly
request = factory.get('/api/recipes/')
print(f"\nRequest URL: {request.path}")
print(f"Request method: {request.method}")

try:
    response = recipe_list(request)
    print(f"\nResponse status code: {response.status_code}")
    print(f"Response type: {type(response)}")

    # Try to get the response data
    if hasattr(response, 'data'):
        print(f"Response data: {response.data}")
    else:
        print(f"Response content: {response.content[:200]}")

except Exception as e:
    print(f"\nError occurred: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
