import request from '@/utils/request'

/**
 * Alarm API
 */

/**
 * Get alarm rules
 * @param {Object} params - Query parameters
 */
export function getAlarmRules(params) {
  return request({
    url: '/alarm-rules/',
    method: 'get',
    params,
  })
}

/**
 * Create alarm rule
 * @param {Object} data - Rule data
 */
export function createAlarmRule(data) {
  return request({
    url: '/alarm-rules/',
    method: 'post',
    data,
  })
}

/**
 * Get alarm rule detail
 * @param {number} id - Rule ID
 */
export function getAlarmRule(id) {
  return request({
    url: `/alarm-rules/${id}/`,
    method: 'get',
  })
}

/**
 * Update alarm rule
 * @param {number} id - Rule ID
 * @param {Object} data - Rule data
 */
export function updateAlarmRule(id, data) {
  return request({
    url: `/alarm-rules/${id}/`,
    method: 'put',
    data,
  })
}

/**
 * Partial update alarm rule
 * @param {number} id - Rule ID
 * @param {Object} data - Rule data
 */
export function patchAlarmRule(id, data) {
  return request({
    url: `/alarm-rules/${id}/`,
    method: 'patch',
    data,
  })
}

/**
 * Delete alarm rule
 * @param {number} id - Rule ID
 */
export function deleteAlarmRule(id) {
  return request({
    url: `/alarm-rules/${id}/`,
    method: 'delete',
  })
}

/**
 * Get alarms
 * @param {Object} params - Query parameters
 */
export function getAlarms(params) {
  return request({
    url: '/alarms/',
    method: 'get',
    params,
  })
}

/**
 * Get alarm detail
 * @param {number} id - Alarm ID
 */
export function getAlarm(id) {
  return request({
    url: `/alarms/${id}/`,
    method: 'get',
  })
}

/**
 * Handle alarm
 * @param {number} id - Alarm ID
 * @param {Object} data - Handle data
 */
export function handleAlarm(id, data) {
  return request({
    url: `/alarms/${id}/handle/`,
    method: 'post',
    data,
  })
}

/**
 * Get alarm statistics
 */
export function getAlarmStatistics() {
  return request({
    url: '/alarms/statistics/',
    method: 'get',
  })
}
