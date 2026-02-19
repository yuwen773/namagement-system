import request from '@/utils/request'

/**
 * Get national overview data
 */
export function getOverview() {
  return request({
    url: '/overview/',
    method: 'get'
  })
}

/**
 * Get top cities by AQI (best/worst)
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of cities to return (default: 10, range: 1-50)
 */
export function getTopCities(params = {}) {
  return request({
    url: '/overview/top-cities/',
    method: 'get',
    params
  })
}

/**
 * Get city details by city code
 * @param {string} code - City code
 */
export function getCityDetail(code) {
  return request({
    url: `/cities/${code}/`,
    method: 'get'
  })
}

/**
 * Get city trend data
 * @param {string} code - City code
 * @param {Object} params - Query parameters
 * @param {number} params.hours - Hours of data to retrieve (default: 24, range: 1-168)
 */
export function getCityTrend(code, params = {}) {
  return request({
    url: `/cities/${code}/trend/`,
    method: 'get',
    params
  })
}

/**
 * Get station details by station code
 * @param {string} code - Station code
 */
export function getStationDetail(code) {
  return request({
    url: `/stations/${code}/`,
    method: 'get'
  })
}

/**
 * Get station trend data
 * @param {string} code - Station code
 * @param {Object} params - Query parameters
 * @param {number} params.hours - Hours of data to retrieve (default: 24, range: 1-168)
 */
export function getStationTrend(code, params = {}) {
  return request({
    url: `/stations/${code}/trend/`,
    method: 'get',
    params
  })
}

/**
 * Get historical data with filters
 * @param {Object} params - Query parameters
 * @param {string} params.city_code - City code
 * @param {string} params.station_code - Station code
 * @param {string} params.start_date - Start date (YYYY-MM-DD)
 * @param {string} params.end_date - End date (YYYY-MM-DD)
 * @param {string} params.ordering - Ordering field (default: -monitor_time)
 * @param {number} params.page - Page number (default: 1, range: 1-100000)
 * @param {number} params.page_size - Page size (default: 20, range: 1-200)
 */
export function getHistoricalData(params) {
  return request({
    url: '/historical-data/',
    method: 'get',
    params
  })
}

/**
 * Export historical data
 * @param {Object} params - Query parameters
 * @param {string} params.format - Export format: 'csv' or 'xlsx' (default: 'csv')
 * @param {string} params.city_code - City code
 * @param {string} params.station_code - Station code
 * @param {string} params.start_date - Start date (YYYY-MM-DD)
 * @param {string} params.end_date - End date (YYYY-MM-DD)
 */
export function exportHistoricalData(params) {
  return request({
    url: '/historical-data/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * Compare cities
 * @param {Object} data - Request data
 * @param {string[]} data.city_codes - City codes to compare
 */
export function compareCities(data) {
  return request({
    url: '/analysis/compare/',
    method: 'post',
    data
  })
}

/**
 * Get correlation analysis data
 * @param {Object} params - Query parameters
 */
export function getCorrelationAnalysis(params) {
  return request({
    url: '/analysis/correlation/',
    method: 'get',
    params
  })
}

/**
 * Get AQI distribution
 * @param {Object} params - Query parameters
 */
export function getAQIDistribution(params) {
  return request({
    url: '/analysis/distribution/',
    method: 'get',
    params
  })
}

/**
 * Get protection guide
 * @param {Object} params - Query parameters
 * @param {string} params.city_code - City code
 */
export function getProtectionGuide(params) {
  return request({
    url: '/protection-guide/',
    method: 'get',
    params
  })
}

/**
 * Get articles list
 * @param {Object} params - Query parameters
 * @param {number} params.category_id - Category ID
 * @param {number} params.page - Page number (default: 1, range: 1-100000)
 * @param {number} params.page_size - Page size (default: 20, range: 1-200)
 */
export function getArticles(params) {
  return request({
    url: '/articles/',
    method: 'get',
    params
  })
}

/**
 * Get article detail
 * @param {number} id - Article ID
 */
export function getArticleDetail(id) {
  return request({
    url: `/articles/${id}/`,
    method: 'get'
  })
}

/**
 * Get categories
 */
export function getCategories() {
  return request({
    url: '/categories/',
    method: 'get'
  })
}

/**
 * Get announcements
 * @param {Object} params - Query parameters
 * @param {number} params.limit - Number of announcements to return (default: 5, range: 5-10)
 */
export function getAnnouncements(params = {}) {
  return request({
    url: '/announcements/',
    method: 'get',
    params
  })
}
