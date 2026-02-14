"""
预测模块序列化器

定义预测相关的所有序列化器，用于验证和序列化预测请求/响应数据。
"""

from rest_framework import serializers


class PredictionItemSerializer(serializers.Serializer):
    """
    单日预测结果序列化器

    用于序列化单日的票房预测结果，包含预测天数和预测票房值。
    """
    day = serializers.IntegerField(help_text='预测天数（从1开始的连续天数）')
    predicted_box_office = serializers.FloatField(help_text='预测票房（单位：万元）')


class HistoryItemSerializer(serializers.Serializer):
    """
    历史数据序列化器

    用于序列化影片的历史票房数据，包含日期、票房、排片场次和观影人次。
    这些数据通常用于预测算法的输入和趋势分析的可视化展示。
    """
    date = serializers.DateField(help_text='日期（YYYY-MM-DD格式）')
    box_office = serializers.FloatField(help_text='当日票房（单位：万元）')
    screening_count = serializers.IntegerField(help_text='当日排片场次')
    audience_count = serializers.IntegerField(help_text='当日观影人次')


class PredictionResultSerializer(serializers.Serializer):
    """
    预测结果序列化器

    用于序列化完整的预测结果，包含成功状态、消息、影片信息、
    预测数据列表、历史数据列表和使用的算法类型。
    这是单个算法（线性回归或移动平均）的预测结果。
    """
    success = serializers.BooleanField(help_text='预测是否成功')
    message = serializers.CharField(help_text='返回消息（成功时为success，失败时为错误信息）')
    movie_id = serializers.IntegerField(help_text='影片ID')
    predictions = PredictionItemSerializer(many=True, help_text='预测数据列表')
    history = HistoryItemSerializer(many=True, help_text='历史数据列表（用于对比）')
    algorithm = serializers.CharField(help_text='使用的预测算法类型')


class LinearRegressionPredictionSerializer(serializers.Serializer):
    """
    线性回归预测序列化器

    用于序列化线性回归模型的参数信息，包括回归系数和截距。
    这些参数用于理解模型的拟合情况和预测趋势。
    """
    coefficient = serializers.FloatField(help_text='回归系数（斜率），表示每天票房的变化趋势')
    intercept = serializers.FloatField(help_text='截距，表示起始点的票房值')


class MovingAverageParamsSerializer(serializers.Serializer):
    """
    移动平均参数序列化器

    用于序列化移动平均算法的参数信息，包括窗口大小和权重列表。
    这些参数用于理解移动平均模型的配置和计算方式。
    """
    window = serializers.IntegerField(help_text='移动平均窗口大小（使用的最近天数）')
    weights = serializers.ListField(
        child=serializers.FloatField(),
        help_text='权重列表（最近的日期权重较高）'
    )


class CombinedPredictionSerializer(serializers.Serializer):
    """
    综合预测结果序列化器

    用于序列化综合预测的结果，同时包含线性回归和移动平均两种算法的预测结果。
    方便前端对比不同算法的预测效果，选择更合适的预测结果。
    """
    success = serializers.BooleanField(help_text='预测是否成功')
    movie_id = serializers.IntegerField(help_text='影片ID')
    linear_regression = PredictionResultSerializer(help_text='线性回归算法的预测结果')
    moving_average = PredictionResultSerializer(help_text='移动平均算法的预测结果')
    history = HistoryItemSerializer(many=True, help_text='历史数据列表（供参考对比）')


class PredictionRequestSerializer(serializers.Serializer):
    """
    预测请求参数序列化器

    用于验证和序列化预测请求的参数，包括影片ID、预测天数和算法类型。
    确保请求参数在有效范围内，提供默认值和参数验证。
    """
    movie_id = serializers.IntegerField(
        help_text='影片ID（必填）',
        min_value=1
    )
    predict_days = serializers.IntegerField(
        required=False,
        default=7,
        min_value=1,
        max_value=30,
        help_text='预测天数，范围1-30天，默认7天'
    )
    algorithm = serializers.ChoiceField(
        choices=['linear_regression', 'moving_average', 'combined'],
        default='combined',
        help_text='预测算法：linear_regression（线性回归）、moving_average（移动平均）、combined（综合预测）'
    )
