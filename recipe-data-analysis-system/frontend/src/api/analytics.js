import request from './auth'

/**
 * 获取菜系分布分析数据
 * @returns {Promise} 菜系分布数据 [{ name, count, percentage }]
 */
export function getCuisinesAnalytics() {
  return request.get('/api/analytics/cuisines/')
}

/**
 * 获取难度等级统计数据
 * @returns {Promise} 难度统计数据 [{ name, value, count, percentage, avg_cooking_time }]
 */
export function getDifficultyAnalytics() {
  return request.get('/api/analytics/difficulty/')
}

/**
 * 获取口味偏好分析数据
 * @returns {Promise} 口味偏好数据 [{ name, count, percentage }]
 */
export function getFlavorsAnalytics() {
  return request.get('/api/analytics/flavors/')
}

/**
 * 获取食材使用频率统计
 * @param {Object} params - 查询参数
 * @param {number} params.limit - 返回数量（1-100，默认20）
 * @returns {Promise} 食材频率数据 [{ id, name, count, category }]
 */
export function getIngredientsAnalytics(params) {
  return request.get('/api/analytics/ingredients/', { params })
}

export default {
  getCuisinesAnalytics,
  getDifficultyAnalytics,
  getFlavorsAnalytics,
  getIngredientsAnalytics
}
