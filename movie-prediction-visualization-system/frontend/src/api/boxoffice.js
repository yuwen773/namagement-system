/**
 * API 接口 - 票房数据
 */
import request from '@/utils/request'

// 获取票房记录列表
export function getBoxOfficeRecords(params) {
  return request({
    url: '/boxoffice/',
    method: 'get',
    params
  })
}

// 获取票房记录详情
export function getBoxOfficeRecord(id) {
  return request({
    url: `/boxoffice/${id}/`,
    method: 'get'
  })
}

// 创建票房记录
export function createBoxOfficeRecord(data) {
  return request({
    url: '/boxoffice/',
    method: 'post',
    data
  })
}

// 更新票房记录
export function updateBoxOfficeRecord(id, data) {
  return request({
    url: `/boxoffice/${id}/`,
    method: 'put',
    data
  })
}

// 删除票房记录
export function deleteBoxOfficeRecord(id) {
  return request({
    url: `/boxoffice/${id}/`,
    method: 'delete'
  })
}

// 批量创建票房记录
export function batchCreateBoxOfficeRecords(data) {
  return request({
    url: '/boxoffice/batch/',
    method: 'post',
    data
  })
}

// 获取票房统计
export function getBoxOfficeStats(params) {
  return request({
    url: '/boxoffice/stats/',
    method: 'get',
    params
  })
}
