import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourist.settings')
django.setup()

from attractions.models import Attraction

total = Attraction.objects.filter(is_deleted=False).count()
print(f'景点总数: {total}')

names = list(Attraction.objects.filter(is_deleted=False).values_list('name', flat=True))
print(f'\n所有景点名称 ({len(names)}个):')
for i, name in enumerate(names, 1):
    print(f'{i}. {name}')
