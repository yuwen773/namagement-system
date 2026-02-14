/**
 * API 接口 - 可视化图表
 */
import request from '@/utils/request'

// 获取票房总榜 Top 10
export function getTop10Movies(params) {
  return request({
    url: '/visualization/stats/top10/',
    method: 'get',
    params
  })
}

// 获取今日大盘票房统计
export function getTodayBoxOffice(params) {
  return request({
    url: '/visualization/stats/today/',
    method: 'get',
    params
  })
}

// 获取本周票房冠军
export function getWeeklyChampion(params) {
  return request({
    url: '/visualization/stats/champion/',
    method: 'get',
    params
  })
}

// 获取各类型票房占比
export function getTypeDistribution(params) {
  return request({
    url: '/visualization/stats/type/',
    method: 'get',
    params
  })
}

// 获取各省份票房分布
export function getRegionDistribution(params) {
  return request({
    url: '/visualization/stats/region/',
    method: 'get',
    params
  })
}

// 获取票房时间走势
export function getTimeSeries(params) {
  return request({
    url: '/visualization/stats/timeseries/',
    method: 'get',
    params
  })
}

// 获取仪表盘概览数据
export function getDashboardData(params) {
  return request({
    url: '/visualization/stats/dashboard/',
    method: 'get',
    params
  })
}

// 获取管理端概览统计数据
export function getOverviewStats(params) {
  return request({
    url: '/visualization/stats/overview/',
    method: 'get',
    params
  })
}
