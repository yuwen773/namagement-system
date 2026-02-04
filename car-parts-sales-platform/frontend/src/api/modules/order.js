import { get, post, patch } from '../request'

/**
 * 订单相关 API
 */

/**
 * 创建订单
 * @param {Object} data - 订单数据
 * @param {number} data.address_id - 地址ID
 * @param {number} data.coupon_id - 优惠券ID（可选）
 * @returns {Promise<Object>}
 */
export function createOrderApi(data) {
  return post('/orders/orders/', data)
}

/**
 * 获取订单列表
 * @param {Object} params - 查询参数
 * @param {string} params.status - 订单状态
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise<Object>}
 */
export function getOrderListApi(params) {
  return get('/orders/orders/', params)
}

/**
 * 获取订单详情
 * @param {number} id - 订单ID
 * @returns {Promise<Object>}
 */
export function getOrderDetailApi(id) {
  return get(`/orders/orders/${id}/`)
}

/**
 * 支付订单
 * @param {number} id - 订单ID
 * @returns {Promise<Object>}
 */
export function payOrderApi(id) {
  return post(`/orders/orders/${id}/pay/`)
}

/**
 * 取消订单
 * @param {number} id - 订单ID
 * @returns {Promise<void>}
 */
export function cancelOrderApi(id) {
  return post(`/orders/orders/${id}/cancel/`)
}

/**
 * 确认收货
 * @param {number} id - 订单ID
 * @returns {Promise<void>}
 */
export function confirmOrderApi(id) {
  return post(`/orders/orders/${id}/confirm/`)
}

/**
 * 申请退换货
 * @param {number} id - 订单ID
 * @param {Object} data - 退换货数据
 * @returns {Promise<Object>}
 */
export function returnOrderApi(id, data) {
  return post(`/orders/orders/${id}/return/`, data)
}

/**
 * 获取售后申请列表
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getReturnListApi(params) {
  return get('/orders/returns/', params)
}

/**
 * 获取售后申请详情
 * @param {number} id - 售后ID
 * @returns {Promise<Object>}
 */
export function getReturnDetailApi(id) {
  return get(`/orders/returns/${id}/`)
}
