import axios from '@/api/axios'

/**
 * 岗位管理 API
 */

/**
 * 获取岗位列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码，默认 1
 * @param {number} params.page_size - 每页数量，默认 10
 * @param {string} params.only_active - true=只返回启用的岗位
 * @param {string} params.keyword - 按名称模糊搜索
 * @returns {Promise}
 */
export function getPostList(params) {
  return axios.get('/organization/posts/', { params })
}

/**
 * 获取单个岗位详情
 * @param {number} id - 岗位ID
 * @returns {Promise}
 */
export function getPost(id) {
  return axios.get(`/organization/posts/${id}/`)
}

/**
 * 根据部门获取岗位列表
 * @param {number} departmentId - 部门ID
 * @returns {Promise}
 */
export function getPostsByDepartment(departmentId) {
  return axios.get('/organization/posts/by_department/', {
    params: { department_id: departmentId }
  })
}

/**
 * 创建岗位
 * @param {Object} data - 岗位数据
 * @param {string} data.name - 岗位名称
 * @param {string} data.code - 岗位编码
 * @param {boolean} [data.is_active] - 是否启用
 * @returns {Promise}
 */
export function createPost(data) {
  return axios.post('/organization/posts/', data)
}

/**
 * 更新岗位
 * @param {number} id - 岗位ID
 * @param {Object} data - 岗位数据
 * @returns {Promise}
 */
export function updatePost(id, data) {
  return axios.put(`/organization/posts/${id}/`, data)
}

/**
 * 删除岗位
 * @param {number} id - 岗位ID
 * @returns {Promise}
 */
export function deletePost(id) {
  return axios.delete(`/organization/posts/${id}/`)
}

export default {
  getPostList,
  getPost,
  getPostsByDepartment,
  createPost,
  updatePost,
  deletePost
}
