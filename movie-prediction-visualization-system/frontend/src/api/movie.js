/**
 * API 接口 - 影片管理
 */
import request from '@/utils/request'

// 获取影片列表
export function getMovies(params) {
  return request({
    url: '/movies/',
    method: 'get',
    params
  })
}

// 获取影片详情
export function getMovie(id) {
  return request({
    url: `/movies/${id}/`,
    method: 'get'
  })
}

// 创建影片
export function createMovie(data) {
  return request({
    url: '/movies/',
    method: 'post',
    data
  })
}

// 更新影片
export function updateMovie(id, data) {
  return request({
    url: `/movies/${id}/`,
    method: 'put',
    data
  })
}

// 删除影片
export function deleteMovie(id) {
  return request({
    url: `/movies/${id}/`,
    method: 'delete'
  })
}

// 获取影片类型列表
export function getMovieTypes() {
  return request({
    url: '/movies/types/',
    method: 'get'
  })
}

// 创建影片类型
export function createMovieType(data) {
  return request({
    url: '/movies/types/',
    method: 'post',
    data
  })
}

// 更新影片类型
export function updateMovieType(id, data) {
  return request({
    url: `/movies/types/${id}/`,
    method: 'put',
    data
  })
}

// 删除影片类型
export function deleteMovieType(id) {
  return request({
    url: `/movies/types/${id}/`,
    method: 'delete'
  })
}
