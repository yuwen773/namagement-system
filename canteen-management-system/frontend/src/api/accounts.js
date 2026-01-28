/**
 * 用户账号管理 API
 */
import request from './request'

/**
 * 获取用户列表
 * @param {Object} params - 查询参数
 * @param {string} params.role - 角色筛选
 * @param {string} params.status - 状态筛选
 * @param {string} params.search - 搜索关键字
 * @param {string} params.ordering - 排序字段
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 * @returns {Promise}
 */
export function getUserList(params = {}) {
  return request({
    url: '/accounts/',
    method: 'get',
    params
  })
}

/**
 * 获取用户详情
 * @param {number} id - 用户ID
 * @returns {Promise}
 */
export function getUserDetail(id) {
  return request({
    url: `/accounts/${id}/`,
    method: 'get'
  })
}

/**
 * 创建用户账号
 * @param {Object} data - 用户数据
 * @returns {Promise}
 */
export function createUser(data) {
  return request({
    url: '/accounts/',
    method: 'post',
    data
  })
}

/**
 * 更新用户账号
 * @param {number} id - 用户ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export function updateUser(id, data) {
  return request({
    url: `/accounts/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 部分更新用户账号
 * @param {number} id - 用户ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export function patchUser(id, data) {
  return request({
    url: `/accounts/${id}/`,
    method: 'patch',
    data
  })
}

/**
 * 删除用户账号
 * @param {number} id - 用户ID
 * @returns {Promise}
 */
export function deleteUser(id) {
  return request({
    url: `/accounts/${id}/`,
    method: 'delete'
  })
}

/**
 * 获取角色列表
 * @returns {Promise}
 */
export function getRoleList() {
  return request({
    url: '/accounts/roles/',
    method: 'get'
  })
}

/**
 * 获取系统设置
 * @returns {Promise}
 */
export function getSystemSettings() {
  return request({
    url: '/accounts/settings/',
    method: 'get'
  })
}

/**
 * 更新系统设置
 * @param {Object} data - 设置数据
 * @returns {Promise}
 */
export function updateSystemSettings(data) {
  return request({
    url: '/accounts/settings/',
    method: 'put',
    data
  })
}
