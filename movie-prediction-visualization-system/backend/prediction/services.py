"""
预测服务模块
提供票房预测算法：线性回归预测、移动平均预测
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import List, Dict, Tuple, Optional
from decimal import Decimal


class PredictionService:
    """票房预测服务类"""

    def __init__(self):
        self.history_days = 30  # 获取历史数据天数
        self.default_predict_days = 7  # 默认预测天数

    def get_movie_history(self, movie_id: int, days: int = None) -> List[Dict]:
        """
        获取影片历史票房数据

        Args:
            movie_id: 影片ID
            days: 获取天数，默认30天

        Returns:
            包含日期和票房数据的字典列表
        """
        from boxoffice.models import BoxOfficeRecord

        if days is None:
            days = self.history_days

        records = BoxOfficeRecord.objects.filter(
            movie_id=movie_id
        ).select_related('movie').order_by('-record_date')[:days]

        # 转换为字典列表
        history_data = []
        for record in records:
            history_data.append({
                'date': record.record_date.isoformat(),
                'box_office': float(record.daily_box_office),
                'screening_count': record.screening_count,
                'audience_count': record.audience_count,
            })

        # 按日期升序排序
        history_data.sort(key=lambda x: x['date'])

        return history_data

    def prepare_prediction_data(self, history_data: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        准备预测数据

        Args:
            history_data: 历史票房数据列表

        Returns:
            X: 时间索引数组 (1, 2, 3, ...)
            y: 票房数组
        """
        if len(history_data) < 2:
            return None, None

        # 提取票房数据
        box_offices = np.array([d['box_office'] for d in history_data])

        # 创建时间索引 (从1开始)
        X = np.arange(1, len(box_offices) + 1).reshape(-1, 1)
        y = box_offices

        return X, y

    def linear_regression_predict(
        self,
        movie_id: int,
        predict_days: int = None
    ) -> Dict:
        """
        线性回归预测

        Args:
            movie_id: 影片ID
            predict_days: 预测天数

        Returns:
            预测结果字典
        """
        if predict_days is None:
            predict_days = self.default_predict_days

        # 获取历史数据
        history_data = self.get_movie_history(movie_id)
        X, y = self.prepare_prediction_data(history_data)

        if X is None or len(X) < 2:
            return {
                'success': False,
                'message': '历史数据不足，无法进行预测',
                'movie_id': movie_id,
                'predictions': [],
                'history': [],
                'algorithm': 'linear_regression'
            }

        # 训练线性回归模型
        model = LinearRegression()
        model.fit(X, y)

        # 预测未来数据
        future_X = np.arange(
            len(X) + 1,
            len(X) + predict_days + 1
        ).reshape(-1, 1)

        predictions = model.predict(future_X)

        # 确保预测值非负
        predictions = np.maximum(predictions, 0)

        # 构建返回结果
        prediction_results = []
        for i, pred in enumerate(predictions):
            prediction_results.append({
                'day': i + 1,
                'predicted_box_office': round(float(pred), 2)
            })

        return {
            'success': True,
            'message': '线性回归预测成功',
            'movie_id': movie_id,
            'predictions': prediction_results,
            'history': history_data,
            'algorithm': 'linear_regression',
            'model_params': {
                'coefficient': round(float(model.coef_[0]), 4),
                'intercept': round(float(model.intercept_), 2)
            }
        }

    def moving_average_predict(
        self,
        movie_id: int,
        predict_days: int = None,
        window: int = 3
    ) -> Dict:
        """
        移动平均预测

        Args:
            movie_id: 影片ID
            predict_days: 预测天数
            window: 移动平均窗口大小

        Returns:
            预测结果字典
        """
        if predict_days is None:
            predict_days = self.default_predict_days

        # 获取历史数据
        history_data = self.get_movie_history(movie_id)

        if len(history_data) < window:
            return {
                'success': False,
                'message': f'历史数据不足（需要至少{window}天），无法进行预测',
                'movie_id': movie_id,
                'predictions': [],
                'history': [],
                'algorithm': 'moving_average'
            }

        # 提取票房数据
        box_offices = np.array([d['box_office'] for d in history_data])

        # 计算移动平均（加权移动平均）
        # 权重: 越近的数据权重越大 (0.5, 0.3, 0.2)
        weights = np.array([0.5, 0.3, 0.2][:window])
        weights = weights / weights.sum()

        # 计算最后一个移动平均值作为预测基础
        recent_values = box_offices[-window:]
        base_prediction = np.average(recent_values, weights=weights)

        # 预测未来数据（使用加权平均法）
        predictions = []
        current_avg = base_prediction

        for i in range(predict_days):
            # 简单的衰减预测：逐渐接近历史平均值
            historical_avg = np.mean(box_offices)
            decay_factor = 0.9 ** (i + 1)

            if len(box_offices) >= 2:
                recent_change = (box_offices[-1] - box_offices[-2]) * 0.5
            else:
                recent_change = 0

            pred_value = current_avg * decay_factor + historical_avg * (1 - decay_factor) + recent_change
            pred_value = max(0, pred_value)  # 确保非负

            predictions.append({
                'day': i + 1,
                'predicted_box_office': round(float(pred_value), 2)
            })

            # 更新当前平均值
            current_avg = (current_avg + pred_value) / 2

        return {
            'success': True,
            'message': '移动平均预测成功',
            'movie_id': movie_id,
            'predictions': predictions,
            'history': history_data,
            'algorithm': 'moving_average',
            'params': {
                'window': window,
                'weights': weights.tolist()
            }
        }

    def combined_prediction(
        self,
        movie_id: int,
        predict_days: int = None
    ) -> Dict:
        """
        综合预测：同时返回线性回归和移动平均预测结果

        Args:
            movie_id: 影片ID
            predict_days: 预测天数

        Returns:
            包含两种预测结果的字典
        """
        if predict_days is None:
            predict_days = self.default_predict_days

        lr_result = self.linear_regression_predict(movie_id, predict_days)
        ma_result = self.moving_average_predict(movie_id, predict_days)

        return {
            'success': lr_result['success'] or ma_result['success'],
            'movie_id': movie_id,
            'linear_regression': lr_result,
            'moving_average': ma_result,
            'history': lr_result.get('history', [])
        }


# 单例服务实例
prediction_service = PredictionService()
