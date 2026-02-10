from rest_framework import serializers


class MovieBoxOfficeSerializer(serializers.Serializer):
    """
    影片票房排行序列化器

    用于序列化票房总榜 Top 10 影片数据。
    包含影片基本信息和累计票房数据，用于排行榜展示。
    """
    id = serializers.IntegerField(help_text='影片ID')
    title = serializers.CharField(help_text='影片名称')
    box_office_total = serializers.DecimalField(max_digits=15, decimal_places=2, help_text='累计票房总额（元）')
    release_date = serializers.DateField(allow_null=True, help_text='上映日期')


class DailyBoxOfficeSerializer(serializers.Serializer):
    """
    每日票房序列化器

    用于序列化每日大盘票房统计数据。
    包含日期、总票房、总场次和总人次，用于大盘走势展示。
    """
    date = serializers.DateField(help_text='统计日期')
    total_box_office = serializers.DecimalField(max_digits=15, decimal_places=2, help_text='当日票房总额（元）')
    total_screening_count = serializers.IntegerField(help_text='当日总放映场次')
    total_audience_count = serializers.IntegerField(help_text='当日总观影人次')


class TypeBoxOfficeSerializer(serializers.Serializer):
    """
    类型票房占比序列化器

    用于序列化各影片类型的票房分布数据。
    包含类型信息、票房总额和占比百分比，用于类型分布饼图或柱状图展示。
    """
    type_id = serializers.IntegerField(allow_null=True, help_text='影片类型ID')
    type_name = serializers.CharField(help_text='影片类型名称')
    box_office = serializers.DecimalField(max_digits=15, decimal_places=2, help_text='该类型票房总额（元）')
    percentage = serializers.FloatField(help_text='票房占比（%）')


class RegionBoxOfficeSerializer(serializers.Serializer):
    """
    地域票房分布序列化器

    用于序列化各省份的票房分布数据。
    包含省份信息、票房总额和影院数量，用于地域票房地图或排行榜展示。
    """
    region_id = serializers.IntegerField(help_text='省份ID')
    region_name = serializers.CharField(help_text='省份名称')
    box_office = serializers.DecimalField(max_digits=15, decimal_places=2, help_text='该省份票房总额（元）')
    cinema_count = serializers.IntegerField(help_text='该省份影院数量')


class WeeklyChampionSerializer(serializers.Serializer):
    """
    周票房冠军序列化器

    用于序列化本周票房冠军影片信息。
    包含影片基本信息和周票房总额，用于周榜冠军展示。
    """
    movie_id = serializers.IntegerField(help_text='影片ID')
    movie_title = serializers.CharField(help_text='影片名称')
    weekly_box_office = serializers.DecimalField(max_digits=15, decimal_places=2, help_text='本周票房总额（元）')


class DashboardStatsSerializer(serializers.Serializer):
    """
    仪表盘统计序列化器

    用于序列化仪表盘综合统计数据。
    包含今日票房、本周冠军、影片总数、影院总数，用于首页仪表盘展示。
    """
    today_box_office = serializers.DecimalField(max_digits=15, decimal_places=2, help_text='今日大盘票房（元）')
    week_champion = WeeklyChampionSerializer(allow_null=True, help_text='本周票房冠军信息')
    total_movies = serializers.IntegerField(help_text='系统影片总数')
    total_cinemas = serializers.IntegerField(help_text='系统影院总数')
