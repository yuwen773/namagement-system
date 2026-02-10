"""
预测模块视图
提供票房预测 API 接口
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .services import prediction_service
from .serializers import (
    PredictionResultSerializer,
    CombinedPredictionSerializer,
    PredictionRequestSerializer,
)


class MoviePredictionView(APIView):
    """
    影片票房预测接口

    提供基于历史票房数据的未来票房预测功能，支持多种预测算法。
    支持线性回归、移动平均和综合预测三种算法。

    GET /api/prediction/movie/{id}/
    GET /api/prediction/movie/{id}/?predict_days=7&algorithm=linear_regression
    """

    permission_classes = [AllowAny]  # 允许所有用户访问

    @extend_schema(
        summary='影片票房预测',
        description='''
        根据影片历史票房数据，使用指定算法预测未来票房。

        支持三种预测算法：
        1. linear_regression - 线性回归算法，使用最小二乘法拟合趋势
        2. moving_average - 移动平均算法，基于历史数据的加权平均值
        3. combined - 综合预测，同时返回两种算法结果供对比

        预测天数范围为 1-30 天，默认 7 天。
        ''',
        parameters=[
            OpenApiParameter(
                name='movie_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='影片ID',
                required=True
            ),
            OpenApiParameter(
                name='predict_days',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='预测天数，范围 1-30，默认 7',
                required=False
            ),
            OpenApiParameter(
                name='algorithm',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='预测算法：linear_regression, moving_average, combined',
                required=False,
                enum=['linear_regression', 'moving_average', 'combined']
            ),
        ],
        responses={
            200: CombinedPredictionSerializer,
            400: {'description': '参数错误'},
            404: {'description': '影片不存在'},
        },
        tags=['预测分析']
    )
    def get(self, request, movie_id):
        """
        获取影片票房预测数据

        Query Parameters:
            - predict_days: 预测天数 (1-30, 默认7)
            - algorithm: 算法类型 (linear_regression, moving_average, combined)
        """
        # 获取请求参数
        predict_days = request.query_params.get('predict_days', 7)
        algorithm = request.query_params.get('algorithm', 'combined')

        try:
            predict_days = int(predict_days)
            if predict_days < 1:
                predict_days = 7
            if predict_days > 30:
                predict_days = 30
        except (ValueError, TypeError):
            predict_days = 7

        # 执行预测
        if algorithm == 'linear_regression':
            result = prediction_service.linear_regression_predict(movie_id, predict_days)
            serializer = PredictionResultSerializer(result)
        elif algorithm == 'moving_average':
            result = prediction_service.moving_average_predict(movie_id, predict_days)
            serializer = PredictionResultSerializer(result)
        else:
            # combined (默认)
            result = prediction_service.combined_prediction(movie_id, predict_days)
            serializer = CombinedPredictionSerializer(result)

        return Response({
            'code': 0,
            'data': serializer.data,
            'message': 'success' if result.get('success') else result.get('message', '')
        })


class PredictionHistoryView(APIView):
    """
    获取影片历史票房数据接口

    提供指定影片的历史票房数据，包括每日票房、排片场次和观影人次。
    用于趋势分析和可视化展示。

    GET /api/prediction/movie/{id}/history/
    """

    permission_classes = [AllowAny]

    @extend_schema(
        summary='获取影片历史票房数据',
        description='''
        获取指定影片的历史票房数据，用于分析影片票房趋势。

        返回数据包括：
        - 日期
        - 每日票房
        - 排片场次
        - 观影人次

        可指定获取天数，范围为 1-365 天，默认 30 天。
        ''',
        parameters=[
            OpenApiParameter(
                name='movie_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='影片ID',
                required=True
            ),
            OpenApiParameter(
                name='days',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='获取天数，范围 1-365，默认 30',
                required=False
            ),
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'description': '响应码'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'movie_id': {'type': 'integer', 'description': '影片ID'},
                            'history': {'type': 'array', 'description': '历史数据列表'},
                            'total_days': {'type': 'integer', 'description': '总天数'}
                        }
                    },
                    'total': {'type': 'integer', 'description': '记录总数'}
                }
            },
            404: {'description': '影片不存在'},
        },
        tags=['预测分析']
    )
    def get(self, request, movie_id):
        """
        获取影片历史票房数据

        Query Parameters:
            - days: 获取天数 (1-365, 默认30)
        """
        days = request.query_params.get('days', 30)

        try:
            days = int(days)
            if days < 1:
                days = 30
            if days > 365:
                days = 365
        except (ValueError, TypeError):
            days = 30

        history_data = prediction_service.get_movie_history(movie_id, days)

        return Response({
            'code': 0,
            'data': {
                'movie_id': movie_id,
                'history': history_data,
                'total_days': len(history_data)
            },
            'total': len(history_data)
        })


class PredictionAlgorithmsView(APIView):
    """
    获取支持的预测算法列表

    返回系统支持的所有预测算法信息，包括算法ID、名称、描述和参数说明。
    用于前端展示算法选择和参数配置界面。

    GET /api/prediction/algorithms/
    """

    permission_classes = [AllowAny]

    @extend_schema(
        summary='获取支持的预测算法列表',
        description='''
        获取系统支持的所有预测算法信息。

        返回每个算法的详细信息：
        - id: 算法唯一标识
        - name: 算法中文名称
        - description: 算法详细说明
        - params: 算法参数说明

        当前支持的算法：
        1. linear_regression - 线性回归
        2. moving_average - 移动平均
        3. combined - 综合预测
        ''',
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer', 'description': '响应码'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string', 'description': '算法ID'},
                                'name': {'type': 'string', 'description': '算法名称'},
                                'description': {'type': 'string', 'description': '算法描述'},
                                'params': {'type': 'object', 'description': '参数说明'}
                            }
                        }
                    },
                    'total': {'type': 'integer', 'description': '算法总数'}
                }
            }
        },
        tags=['预测分析']
    )
    def get(self, request):
        """获取支持的预测算法列表"""
        algorithms = [
            {
                'id': 'linear_regression',
                'name': '线性回归',
                'description': '使用最小二乘法拟合历史数据趋势，预测未来票房',
                'params': {
                    'predict_days': '预测天数 (1-30)'
                }
            },
            {
                'id': 'moving_average',
                'name': '移动平均',
                'description': '基于历史数据的加权移动平均值进行预测',
                'params': {
                    'predict_days': '预测天数 (1-30)',
                    'window': '平均窗口大小 (默认3)'
                }
            },
            {
                'id': 'combined',
                'name': '综合预测',
                'description': '同时返回线性回归和移动平均两种预测结果，方便对比',
                'params': {
                    'predict_days': '预测天数 (1-30)'
                }
            }
        ]

        return Response({
            'code': 0,
            'data': algorithms,
            'total': len(algorithms)
        })
