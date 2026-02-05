import { get, post, put, patch, del } from '../request'

/**
 * 内容管理相关 API
 * 包含改装案例 (ModificationCase) 和常见问题 (FAQ)
 */

// ==================== 改装案例相关接口 ====================

/**
 * 获取改装案例列表
 * @param {Object} params - 查询参数
 * @param {string} params.status - 案例状态筛选
 * @param {string} params.ordering - 排序字段
 * @param {string} params.search - 搜索关键词
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise<Object>}
 */
export function getCasesListApi(params) {
  return get('/content/cases/', params)
}

/**
 * 获取案例详情
 * @param {number} id - 案例ID
 * @returns {Promise<Object>}
 */
export function getCaseDetailApi(id) {
  return get(`/content/cases/${id}/`)
}

/**
 * 创建改装案例
 * @param {Object} data - 案例数据
 * @param {string} data.title - 案例标题
 * @param {string} data.summary - 案例摘要
 * @param {string} data.content - 案例详细内容
 * @param {string} data.cover_image - 封面图片URL
 * @param {string} data.author - 作者
 * @param {string} data.status - 状态 (draft/published)
 * @param {number} data.sort_order - 排序值
 * @param {string} data.published_at - 发布时间
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
 * 部分更新改装案例
 * @param {number} id - 案例ID
 * @param {Object} data - 案例数据
 * @returns {Promise<Object>}
 */
export function patchCaseApi(id, data) {
  return patch(`/content/cases/${id}/`, data)
}

/**
 * 删除改装案例
 * @param {number} id - 案例ID
 * @returns {Promise<void>}
 */
export function deleteCaseApi(id) {
  return del(`/content/cases/${id}/`)
}

// ==================== FAQ 相关接口 ====================

/**
 * 获取 FAQ 列表
 * @param {Object} params - 查询参数
 * @param {string} params.category - 问题分类
 * @param {string} params.is_active - 是否启用
 * @param {string} params.ordering - 排序字段
 * @param {string} params.search - 搜索关键词
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise<Object>}
 */
export function getFAQListApi(params) {
  return get('/content/faqs/', params)
}

/**
 * 获取 FAQ 详情
 * @param {number} id - FAQ ID
 * @returns {Promise<Object>}
 */
export function getFAQDetailApi(id) {
  return get(`/content/faqs/${id}/`)
}

/**
 * 创建 FAQ
 * @param {Object} data - FAQ 数据
 * @param {string} data.question - 问题
 * @param {string} data.answer - 答案
 * @param {string} data.category - 分类 (order/payment/shipping/product/return/other)
 * @param {number} data.sort_order - 排序值
 * @param {boolean} data.is_active - 是否启用
 * @returns {Promise<Object>}
 */
export function createFAQApi(data) {
  return post('/content/faqs/', data)
}

/**
 * 更新 FAQ
 * @param {number} id - FAQ ID
 * @param {Object} data - FAQ 数据
 * @returns {Promise<Object>}
 */
export function updateFAQApi(id, data) {
  return put(`/content/faqs/${id}/`, data)
}

/**
 * 部分更新 FAQ
 * @param {number} id - FAQ ID
 * @param {Object} data - FAQ 数据
 * @returns {Promise<Object>}
 */
export function patchFAQApi(id, data) {
  return patch(`/content/faqs/${id}/`, data)
}

/**
 * 删除 FAQ
 * @param {number} id - FAQ ID
 * @returns {Promise<void>}
 */
export function deleteFAQApi(id) {
  return del(`/content/faqs/${id}/`)
}

// ==================== 工具函数 ====================

/**
 * 获取案例状态标签
 * @param {string} status - 状态值
 * @returns {string}
 */
export function getCaseStatusLabel(status) {
  const statusMap = {
    draft: '草稿',
    published: '已发布'
  }
  return statusMap[status] || status
}

/**
 * 获取案例状态类型
 * @param {string} status - 状态值
 * @returns {string}
 */
export function getCaseStatusType(status) {
  const typeMap = {
    draft: 'info',
    published: 'success'
  }
  return typeMap[status] || 'info'
}

/**
 * 获取 FAQ 分类标签
 * @param {string} category - 分类值
 * @returns {string}
 */
export function getFAQCategoryLabel(category) {
  const categoryMap = {
    order: '订单相关',
    payment: '支付相关',
    shipping: '物流相关',
    product: '商品相关',
    return: '退换货',
    other: '其他问题'
  }
  return categoryMap[category] || category
}

/**
 * 获取 FAQ 分类类型颜色
 * @param {string} category - 分类值
 * @returns {string}
 */
export function getFAQCategoryType(category) {
  const typeMap = {
    order: 'primary',
    payment: 'success',
    shipping: 'warning',
    product: 'info',
    return: 'danger',
    other: 'info'
  }
  return typeMap[category] || 'info'
}
