from rest_framework import serializers
from django.utils import timezone
from .models import MovieType, Movie


class MovieTypeSerializer(serializers.ModelSerializer):
    """
    影片类型序列化器（用于列表和详情展示）

    字段说明：
    - id: 类型ID
    - name: 类型名称
    - movie_count: 该类型下的影片数量（动态计算）
    - created_at: 创建时间

    用于影片类型的列表查询和详情展示，包含影片数量统计。
    """
    movie_count = serializers.SerializerMethodField(
        help_text='该类型下的影片数量'
    )

    class Meta:
        model = MovieType
        fields = ['id', 'name', 'description', 'movie_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_movie_count(self, obj):
        """
        获取该类型下的影片数量

        Args:
            obj: MovieType 实例

        Returns:
            int: 影片数量
        """
        return obj.movies.count()


class MovieTypeCreateSerializer(serializers.ModelSerializer):
    """
    影片类型创建序列化器

    字段说明：
    - id: 类型ID（自动生成）
    - name: 类型名称

    用于创建新的影片类型，字段简洁，仅包含必要信息。
    """

    class Meta:
        model = MovieType
        fields = ['id', 'name']
        read_only_fields = ['id']


class MovieSerializer(serializers.ModelSerializer):
    """
    影片序列化器（包含完整信息）

    字段说明：
    - id: 影片ID
    - title: 影片标题
    - director: 导演
    - actors: 演员
    - release_date: 上映日期
    - duration: 片长（分钟）
    - type: 类型ID
    - type_name: 类型名称（从关联对象获取）
    - poster_url: 海报URL
    - description: 剧情简介
    - box_office_total: 累计票房（只读）
    - status: 状态（RELEASED-已上映, COMING-即将上映）
    - created_at: 创建时间（只读）
    - updated_at: 更新时间（只读）

    用于影片详情展示，包含所有字段信息和关联的类型名称。
    """
    type_name = serializers.CharField(
        source='type.name',
        read_only=True,
        allow_null=True,
        help_text='类型名称（从关联对象获取）'
    )

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'director', 'actors', 'release_date', 'duration',
            'type', 'type_name', 'poster_url', 'description', 'box_office_total',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'box_office_total', 'created_at', 'updated_at']


class MovieListSerializer(serializers.ModelSerializer):
    """
    影片列表序列化器（精简版）

    字段说明：
    - id: 影片ID
    - title: 影片标题
    - director: 导演
    - actors: 主演
    - type: 类型ID
    - type_name: 类型名称（从关联对象获取）
    - release_date: 上映日期
    - duration: 片长（分钟）
    - box_office_total: 累计票房
    - status: 状态（RELEASED-已上映, COMING-即将上映）

    用于影片列表展示，包含核心字段，支持编辑功能。
    """
    type_name = serializers.CharField(
        source='type.name',
        read_only=True,
        allow_null=True,
        help_text='类型名称（从关联对象获取）'
    )

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'director', 'actors', 'type', 'type_name',
            'release_date', 'duration', 'box_office_total', 'status'
        ]


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    """
    影片创建/更新序列化器

    字段说明：
    - title: 影片标题（必填，唯一）
    - director: 导演
    - actors: 演员
    - release_date: 上映日期（必填，不能早于今天）
    - duration: 片长（分钟，必填，1-1000之间）
    - type: 类型ID（必填）
    - poster_url: 海报URL（可选，需为有效URL）
    - description: 剧情简介
    - status: 状态（RELEASED-已上映, COMING-即将上映）

    用于创建和更新影片，仅包含可编辑字段，不包含只读字段如票房、时间戳等。
    """

    class Meta:
        model = Movie
        fields = [
            'title', 'director', 'actors', 'release_date', 'duration',
            'type', 'poster_url', 'description', 'status'
        ]

    def validate_title(self, value):
        """
        验证影片名称唯一性

        Args:
            value: 影片名称

        Returns:
            str: 验证通过后的影片名称

        Raises:
            ValidationError: 当影片名称已存在时
        """
        # 获取当前实例（用于更新时排除自身）
        instance = getattr(self, 'instance', None)

        # 检查是否已存在同名影片
        queryset = Movie.objects.filter(title__iexact=value)
        if instance and instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

        if queryset.exists():
            raise serializers.ValidationError('影片名称已存在')

        return value

    def validate_duration(self, value):
        """
        验证片长范围

        Args:
            value: 片长（分钟）

        Returns:
            int: 验证通过后的片长

        Raises:
            ValidationError: 当片长不在1-1000分钟范围内时
        """
        if value < 1 or value > 1000:
            raise serializers.ValidationError('片长必须在1-1000分钟之间')
        return value

    def validate_release_date(self, value):
        """
        验证上映日期

        Args:
            value: 上映日期

        Returns:
            date: 验证通过后的上映日期

        Raises:
            ValidationError: 当上映日期早于今天时
        """
        from django.utils import timezone
        today = timezone.now().date()

        if value < today:
            raise serializers.ValidationError(f'上映日期不能早于今天 ({today})')

        return value

    def validate_poster_url(self, value):
        """
        验证海报URL格式

        Args:
            value: 海报URL

        Returns:
            str: 验证通过后的海报URL

        Raises:
            ValidationError: 当URL格式不正确时
        """
        if value:
            from django.core.validators import URLValidator
            from django.core.exceptions import ValidationError as DjangoValidationError

            validator = URLValidator()
            try:
                validator(value)
            except DjangoValidationError:
                raise serializers.ValidationError('海报URL格式不正确')

        return value
