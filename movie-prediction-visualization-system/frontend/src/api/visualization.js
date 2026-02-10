/**
 * API 接口 - 可视化图表
 */
import request from '@/utils/request'

// 获取票房趋势数据
export function getBoxOfficeTrend(params) {
  return request({
    url: '/visualization/trend/',
    method: 'get',
    params
  })
}

// 获取地域分布数据
export function getRegionDistribution(params) {
  return request({
    url: '/visualization/region/',
    method: 'get',
    params
  })
}

// 获取类型占比数据
export function getTypeDistribution(params) {
  return request({
    url: '/visualization/type/',
    method: 'get',
    params
  })
}

// 获取 Top10 影片
export function getTop10Movies(params) {
  return request({
    url: '/visualization/top10/',
    method: 'get',
    params
  })
}

// 获取票房仪表盘数据
export function getDashboardData(params) {
  return request({
    url: '/visualization/dashboard/',
    method: 'get',
    params
  })
}
