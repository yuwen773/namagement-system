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

// ==================== 管理员仪表盘 API ====================

/**
 * 获取数据总览（仅管理员）
 * @returns {Promise} 数据总览 { total_recipes, total_users, today_new_recipes, today_new_users, today_active_users, total_favorites, updated_at }
 */
export function getDashboardOverview() {
  return request.get('/api/admin/dashboard/overview/')
}

/**
 * 获取数据趋势（仅管理员）
 * @param {Object} params - 查询参数
 * @param {string} params.period - 时间范围（day/week/month）
 * @param {number} params.days - 天数（1-90）
 * @returns {Promise} 数据趋势 { period, days, data: { dates, recipe_counts, user_counts, favorite_counts } }
 */
export function getDashboardTrends(params) {
  return request.get('/api/admin/dashboard/trends/', { params })
}

/**
 * 获取用户行为统计（仅管理员）
 * @returns {Promise} 用户行为统计 { behavior_distribution, active_user_distribution, page_views, updated_at }
 */
/**
 * 获取用户行为统计（仅管理员）
 * @returns {Promise} 用户行为统计 { behavior_distribution, active_user_distribution, page_views, updated_at }
 */
export function getDashboardBehaviors() {
  return request.get('/api/admin/dashboard/behaviors/')
}

/**
 * 获取点击流分析数据（仅管理员）
 * @param {Object} params - 查询参数
 * @param {number} params.days - 分析时间范围天数（1-90，默认30）
 * @param {number} params.limit_path - 返回路径数量（1-50，默认20）
 * @returns {Promise} 点击流分析数据 { summary, behavior_distribution, conversion_funnel, path_patterns }
 */
export function getClickStreamAnalytics(params) {
  return request.get('/api/admin/analytics/clickstream/', { params })
}

/**
 * 获取活跃用户分析数据（仅管理员）
 * @param {Object} params - 查询参数
 * @param {number} params.days - 分析时间范围天数（7-90，默认30）
 * @param {string} params.trend_by - 趋势聚合方式（day/week/month，默认day）
 * @param {boolean} params.include_trend - 是否返回趋势数据（默认true）
 * @returns {Promise} 活跃用户分析数据 { summary, dau, wau, mau, stickiness, trend }
 */
export function getActiveUsersAnalytics(params) {
  return request.get('/api/admin/analytics/active-users/', { params })
}

/**
 * 获取登录频次分析数据（仅管理员）
 * @param {Object} params - 查询参数
 * @param {number} params.days - 分析时间范围天数（1-90，默认30）
 * @returns {Promise} 登录频次分析数据 { summary, login_frequency_distribution, hourly_distribution, daily_trend }
 */
export function getLoginFrequencyAnalytics(params) {
  return request.get('/api/admin/analytics/login-frequency/', { params })
}

/**
 * 获取页面停留分析数据（仅管理员）
 * @param {Object} params - 查询参数
 * @param {number} params.days - 分析时间范围天数（1-90，默认30）
 * @param {string} params.page - 页面类型筛选（可选）
 * @returns {Promise} 页面停留分析数据 { summary, page_statistics, duration_distribution, trend }
 */
export function getPageDurationAnalytics(params) {
  return request.get('/api/admin/analytics/page-duration/', { params })
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
  getAdminIngredientPairsAnalytics,
  // 管理员仪表盘 API
  getDashboardOverview,
  getDashboardTrends,
  getDashboardBehaviors,
  // 用户行为分析 API
  getClickStreamAnalytics,
  getActiveUsersAnalytics,
  getLoginFrequencyAnalytics,
  getPageDurationAnalytics
}
