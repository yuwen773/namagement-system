import request from '@/utils/request'

/**
 * Analysis API
 */

/**
 * Get dashboard data
 * @param {Object} params - Query parameters (start_date, end_date, campus_id, building_id, room_id, energy_type, device_id)
 */
export function getDashboardData(params) {
  return request({
    url: '/analysis/dashboard/',
    method: 'get',
    params,
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
 * Get user achievements
 */
export function getAchievements() {
  return request({
    url: '/analysis/achievements/',
    method: 'get',
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

/**
 * Get hourly energy distribution
 * @param {Object} params - Query parameters
 */
export function getHourlyDistribution(params) {
  return request({
    url: '/analysis/hourly-distribution/',
    method: 'get',
    params,
  })
}
