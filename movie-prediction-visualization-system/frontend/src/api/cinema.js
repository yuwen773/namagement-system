/**
 * API 接口 - 影院管理
 */
import request from '@/utils/request'

// 获取影院列表
export function getCinemas(params) {
  return request({
    url: '/cinemas/',
    method: 'get',
    params
  })
}

// 获取影院详情
export function getCinema(id) {
  return request({
    url: `/cinemas/${id}/`,
    method: 'get'
  })
}

// 创建影院
export function createCinema(data) {
  return request({
    url: '/cinemas/',
    method: 'post',
    data
  })
}

// 更新影院
export function updateCinema(id, data) {
  return request({
    url: `/cinemas/${id}/`,
    method: 'put',
    data
  })
}

// 删除影院
export function deleteCinema(id) {
  return request({
    url: `/cinemas/${id}/`,
    method: 'delete'
  })
}

// 获取地域列表
export function getRegions(params) {
  return request({
    url: '/cinemas/regions/',
    method: 'get',
    params
  })
}

// 创建地域
export function createRegion(data) {
  return request({
    url: '/cinemas/regions/',
    method: 'post',
    data
  })
}

// 更新地域
export function updateRegion(id, data) {
  return request({
    url: `/cinemas/regions/${id}/`,
    method: 'put',
    data
  })
}

// 删除地域
export function deleteRegion(id) {
  return request({
    url: `/cinemas/regions/${id}/`,
    method: 'delete'
  })
}
