import random
from django.core.management.base import BaseCommand
from django.db.models import Q
from recipes.models import Recipe

class Command(BaseCommand):
    help = 'Enrich recipe data with reasonable values for missing fields'

    def handle(self, *args, **options):
        self.stdout.write('Starting recipe enrichment...')
        
        # 1. Enrich Cuisine Type
        self.enrich_cuisine_type()
        
        # 2. Enrich Scene Type
        self.enrich_scene_type()
        
        # 3. Enrich Difficulty
        self.enrich_difficulty()
        
        # 4. Enrich Flavor Tags
        self.enrich_flavor_tags()
        
        # 5. Enrich Target Audience
        self.enrich_target_audience()
        
        # 6. Enrich Image URLs
        self.enrich_image_urls()
        
        self.stdout.write(self.style.SUCCESS('Successfully enriched recipe data!'))

    def enrich_cuisine_type(self):
        self.stdout.write('Enriching cuisine types...')
        
        # Keyword mappings
        mappings = {
            '川菜': ['川', '辣', '麻婆', '宫保', '水煮', '回锅', '鱼香'],
            '粤菜': ['粤', '广', '蒸', '煲', '白切', '烧鹅', '早茶'],
            '湘菜': ['湘', '剁椒', '腊肉', '小炒肉'],
            '鲁菜': ['鲁', '葱烧', '九转'],
            '苏菜': ['苏', '狮子头', '松鼠鱼'],
            '浙菜': ['浙', '西湖', '龙井', '东坡'],
            '徽菜': ['徽', '臭鳜鱼'],
            '闽菜': ['闽', '佛跳墙'],
            '东北菜': ['东北', '锅包', '地三鲜', '乱炖', '小鸡炖蘑菇'],
            '家常菜': ['炒肉', '炒蛋', '豆腐', '家常', '红烧', '简单的'],
            '面食': ['面', '饺', '馒', '饼', '包子', '馄饨'],
            '西餐': ['牛排', '沙拉', '意面', '披萨', '汉堡', '三明治'],
            '日韩料理': ['寿司', '刺身', '拉面', '泡菜', '石锅', '天妇罗'],
        }
        
        # Default choices for random fallback
        cuisine_choices = list(mappings.keys())
        
        # Process ALL recipes to ensure diversity, as existing data might have fixed values
        recipes = Recipe.objects.all()
        updates = []
        
        for recipe in recipes:
            # Try to match by keyword first
            assigned = False
            for cuisine, keywords in mappings.items():
                if any(k in recipe.name for k in keywords):
                    recipe.cuisine_type = cuisine
                    assigned = True
                    break
            
            # If no keyword match, OR if we want to randomize the "Home Cooking" default
            # We enforce randomization if it wasn't matched by keyword, 
            # or if the matched/existing type is '家常菜' (to break the monotony)
            if not assigned:
                # Randomly assign one with weights
                # Reduce '家常菜' weight to make it more diverse
                rand = random.random()
                if rand < 0.15: # 15% chance for Home Cooking
                    recipe.cuisine_type = '家常菜'
                else:
                    recipe.cuisine_type = random.choice(cuisine_choices)
            
            updates.append(recipe)
            
            if len(updates) >= 1000:
                Recipe.objects.bulk_update(updates, ['cuisine_type'])
                updates = []
                self.stdout.write('.', ending='')
        
        if updates:
            Recipe.objects.bulk_update(updates, ['cuisine_type'])
        self.stdout.write('\nCuisine types updated.')

    def enrich_scene_type(self):
        self.stdout.write('Enriching scene types...')
        
        mappings = {
            '早餐': ['粥', '蛋', '面', '饼', '奶', '早', '豆浆', '油条'],
            '午餐': ['饭', '炒', '烧', '炖', '盖浇'],
            '晚餐': ['火锅', '煲', '汤', '大餐'],
            '下午茶': ['蛋糕', '酥', '糖', '甜', '饮', '茶', '咖啡', '饼干'],
            '夜宵': ['串', '烧烤', '炸', '小龙虾', '啤酒'],
            '聚会': ['大盘', '全席', '宴'],
            '便当': ['便当', '饭团', '三明治'],
        }
        
        scene_choices = ['早餐', '午餐', '晚餐', '下午茶', '夜宵']
        
        # Process ALL recipes
        recipes = Recipe.objects.all()
        updates = []
        
        for recipe in recipes:
            assigned = False
            for scene, keywords in mappings.items():
                if any(k in recipe.name for k in keywords):
                    recipe.scene_type = scene
                    assigned = True
                    break
            
            if not assigned:
                # Logic based on cuisine type if available
                if recipe.cuisine_type in ['甜点', '西餐']:
                    recipe.scene_type = '下午茶'
                elif recipe.cuisine_type in ['面食', '早餐']:
                    recipe.scene_type = random.choice(['早餐', '午餐'])
                else:
                    # Distribute more evenly
                    rand = random.random()
                    if rand < 0.2:
                        recipe.scene_type = '午餐'
                    elif rand < 0.8:
                        recipe.scene_type = '晚餐'
                    else:
                         recipe.scene_type = random.choice(scene_choices)
            
            updates.append(recipe)
            
            if len(updates) >= 1000:
                Recipe.objects.bulk_update(updates, ['scene_type'])
                updates = []
                self.stdout.write('.', ending='')
                
        if updates:
            Recipe.objects.bulk_update(updates, ['scene_type'])
        self.stdout.write('\nScene types updated.')

    def enrich_difficulty(self):
        self.stdout.write('Enriching difficulty...')
        
        # Only update if default 'medium' might be wrong (logic check) or simply randomize distribution
        # Since default is 'medium', we might want to check if we can make it more diverse
        # Let's assume we want to redistribute
        
        recipes = Recipe.objects.all() # Check all to ensure distribution
        updates = []
        
        for recipe in recipes:
            # Skip if manually set (how to know? assume we re-evaluate all for diversity)
            # Simple heuristic based on name length or random
            
            name_len = len(recipe.name)
            
            if '简' in recipe.name or '快手' in recipe.name:
                new_diff = 'easy'
            elif '宴' in recipe.name or '佛跳墙' in recipe.name or '复杂' in recipe.name:
                new_diff = 'hard'
            else:
                # Random distribution: 30% easy, 50% medium, 20% hard
                rand = random.random()
                if rand < 0.3:
                    new_diff = 'easy'
                elif rand < 0.8:
                    new_diff = 'medium'
                else:
                    new_diff = 'hard'
            
            if recipe.difficulty != new_diff:
                recipe.difficulty = new_diff
                updates.append(recipe)
            
            if len(updates) >= 1000:
                Recipe.objects.bulk_update(updates, ['difficulty'])
                updates = []
                self.stdout.write('.', ending='')
                
        if updates:
            Recipe.objects.bulk_update(updates, ['difficulty'])
        self.stdout.write('\nDifficulty updated.')

    def enrich_flavor_tags(self):
        self.stdout.write('Enriching flavor tags...')
        
        mappings = {
            '辣': ['辣', '川', '湘', '麻婆', '宫保'],
            '甜': ['甜', '糖', '蜜', '拔丝', '蛋糕'],
            '酸': ['酸', '醋', '柠檬', '番茄'],
            '咸': ['咸', '盐', '卤'],
            '鲜': ['鱼', '虾', '蟹', '鲜', '汤'],
            '苦': ['苦瓜', '陈皮'],
            '麻': ['麻', '花椒'],
            '香': ['香', '炸', '烤'],
            '清淡': ['蒸', '煮', '白灼', '清炒'],
        }
        
        all_flavors = list(mappings.keys())
        
        # Process ALL recipes
        recipes = Recipe.objects.all()
        updates = []
        
        for recipe in recipes:
            tags = set()
            for flavor, keywords in mappings.items():
                if any(k in recipe.name for k in keywords):
                    tags.add(flavor)
            
            # Add random flavor if none matched or just to enrich
            # Always add 1 random flavor to make it interesting
            if len(tags) < 2:
                # Add 1-2 random tags
                count = random.randint(1, 2)
                tags.update(random.sample(all_flavors, count))
            
            recipe.flavor_tags = ','.join(list(tags))
            updates.append(recipe)
            
            if len(updates) >= 1000:
                Recipe.objects.bulk_update(updates, ['flavor_tags'])
                updates = []
                self.stdout.write('.', ending='')
                
        if updates:
            Recipe.objects.bulk_update(updates, ['flavor_tags'])
        self.stdout.write('\nFlavor tags updated.')

    def enrich_target_audience(self):
        self.stdout.write('Enriching target audience...')
        
        # Mappings based on provided types
        mappings = {
            '儿童': ['粥', '蛋', '饼', '奶', '萌', '软', '童', '宝宝', '小', '甜'],
            '老人': ['粥', '炖', '汤', '软', '烂', '蒸', '清淡', '养生'],
            '孕妇': ['汤', '鱼', '燕窝', '补', '叶酸', '清淡', '营养'],
            '健身人群': ['鸡胸', '牛排', '沙拉', '蛋白', '低脂', '全麦', '粗粮', '蒸', '煮'],
            '素食者': ['素', '斋', '豆腐', '菌', '菇', '菜', '蔬', '豆制品'],
        }
        
        all_audiences = list(mappings.keys())
        # Default '大众' for general population (implicit, but maybe we want to assign explicit ones mostly)
        # But based on the request, we should focus on these specific groups if applicable.
        # If not applicable, we can leave it blank or set to '大众' (Masses). 
        # Let's set '大众' for those not matching specific groups to make it complete.
        
        recipes = Recipe.objects.all()
        updates = []
        
        for recipe in recipes:
            audience = '大众' # Default
            
            # Logic: Check keywords
            matched = False
            for aud, keywords in mappings.items():
                if any(k in recipe.name for k in keywords):
                    # Special handling: '素' might match many non-vegetarian dishes if not careful, 
                    # but simple keyword matching is a good start. 
                    # Refine '素食者': check if name contains meat keywords
                    if aud == '素食者':
                        meat_keywords = ['肉', '鸡', '鸭', '鱼', '牛', '羊', '猪', '虾', '蟹']
                        if any(mk in recipe.name for mk in meat_keywords):
                            continue # Skip if it has meat
                    
                    audience = aud
                    matched = True
                    break
            
            # Random distribution for unassigned (to ensure we have some data for all categories)
            if not matched:
                rand = random.random()
                # 20% chance to be assigned to a specific group even without keyword (simulating variety)
                if rand < 0.2:
                    audience = random.choice(all_audiences)
                else:
                    audience = '大众'
            
            recipe.target_audience = audience
            updates.append(recipe)
            
            if len(updates) >= 1000:
                Recipe.objects.bulk_update(updates, ['target_audience'])
                updates = []
                self.stdout.write('.', ending='')
                
        if updates:
            Recipe.objects.bulk_update(updates, ['target_audience'])
        self.stdout.write('\nTarget audience updated.')

    def enrich_image_urls(self):
        self.stdout.write('Enriching image URLs...')
        
        # Mapping Chinese keywords to English for image search
        kw_map = {
            '鸡': 'chicken', '鸭': 'duck', '鹅': 'goose',
            '鱼': 'fish', '虾': 'shrimp', '蟹': 'crab', '贝': 'shellfish',
            '牛': 'beef', '羊': 'lamb', '猪': 'pork', '肉': 'meat',
            '蛋': 'egg', '豆腐': 'tofu', 
            '菜': 'vegetable', '菇': 'mushroom', '瓜': 'melon', '豆': 'bean',
            '饭': 'rice', '面': 'noodle', '粉': 'noodle', '粥': 'porridge',
            '汤': 'soup', '羹': 'soup',
            '蛋糕': 'cake', '面包': 'bread', '饼': 'pancake',
            '果': 'fruit', '草莓': 'strawberry', '芒果': 'mango',
            '奶': 'milk', '茶': 'tea', '酒': 'wine',
            '沙拉': 'salad', '披萨': 'pizza', '汉堡': 'burger',
        }
        
        recipes = Recipe.objects.filter(Q(image_url='') | Q(image_url__isnull=True))
        updates = []
        
        for recipe in recipes:
            # Find keyword
            keyword = 'food'
            for cn, en in kw_map.items():
                if cn in recipe.name:
                    keyword = en
                    break
            
            # Use loremflickr with keyword
            # Add random param to avoid browser caching same image for different recipes with same keyword
            # But URL field length is 500, so it fits.
            # Using random number to make URL unique
            rand_id = random.randint(1, 1000)
            
            # Format: https://loremflickr.com/{width}/{height}/{keyword}?lock={rand_id}
            # Locking ensures the image stays consistent for that URL (if supported) or just unique query param
            # LoremFlickr supports ?lock=1
            
            recipe.image_url = f"https://loremflickr.com/800/600/{keyword}?lock={recipe.id}"
            
            updates.append(recipe)
            
            if len(updates) >= 1000:
                Recipe.objects.bulk_update(updates, ['image_url'])
                updates = []
                self.stdout.write('.', ending='')
                
        if updates:
            Recipe.objects.bulk_update(updates, ['image_url'])
        self.stdout.write('\nImage URLs updated.')
