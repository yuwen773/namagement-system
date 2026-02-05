import { get, post, put, patch, del } from '../request'

/**
 * 营销相关 API
 */

// ==================== 用户端优惠券接口 ====================

/**
 * 获取优惠券列表
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getCouponListApi(params) {
  return get('/marketing/coupons/', params)
}

/**
 * 获取优惠券详情
 * @param {number} id - 优惠券ID
 * @returns {Promise<Object>}
 */
export function getCouponDetailApi(id) {
  return get(`/marketing/coupons/${id}/`)
}

/**
 * 领取优惠券
 * @param {number} id - 优惠券ID
 * @returns {Promise<Object>}
 */
export function claimCouponApi(id) {
  return post(`/marketing/coupons/${id}/claim/`)
}

/**
 * 获取我的优惠券列表
 * @param {Object} params - 查询参数
 * @param {string} params.status - 状态 (available/used/expired)
 * @returns {Promise<Object>}
 */
export function getMyCouponsApi(params) {
  return get('/marketing/my-coupons/', params)
}

// ==================== 管理员优惠券管理接口 ====================

/**
 * 创建优惠券
 * @param {Object} data - 优惠券数据
 * @returns {Promise<Object>}
 */
export function createCouponApi(data) {
  return post('/marketing/coupons/', data)
}

/**
 * 更新优惠券
 * @param {number} id - 优惠券ID
 * @param {Object} data - 优惠券数据
 * @returns {Promise<Object>}
 */
export function updateCouponApi(id, data) {
  return put(`/marketing/coupons/${id}/`, data)
}

/**
 * 部分更新优惠券
 * @param {number} id - 优惠券ID
 * @param {Object} data - 优惠券数据
 * @returns {Promise<Object>}
 */
export function patchCouponApi(id, data) {
  return patch(`/marketing/coupons/${id}/`, data)
}

/**
 * 删除优惠券
 * @param {number} id - 优惠券ID
 * @returns {Promise<Object>}
 */
export function deleteCouponApi(id) {
  return del(`/marketing/coupons/${id}/`)
}

/**
 * 获取用户优惠券列表（用于统计）
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getUserCouponsApi(params) {
  return get('/marketing/user-coupons/', params)
}

/**
 * 获取用户优惠券详情
 * @param {number} id - 用户优惠券ID
 * @returns {Promise<Object>}
 */
export function getUserCouponDetailApi(id) {
  return get(`/marketing/user-coupons/${id}/`)
}

/**
 * 更新用户优惠券
 * @param {number} id - 用户优惠券ID
 * @param {Object} data - 更新数据
 * @returns {Promise<Object>}
 */
export function updateUserCouponApi(id, data) {
  return patch(`/marketing/user-coupons/${id}/`, data)
}

/**
 * 删除用户优惠券
 * @param {number} id - 用户优惠券ID
 * @returns {Promise<Object>}
 */
export function deleteUserCouponApi(id) {
  return del(`/marketing/user-coupons/${id}/`)
}

// ==================== 推荐与内容接口 ====================

/**
 * 获取推荐商品列表
 * @param {Object} params - 查询参数
 * @param {string} params.type - 推荐类型 (hot/new/personalized)
 * @param {number} params.page - 页码
 * @returns {Promise<Object>}
 */
export function getRecommendedProductsApi(params) {
  return get('/recommendations/products/', params)
}

/**
 * 获取改装案例列表
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getCaseListApi(params) {
  return get('/content/cases/', params)
}

/**
 * 获取改装案例详情
 * @param {number} id - 案例ID
 * @returns {Promise<Object>}
 */
export function getCaseDetailApi(id) {
  return get(`/content/cases/${id}/`)
}

/**
 * 创建改装案例
 * @param {Object} data - 案例数据
 * @returns {Promise<Object>}
 */
export function createCaseApi(data) {
  return post('/content/cases/', data)
}

/**
 * 更新改装案例
 * @param {number} id - 案例ID
 * @param {Object} data - 案例数据
 * @returns {Promise<Object>}
 */
export function updateCaseApi(id, data) {
  return put(`/content/cases/${id}/`, data)
}

/**
 * 删除改装案例
 * @param {number} id - 案例ID
 * @returns {Promise<Object>}
 */
export function deleteCaseApi(id) {
  return del(`/content/cases/${id}/`)
}

/**
 * 获取FAQ列表
 * @param {Object} params - 查询参数
 * @param {string} params.category - 分类
 * @returns {Promise<Object>}
 */
export function getFaqListApi(params) {
  return get('/content/faqs/', params)
}

/**
 * 创建FAQ
 * @param {Object} data - FAQ数据
 * @returns {Promise<Object>}
 */
export function createFaqApi(data) {
  return post('/content/faqs/', data)
}

/**
 * 更新FAQ
 * @param {number} id - FAQ ID
 * @param {Object} data - FAQ数据
 * @returns {Promise<Object>}
 */
export function updateFaqApi(id, data) {
  return put(`/content/faqs/${id}/`, data)
}

/**
 * 删除FAQ
 * @param {number} id - FAQ ID
 * @returns {Promise<Object>}
 */
export function deleteFaqApi(id) {
  return del(`/content/faqs/${id}/`)
}

// ==================== 营销统计接口（管理员）====================

/**
 * 获取营销统计数据
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getMarketingStatsApi(params) {
  return get('/marketing/stats/', params)
}
