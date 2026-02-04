import { get, post, put, del } from '../request'

/**
 * 购物车相关 API
 */

/**
 * 获取购物车
 * @returns {Promise<Object>}
 */
export function getCartApi() {
  return get('/orders/cart/')
}

/**
 * 添加商品到购物车
 * @param {Object} data - 购物车数据
 * @param {number} data.product_id - 商品ID
 * @param {number} data.quantity - 数量
 * @returns {Promise<Object>}
 */
export function addCartItemApi(data) {
  return post('/orders/cart/items/', data)
}

/**
 * 更新购物车商品数量
 * @param {number} id - 购物车项ID
 * @param {Object} data - 更新数据
 * @param {number} data.quantity - 数量
 * @returns {Promise<Object>}
 */
export function updateCartItemApi(id, data) {
  return put(`/orders/cart/items/${id}/`, data)
}

/**
 * 删除购物车商品
 * @param {number} id - 购物车项ID
 * @returns {Promise<void>}
 */
export function deleteCartItemApi(id) {
  return del(`/orders/cart/items/${id}/`)
}

/**
 * 清空购物车
 * @returns {Promise<void>}
 */
export function clearCartApi() {
  return del('/orders/cart/clear/')
}
