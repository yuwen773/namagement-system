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
 */
export function getTopCities() {
  return request({
    url: '/overview/top-cities/',
    method: 'get'
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
 * Get city trend data (24 hours)
 * @param {string} code - City code
 */
export function getCityTrend(code) {
  return request({
    url: `/cities/${code}/trend/`,
    method: 'get'
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
 * Get station trend data (24 hours)
 * @param {string} code - Station code
 */
export function getStationTrend(code) {
  return request({
    url: `/stations/${code}/trend/`,
    method: 'get'
  })
}

/**
 * Get historical data with filters
 * @param {Object} params - Query parameters
 * @param {string} params.city - City code
 * @param {string} params.start_date - Start date
 * @param {string} params.end_date - End date
 * @param {number} params.page - Page number
 * @param {number} params.page_size - Page size
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
 * @param {number} params.category - Category ID
 * @param {number} params.page - Page number
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
 */
export function getAnnouncements() {
  return request({
    url: '/announcements/',
    method: 'get'
  })
}
