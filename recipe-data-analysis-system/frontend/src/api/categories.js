import request from './auth'

/**
 * 分类类型选项
 */
export const CATEGORY_TYPES = [
  { value: 'cuisine', label: '菜系' },
  { value: 'scene', label: '场景' },
  { value: 'crowd', label: '人群' },
  { value: 'taste', label: '口味' },
  { value: 'difficulty', label: '难度' }
]

/**
 * 获取管理员分类列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码（默认1）
 * @param {number} params.page_size - 每页数量（默认20，最大100）
 * @param {string} params.type - 分类类型筛选（可选）
 * @param {string} params.search - 搜索关键词（可选，搜索分类名称）
 * @returns {Promise} 分类列表
 */
export function getAdminCategoryList(params) {
  return request.get('/api/admin/categories/', { params })
}

/**
 * 创建分类（管理员）
 * @param {Object} data - 分类数据
 * @param {string} data.name - 分类名称（必填）
 * @param {string} data.type - 分类类型（必填，可选值：cuisine/scene/crowd/taste/difficulty）
 * @param {number} data.sort_order - 排序序号（可选，默认0）
 * @returns {Promise} 创建的分类
 */
export function createCategory(data) {
  return request.post('/api/admin/categories/create/', data)
}

/**
 * 更新分类（管理员）
 * @param {number} id - 分类ID
 * @param {Object} data - 分类数据（所有字段可选）
 * @param {string} data.name - 分类名称
 * @param {string} data.type - 分类类型
 * @param {number} data.sort_order - 排序序号
 * @returns {Promise} 更新后的分类
 */
export function updateCategory(id, data) {
  return request.put(`/api/admin/categories/${id}/update/`, data)
}

/**
 * 删除分类（管理员）
 * @param {number} id - 分类ID
 * @returns {Promise} 删除结果
 */
export function deleteCategory(id) {
  return request.delete(`/api/admin/categories/${id}/delete/`)
}

/**
 * 获取分类列表（普通用户）
 * @param {Object} params - 查询参数
 * @param {string} params.type - 分类类型（可选）
 * @returns {Promise} 分类列表
 */
export function getCategories(params) {
  return request.get('/api/categories/', { params })
}

/**
 * 按类型获取分类（普通用户）
 * @param {string} type - 分类类型（cuisine/scene/crowd/taste/difficulty）
 * @returns {Promise} 分类列表
 */
export function getCategoriesByType(type) {
  return request.get(`/api/categories/${type}/`)
}

export default {
  CATEGORY_TYPES,
  getAdminCategoryList,
  createCategory,
  updateCategory,
  deleteCategory,
  getCategories,
  getCategoriesByType
}
