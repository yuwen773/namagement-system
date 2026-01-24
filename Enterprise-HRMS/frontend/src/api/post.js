import axios from '@/api/axios'

/**
 * 获取岗位列表
 * @param {Object} params - 查询参数
 * @param {boolean} params.only_active - 只返回启用的岗位
 * @returns {Promise} 岗位列表
 */
export function getPostList(params) {
  return axios.get('/organization/posts/', { params })
}
