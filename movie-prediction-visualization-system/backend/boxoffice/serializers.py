from rest_framework import serializers
from django.utils import timezone
from .models import BoxOfficeRecord


class BoxOfficeRecordSerializer(serializers.ModelSerializer):
    """票房记录序列化器"""
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
    """票房记录创建序列化器"""

    class Meta:
        model = BoxOfficeRecord
        fields = ['movie', 'cinema', 'record_date', 'daily_box_office', 'screening_count', 'audience_count']

    def validate(self, attrs):
        """验证数据"""
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
        """创建票房记录并更新影片累计票房"""
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
    """票房记录更新序列化器"""

    class Meta:
        model = BoxOfficeRecord
        fields = ['daily_box_office', 'screening_count', 'audience_count']

    def validate_daily_box_office(self, value):
        if value < 0:
            raise serializers.ValidationError('票房金额必须大于0')
        return value

    def update(self, instance, validated_data):
        """更新票房记录并更新影片累计票房"""
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
    """票房统计序列化器"""
    total_box_office = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_screening_count = serializers.IntegerField()
    total_audience_count = serializers.IntegerField()
    record_count = serializers.IntegerField()
