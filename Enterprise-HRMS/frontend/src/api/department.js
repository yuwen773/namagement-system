import axios from '@/api/axios'

/**
 * 部门管理 API
 */

/**
 * 获取部门列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码，默认 1
 * @param {number} params.page_size - 每页数量，默认 10
 * @param {string} params.only_root - true=只返回根部门
 * @param {string} params.only_active - true=只返回启用的部门
 * @param {string} params.keyword - 按名称模糊搜索
 * @returns {Promise}
 */
export function getDepartmentList(params) {
  return axios.get('/organization/departments/', { params })
}

/**
 * 获取部门树形结构
 * @returns {Promise}
 */
export function getDepartmentTree() {
  return axios.get('/organization/departments/tree/')
}

/**
 * 获取单个部门详情
 * @param {number} id - 部门ID
 * @returns {Promise}
 */
export function getDepartment(id) {
  return axios.get(`/organization/departments/${id}/`)
}

/**
 * 创建部门
 * @param {Object} data - 部门数据
 * @param {string} data.name - 部门名称
 * @param {string} data.code - 部门编码
 * @param {number} [data.parent] - 上级部门ID
 * @param {number} [data.sort_order] - 排序
 * @param {boolean} [data.is_active] - 是否启用
 * @returns {Promise}
 */
export function createDepartment(data) {
  return axios.post('/organization/departments/', data)
}

/**
 * 更新部门
 * @param {number} id - 部门ID
 * @param {Object} data - 部门数据
 * @returns {Promise}
 */
export function updateDepartment(id, data) {
  return axios.put(`/organization/departments/${id}/`, data)
}

/**
 * 删除部门
 * @param {number} id - 部门ID
 * @returns {Promise}
 */
export function deleteDepartment(id) {
  return axios.delete(`/organization/departments/${id}/`)
}

export default {
  getDepartmentList,
  getDepartmentTree,
  getDepartment,
  createDepartment,
  updateDepartment,
  deleteDepartment
}
