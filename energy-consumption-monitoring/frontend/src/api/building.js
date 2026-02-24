import request from '@/utils/request'

/**
 * Building API
 */

/**
 * Get campus list
 */
export function getCampuses() {
  return request({
    url: '/campuses/',
    method: 'get',
  })
}

/**
 * Get campus detail
 * @param {number} id - Campus ID
 */
export function getCampus(id) {
  return request({
    url: `/campuses/${id}/`,
    method: 'get',
  })
}

/**
 * Get building list
 * @param {Object} params - Query parameters
 */
export function getBuildings(params) {
  return request({
    url: '/buildings/',
    method: 'get',
    params,
  })
}

/**
 * Get building detail
 * @param {number} id - Building ID
 */
export function getBuilding(id) {
  return request({
    url: `/buildings/${id}/`,
    method: 'get',
  })
}

/**
 * Create building
 * @param {Object} data - Building data
 */
export function createBuilding(data) {
  return request({
    url: '/buildings/',
    method: 'post',
    data,
  })
}

/**
 * Update building
 * @param {number} id - Building ID
 * @param {Object} data - Building data
 */
export function updateBuilding(id, data) {
  return request({
    url: `/buildings/${id}/`,
    method: 'put',
    data,
  })
}

/**
 * Delete building
 * @param {number} id - Building ID
 */
export function deleteBuilding(id) {
  return request({
    url: `/buildings/${id}/`,
    method: 'delete',
  })
}

/**
 * Get building tree structure
 */
export function getBuildingTree() {
  return request({
    url: '/buildings/tree/',
    method: 'get',
  })
}

/**
 * Get floors
 * @param {Object} params - Query parameters
 */
export function getFloors(params) {
  return request({
    url: '/floors/',
    method: 'get',
    params,
  })
}

/**
 * Get rooms
 * @param {Object} params - Query parameters
 */
export function getRooms(params) {
  return request({
    url: '/rooms/',
    method: 'get',
    params,
  })
}
