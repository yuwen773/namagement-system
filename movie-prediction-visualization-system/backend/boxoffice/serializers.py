from rest_framework import serializers
from django.utils import timezone
from .models import BoxOfficeRecord


class BoxOfficeRecordSerializer(serializers.ModelSerializer):
    """
    票房记录序列化器

    用于序列化票房记录的完整信息，包含关联的影片、影院和地域信息。
    主要用于查询和展示票房记录详情。

    Fields:
        id: 票房记录ID
        movie: 关联影片ID
        movie_title: 影片名称（只读）
        cinema: 关联影院ID
        cinema_name: 影院名称（只读）
        region_name: 地域名称（只读）
        record_date: 记录日期
        daily_box_office: 日票房（元）
        screening_count: 场次
        audience_count: 人次
        created_at: 创建时间
    """
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    cinema_name = serializers.CharField(source='cinema.name', read_only=True)
    region_name = serializers.CharField(source='cinema.region.name', read_only=True)

    class Meta:
        model = BoxOfficeRecord
        fields = [
            'id', 'movie', 'movie_title', 'cinema', 'cinema_name',
            'region_name', 'record_date', 'daily_box_office',
            'screening_count', 'audience_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class BoxOfficeRecordCreateSerializer(serializers.ModelSerializer):
    """
    票房记录创建序列化器

    用于创建新的票房记录，包含数据验证逻辑：
    - 验证记录日期不早于影片上映日期
    - 验证票房金额必须为非负数
    - 创建成功后自动更新影片的累计票房

    Fields:
        movie: 关联影片ID（必填）
        cinema: 关联影院ID（必填）
        record_date: 记录日期（必填）
        daily_box_office: 日票房（元，必填）
        screening_count: 场次（可选）
        audience_count: 人次（可选）
    """

    class Meta:
        model = BoxOfficeRecord
        fields = ['movie', 'cinema', 'record_date', 'daily_box_office', 'screening_count', 'audience_count']

    def validate(self, attrs):
        """
        验证票房记录数据

        验证规则：
        - 记录日期不能早于影片上映日期
        - 票房金额必须大于等于0

        Args:
            attrs: 待验证的字段字典

        Returns:
            dict: 验证通过的字段字典

        Raises:
            ValidationError: 当验证失败时
        """
        movie = attrs.get('movie')
        record_date = attrs.get('record_date')
        daily_box_office = attrs.get('daily_box_office', 0)

        # 验证日期不早于上映日期
        if movie and movie.release_date and record_date:
            if record_date < movie.release_date:
                raise serializers.ValidationError({
                    'record_date': f'记录日期不能早于影片上映日期 ({movie.release_date})'
                })

        # 验证票房金额
        if daily_box_office < 0:
            raise serializers.ValidationError({
                'daily_box_office': '票房金额必须大于0'
            })

        return attrs

    def create(self, validated_data):
        """
        创建票房记录并更新影片累计票房

        创建流程：
        1. 创建票房记录
        2. 重新计算该影片的累计票房（所有记录的总和）
        3. 将累计票房转换为万元单位并更新到影片信息

        Args:
            validated_data: 验证通过的字段数据

        Returns:
            BoxOfficeRecord: 创建的票房记录实例
        """
        record = BoxOfficeRecord.objects.create(**validated_data)

        # 更新影片累计票房
        movie = validated_data.get('movie')
        if movie:
            total = BoxOfficeRecord.objects.filter(movie=movie).aggregate(
                total=sum('daily_box_office')
            )['total'] or 0
            movie.box_office_total = total / 10000  # 转换为万元
            movie.save()

        return record


class BoxOfficeRecordUpdateSerializer(serializers.ModelSerializer):
    """
    票房记录更新序列化器

    用于更新已有票房记录的部分字段（票房、场次、人次）。
    不允许修改关联的影片、影院和记录日期，保证数据的一致性。
    更新成功后自动更新影片的累计票房。

    Fields:
        daily_box_office: 日票房（元）
        screening_count: 场次
        audience_count: 人次
    """

    class Meta:
        model = BoxOfficeRecord
        fields = ['daily_box_office', 'screening_count', 'audience_count']

    def validate_daily_box_office(self, value):
        """
        验证票房金额

        Args:
            value: 待验证的票房金额

        Returns:
            decimal.Decimal: 验证通过后的票房金额

        Raises:
            ValidationError: 当票房金额为负数时
        """
        if value < 0:
            raise serializers.ValidationError('票房金额必须大于0')
        return value

    def update(self, instance, validated_data):
        """
        更新票房记录并更新影片累计票房

        更新流程：
        1. 更新票房记录的字段
        2. 重新计算该影片的累计票房（所有记录的总和）
        3. 将累计票房转换为万元单位并更新到影片信息

        Args:
            instance: 待更新的票房记录实例
            validated_data: 验证通过的字段数据

        Returns:
            BoxOfficeRecord: 更新后的票房记录实例
        """
        instance = super().update(instance, validated_data)

        # 更新影片累计票房
        movie = instance.movie
        total = BoxOfficeRecord.objects.filter(movie=movie).aggregate(
            total=sum('daily_box_office')
        )['total'] or 0
        movie.box_office_total = total / 10000  # 转换为万元
        movie.save()

        return instance


class BoxOfficeStatsSerializer(serializers.Serializer):
    """
    票房统计序列化器

    用于序列化票房统计数据，提供票房汇总信息。
    通常用于统计视图返回聚合结果。

    Fields:
        total_box_office: 总票房（元）
        total_screening_count: 总场次
        total_audience_count: 总人次
        record_count: 记录数量
    """
    total_box_office = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_screening_count = serializers.IntegerField()
    total_audience_count = serializers.IntegerField()
    record_count = serializers.IntegerField()


class BoxOfficeBatchInputSerializer(serializers.Serializer):
    """
    票房批量录入序列化器

    用于验证批量录入票房记录的请求数据格式。
    要求每次提交1-100条记录，每条记录必须包含必填字段。

    Fields:
        records: 票房记录列表，每条记录为字典格式
    """
    records = serializers.ListField(
        child=serializers.DictField(),
        min_length=1,
        max_length=100,
        help_text='票房记录列表，每次最多100条'
    )

    def validate_records(self, value):
        """
        验证批量录入的数据

        验证每条记录是否包含所有必填字段：
        - movie: 影片ID
        - cinema: 影院ID
        - record_date: 记录日期
        - daily_box_office: 日票房

        Args:
            value: 待验证的记录列表

        Returns:
            list: 验证通过后的记录列表

        Raises:
            ValidationError: 当记录缺少必填字段时
        """
        required_fields = ['movie', 'cinema', 'record_date', 'daily_box_office']
        for idx, record in enumerate(value):
            missing_fields = [f for f in required_fields if f not in record]
            if missing_fields:
                raise serializers.ValidationError(
                    f'第 {idx + 1} 条记录缺少必填字段: {", ".join(missing_fields)}'
                )
        return value


class BoxOfficeBatchInputRecordSerializer(serializers.ModelSerializer):
    """
    单条票房记录序列化器（用于批量录入）

    在批量录入时验证每条票房记录的数据完整性和正确性。
    包含与创建序列化器相同的验证逻辑。

    Fields:
        movie: 关联影片ID（必填）
        cinema: 关联影院ID（必填）
        record_date: 记录日期（必填）
        daily_box_office: 日票房（元，必填）
        screening_count: 场次（可选）
        audience_count: 人次（可选）
    """

    class Meta:
        model = BoxOfficeRecord
        fields = ['movie', 'cinema', 'record_date', 'daily_box_office', 'screening_count', 'audience_count']

    def validate(self, attrs):
        """
        验证票房记录数据

        验证规则：
        - 记录日期不能早于影片上映日期
        - 票房金额必须大于等于0

        Args:
            attrs: 待验证的字段字典

        Returns:
            dict: 验证通过的字段字典

        Raises:
            ValidationError: 当验证失败时
        """
        movie = attrs.get('movie')
        record_date = attrs.get('record_date')
        daily_box_office = attrs.get('daily_box_office', 0)

        # 验证日期不早于上映日期
        if movie and movie.release_date and record_date:
            if record_date < movie.release_date:
                raise serializers.ValidationError({
                    'record_date': f'记录日期不能早于影片上映日期 ({movie.release_date})'
                })

        # 验证票房金额
        if daily_box_office < 0:
            raise serializers.ValidationError({
                'daily_box_office': '票房金额必须大于0'
            })

        return attrs
