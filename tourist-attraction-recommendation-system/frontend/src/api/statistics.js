/**
 * 统计相关 API
 * 对应后端: backend/statistics/
 *
 * 包含: 热门景点、数据看板、月度报告、用户管理、用户状态更新
 */

import request from './request'

export default {
  /**
   * 获取热门景点排行 TOP 10 (无需认证)
   * @returns {Promise} { code: 0, data: [{ id, name, cover_image, category, region, view_count, comment_count, avg_rating, hot_score }, ...], total: 10 }
   * @note 热度公式: hot_score = (view_count * 0.2) + (comment_count * 0.3) + (avg_rating * view_count * 0.5)
   */
  getHotAttractions() {
    return request({
      url: '/statistics/hot/',
      method: 'get'
    })
  },

  /**
   * 获取数据看板 (仅管理员)
   * @returns {Promise} { code: 0, data: { total_users, total_attractions, total_comments, monthly_new_users, monthly_new_attractions, monthly_new_comments } }
   */
  getDashboard() {
    return request({
      url: '/statistics/dashboard/',
      method: 'get'
    })
  },

  /**
   * 获取月度数据报告 (仅管理员)
   * @returns {Promise} { code: 0, data: [{ month, new_users, new_attractions, new_comments }, ...], total: 6 }
   * @note 返回最近6个月数据，按时间倒序
   */
  getMonthlyReport() {
    return request({
      url: '/statistics/monthly/',
      method: 'get'
    })
  },

  /**
   * 获取用户管理列表 (仅管理员, 分页)
   * @param {Object} params - 查询参数
   * @param {string} params.keyword - 搜索关键词 (可选, 模糊匹配 username/real_name/email)
   * @param {string} params.role - 角色筛选 (可选: USER/ADMIN)
   * @param {boolean} params.is_active - 状态筛选 (可选)
   * @param {string} params.ordering - 排序字段 (可选, 默认: "-created_at")
   * @param {number} params.page - 页码 (可选, 默认1)
   * @param {number} params.page_size - 每页数量 (可选, 默认10)
   * @returns {Promise} { code: 0, data: [...], total: n }
   */
  getUserList(params) {
    return request({
      url: '/statistics/users/',
      method: 'get',
      params: {
        keyword: params.keyword,
        role: params.role,
        is_active: params.isActive,
        ordering: params.ordering,
        page: params.page,
        page_size: params.pageSize
      }
    })
  },

  /**
   * 更新用户状态 (启用/禁用, 仅管理员)
   * @param {number} userId - 用户ID
   * @param {boolean} isActive - 是否启用
   * @returns {Promise} { code: 0, message: "用户状态更新成功", data: {...} }
   */
  updateUserStatus(userId, isActive) {
    return request({
      url: `/statistics/users/${userId}/status/`,
      method: 'put',
      data: { is_active: isActive }
    })
  }
}
