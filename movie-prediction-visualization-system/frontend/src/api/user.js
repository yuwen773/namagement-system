/**
 * API 接口 - 用户管理 (管理员)
 */
import request from '@/utils/request'

// 获取用户列表
export function getUsers(params) {
  return request({
    url: '/accounts/users/',
    method: 'get',
    params
  })
}

// 获取用户详情
export function getUser(id) {
  return request({
    url: `/accounts/users/${id}/`,
    method: 'get'
  })
}

// 创建用户
export function createUser(data) {
  return request({
    url: '/accounts/users/',
    method: 'post',
    data
  })
}

// 更新用户
export function updateUser(id, data) {
  return request({
    url: `/accounts/users/${id}/`,
    method: 'put',
    data
  })
}

// 删除用户
export function deleteUser(id) {
  return request({
    url: `/accounts/users/${id}/`,
    method: 'delete'
  })
}

// 更新用户角色
export function updateUserRole(id, data) {
  return request({
    url: `/accounts/users/${id}/role/`,
    method: 'put',
    data
  })
}

// 禁用用户
export function disableUser(id) {
  return request({
    url: `/accounts/users/${id}/disable/`,
    method: 'post'
  })
}

// 启用用户
export function enableUser(id) {
  return request({
    url: `/accounts/users/${id}/enable/`,
    method: 'post'
  })
}

// 重置用户密码
export function resetUserPassword(id, data) {
  return request({
    url: `/accounts/users/${id}/reset_password/`,
    method: 'post',
    data
  })
}
