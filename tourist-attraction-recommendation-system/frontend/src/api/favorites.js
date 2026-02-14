/**
 * 收藏相关 API
 * 对应后端: backend/comments/ (FavoriteViewSet)
 *
 * 包含: 添加收藏、取消收藏、我的收藏列表
 */

import request from './request'

export default {
  /**
   * 添加收藏
   * @param {number} attractionId - 景点ID
   * @returns {Promise} { code: 0, message: "收藏成功", data: { id, attraction, attraction_name, attraction_cover, created_at } }
   */
  add(attractionId) {
    return request({
      url: '/comments/favorites/',
      method: 'post',
      data: { attraction: attractionId }
    })
  },

  /**
   * 取消收藏
   * @param {number} id - 收藏记录ID
   * @returns {Promise} { code: 0, message: "取消成功" }
   */
  remove(id) {
    return request({
      url: `/comments/favorites/${id}/`,
      method: 'delete'
    })
  },

  /**
   * 获取我的收藏列表
   * @returns {Promise} { code: 0, data: [...], total: n }
   */
  getMyFavorites() {
    return request({
      url: '/comments/favorites/my/',
      method: 'get'
    })
  }
}
