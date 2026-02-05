/**
 * 推荐管理 API 模块
 * 包含推荐规则和推荐商品的管理接口
 */

import { get, post, put, patch, del } from '../request'

// ==================== 推荐规则 ====================

/**
 * 获取推荐规则列表
 * @param {Object} params - 查询参数
 * @param {string} params.rule_type - 规则类型筛选 (hot/new/personalized/category)
 * @param {string} params.is_active - 是否启用筛选
 * @param {string} params.ordering - 排序字段
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise<Object>} 分页数据
 */
export function getRecommendationRules(params = {}) {
  return get('/recommendations/rules/', params)
}

/**
 * 获取启用的推荐规则列表
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>} 分页数据
 */
export function getActiveRecommendationRules(params = {}) {
  return get('/recommendations/rules/active/', params)
}

/**
 * 获取推荐规则详情
 * @param {number} id - 规则ID
 * @returns {Promise<Object>} 规则详情
 */
export function getRecommendationRuleDetail(id) {
  return get(`/recommendations/rules/${id}/`)
}

/**
 * 创建推荐规则
 * @param {Object} data - 规则数据
 * @param {string} data.name - 规则名称
 * @param {string} data.rule_type - 规则类型 (hot/new/personalized/category)
 * @param {string} data.description - 规则描述
 * @param {Object} data.config - 规则配置 (JSON)
 * @param {number} data.priority - 优先级
 * @param {number} data.limit - 返回商品数量限制
 * @param {boolean} data.is_active - 是否启用
 * @returns {Promise<Object>} 创建的规则
 */
export function createRecommendationRule(data) {
  return post('/recommendations/rules/', data)
}

/**
 * 更新推荐规则（完整更新）
 * @param {number} id - 规则ID
 * @param {Object} data - 规则数据
 * @returns {Promise<Object>} 更新后的规则
 */
export function updateRecommendationRule(id, data) {
  return put(`/recommendations/rules/${id}/`, data)
}

/**
 * 部分更新推荐规则
 * @param {number} id - 规则ID
 * @param {Object} data - 要更新的字段
 * @returns {Promise<Object>} 更新后的规则
 */
export function patchRecommendationRule(id, data) {
  return patch(`/recommendations/rules/${id}/`, data)
}

/**
 * 删除推荐规则
 * @param {number} id - 规则ID
 * @returns {Promise<void>}
 */
export function deleteRecommendationRule(id) {
  return del(`/recommendations/rules/${id}/`)
}

/**
 * 切换推荐规则启用状态
 * @param {number} id - 规则ID
 * @param {boolean} isActive - 是否启用
 * @returns {Promise<Object>} 更新后的规则
 */
export function toggleRecommendationRuleActive(id, isActive) {
  return patchRecommendationRule(id, { is_active: isActive })
}

// ==================== 推荐商品 ====================

/**
 * 获取推荐商品列表
 * @param {Object} params - 查询参数
 * @param {number} params.rule - 按规则ID筛选
 * @param {string} params.ordering - 排序字段
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise<Object>} 分页数据
 */
export function getRecommendedProducts(params = {}) {
  return get('/recommendations/products/', params)
}

/**
 * 获取推荐商品详情
 * @param {number} id - 推荐商品ID
 * @returns {Promise<Object>} 推荐商品详情
 */
export function getRecommendedProductDetail(id) {
  return get(`/recommendations/products/${id}/`)
}

/**
 * 添加推荐商品
 * @param {Object} data - 推荐商品数据
 * @param {number} data.rule - 规则ID
 * @param {number} data.product - 商品ID
 * @param {number} data.sort_order - 排序权重
 * @param {string} data.remark - 备注
 * @returns {Promise<Object>} 创建的推荐商品
 */
export function addRecommendedProduct(data) {
  return post('/recommendations/products/', data)
}

/**
 * 更新推荐商品（完整更新）
 * @param {number} id - 推荐商品ID
 * @param {Object} data - 推荐商品数据
 * @returns {Promise<Object>} 更新后的推荐商品
 */
export function updateRecommendedProduct(id, data) {
  return put(`/recommendations/products/${id}/`, data)
}

/**
 * 部分更新推荐商品
 * @param {number} id - 推荐商品ID
 * @param {Object} data - 要更新的字段
 * @returns {Promise<Object>} 更新后的推荐商品
 */
export function patchRecommendedProduct(id, data) {
  return patch(`/recommendations/products/${id}/`, data)
}

/**
 * 删除推荐商品
 * @param {number} id - 推荐商品ID
 * @returns {Promise<void>}
 */
export function deleteRecommendedProduct(id) {
  return del(`/recommendations/products/${id}/`)
}

/**
 * 批量添加推荐商品
 * @param {number} ruleId - 规则ID
 * @param {Array<number>} productIds - 商品ID列表
 * @returns {Promise<Array>} 批量添加结果
 */
export async function batchAddRecommendedProducts(ruleId, productIds) {
  const promises = productIds.map(productId =>
    addRecommendedProduct({
      rule: ruleId,
      product: productId,
      sort_order: 0
    })
  )
  return Promise.all(promises)
}

/**
 * 更新推荐商品排序
 * @param {number} id - 推荐商品ID
 * @param {number} sortOrder - 排序权重
 * @returns {Promise<Object>} 更新后的推荐商品
 */
export function updateRecommendedProductSortOrder(id, sortOrder) {
  return patchRecommendedProduct(id, { sort_order: sortOrder })
}

// ==================== 推荐类型常量 ====================

/**
 * 推荐规则类型枚举
 */
export const RecommendationRuleTypes = {
  HOT: 'hot',
  NEW: 'new',
  PERSONALIZED: 'personalized',
  CATEGORY: 'category'
}

/**
 * 推荐规则类型显示名称
 */
export const RecommendationRuleTypeLabels = {
  hot: '热门推荐',
  new: '新品推荐',
  personalized: '个性化推荐',
  category: '分类推荐'
}

/**
 * 获取规则类型显示名称
 * @param {string} type - 规则类型
 * @returns {string} 显示名称
 */
export function getRuleTypeLabel(type) {
  return RecommendationRuleTypeLabels[type] || type
}
