import { get, post, put, patch, del } from '../request'

/**
 * 商品相关 API
 */

/**
 * 获取商品分类列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise<Array>}
 */
export function getCategoryListApi(params) {
  return get('/products/categories/', params)
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

// ==================== 管理员专用接口 ====================

/**
 * 获取商品分类树
 * @returns {Promise<Array>}
 */
export function getCategoryTreeApi() {
  return get('/products/categories/tree/')
}

/**
 * 创建商品分类
 * @param {Object} data - 分类数据
 * @returns {Promise<Object>}
 */
export function createCategoryApi(data) {
  return post('/products/categories/', data)
}

/**
 * 更新商品分类
 * @param {number} id - 分类ID
 * @param {Object} data - 分类数据
 * @returns {Promise<Object>}
 */
export function updateCategoryApi(id, data) {
  return put(`/products/categories/${id}/`, data)
}

/**
 * 删除商品分类
 * @param {number} id - 分类ID
 * @returns {Promise<void>}
 */
export function deleteCategoryApi(id) {
  return del(`/products/categories/${id}/`)
}

/**
 * 创建商品
 * @param {Object} data - 商品数据
 * @returns {Promise<Object>}
 */
export function createProductApi(data) {
  return post('/products/products/', data)
}

/**
 * 更新商品
 * @param {number} id - 商品ID
 * @param {Object} data - 商品数据
 * @returns {Promise<Object>}
 */
export function updateProductApi(id, data) {
  return put(`/products/products/${id}/`, data)
}

/**
 * 部分更新商品
 * @param {number} id - 商品ID
 * @param {Object} data - 商品数据
 * @returns {Promise<Object>}
 */
export function patchProductApi(id, data) {
  return patch(`/products/products/${id}/`, data)
}

/**
 * 删除商品
 * @param {number} id - 商品ID
 * @returns {Promise<void>}
 */
export function deleteProductApi(id) {
  return del(`/products/products/${id}/`)
}

/**
 * 发布商品
 * @param {number} id - 商品ID
 * @returns {Promise<Object>}
 */
export function publishProductApi(id) {
  return post(`/products/products/${id}/publish/`)
}

/**
 * 下架商品
 * @param {number} id - 商品ID
 * @returns {Promise<Object>}
 */
export function archiveProductApi(id) {
  return post(`/products/products/${id}/archive/`)
}

/**
 * 获取商品属性列表
 * @param {number} productId - 商品ID
 * @returns {Promise<Array>}
 */
export function getProductAttributesApi(productId) {
  return get('/products/attributes/', { product: productId })
}

/**
 * 创建商品属性
 * @param {Object} data - 属性数据
 * @returns {Promise<Object>}
 */
export function createProductAttributeApi(data) {
  return post('/products/attributes/', data)
}

/**
 * 更新商品属性
 * @param {number} id - 属性ID
 * @param {Object} data - 属性数据
 * @returns {Promise<Object>}
 */
export function updateProductAttributeApi(id, data) {
  return put(`/products/attributes/${id}/`, data)
}

/**
 * 删除商品属性
 * @param {number} id - 属性ID
 * @returns {Promise<void>}
 */
export function deleteProductAttributeApi(id) {
  return del(`/products/attributes/${id}/`)
}

/**
 * 获取商品图片列表
 * @param {number} productId - 商品ID
 * @returns {Promise<Array>}
 */
export function getProductImagesApi(productId) {
  return get('/products/images/', { product: productId })
}

/**
 * 创建商品图片
 * @param {Object} data - 图片数据
 * @returns {Promise<Object>}
 */
export function createProductImageApi(data) {
  return post('/products/images/', data)
}

/**
 * 更新商品图片
 * @param {number} id - 图片ID
 * @param {Object} data - 图片数据
 * @returns {Promise<Object>}
 */
export function updateProductImageApi(id, data) {
  return put(`/products/images/${id}/`, data)
}

/**
 * 删除商品图片
 * @param {number} id - 图片ID
 * @returns {Promise<void>}
 */
export function deleteProductImageApi(id) {
  return del(`/products/images/${id}/`)
}
