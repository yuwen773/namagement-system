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
 * @param {string} dataset_type - Type of dataset: provinces, cities, stations, air_quality_data
 */
export function uploadDataFile(formData, datasetType) {
  return request({
    url: '/admin/data-import/',
    method: 'post',
    data: formData,
    params: { dataset_type: datasetType },
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
 * @param {Object} params - Query parameters
 * @param {number} params.page - Page number (default: 1)
 * @param {number} params.page_size - Page size (default: 50)
 */
export function getImportTaskLogs(taskId, params = {}) {
  return request({
    url: `/admin/data-import/tasks/${taskId}/logs/`,
    method: 'get',
    params
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
 * @param {Object} data - Data to update (must include id)
 * @param {number} data.id - Data ID (required)
 * @param {number} data.station_id - Station ID
 * @param {string} data.monitor_time - Monitor time
 * @param {number} data.aqi - AQI value
 * @param {number} data.pm25 - PM2.5 value
 * @param {number} data.pm10 - PM10 value
 * @param {number} data.so2 - SO2 value
 * @param {number} data.no2 - NO2 value
 * @param {number} data.co - CO value
 * @param {number} data.o3 - O3 value
 */
export function updateAirQualityData(data) {
  return request({
    url: '/admin/air-quality/',
    method: 'put',
    data
  })
}

/**
 * Delete air quality data (single or batch)
 * @param {Object} data - Delete parameters
 * @param {number} data.id - Single data ID (optional, mutually exclusive with ids)
 * @param {number[]} data.ids - Array of data IDs for batch delete (optional, mutually exclusive with id)
 */
export function deleteAirQualityData(data) {
  return request({
    url: '/admin/air-quality/',
    method: 'delete',
    data
  })
}

/**
 * Helper function to delete single air quality data by ID
 * @param {number} id - Data ID
 */
export function deleteAirQualityDataById(id) {
  return deleteAirQualityData({ id })
}

/**
 * Helper function to batch delete air quality data by IDs
 * @param {number[]} ids - Array of data IDs
 */
export function deleteAirQualityDataByIds(ids) {
  return deleteAirQualityData({ ids })
}

/**
 * Get protection rules list
 * @param {Object} params - Query parameters
 * @param {string} params.population_type - Population type filter (GENERAL, CHILDREN, ELDERLY, PATIENTS, SENSITIVE)
 * @param {boolean} params.is_enabled - Enable status filter
 * @param {string} params.keyword - Keyword search in rule_name or advice
 */
export function getRulesList(params = {}) {
  return request({
    url: '/admin/rules/',
    method: 'get',
    params
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
 * Delete protection rule (single or batch)
 * @param {Object} data - Delete parameters
 * @param {number} data.id - Single rule ID (optional, mutually exclusive with ids)
 * @param {number[]} data.ids - Array of rule IDs for batch delete (optional, mutually exclusive with id)
 */
export function deleteRule(data) {
  return request({
    url: '/admin/rules/',
    method: 'delete',
    data
  })
}

/**
 * Helper function to delete single rule by ID
 * @param {number} id - Rule ID
 */
export function deleteRuleById(id) {
  return deleteRule({ id })
}

/**
 * Helper function to batch delete rules by IDs
 * @param {number[]} ids - Array of rule IDs
 */
export function deleteRuleByIds(ids) {
  return deleteRule({ ids })
}

/**
 * Batch update rules status
 * @param {Object} data - Batch update parameters
 * @param {number[]} data.ids - Array of rule IDs
 * @param {boolean} data.is_enabled - Enable/disable status
 */
export function batchUpdateRules(data) {
  return request({
    url: '/admin/rules/',
    method: 'put',
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
 * Delete user (soft delete, single or batch)
 * @param {Object} data - Delete parameters
 * @param {number} data.id - Single user ID (optional, mutually exclusive with ids)
 * @param {number[]} data.ids - Array of user IDs for batch delete (optional, mutually exclusive with id)
 */
export function deleteUser(data) {
  return request({
    url: '/admin/users/',
    method: 'delete',
    data
  })
}

/**
 * Helper function to delete single user by ID
 * @param {number} id - User ID
 */
export function deleteUserById(id) {
  return deleteUser({ id })
}

/**
 * Helper function to batch delete users by IDs
 * @param {number[]} ids - Array of user IDs
 */
export function deleteUserByIds(ids) {
  return deleteUser({ ids })
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
 * Delete article (single or batch)
 * @param {Object} data - Delete parameters
 * @param {number} data.id - Single article ID (optional, mutually exclusive with ids)
 * @param {number[]} data.ids - Array of article IDs for batch delete (optional, mutually exclusive with id)
 */
export function deleteArticle(data) {
  return request({
    url: '/admin/articles/',
    method: 'delete',
    data
  })
}

/**
 * Helper function to delete single article by ID
 * @param {number} id - Article ID
 */
export function deleteArticleById(id) {
  return deleteArticle({ id })
}

/**
 * Helper function to batch delete articles by IDs
 * @param {number[]} ids - Array of article IDs
 */
export function deleteArticleByIds(ids) {
  return deleteArticle({ ids })
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
 * Delete category (single or batch)
 * @param {Object} data - Delete parameters
 * @param {number} data.id - Single category ID (optional, mutually exclusive with ids)
 * @param {number[]} data.ids - Array of category IDs for batch delete (optional, mutually exclusive with id)
 */
export function deleteCategory(data) {
  return request({
    url: '/admin/categories/',
    method: 'delete',
    data
  })
}

/**
 * Helper function to delete single category by ID
 * @param {number} id - Category ID
 */
export function deleteCategoryById(id) {
  return deleteCategory({ id })
}

/**
 * Helper function to batch delete categories by IDs
 * @param {number[]} ids - Array of category IDs
 */
export function deleteCategoryByIds(ids) {
  return deleteCategory({ ids })
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

/**
 * Get system logs
 * @param {Object} params - Query parameters
 * @param {string} params.level - Log level filter (DEBUG, INFO, WARNING, ERROR, CRITICAL)
 * @param {string} params.module - Module filter
 * @param {string} params.search - Keyword search
 * @param {string} params.start_time - Start time filter
 * @param {string} params.end_time - End time filter
 */
export function getSystemLogs(params) {
  return request({
    url: '/admin/logs/system/',
    method: 'get',
    params
  })
}
