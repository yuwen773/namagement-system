/**
 * API 接口 - 影院管理
 */
import request from '@/utils/request'

// 获取影院列表
export function getCinemas(params, regionList = []) {
  const queryParams = { ...params }
  if (queryParams.region) {
    const regionId = queryParams.region
    // 查找选择的地域信息
    const selectedRegion = regionList.find(r => r.id === regionId)
    if (selectedRegion) {
      // 如果是省份（parent 为 null），使用 province_id 筛选该省下所有城市
      if (!selectedRegion.parent) {
        queryParams.province_id = regionId
      } else {
        // 如果是城市，使用 region_id 精确匹配
        queryParams.region_id = regionId
      }
    } else {
      // 如果找不到地域信息，默认使用 region_id
      queryParams.region_id = regionId
    }
    delete queryParams.region
  }
  return request({
    url: '/cinemas/',
    method: 'get',
    params: queryParams
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
