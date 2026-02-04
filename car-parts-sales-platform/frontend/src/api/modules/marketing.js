import { get, post } from '../request'

/**
 * 营销相关 API
 */

/**
 * 获取优惠券列表
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getCouponListApi(params) {
  return get('/marketing/coupons/', params)
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
 * 获取FAQ列表
 * @param {Object} params - 查询参数
 * @param {string} params.category - 分类
 * @returns {Promise<Object>}
 */
export function getFaqListApi(params) {
  return get('/content/faqs/', params)
}
