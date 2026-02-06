import os
import sys
import django
import json

# Setup Django environment
sys.path.append(os.path.join(os.getcwd(), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category, Product
from apps.products.serializers import CategoryTreeSerializer

def check_category_data():
    # 1. Get a product with a category
    try:
        product = Product.objects.filter(category__isnull=False).first()
        if not product:
            print("No products with category found.")
            return
        
        print(f"Product ID: {product.id}")
        print(f"Product Name: {product.name}")
        print(f"Product Category ID: {product.category_id}")
        print(f"Product Category Name: {product.category.name}")
        
        # 2. Get the category tree
        root_categories = Category.objects.filter(parent__isnull=True, is_active=True)
        serializer = CategoryTreeSerializer(root_categories, many=True)
        tree_data = serializer.data
        
        # 3. Search for the category ID in the tree
        def find_in_tree(nodes, target_id):
            for node in nodes:
                if node['id'] == target_id:
                    return True
                if node.get('children'):
                    if find_in_tree(node['children'], target_id):
                        return True
            return False

        found = find_in_tree(tree_data, product.category_id)
        print(f"Category ID {product.category_id} found in tree: {found}")
        
        # 4. Check data types
        if tree_data:
            print(f"Tree ID type: {type(tree_data[0]['id'])}")
        print(f"Product Category ID type: {type(product.category_id)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_category_data()
