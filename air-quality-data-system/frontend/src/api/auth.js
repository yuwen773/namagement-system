import request from '@/utils/request'

/**
 * User login
 * @param {string} username - Username
 * @param {string} password - Password
 */
export function login(username, password) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data: { username, password }
  })
}

/**
 * User registration
 * @param {Object} data - Registration data
 * @param {string} data.username - Username
 * @param {string} data.password - Password
 * @param {string} data.email - Email
 * @param {string} data.phone - Phone number (optional)
 */
export function register(data) {
  return request({
    url: '/auth/register/',
    method: 'post',
    data
  })
}

/**
 * User logout
 * @param {string} token - Auth token (optional, will use localStorage if not provided)
 */
export function logout() {
  // Client-side cleanup
  localStorage.removeItem('token')
  localStorage.removeItem('user')

  // Optional: Call backend logout endpoint if token exists
  // return request({
  //   url: '/auth/logout/',
  //   method: 'post'
  // })
}
