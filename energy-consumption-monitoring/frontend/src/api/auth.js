import request from '@/utils/request'

/**
 * Authentication API
 */

/**
 * User login
 * @param {Object} data - Login credentials { username, password }
 */
export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data,
  })
}

/**
 * User registration
 * @param {Object} data - Registration data
 */
export function register(data) {
  return request({
    url: '/auth/register/',
    method: 'post',
    data,
  })
}

/**
 * Refresh access token
 * @param {string} refreshToken - Refresh token
 */
export function refreshToken(refreshToken) {
  return request({
    url: '/auth/refresh/',
    method: 'post',
    data: { refresh: refreshToken },
  })
}

/**
 * Get current user info
 */
export function getUserInfo() {
  return request({
    url: '/auth/user-info/',
    method: 'get',
  })
}

/**
 * Change password
 * @param {Object} data - { old_password, new_password }
 */
export function changePassword(data) {
  return request({
    url: '/auth/change-password/',
    method: 'post',
    data,
  })
}
