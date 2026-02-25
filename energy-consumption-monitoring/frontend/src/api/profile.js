import request from '@/utils/request'

/**
 * Profile API
 */

/**
 * Get my profile
 */
export function getMyProfile() {
  return request({
    url: '/profile/',
    method: 'get',
  })
}

/**
 * Update my profile
 * @param {Object} data - Profile data
 */
export function updateMyProfile(data) {
  return request({
    url: '/profile/',
    method: 'put',
    data,
  })
}

/**
 * Get my binded rooms
 */
export function getMyBindRooms() {
  return request({
    url: '/profile/bind-rooms/',
    method: 'get',
  })
}

/**
 * Bind room to my profile
 * @param {Object} data - { room_ids }
 */
export function bindRoom(data) {
  return request({
    url: '/profile/bind-rooms/',
    method: 'post',
    data,
  })
}

/**
 * Unbind room from my profile
 * @param {number} roomId - Room ID
 */
export function unbindRoom(roomId) {
  return request({
    url: '/profile/bind-rooms/',
    method: 'delete',
    data: { room_ids: [roomId] },
  })
}

/**
 * Get my alarm subscriptions
 */
export function getMyAlarmSubscriptions() {
  return request({
    url: '/profile/alarm-subscriptions/',
    method: 'get',
  })
}

/**
 * Update my alarm subscriptions
 * @param {Object} data - Subscription settings
 */
export function updateAlarmSubscriptions(data) {
  return request({
    url: '/profile/alarm-subscriptions/',
    method: 'put',
    data,
  })
}

/**
 * Upload avatar
 * @param {FormData} data - File data
 */
export function uploadAvatar(data) {
  return request({
    url: '/profile/avatar/',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}
