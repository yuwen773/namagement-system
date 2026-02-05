import { get, post, put, patch, del } from '../request'

/**
 * 用户相关 API
 */

// ==================== 用户个人接口 ====================

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
  return post(`/system/messages/${id}/mark-read/`)
}

/**
 * 获取浏览历史列表
 * @returns {Promise<Array>}
 */
export function getBrowsingHistoryApi() {
  return get('/users/browsing-history/list_history/')
}

/**
 * 添加浏览记录
 * @param {Object} data - 浏览记录数据
 * @returns {Promise<Object>}
 */
export function addBrowsingHistoryApi(data) {
  return post('/users/browsing-history/add/', data)
}

/**
 * 清空浏览历史
 * @returns {Promise<Object>}
 */
export function clearBrowsingHistoryApi() {
  return del('/users/browsing-history/clear/')
}

// ==================== 管理员用户管理接口 ====================

/**
 * 获取用户列表（管理员）
 * @param {Object} params - 查询参数
 * @returns {Promise<Object>}
 */
export function getUserListApi(params) {
  return get('/users/', params)
}

/**
 * 获取用户详情（管理员）- 包含地址信息
 * @param {number} id - 用户ID
 * @returns {Promise<Object>}
 */
export function getUserDetailApi(id) {
  return get(`/users/${id}/admin-detail/`)
}

/**
 * 更新用户状态（管理员）- 启用/禁用
 * @param {number} id - 用户ID
 * @param {string} status - 状态 (active/banned)
 * @returns {Promise<Object>}
 */
export function updateUserStatusApi(id, status) {
  return patch(`/users/${id}/status/`, { status })
}

/**
 * 获取用户地址列表（管理员）
 * @param {number} id - 用户ID
 * @returns {Promise<Object>}
 */
export function getUserAddressesApi(id) {
  return get(`/users/${id}/admin-addresses/`)
}

/**
 * 创建用户（管理员）
 * @param {Object} data - 用户数据
 * @returns {Promise<Object>}
 */
export function createUserApi(data) {
  return post('/users/', data)
}

/**
 * 更新用户信息（管理员）
 * @param {number} id - 用户ID
 * @param {Object} data - 用户数据
 * @returns {Promise<Object>}
 */
export function updateUserApi(id, data) {
  return patch(`/users/${id}/`, data)
}

/**
 * 删除用户（管理员）
 * @param {number} id - 用户ID
 * @returns {Promise<void>}
 */
export function deleteUserApi(id) {
  return del(`/users/${id}/`)
}
