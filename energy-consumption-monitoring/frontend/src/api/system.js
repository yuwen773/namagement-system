import request from '@/utils/request'

/**
 * System API
 */

/**
 * Get users
 * @param {Object} params - Query parameters
 */
export function getUsers(params) {
  return request({
    url: '/users/',
    method: 'get',
    params,
  })
}

/**
 * Get user detail
 * @param {number} id - User ID
 */
export function getUser(id) {
  return request({
    url: `/users/${id}/`,
    method: 'get',
  })
}

/**
 * Create user
 * @param {Object} data - User data
 */
export function createUser(data) {
  return request({
    url: '/users/',
    method: 'post',
    data,
  })
}

/**
 * Update user
 * @param {number} id - User ID
 * @param {Object} data - User data
 */
export function updateUser(id, data) {
  return request({
    url: `/users/${id}/`,
    method: 'put',
    data,
  })
}

/**
 * Delete user
 * @param {number} id - User ID
 */
export function deleteUser(id) {
  return request({
    url: `/users/${id}/`,
    method: 'delete',
  })
}

/**
 * Reset user password
 * @param {number} id - User ID
 * @param {Object} data - { new_password }
 */
export function resetUserPassword(id, data) {
  return request({
    url: `/users/${id}/reset-password/`,
    method: 'post',
    data,
  })
}

/**
 * Get roles
 * @param {Object} params - Query parameters
 */
export function getRoles(params) {
  return request({
    url: '/roles/',
    method: 'get',
    params,
  })
}

/**
 * Get bills
 * @param {Object} params - Query parameters
 */
export function getBills(params) {
  return request({
    url: '/bills/',
    method: 'get',
    params,
  })
}

/**
 * Get my bills
 */
export function getMyBills() {
  return request({
    url: '/bills/my/',
    method: 'get',
  })
}

/**
 * Get notices
 * @param {Object} params - Query parameters
 */
export function getNotices(params) {
  return request({
    url: '/notices/',
    method: 'get',
    params,
  })
}

/**
 * Get notice detail
 * @param {number} id - Notice ID
 */
export function getNotice(id) {
  return request({
    url: `/notices/${id}/`,
    method: 'get',
  })
}

/**
 * Create notice (Admin)
 * @param {Object} data - Notice data
 */
export function createNotice(data) {
  return request({
    url: '/admin/notices/',
    method: 'post',
    data,
  })
}

/**
 * Update notice (Admin)
 * @param {number} id - Notice ID
 * @param {Object} data - Notice data
 */
export function updateNotice(id, data) {
  return request({
    url: `/admin/notices/${id}/`,
    method: 'put',
    data,
  })
}

/**
 * Delete notice (Admin)
 * @param {number} id - Notice ID
 */
export function deleteNotice(id) {
  return request({
    url: `/admin/notices/${id}/`,
    method: 'delete',
  })
}

/**
 * Get operation logs
 * @param {Object} params - Query parameters
 */
export function getOperationLogs(params) {
  return request({
    url: '/logs/',
    method: 'get',
    params,
  })
}
