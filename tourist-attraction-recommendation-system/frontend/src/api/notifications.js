/**
 * 通知相关 API
 * 对应后端: backend/notifications/
 *
 * 包含: 通知列表、标记已读、发布公告、通知 CRUD
 */

import request from './request'

export default {
  /**
   * 获取通知列表 (包含未读数)
   * @returns {Promise} { code: 0, data: [...], total: n, unread_count: n }
   * @note 普通用户看到: 自己的通知 + 全员公告
   * @note 管理员看到: 所有通知
   */
  getList() {
    return request({
      url: '/notifications/',
      method: 'get'
    })
  },

  /**
   * 标记通知已读 (单个或全部)
   * @param {number|null} id - 通知ID (传 null 或不传表示全部标记已读)
   * @returns {Promise} { code: 0, message: "已标记已读" 或 "已全部标记已读" }
   */
  markRead(id) {
    return request({
      url: '/notifications/mark_read/',
      method: 'post',
      data: id !== null ? { id } : {}
    })
  },

  /**
   * 标记全部已读
   * @returns {Promise} { code: 0, message: "已全部标记已读" }
   */
  markAllRead() {
    return request({
      url: '/notifications/mark_read/',
      method: 'post',
      data: {}
    })
  },

  /**
   * 发布公告 (仅管理员)
   * @param {Object} data - 公告数据
   * @param {string} data.title - 标题 (必填)
   * @param {string} data.content - 内容 (必填)
   * @param {string} data.type - 类型 (固定为 "ANNOUNCEMENT")
   * @returns {Promise} { code: 0, message: "公告发布成功", data: {...} }
   */
  publishAnnouncement(data) {
    return request({
      url: '/notifications/announcement/',
      method: 'post',
      data
    })
  },

  /**
   * 获取通知详情
   * @param {number} id - 通知ID
   * @returns {Promise} { code: 0, data: {...} }
   */
  getById(id) {
    return request({
      url: `/notifications/${id}/`,
      method: 'get'
    })
  },

  /**
   * 创建通知
   * @param {Object} data - 通知数据
   * @param {string} data.title - 标题 (必填)
   * @param {string} data.content - 内容 (必填)
   * @param {string} data.type - 类型 (SYSTEM/ANNOUNCEMENT/COMMENT)
   * @param {number} data.user - 用户ID (可选, 不传表示全员通知)
   * @returns {Promise} { code: 0, data: {...} }
   */
  create(data) {
    return request({
      url: '/notifications/',
      method: 'post',
      data
    })
  },

  /**
   * 更新通知
   * @param {number} id - 通知ID
   * @param {Object} data - 更新数据
   * @returns {Promise} { code: 0, data: {...} }
   */
  update(id, data) {
    return request({
      url: `/notifications/${id}/`,
      method: 'put',
      data
    })
  },

  /**
   * 删除通知
   * @param {number} id - 通知ID
   * @returns {Promise} 204 No Content
   */
  delete(id) {
    return request({
      url: `/notifications/${id}/`,
      method: 'delete'
    })
  }
}
