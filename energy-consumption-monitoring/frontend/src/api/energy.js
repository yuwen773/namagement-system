import request from '@/utils/request'

/**
 * Energy Data API
 */

/**
 * Get energy data list
 * @param {Object} params - Query parameters
 */
export function getEnergyData(params) {
  return request({
    url: '/energy-data/',
    method: 'get',
    params,
  })
}

/**
 * Create single energy data record
 * @param {Object} data - Energy data
 */
export function createEnergyData(data) {
  return request({
    url: '/energy-data/',
    method: 'post',
    data,
  })
}

/**
 * Batch import energy data
 * @param {FormData} data - File data
 */
export function batchImportEnergyData(data) {
  return request({
    url: '/energy-data/batch-import/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}

/**
 * Get latest energy data
 * @param {Object} params - Query parameters
 */
export function getLatestEnergyData(params) {
  return request({
    url: '/energy-data/latest/',
    method: 'get',
    params,
  })
}

/**
 * Get energy statistics
 * @param {Object} params - Query parameters
 */
export function getEnergyStatistics(params) {
  return request({
    url: '/energy-statistics/',
    method: 'get',
    params,
  })
}

/**
 * Export energy data
 * @param {Object} params - Query parameters
 */
export function exportEnergyData(params) {
  return request({
    url: '/energy-data/export/',
    method: 'get',
    params,
    responseType: 'blob',
  })
}

/**
 * Get energy data details (for data table in analysis page)
 * @param {Object} params - Query parameters
 */
export function getEnergyDataDetails(params) {
  return request({
    url: '/energy-data/',
    method: 'get',
    params,
  })
}
