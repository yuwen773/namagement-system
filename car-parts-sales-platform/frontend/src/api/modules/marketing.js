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
  return get('/marketing/user-coupons/', params)
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

// ==================== 促销活动管理接口（管理员）====================

/**
 * 获取促销活动列表（管理员）
 * @param {Object} params - 查询参数
 * @param {string} params.promotion_type - 活动类型
 * @param {string} params.is_active - 是否启用
 * @param {number} params.page - 页码
 * @returns {Promise<Object>}
 */
export function getPromotionListApi(params) {
  return get('/marketing/promotions/', params)
}

/**
 * 获取促销活动详情
 * @param {number} id - 活动ID
 * @returns {Promise<Object>}
 */
export function getPromotionDetailApi(id) {
  return get(`/marketing/promotions/${id}/`)
}

/**
 * 创建促销活动
 * @param {Object} data - 活动数据
 * @param {string} data.name - 活动名称
 * @param {string} data.promotion_type - 活动类型 (flash_sale/discount/full_reduce/gift)
 * @param {string} data.description - 活动描述
 * @param {Object} data.config - 活动配置
 * @param {string} data.start_time - 开始时间
 * @param {string} data.end_time - 结束时间
 * @param {number} data.priority - 优先级
 * @param {boolean} data.is_active - 是否启用
 * @returns {Promise<Object>}
 */
export function createPromotionApi(data) {
  return post('/marketing/promotions/', data)
}

/**
 * 更新促销活动
 * @param {number} id - 活动ID
 * @param {Object} data - 活动数据
 * @returns {Promise<Object>}
 */
export function updatePromotionApi(id, data) {
  return put(`/marketing/promotions/${id}/`, data)
}

/**
 * 部分更新促销活动
 * @param {number} id - 活动ID
 * @param {Object} data - 活动数据
 * @returns {Promise<Object>}
 */
export function patchPromotionApi(id, data) {
  return patch(`/marketing/promotions/${id}/`, data)
}

/**
 * 删除促销活动
 * @param {number} id - 活动ID
 * @returns {Promise<void>}
 */
export function deletePromotionApi(id) {
  return del(`/marketing/promotions/${id}/`)
}

// ==================== Banner管理接口（管理员）====================

/**
 * 获取Banner列表（管理员）
 * @param {Object} params - 查询参数
 * @param {string} params.position - 位置筛选
 * @param {string} params.is_active - 是否启用
 * @param {number} params.page - 页码
 * @returns {Promise<Object>}
 */
export function getBannerListApi(params) {
  return get('/marketing/banners/', params)
}

/**
 * 获取Banner详情
 * @param {number} id - BannerID
 * @returns {Promise<Object>}
 */
export function getBannerDetailApi(id) {
  return get(`/marketing/banners/${id}/`)
}

/**
 * 创建Banner
 * @param {Object} data - Banner数据
 * @param {string} data.title - Banner标题
 * @param {string} data.image - 图片URL
 * @param {string} data.link - 跳转链接
 * @param {string} data.position - 位置 (home/promotion/category)
 * @param {number} data.sort_order - 排序权重
 * @param {string} data.start_time - 开始时间
 * @param {string} data.end_time - 结束时间
 * @param {boolean} data.is_active - 是否启用
 * @returns {Promise<Object>}
 */
export function createBannerApi(data) {
  return post('/marketing/banners/', data)
}

/**
 * 更新Banner
 * @param {number} id - BannerID
 * @param {Object} data - Banner数据
 * @returns {Promise<Object>}
 */
export function updateBannerApi(id, data) {
  return put(`/marketing/banners/${id}/`, data)
}

/**
 * 部分更新Banner
 * @param {number} id - BannerID
 * @param {Object} data - Banner数据
 * @returns {Promise<Object>}
 */
export function patchBannerApi(id, data) {
  return patch(`/marketing/banners/${id}/`, data)
}

/**
 * 删除Banner
 * @param {number} id - BannerID
 * @returns {Promise<void>}
 */
export function deleteBannerApi(id) {
  return del(`/marketing/banners/${id}/`)
}
