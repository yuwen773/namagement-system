import { get, post, put, patch, del } from '../request'

/**
 * 用户相关 API
 */

/**
 * 获取用户地址列表
 * @returns {Promise<Array>}
 */
export function getAddressListApi() {
  return get('/users/addresses/')
}

/**
 * 创建用户地址
 * @param {Object} data - 地址数据
 * @returns {Promise<Object>}
 */
export function createAddressApi(data) {
  return post('/users/addresses/', data)
}

/**
 * 更新用户地址
 * @param {number} id - 地址ID
 * @param {Object} data - 地址数据
 * @returns {Promise<Object>}
 */
export function updateAddressApi(id, data) {
  return put(`/users/addresses/${id}/`, data)
}

/**
 * 删除用户地址
 * @param {number} id - 地址ID
 * @returns {Promise<void>}
 */
export function deleteAddressApi(id) {
  return del(`/users/addresses/${id}/`)
}

/**
 * 设置默认地址
 * @param {number} id - 地址ID
 * @returns {Promise<Object>}
 */
export function setDefaultAddressApi(id) {
  return patch(`/users/addresses/${id}/set-default/`)
}

/**
 * 更新用户资料
 * @param {Object} data - 用户数据
 * @returns {Promise<Object>}
 */
export function updateProfileApi(data) {
  return put('/users/profile/', data)
}

/**
 * 修改密码
 * @param {Object} data - 密码数据
 * @returns {Promise<void>}
 */
export function changePasswordApi(data) {
  return post('/users/change-password/', data)
}

/**
 * 获取我的消息列表
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getMessagesApi(params) {
  return get('/system/messages/', params)
}

/**
 * 标记消息为已读
 * @param {number} id - 消息ID
 * @returns {Promise<void>}
 */
export function readMessageApi(id) {
  return patch(`/system/messages/${id}/read/`)
}
