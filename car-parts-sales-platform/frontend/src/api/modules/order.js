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

// ========== 管理员端订单管理接口 ==========

/**
 * 订单发货
 * @param {number} id - 订单ID
 * @param {Object} data - 发货数据
 * @param {string} data.express_company - 物流公司
 * @param {string} data.tracking_number - 物流单号
 * @returns {Promise<Object>}
 */
export function shipOrderApi(id, data) {
  return post(`/orders/orders/${id}/ship/`, data)
}

/**
 * 更新订单状态/备注（管理员）
 * @param {number} id - 订单ID
 * @param {Object} data - 更新数据
 * @param {string} data.status - 订单状态
 * @param {string} data.remark - 备注
 * @returns {Promise<Object>}
 */
export function updateOrderStatusApi(id, data) {
  return patch(`/orders/orders/${id}/`, data)
}

/**
 * 处理退换货申请（管理员审核）
 * @param {number} id - 退换货申请ID
 * @param {Object} data - 处理数据
 * @param {string} data.status - 处理状态 (approved/rejected/completed)
 * @param {string} data.admin_note - 处理意见
 * @returns {Promise<Object>}
 */
export function processReturnApi(id, data) {
  return post(`/orders/returns/${id}/process/`, data)
}

/**
 * 获取交易统计数据（仪表盘）
 * @param {Object} params - 查询参数
 * @param {string} params.start_date - 开始日期 (可选)
 * @param {string} params.end_date - 结束日期 (可选)
 * @param {string} params.period - 统计周期 (day/week/month)
 * @returns {Promise<Object>}
 */
export function getOrderStatsApi(params) {
  return get('/orders/stats/', params)
}
