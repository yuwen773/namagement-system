import api from './axios'

/**
 * 获取系统配置
 */
export function getSystemConfig() {
  return api.get('/auth/system-config/')
}

/**
 * 更新系统配置
 * @param {Object} data - 系统配置数据
 */
export function updateSystemConfig(data) {
  return api.put('/auth/system-config/update_config/', data)
}

/**
 * 部分更新系统配置
 * @param {Object} data - 系统配置数据
 */
export function patchSystemConfig(data) {
  return api.patch('/auth/system-config/update_config/', data)
}
