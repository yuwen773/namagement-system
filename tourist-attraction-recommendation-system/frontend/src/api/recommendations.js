/**
 * 推荐相关 API
 * 对应后端: backend/recommendations/
 *
 * 包含: 热门推荐、个性化推荐、相似景点推荐
 */

import request from './request'

export default {
  /**
   * 获取热门景点推荐 (无需认证)
   * @param {Object} params - 查询参数
   * @param {number} params.limit - 返回数量 (可选, 默认10, 最大50)
   * @returns {Promise} { code: 0, data: [...], total: n }
   */
  getPopular(params) {
    return request({
      url: '/recommendations/popular/',
      method: 'get',
      params: { limit: params?.limit }
    })
  },

  /**
   * 获取个性化推荐
   * @param {Object} params - 查询参数
   * @param {number} params.limit - 返回数量 (可选, 默认10, 最大50)
   * @returns {Promise}
   *   - 未登录: { code: 0, data: [...], total: n, message: "未登录，返回热门推荐" }
   *   - 已登录: { code: 0, data: [...], total: n }
   * @note 基于用户收藏和评分数据推荐
   */
  getPersonalized(params) {
    return request({
      url: '/recommendations/personalized/',
      method: 'get',
      params: { limit: params?.limit }
    })
  },

  /**
   * 获取相似景点推荐 (无需认证)
   * @param {number} attractionId - 景点ID
   * @param {Object} params - 查询参数
   * @param {number} params.limit - 返回数量 (可选, 默认6, 最大20)
   * @returns {Promise} { code: 0, data: [...], total: n }
   * @note 基于类别和地区推荐相似景点
   */
  getSimilar(attractionId, params) {
    return request({
      url: `/recommendations/similar/${attractionId}/`,
      method: 'get',
      params: { limit: params?.limit }
    })
  }
}
