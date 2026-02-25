import request from '@/utils/request'

/**
 * Analysis API
 */

/**
 * Get dashboard data
 */
export function getDashboardData() {
  return request({
    url: '/analysis/dashboard/',
    method: 'get',
  })
}

/**
 * Get energy trend data
 * @param {Object} params - Query parameters
 */
export function getTrendData(params) {
  return request({
    url: '/analysis/trend/',
    method: 'get',
    params,
  })
}

/**
 * Get energy distribution data
 * @param {Object} params - Query parameters
 */
export function getDistributionData(params) {
  return request({
    url: '/analysis/distribution/',
    method: 'get',
    params,
  })
}

/**
 * Get energy ranking data
 * @param {Object} params - Query parameters
 */
export function getRankingData(params) {
  return request({
    url: '/analysis/ranking/',
    method: 'get',
    params,
  })
}

/**
 * Get comparison data
 * @param {Object} params - Query parameters
 */
export function getComparisonData(params) {
  return request({
    url: '/analysis/comparison/',
    method: 'get',
    params,
  })
}

/**
 * Get forecast data
 * @param {Object} params - Query parameters
 */
export function getForecastData(params) {
  return request({
    url: '/analysis/forecast/',
    method: 'get',
    params,
  })
}

/**
 * Get real-time power data
 * @param {Object} params - Query parameters
 */
export function getRealTimePowerData(params) {
  return request({
    url: '/analysis/real-time-power/',
    method: 'get',
    params,
  })
}
