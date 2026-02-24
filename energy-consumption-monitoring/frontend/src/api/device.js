import request from '@/utils/request'

/**
 * Device API
 */

/**
 * Get energy types
 */
export function getEnergyTypes() {
  return request({
    url: '/energy-types/',
    method: 'get',
  })
}

/**
 * Get device list
 * @param {Object} params - Query parameters
 */
export function getDevices(params) {
  return request({
    url: '/devices/',
    method: 'get',
    params,
  })
}

/**
 * Get device detail
 * @param {number} id - Device ID
 */
export function getDevice(id) {
  return request({
    url: `/devices/${id}/`,
    method: 'get',
  })
}

/**
 * Create device
 * @param {Object} data - Device data
 */
export function createDevice(data) {
  return request({
    url: '/devices/',
    method: 'post',
    data,
  })
}

/**
 * Update device
 * @param {number} id - Device ID
 * @param {Object} data - Device data
 */
export function updateDevice(id, data) {
  return request({
    url: `/devices/${id}/`,
    method: 'put',
    data,
  })
}

/**
 * Delete device
 * @param {number} id - Device ID
 */
export function deleteDevice(id) {
  return request({
    url: `/devices/${id}/`,
    method: 'delete',
  })
}

/**
 * Get device data status
 */
export function getDeviceDataStatus(params) {
  return request({
    url: '/devices/data-status/',
    method: 'get',
    params,
  })
}

/**
 * Bind device to room
 * @param {number} id - Device ID
 * @param {Object} data - { room_id }
 */
export function bindDeviceRoom(id, data) {
  return request({
    url: `/devices/${id}/bind-room/`,
    method: 'post',
    data,
  })
}
