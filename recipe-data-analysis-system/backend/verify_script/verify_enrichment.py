import os
import sys
import django
from django.db.models import Count

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from recipes.models import Recipe

def verify():
    print("===== Verification of Recipe Enrichment =====")
    
    # 1. Check random samples
    print("\n--- Random Samples (5) ---")
    samples = Recipe.objects.order_by('?')[:5]
    for r in samples:
        print(f"ID: {r.id}")
        print(f"Name: {r.name}")
        print(f"Cuisine: {r.cuisine_type}")
        print(f"Scene: {r.scene_type}")
        print(f"Difficulty: {r.difficulty}")
        print(f"Flavors: {r.flavor_tags}")
        print(f"Image: {r.image_url}")
        print("-" * 30)

    # 2. Check Distributions
    print("\n--- Distribution: Cuisine Type ---")
    cuisines = Recipe.objects.values('cuisine_type').annotate(count=Count('id')).order_by('-count')
    for c in cuisines[:10]:
        print(f"{c['cuisine_type']}: {c['count']}")

    print("\n--- Distribution: Scene Type ---")
    scenes = Recipe.objects.values('scene_type').annotate(count=Count('id')).order_by('-count')
    for s in scenes:
        print(f"{s['scene_type']}: {s['count']}")
        
    print("\n--- Distribution: Difficulty ---")
    diffs = Recipe.objects.values('difficulty').annotate(count=Count('id')).order_by('-count')
    for d in diffs:
        print(f"{d['difficulty']}: {d['count']}")

    print("\n--- Distribution: Target Audience ---")
    audiences = Recipe.objects.values('target_audience').annotate(count=Count('id')).order_by('-count')
    for a in audiences:
        print(f"{a['target_audience']}: {a['count']}")

    # 3. Check Image URL Coverage
    empty_imgs = Recipe.objects.filter(image_url='').count()
    print(f"\nEmpty Image URLs: {empty_imgs}")

if __name__ == '__main__':
    verify()
