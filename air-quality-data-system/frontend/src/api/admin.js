import request from '@/utils/request'

/**
 * Get admin dashboard data
 */
export function getDashboardData() {
  return request({
    url: '/admin/dashboard/',
    method: 'get'
  })
}

/**
 * Upload data file for import
 * @param {FormData} formData - File data
 */
export function uploadDataFile(formData) {
  return request({
    url: '/admin/data-import/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * Get import task list
 * @param {Object} params - Query parameters
 */
export function getImportTasks(params) {
  return request({
    url: '/admin/data-import/tasks/',
    method: 'get',
    params
  })
}

/**
 * Get import task detail
 * @param {string} taskId - Task ID
 */
export function getImportTaskDetail(taskId) {
  return request({
    url: `/admin/data-import/tasks/${taskId}/`,
    method: 'get'
  })
}

/**
 * Get import task logs
 * @param {string} taskId - Task ID
 */
export function getImportTaskLogs(taskId) {
  return request({
    url: `/admin/data-import/tasks/${taskId}/logs/`,
    method: 'get'
  })
}

/**
 * Get air quality data list (admin)
 * @param {Object} params - Query parameters
 */
export function getAirQualityDataList(params) {
  return request({
    url: '/admin/air-quality/',
    method: 'get',
    params
  })
}

/**
 * Update air quality data
 * @param {number} id - Data ID
 * @param {Object} data - Data to update
 */
export function updateAirQualityData(id, data) {
  return request({
    url: `/admin/air-quality/${id}/`,
    method: 'put',
    data
  })
}

/**
 * Delete air quality data
 * @param {number} id - Data ID
 */
export function deleteAirQualityData(id) {
  return request({
    url: `/admin/air-quality/${id}/`,
    method: 'delete'
  })
}

/**
 * Get protection rules list
 */
export function getRulesList() {
  return request({
    url: '/admin/rules/',
    method: 'get'
  })
}

/**
 * Create protection rule
 * @param {Object} data - Rule data
 */
export function createRule(data) {
  return request({
    url: '/admin/rules/',
    method: 'post',
    data
  })
}

/**
 * Update protection rule
 * @param {number} id - Rule ID
 * @param {Object} data - Rule data
 */
export function updateRule(id, data) {
  return request({
    url: `/admin/rules/${id}/`,
    method: 'put',
    data
  })
}

/**
 * Delete protection rule
 * @param {number} id - Rule ID
 */
export function deleteRule(id) {
  return request({
    url: `/admin/rules/${id}/`,
    method: 'delete'
  })
}

/**
 * Batch update rules status
 * @param {Object} data - { ids: number[], is_enabled: boolean }
 */
export function batchUpdateRules(data) {
  return request({
    url: '/admin/rules/batch/',
    method: 'post',
    data
  })
}

/**
 * Get users list
 * @param {Object} params - Query parameters
 */
export function getUsersList(params) {
  return request({
    url: '/admin/users/',
    method: 'get',
    params
  })
}

/**
 * Update user
 * @param {number} id - User ID
 * @param {Object} data - User data
 */
export function updateUser(id, data) {
  return request({
    url: `/admin/users/${id}/`,
    method: 'put',
    data
  })
}

/**
 * Delete user (soft delete)
 * @param {number} id - User ID
 */
export function deleteUser(id) {
  return request({
    url: `/admin/users/${id}/`,
    method: 'delete'
  })
}

/**
 * Get articles list (admin)
 * @param {Object} params - Query parameters
 */
export function getAdminArticles(params) {
  return request({
    url: '/admin/articles/',
    method: 'get',
    params
  })
}

/**
 * Create article
 * @param {Object} data - Article data
 */
export function createArticle(data) {
  return request({
    url: '/admin/articles/',
    method: 'post',
    data
  })
}

/**
 * Update article
 * @param {number} id - Article ID
 * @param {Object} data - Article data
 */
export function updateArticle(id, data) {
  return request({
    url: `/admin/articles/${id}/`,
    method: 'put',
    data
  })
}

/**
 * Delete article
 * @param {number} id - Article ID
 */
export function deleteArticle(id) {
  return request({
    url: `/admin/articles/${id}/`,
    method: 'delete'
  })
}

/**
 * Get categories list (admin)
 */
export function getAdminCategories() {
  return request({
    url: '/admin/categories/',
    method: 'get'
  })
}

/**
 * Create category
 * @param {Object} data - Category data
 */
export function createCategory(data) {
  return request({
    url: '/admin/categories/',
    method: 'post',
    data
  })
}

/**
 * Update category
 * @param {number} id - Category ID
 * @param {Object} data - Category data
 */
export function updateCategory(id, data) {
  return request({
    url: `/admin/categories/${id}/`,
    method: 'put',
    data
  })
}

/**
 * Delete category
 * @param {number} id - Category ID
 */
export function deleteCategory(id) {
  return request({
    url: `/admin/categories/${id}/`,
    method: 'delete'
  })
}

/**
 * Get operation logs
 * @param {Object} params - Query parameters
 */
export function getOperationLogs(params) {
  return request({
    url: '/admin/logs/operations/',
    method: 'get',
    params
  })
}

/**
 * Get error logs
 * @param {Object} params - Query parameters
 */
export function getErrorLogs(params) {
  return request({
    url: '/admin/logs/errors/',
    method: 'get',
    params
  })
}
