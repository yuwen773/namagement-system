import api from './axios'

/**
 * 获取所有角色权限配置列表
 */
export function getRolePermissionList() {
  return api.get('/auth/permissions/')
}

/**
 * 获取单个角色权限配置
 * @param {number} id - 权限配置ID
 */
export function getRolePermissionDetail(id) {
  return api.get(`/auth/permissions/${id}/`)
}

/**
 * 更新角色权限配置
 * @param {number} id - 权限配置ID
 * @param {Object} data - 权限配置数据
 */
export function updateRolePermission(id, data) {
  return api.put(`/auth/permissions/${id}/`, data)
}

/**
 * 部分更新角色权限配置
 * @param {number} id - 权限配置ID
 * @param {Object} data - 权限配置数据
 */
export function patchRolePermission(id, data) {
  return api.patch(`/auth/permissions/${id}/`, data)
}

/**
 * 初始化默认权限配置
 */
export function initializePermissions() {
  return api.post('/auth/permissions/initialize/')
}

/**
 * 根据角色获取权限配置
 * @param {string} role - 角色标识
 */
export function getPermissionByRole(role) {
  return api.get('/auth/permissions/by_role/', {
    params: { role }
  })
}
