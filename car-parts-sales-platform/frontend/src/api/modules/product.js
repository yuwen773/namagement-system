import { get, post, put, patch, del } from '../request'

/**
 * 商品相关 API
 */

/**
 * 获取商品分类列表
 * @returns {Promise<Array>}
 */
export function getCategoryListApi() {
  return get('/products/categories/')
}

/**
 * 获取商品列表
 * @param {Object} params - 查询参数
 * @param {number} params.category_id - 分类ID
 * @param {number} params.min_price - 最低价格
 * @param {number} params.max_price - 最高价格
 * @param {string} params.ordering - 排序方式
 * @param {string} params.search - 搜索关键词
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise<Object>}
 */
export function getProductListApi(params) {
  return get('/products/products/', params)
}

/**
 * 获取商品详情
 * @param {number} id - 商品ID
 * @returns {Promise<Object>}
 */
export function getProductDetailApi(id) {
  return get(`/products/products/${id}/`)
}

/**
 * 获取商品评价列表
 * @param {number} productId - 商品ID
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getProductReviewsApi(productId, params) {
  return get(`/products/products/${productId}/reviews/`, params)
}

/**
 * 提交商品评价
 * @param {number} productId - 商品ID
 * @param {Object} data - 评价数据
 * @returns {Promise<Object>}
 */
export function createProductReviewApi(productId, data) {
  return post(`/products/products/${productId}/reviews/`, data)
}

/**
 * 获取我的评价列表
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getMyReviewsApi(params) {
  return get('/products/reviews/me/', params)
}

/**
 * 删除评价
 * @param {number} id - 评价ID
 * @returns {Promise<void>}
 */
export function deleteReviewApi(id) {
  return del(`/products/reviews/${id}/`)
}

/**
 * 增加商品浏览量
 * @param {number} id - 商品ID
 * @returns {Promise<void>}
 */
export function incrementProductViewsApi(id) {
  return post(`/products/products/${id}/view/`)
}
