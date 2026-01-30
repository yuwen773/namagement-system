# -*- coding: utf-8 -*-
"""
数据清洗脚本测试

测试各种清洗场景：
1. 正常数据清洗
2. 重复数据检测
3. 缺失字段补全
4. 格式标准化
5. 无效数据过滤
"""

import os
import sys
import json
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from clean_recipes import RecipeCleaner, load_input_file, save_output_file


def create_test_data():
    """创建测试数据"""
    return [
        # 正常数据
        {
            'recipe_id': 1,
            'name': '宫保鸡丁',
            'cuisine_type': '川菜',
            'scene_type': '晚餐',
            'difficulty': 'medium',
            'cooking_time': 30,
            'flavor_tags': ['辣', '甜'],
            'image_url': 'https://example.com/image1.jpg',
            'ingredients': [
                {'name': '鸡肉', 'amount': '300g'},
                {'name': '花生', 'amount': '50g'}
            ],
            'steps': ['1. 鸡肉切丁', '2. 爆炒鸡肉', '3. 加入调料'],
            'view_count': 1000,
            'favorite_count': 100
        },
        # 重复数据（相同名称）
        {
            'recipe_id': 2,
            'name': '宫保鸡丁',  # 与上面重复
            'cuisine_type': '川菜',
            'difficulty': 'medium',
            'ingredients': [{'name': '鸡肉', 'amount': '300g'}],
            'steps': ['步骤1', '步骤2']
        },
        # 缺失字段
        {
            'recipe_id': 3,
            'name': '  清炒时蔬  ',  # 有多余空格
            # 缺少 cuisine_type
            # 缺少 scene_type
            'difficulty': '简单',  # 需要标准化
            'cooking_time': '约20分钟',  # 需要提取数字
            'flavor_tags': '辣,甜,酸',  # 字符串格式
            'ingredients': '时蔬 300g\n盐 适量',  # 字符串格式
            'steps': '1. 洗净时蔬\n2. 热锅炒制\n3. 调味出锅'
        },
        # 无效数据（缺少名称）
        {
            'recipe_id': 4,
            # name': '应该缺少',
            'cuisine_type': '粤菜',
            'difficulty': 'medium',
            'ingredients': [{'name': '虾', 'amount': '200g'}],
            'steps': ['步骤1']
        },
        # 无效数据（缺少食材）
        {
            'recipe_id': 5,
            'name': '清蒸鱼',
            'cuisine_type': '粤菜',
            'difficulty': 'medium',
            'ingredients': [],
            'steps': ['步骤1']
        },
        # 格式需要标准化
        {
            'recipe_id': 6,
            'name': '红烧肉',
            'cuisine_type': '家常菜',  # 不在标准菜系列表
            'scene_type': '午餐',
            'difficulty': '困难',  # 中文
            'cooking_time': 45,
            'flavor_tags': ['咸', '麻', '特辣'],  # '特辣' 不在标准列表
            'image_url': 'invalid-url',  # 无效 URL
            'ingredients': [
                {'name': '五花肉', 'amount': '500克'},
                {'name': '冰糖', 'amount': '2勺'}
            ],
            'steps': [
                '五花肉切块',  # 缺少编号
                '焯水去腥',
                '炒糖色',
                '炖煮收汁'
            ]
        },
        # 另一个正常数据
        {
            'recipe_id': 7,
            'name': '西红柿炒鸡蛋',
            'cuisine_type': '家常菜',
            'scene_type': '晚餐',
            'difficulty': 'easy',
            'cooking_time': 15,
            'flavor_tags': ['鲜'],
            'image_url': 'https://example.com/image2.jpg',
            'ingredients': [
                {'name': '鸡蛋', 'amount': '3个'},
                {'name': '西红柿', 'amount': '2个'}
            ],
            'steps': ['1. 鸡蛋打散', '2. 西红柿切块', '3. 炒制'],
            'view_count': 5000,
            'favorite_count': 800
        },
        # recipe_id 重复
        {
            'recipe_id': 1,  # 与第一条重复
            'name': '不同的菜谱',
            'cuisine_type': '鲁菜',
            'difficulty': 'medium',
            'ingredients': [{'name': '牛肉', 'amount': '300g'}],
            'steps': ['步骤1', '步骤2']
        }
    ]


def run_test():
    """运行测试"""
    print("=" * 60)
    print("数据清洗脚本测试")
    print("=" * 60)

    # 创建测试数据
    test_data = create_test_data()
    print(f"\n创建 {len(test_data)} 条测试数据")

    # 保存测试数据到文件
    test_input_path = Path(__file__).parent.parent / 'output' / 'test_input.json'
    test_input_path.parent.mkdir(parents=True, exist_ok=True)

    with open(test_input_path, 'w', encoding='utf-8') as f:
        json.dump({'recipes': test_data}, f, ensure_ascii=False, indent=2)
    print(f"测试数据已保存到: {test_input_path}")

    # 加载测试数据
    print("\n加载测试数据...")
    loaded_data = load_input_file(str(test_input_path))
    print(f"成功加载 {len(loaded_data)} 条记录")

    # 创建清洗器
    cleaner = RecipeCleaner()

    # 清洗数据
    print("\n开始清洗数据...")
    cleaned_data = cleaner.clean_recipes(loaded_data)

    # 打印报告
    cleaner.print_report()

    # 保存结果
    test_output_path = Path(__file__).parent.parent / 'output' / 'test_cleaned_output.json'
    report = cleaner.get_report_dict()
    save_output_file(cleaned_data, str(test_output_path), report)

    # 验证结果
    print("\n" + "=" * 60)
    print("验证结果")
    print("=" * 60)

    print(f"\n原始数据: {len(test_data)} 条")
    print(f"清洗后数据: {len(cleaned_data)} 条")
    print(f"去除重复: {cleaner.stats.duplicates_removed} 条")
    print(f"无效记录: {cleaner.stats.invalid_records_removed} 条")

    # 显示清洗后的数据
    print("\n清洗后的数据:")
    for i, recipe in enumerate(cleaned_data, 1):
        print(f"\n{i}. {recipe['name']}")
        print(f"   ID: {recipe.get('recipe_id', 'N/A')}")
        print(f"   菜系: {recipe['cuisine_type']}")
        print(f"   场景: {recipe['scene_type']}")
        print(f"   难度: {recipe['difficulty']}")
        print(f"   时长: {recipe['cooking_time']} 分钟")
        print(f"   口味: {', '.join(recipe['flavor_tags'])}")
        print(f"   食材数: {len(recipe['ingredients'])}")
        print(f"   步骤数: {len(recipe['steps'])}")

    # 验证预期结果
    print("\n" + "=" * 60)
    print("预期验证")
    print("=" * 60)

    checks = []

    # 1. 检查去重
    names = [r['name'] for r in cleaned_data]
    duplicate_names = [name for name in names if names.count(name) > 1]
    checks.append(('去重检测', len(duplicate_names) == 0, f"重复菜谱: {duplicate_names if duplicate_names else '无'}"))

    # 2. 检查必填字段
    all_have_name = all(r.get('name') for r in cleaned_data)
    all_have_ingredients = all(r.get('ingredients') for r in cleaned_data)
    all_have_steps = all(r.get('steps') for r in cleaned_data)
    checks.append(('必填字段', all_have_name and all_have_ingredients and all_have_steps,
                   f"名称: {all_have_name}, 食材: {all_have_ingredients}, 步骤: {all_have_steps}"))

    # 3. 检查难度标准化
    all_valid_difficulty = all(r.get('difficulty') in ['easy', 'medium', 'hard'] for r in cleaned_data)
    checks.append(('难度标准化', all_valid_difficulty,
                   f"所有难度都是有效值: {all_valid_difficulty}"))

    # 4. 检查烹饪时间格式
    all_valid_time = all(isinstance(r.get('cooking_time'), int) for r in cleaned_data)
    checks.append(('时间格式', all_valid_time,
                   f"所有时间都是整数: {all_valid_time}"))

    # 5. 检查食材格式
    all_valid_ingredients = all(
        all(isinstance(ing, dict) and 'name' in ing for ing in r.get('ingredients', []))
        for r in cleaned_data
    )
    checks.append(('食材格式', all_valid_ingredients,
                   f"所有食材都是字典格式: {all_valid_ingredients}"))

    # 打印验证结果
    for check_name, passed, detail in checks:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status} - {check_name}: {detail}")

    # 总体结果
    all_passed = all(check[1] for check in checks)
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败，请检查")
    print("=" * 60)

    return all_passed


def main():
    """主函数"""
    try:
        success = run_test()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
