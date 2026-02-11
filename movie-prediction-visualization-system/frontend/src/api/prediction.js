/**
 * API 接口 - 票房预测
 */
import request from '@/utils/request'

// 获取影片预测结果
// GET /api/prediction/movie/{movie_id}/?predict_days=7&algorithm=combined
export function getMoviePrediction(movieId, params = {}) {
  return request({
    url: `/prediction/movie/${movieId}/`,
    method: 'get',
    params: {
      predict_days: params.predictDays || 7,
      algorithm: params.algorithm || 'combined'
    }
  })
}

// 获取影片历史票房数据
// GET /api/prediction/movie/{movie_id}/history/?days=30
export function getMovieHistory(movieId, days = 30) {
  return request({
    url: `/prediction/movie/${movieId}/history/`,
    method: 'get',
    params: { days }
  })
}

// 获取支持的预测算法列表
// GET /api/prediction/algorithms/
export function getAlgorithmInfo() {
  return request({
    url: '/prediction/algorithms/',
    method: 'get'
  })
}
