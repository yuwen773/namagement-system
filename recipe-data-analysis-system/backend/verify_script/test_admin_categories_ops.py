
import os
import sys
import json
import django

# Windows console fix
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)
django.setup()

from django.test import Client
from accounts.models import User
from categories.models import Category
from utils.constants import UserRole

def cleanup():
    User.objects.filter(username='test_admin_cat').delete()
    Category.objects.filter(name='TestCategory').delete()
    Category.objects.filter(name='UpdatedTestCategory').delete()

def run_test():
    cleanup()
    
    # 1. Create Admin User
    print("Creating admin user...")
    admin_user = User.objects.create_user(
        username='test_admin_cat',
        email='admin@test.com',
        password='Password123',
        role=UserRole.ADMIN
    )
    admin_user.is_active = True
    admin_user.save()
    
    # 2. Login
    client = Client()
    print("Logging in...")
    resp = client.post('/api/accounts/login/', 
        data=json.dumps({'username': 'test_admin_cat', 'password': 'Password123'}),
        content_type='application/json'
    )
    if resp.status_code != 200:
        print(f"Login failed: {resp.content}")
        return
    token = resp.json()['data']['token']
    headers = {'HTTP_AUTHORIZATION': f'Bearer {token}'}
    
    # 3. Create Category
    print("Testing Create Category...")
    resp = client.post('/api/admin/categories/create/',
        data=json.dumps({
            'name': 'TestCategory',
            'type': 'cuisine',
            'sort_order': 99
        }),
        content_type='application/json',
        **headers
    )
    if resp.status_code not in [200, 201]:
        print(f"Create failed: {resp.content}")
        return
    cat_id = resp.json()['data']['id']
    print(f"Category created with ID: {cat_id}")
    
    # 4. List Categories
    print("Testing List Categories...")
    resp = client.get('/api/admin/categories/?type=cuisine', **headers)
    if resp.status_code != 200:
        print(f"List failed: {resp.content}")
        return
    cats = resp.json()['data']['results']
    found = False
    for c in cats:
        if c['id'] == cat_id:
            found = True
            break
    if not found:
        print("Created category not found in list")
        return
    print("Category found in list")
    
    # 5. Update Category
    print("Testing Update Category...")
    resp = client.put(f'/api/admin/categories/{cat_id}/update/',
        data=json.dumps({
            'name': 'UpdatedTestCategory',
            'type': 'cuisine',
            'sort_order': 100
        }),
        content_type='application/json',
        **headers
    )
    if resp.status_code != 200:
        print(f"Update failed: {resp.content}")
        return
    print("Category updated")
    
    # 6. Delete Category
    print("Testing Delete Category...")
    resp = client.delete(f'/api/admin/categories/{cat_id}/delete/', **headers)
    if resp.status_code != 200:
        print(f"Delete failed: {resp.content}")
        return
    print("Category deleted")
    
    # Verify deletion
    resp = client.get(f'/api/admin/categories/?type=cuisine', **headers)
    cats = resp.json()['data']['results']
    for c in cats:
        if c['id'] == cat_id:
            print("Category still exists after delete!")
            return
    print("Category deletion verified")
    
    cleanup()
    print("All tests passed!")

if __name__ == '__main__':
    run_test()
