/**
 * API 接口 - 票房预测
 */
import request from '@/utils/request'

// 获取预测结果
export function getPrediction(params) {
  return request({
    url: '/prediction/',
    method: 'get',
    params
  })
}

// 执行预测
export function executePrediction(data) {
  return request({
    url: '/prediction/',
    method: 'post',
    data
  })
}

// 获取预测历史
export function getPredictionHistory(params) {
  return request({
    url: '/prediction/history/',
    method: 'get',
    params
  })
}

// 获取预测算法说明
export function getAlgorithmInfo() {
  return request({
    url: '/prediction/algorithms/',
    method: 'get'
  })
}
