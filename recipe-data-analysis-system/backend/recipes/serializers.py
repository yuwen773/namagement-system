"""
菜谱模块 - 序列化器定义

本模块定义菜谱相关的序列化器，包括：
- RecipeSerializer: 菜谱基本信息序列化器
- RecipeListSerializer: 菜谱列表序列化器
- RecipeImageUploadSerializer: 菜谱图片上传序列化器
"""
from rest_framework import serializers
from .models import Recipe, RecipeIngredient
from ingredients.models import Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    """
    菜谱基本信息序列化器

    用于菜谱的详情展示和创建/更新操作
    """

    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'cuisine_type', 'scene_type', 'target_audience',
            'difficulty', 'cooking_time', 'image_url', 'steps', 'flavor_tags',
            'view_count', 'favorite_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'view_count', 'favorite_count', 'created_at', 'updated_at']


class RecipeListSerializer(serializers.ModelSerializer):
    """
    菜谱列表序列化器

    用于菜谱列表的展示，包含较少字段以提升性能
    """

    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'cuisine_type', 'scene_type', 'difficulty',
            'cooking_time', 'image_url', 'flavor_tags', 'view_count',
            'favorite_count', 'created_at', 'target_audience', 'steps',
            'ingredients'
        ]

    ingredients = serializers.SerializerMethodField()

    def get_ingredients(self, obj):
        """获取食材列表"""
        ingredients = obj.recipe_ingredients.all()
        return RecipeIngredientSerializer(ingredients, many=True).data


class RecipeImageUploadSerializer(serializers.Serializer):
    """
    菜谱图片上传序列化器

    用于验证图片上传请求
    """

    image = serializers.ImageField(
        help_text='图片文件，支持 jpg、jpeg、png、webp 格式',
        allow_empty_file=False,
        required=True
    )

    def validate_image(self, value):
        """
        验证图片文件

        Args:
            value: 上传的图片文件

        Returns:
            ImageField: 验证后的图片文件

        Raises:
            ValidationError: 图片格式或大小不符合要求
        """
        # 检查文件大小（Django 默认限制 2.5MB，约 2621440 字节）
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError('图片大小不能超过 5MB')

        # 检查文件扩展名
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        import os
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError('仅支持 jpg、jpeg、png、webp 格式的图片')

        return value


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    菜谱食材关联序列化器

    用于展示菜谱的食材列表
    """

    ingredient_name = serializers.CharField(source='ingredient.name', read_only=True)

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'ingredient_name', 'amount', 'sort_order']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """
    菜谱详情序列化器

    继承自 RecipeSerializer，增加食材列表等详细信息
    """

    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        many=True,
        read_only=True
    )
    flavor_list = serializers.ListField(
        source='get_flavor_list',
        read_only=True
    )

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['ingredients', 'flavor_list']


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    菜谱创建序列化器（管理员专用）

    用于创建新菜谱，支持食材关联
    """

    # 食材列表： [{"ingredient_id": 1, "amount": "200g", "sort_order": 1}, ...]
    ingredients = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        help_text='食材列表，每项包含 ingredient_id、amount、sort_order'
    )

    class Meta:
        model = Recipe
        fields = [
            'name', 'cuisine_type', 'scene_type', 'target_audience',
            'difficulty', 'cooking_time', 'image_url', 'steps', 'flavor_tags',
            'ingredients'
        ]

    def validate_name(self, value):
        """验证菜谱名称"""
        if not value or not value.strip():
            raise serializers.ValidationError('菜谱名称不能为空')
        return value.strip()

    def validate_difficulty(self, value):
        """验证难度等级"""
        valid_choices = ['easy', 'medium', 'hard']
        if value and value not in valid_choices:
            raise serializers.ValidationError(f'难度等级必须是以下之一：{", ".join(valid_choices)}')
        return value

    def validate_cooking_time(self, value):
        """验证烹饪时长"""
        if value is not None and value < 0:
            raise serializers.ValidationError('烹饪时长不能为负数')
        return value

    def validate_ingredients(self, value):
        """验证食材列表"""
        if not value:
            return value

        for idx, item in enumerate(value):
            if 'ingredient_id' not in item:
                raise serializers.ValidationError(f'食材列表第 {idx + 1} 项缺少 ingredient_id 字段')

            # 验证食材是否存在
            try:
                Ingredient.objects.get(id=item['ingredient_id'])
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    f'食材列表第 {idx + 1} 项：食材 ID {item["ingredient_id"]} 不存在'
                )

        return value

    def create(self, validated_data):
        """
        创建菜谱及其食材关联

        Args:
            validated_data: 验证后的数据

        Returns:
            Recipe: 创建的菜谱对象
        """
        from django.db import transaction

        # 提取食材数据
        ingredients_data = validated_data.pop('ingredients', [])

        # 使用事务确保数据一致性
        with transaction.atomic():
            # 创建菜谱
            recipe = Recipe.objects.create(**validated_data)

            # 创建食材关联
            if ingredients_data:
                recipe_ingredients = []
                for item in ingredients_data:
                    recipe_ingredients.append(
                        RecipeIngredient(
                            recipe=recipe,
                            ingredient_id=item['ingredient_id'],
                            amount=item.get('amount', ''),
                            sort_order=item.get('sort_order', 0)
                        )
                    )
                RecipeIngredient.objects.bulk_create(recipe_ingredients)

        return recipe


class RecipeUpdateSerializer(serializers.ModelSerializer):
    """
    菜谱更新序列化器（管理员专用）

    用于更新菜谱信息，支持食材关联更新
    """

    # 食材列表： [{"ingredient_id": 1, "amount": "200g", "sort_order": 1}, ...]
    ingredients = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        help_text='食材列表，每项包含 ingredient_id、amount、sort_order'
    )

    class Meta:
        model = Recipe
        fields = [
            'name', 'cuisine_type', 'scene_type', 'target_audience',
            'difficulty', 'cooking_time', 'image_url', 'steps', 'flavor_tags',
            'ingredients'
        ]

    def validate_name(self, value):
        """验证菜谱名称"""
        if value is not None and not value.strip():
            raise serializers.ValidationError('菜谱名称不能为空')
        return value.strip() if value else value

    def validate_difficulty(self, value):
        """验证难度等级"""
        if value is not None:
            valid_choices = ['easy', 'medium', 'hard']
            if value not in valid_choices:
                raise serializers.ValidationError(f'难度等级必须是以下之一：{", ".join(valid_choices)}')
        return value

    def validate_cooking_time(self, value):
        """验证烹饪时长"""
        if value is not None and value < 0:
            raise serializers.ValidationError('烹饪时长不能为负数')
        return value

    def validate_ingredients(self, value):
        """验证食材列表"""
        if not value:
            return value

        for idx, item in enumerate(value):
            if 'ingredient_id' not in item:
                raise serializers.ValidationError(f'食材列表第 {idx + 1} 项缺少 ingredient_id 字段')

            # 验证食材是否存在
            try:
                Ingredient.objects.get(id=item['ingredient_id'])
            except Ingredient.DoesNotExist:
                raise serializers.ValidationError(
                    f'食材列表第 {idx + 1} 项：食材 ID {item["ingredient_id"]} 不存在'
                )

        return value

    def update(self, instance, validated_data):
        """
        更新菜谱及其食材关联

        Args:
            instance: 要更新的菜谱实例
            validated_data: 验证后的数据

        Returns:
            Recipe: 更新后的菜谱对象
        """
        from django.db import transaction

        # 提取食材数据
        ingredients_data = validated_data.pop('ingredients', None)

        # 使用事务确保数据一致性
        with transaction.atomic():
            # 更新菜谱基本信息
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # 如果提供了食材数据，则更新食材关联
            if ingredients_data is not None:
                # 删除旧的食材关联
                instance.recipe_ingredients.all().delete()

                # 创建新的食材关联
                if ingredients_data:
                    recipe_ingredients = []
                    for item in ingredients_data:
                        recipe_ingredients.append(
                            RecipeIngredient(
                                recipe=instance,
                                ingredient_id=item['ingredient_id'],
                                amount=item.get('amount', ''),
                                sort_order=item.get('sort_order', 0)
                            )
                        )
                    RecipeIngredient.objects.bulk_create(recipe_ingredients)

        return instance
