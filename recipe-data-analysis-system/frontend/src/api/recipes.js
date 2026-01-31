import request from './auth'

/**
 * 获取菜谱列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码（默认1）
 * @param {number} params.page_size - 每页数量（默认20，最大100）
 * @param {string} params.ordering - 排序字段（view_count, -view_count, favorite_count, -favorite_count, created_at, -created_at）
 * @param {string} params.cuisine_type - 菜系筛选
 * @param {string} params.difficulty - 难度筛选（easy/medium/hard）
 * @param {string} params.scene_type - 场景筛选
 * @param {string} params.target_audience - 人群筛选
 * @returns {Promise} 菜谱列表
 */
export function getRecipeList(params) {
  return request.get('/api/recipes/', { params })
}

/**
 * 搜索菜谱
 * @param {Object} params - 查询参数
 * @param {string} params.keyword - 搜索关键词（必填）
 * @param {string} params.search_type - 搜索类型（name/ingredient，默认name）
 * @param {number} params.page - 页码（默认1）
 * @param {number} params.page_size - 每页数量（默认20，最大100）
 * @returns {Promise} 搜索结果
 */
export function searchRecipes(params) {
  return request.get('/api/recipes/search/', { params })
}

/**
 * 获取菜谱详情
 * @param {number} id - 菜谱ID
 * @returns {Promise} 菜谱详情
 */
export function getRecipeDetail(id) {
  return request.get(`/api/recipes/${id}/`)
}

/**
 * 获取热门菜谱
 * @param {Object} params - 查询参数
 * @param {string} params.sort_by - 排序方式（view_count/favorite_count，默认view_count）
 * @param {number} params.limit - 返回数量（1-50，默认20）
 * @returns {Promise} 热门菜谱列表
 */
export function getHotRecipes(params) {
  return request.get('/api/recipes/hot/', { params })
}

/**
 * 获取分类列表
 * @param {Object} params - 查询参数
 * @param {string} params.type - 分类类型（cuisine/scene/crowd/taste/difficulty）
 * @returns {Promise} 分类列表
 */
export function getCategories(params) {
  return request.get('/api/categories/', { params })
}

/**
 * 按类型获取分类
 * @param {string} type - 分类类型（cuisine/scene/crowd/taste/difficulty）
 * @returns {Promise} 分类列表
 */
export function getCategoriesByType(type) {
  return request.get(`/api/categories/${type}/`)
}

/**
 * 获取食材列表
 * @param {Object} params - 查询参数
 * @param {string} params.category - 食材分类
 * @param {string} params.search - 搜索关键词
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise} 食材列表
 */
export function getIngredients(params) {
  return request.get('/api/ingredients/', { params })
}

/**
 * 收藏菜谱
 * @param {number} recipeId - 菜谱ID
 * @returns {Promise} 收藏结果
 */
export function addFavorite(recipeId) {
  return request.post('/api/favorites/', { recipe_id: recipeId })
}

/**
 * 取消收藏
 * @param {number} recipeId - 菜谱ID
 * @returns {Promise} 取消收藏结果
 */
export function removeFavorite(recipeId) {
  return request.delete(`/api/favorites/${recipeId}/`)
}

/**
 * 检查收藏状态
 * @param {number} recipeId - 菜谱ID
 * @returns {Promise} 收藏状态
 */
export function checkFavoriteStatus(recipeId) {
  return request.get(`/api/favorites/check/${recipeId}/`)
}

/**
 * 获取收藏列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @param {string} params.ordering - 排序字段
 * @returns {Promise} 收藏列表
 */
export function getFavoriteList(params) {
  return request.get('/api/favorites/', { params })
}

// ===== 管理员菜谱管理 API =====

/**
 * 获取管理员菜谱列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码（默认1）
 * @param {number} params.page_size - 每页数量（默认20，最大100）
 * @param {string} params.search - 搜索关键词
 * @param {string} params.cuisine_type - 菜系筛选
 * @param {string} params.difficulty - 难度筛选
 * @param {string} params.scene_type - 场景筛选
 * @param {string} params.target_audience - 人群筛选
 * @param {string} params.ordering - 排序字段
 * @returns {Promise} 菜谱列表
 */
export function getAdminRecipeList(params) {
  return request.get('/api/admin/recipes/', { params })
}

/**
 * 创建菜谱（管理员）
 * @param {Object} data - 菜谱数据
 * @param {string} data.name - 菜谱名称（必填）
 * @param {string} data.cuisine_type - 菜系分类
 * @param {string} data.scene_type - 场景分类
 * @param {string} data.target_audience - 适用人群
 * @param {string} data.difficulty - 难度等级（easy/medium/hard）
 * @param {number} data.cooking_time - 烹饪时长（分钟）
 * @param {string} data.image_url - 成品图片URL
 * @param {string} data.steps - 制作步骤
 * @param {string} data.flavor_tags - 口味标签，逗号分隔
 * @param {Array} data.ingredients - 食材列表
 * @returns {Promise} 创建的菜谱
 */
export function createRecipe(data) {
  return request.post('/api/admin/recipes/create/', data)
}

/**
 * 更新菜谱（管理员）
 * @param {number} id - 菜谱ID
 * @param {Object} data - 菜谱数据（所有字段可选）
 * @returns {Promise} 更新后的菜谱
 */
export function updateRecipe(id, data) {
  return request.put(`/api/admin/recipes/${id}/update/`, data)
}

/**
 * 删除菜谱（管理员）
 * @param {number} id - 菜谱ID
 * @returns {Promise} 删除结果
 */
export function deleteRecipe(id) {
  return request.delete(`/api/admin/recipes/${id}/delete/`)
}

/**
 * 批量导入菜谱（管理员）
 * @param {File} file - 导入文件（CSV 或 JSON 格式）
 * @param {string} fileType - 文件类型（csv/json，可选，自动检测）
 * @returns {Promise} 导入结果
 */
export function importRecipes(file, fileType = '') {
  const formData = new FormData()
  formData.append('file', file)
  if (fileType) {
    formData.append('file_type', fileType)
  }
  return request.post('/api/admin/recipes/import/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export default {
  getRecipeList,
  searchRecipes,
  getRecipeDetail,
  getHotRecipes,
  getCategories,
  getCategoriesByType,
  getIngredients,
  addFavorite,
  removeFavorite,
  checkFavoriteStatus,
  getFavoriteList,
  // 管理员 API
  getAdminRecipeList,
  createRecipe,
  updateRecipe,
  deleteRecipe,
  importRecipes
}
