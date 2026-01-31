import request from './auth'

/**
 * 获取食材列表
 * @param {Object} params - 查询参数
 * @param {string} params.category - 食材分类筛选
 * @param {string} params.search - 搜索食材名称
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise} 食材列表
 */
export function getIngredients(params) {
  return request.get('/api/ingredients/', { params })
}

/**
 * 获取管理员食材列表
 * @param {Object} params - 查询参数
 * @param {string} params.category - 食材分类筛选
 * @param {string} params.search - 搜索食材名称
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise} 食材列表
 */
export function getAdminIngredientList(params) {
  return request.get('/api/admin/ingredients/', { params })
}

/**
 * 创建食材（管理员）
 * @param {Object} data - 食材数据
 * @param {string} data.name - 食材名称
 * @param {string} data.category - 食材分类
 * @returns {Promise} 创建的食材
 */
export function createIngredient(data) {
  return request.post('/api/admin/ingredients/create/', data)
}

/**
 * 更新食材（管理员）
 * @param {number} id - 食材ID
 * @param {Object} data - 食材数据
 * @returns {Promise} 更新后的食材
 */
export function updateIngredient(id, data) {
  return request.put(`/api/admin/ingredients/${id}/update/`, data)
}

/**
 * 删除食材（管理员）
 * @param {number} id - 食材ID
 * @returns {Promise} 删除结果
 */
export function deleteIngredient(id) {
  return request.delete(`/api/admin/ingredients/${id}/delete/`)
}

/**
 * 食材分类选项
 */
export const INGREDIENT_CATEGORIES = [
  { value: 'vegetable', label: '蔬菜' },
  { value: 'meat', label: '肉类' },
  { value: 'seafood', label: '海鲜' },
  { value: 'seasoning', label: '调料' },
  { value: 'fruit', label: '水果' },
  { value: 'grain', label: '谷物' },
  { value: 'dairy', label: '乳制品' },
  { value: 'other', label: '其他' }
]

export default {
  getIngredients,
  getAdminIngredientList,
  createIngredient,
  updateIngredient,
  deleteIngredient,
  INGREDIENT_CATEGORIES
}
