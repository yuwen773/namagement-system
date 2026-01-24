import axios from '@/api/axios'

/**
 * 获取部门列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 部门列表
 */
export function getDepartmentList(params) {
  return axios.get('/organization/departments/', { params })
}

/**
 * 获取部门树形结构
 * @returns {Promise} 部门树
 */
export function getDepartmentTree() {
  return axios.get('/organization/departments/tree/')
}

/**
 * 获取单个部门详情
 * @param {number} id - 部门ID
 * @returns {Promise} 部门详情
 */
export function getDepartment(id) {
  return axios.get(`/organization/departments/${id}/`)
}

/**
 * 创建部门
 * @param {Object} data - 部门数据
 * @returns {Promise} 创建结果
 */
export function createDepartment(data) {
  return axios.post('/organization/departments/', data)
}

/**
 * 更新部门
 * @param {number} id - 部门ID
 * @param {Object} data - 部门数据
 * @returns {Promise} 更新结果
 */
export function updateDepartment(id, data) {
  return axios.put(`/organization/departments/${id}/`, data)
}

/**
 * 删除部门
 * @param {number} id - 部门ID
 * @returns {Promise} 删除结果
 */
export function deleteDepartment(id) {
  return axios.delete(`/organization/departments/${id}/`)
}
