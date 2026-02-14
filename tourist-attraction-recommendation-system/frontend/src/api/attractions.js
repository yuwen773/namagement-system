/**
 * 景点相关 API
 * 对应后端: backend/attractions/
 *
 * 包含: 景点列表、详情、创建、更新、删除、搜索
 */

import request from './request'

export default {
  /**
   * 获取景点列表 (分页)
   * @param {Object} params - 查询参数
   * @param {string} params.category - 类别筛选 (可选: 自然风光/人文古迹/主题乐园/其他)
   * @param {string} params.region - 地区筛选 (可选)
   * @param {number} params.page - 页码 (可选, 默认1)
   * @param {number} params.page_size - 每页数量 (可选)
   * @returns {Promise} { code: 0, data: [...], total: n }
   */
  getList(params) {
    return request({
      url: '/attractions/',
      method: 'get',
      params
    })
  },

  /**
   * 获取景点详情
   * @param {number} id - 景点ID
   * @returns {Promise} { code: 0, data: { id, name, description, address, category, region, opening_hours, cover_image, images, view_count, ... } }
   * @note 每次调用会自动增加 view_count
   */
  getDetail(id) {
    return request({
      url: `/attractions/${id}/`,
      method: 'get'
    })
  },

  /**
   * 创建景点 (仅管理员)
   * @param {Object} data - 景点数据
   * @param {string} data.name - 景点名称 (必填)
   * @param {string} data.description - 景点简介 (必填)
   * @param {string} data.address - 详细地址 (必填)
   * @param {string} data.category - 类别 (必填: 自然风光/人文古迹/主题乐园/其他)
   * @param {string} data.region - 地区 (必填)
   * @param {string} data.opening_hours - 开放时间 (可选)
   * @param {string} data.cover_image - 封面图 (可选)
   * @param {Array<string>} data.images - 轮播图数组 (可选)
   * @returns {Promise} { code: 0, message: "创建成功", data: {...} }
   */
  create(data) {
    return request({
      url: '/attractions/',
      method: 'post',
      data
    })
  },

  /**
   * 更新景点 (仅管理员)
   * @param {number} id - 景点ID
   * @param {Object} data - 景点数据 (同创建)
   * @returns {Promise} { code: 0, message: "更新成功", data: {...} }
   */
  update(id, data) {
    return request({
      url: `/attractions/${id}/`,
      method: 'put',
      data
    })
  },

  /**
   * 部分更新景点 (仅管理员)
   * @param {number} id - 景点ID
   * @param {Object} data - 部分景点数据
   * @returns {Promise} { code: 0, message: "更新成功", data: {...} }
   */
  partialUpdate(id, data) {
    return request({
      url: `/attractions/${id}/`,
      method: 'patch',
      data
    })
  },

  /**
   * 删除景点 (逻辑删除, 仅管理员)
   * @param {number} id - 景点ID
   * @returns {Promise} { code: 0, message: "删除成功" }
   */
  delete(id) {
    return request({
      url: `/attractions/${id}/`,
      method: 'delete'
    })
  },

  /**
   * 搜索景点 (按名称或描述模糊搜索)
   * @param {string} keyword - 搜索关键词 (必填)
   * @returns {Promise} { code: 0, data: [...], total: n }
   */
  search(keyword) {
    return request({
      url: '/attractions/search/',
      method: 'get',
      params: { keyword }
    })
  }
}
