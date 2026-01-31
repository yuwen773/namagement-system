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

// ==================== 管理员专用 API ====================

/**
 * 获取菜系深度分析数据（仅管理员）
 * @returns {Promise} 菜系深度分析数据 { summary, cuisines: [{ name, count, percentage, avg_view_count, avg_favorite_count, avg_cooking_time, difficulty_distribution }] }
 */
export function getAdminCuisinesAnalytics() {
  return request.get('/api/admin/analytics/cuisines/')
}

/**
 * 获取难度深度分析数据（仅管理员）
 * @returns {Promise} 难度深度分析数据 { summary, difficulties: [{ name, value, count, percentage, avg_cooking_time, avg_view_count, avg_favorite_count }] }
 */
export function getAdminDifficultyAnalytics() {
  return request.get('/api/admin/analytics/difficulty/')
}

/**
 * 获取热门菜谱分析数据（仅管理员）
 * @param {Object} params - 查询参数
 * @param {string} params.sort_by - 排序字段（view_count/favorite_count）
 * @param {number} params.limit - 返回数量（1-100，默认50）
 * @returns {Promise} 热门菜谱分析数据 { summary, trends, recipes: [{ id, name, cuisine_type, difficulty, view_count, favorite_count, conversion_rate }] }
 */
export function getAdminHotRecipesAnalytics(params) {
  return request.get('/api/admin/analytics/hot/', { params })
}

/**
 * 获取食材关联分析数据（仅管理员）
 * @param {Object} params - 查询参数
 * @param {number} params.min_count - 最小共现次数（默认10）
 * @param {number} params.limit - 返回数量（1-100，默认50）
 * @param {string} params.category - 食材分类筛选
 * @returns {Promise} 食材关联分析数据 { summary, pairs: [{ ingredient_1, ingredient_2, count, percentage }] }
 */
export function getAdminIngredientPairsAnalytics(params) {
  return request.get('/api/admin/analytics/ingredient-pairs/', { params })
}

export default {
  // 普通用户 API
  getCuisinesAnalytics,
  getDifficultyAnalytics,
  getFlavorsAnalytics,
  getIngredientsAnalytics,
  // 管理员 API
  getAdminCuisinesAnalytics,
  getAdminDifficultyAnalytics,
  getAdminHotRecipesAnalytics,
  getAdminIngredientPairsAnalytics
}
