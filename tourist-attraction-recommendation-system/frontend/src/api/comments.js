/**
 * 评论相关 API
 * 对应后端: backend/comments/
 *
 * 包含: 发表评论、删除评论、我的评论、景点评论列表、审核评论
 */

import request from './request'

export default {
  /**
   * 发表评论
   * @param {Object} data - 评论数据
   * @param {number} data.attraction - 景点ID (必填)
   * @param {string} data.content - 评论内容 (必填)
   * @param {number} data.rating - 评分 1-5 (必填, 默认5)
   * @returns {Promise} { code: 0, message: "评论已提交，等待审核", data: {...} }
   */
  create(data) {
    return request({
      url: '/comments/comments/',
      method: 'post',
      data
    })
  },

  /**
   * 删除评论 (只能删除自己的评论)
   * @param {number} id - 评论ID
   * @returns {Promise} { code: 0, message: "删除成功" }
   */
  delete(id) {
    return request({
      url: `/comments/comments/${id}/`,
      method: 'delete'
    })
  },

  /**
   * 获取我的评论列表
   * @returns {Promise} { code: 0, data: [...], total: n }
   */
  getMyComments() {
    return request({
      url: '/comments/comments/my/',
      method: 'get'
    })
  },

  /**
   * 获取指定景点的评论列表 (仅已审核通过的评论)
   * @param {number} attractionId - 景点ID
   * @returns {Promise} { code: 0, data: [...], total: n }
   */
  getByAttraction(attractionId) {
    return request({
      url: `/comments/comments/attraction/${attractionId}/`,
      method: 'get'
    })
  },

  /**
   * 审核评论 (仅管理员)
   * @param {number} id - 评论ID
   * @param {Object} data - 审核数据
   * @param {string} data.action - 操作类型: "approve" (通过) 或 "reject" (驳回)
   * @returns {Promise} { code: 0, message: "审核成功" }
   */
  review(id, data) {
    return request({
      url: `/comments/comments/${id}/review/`,
      method: 'put',
      data
    })
  }
}
