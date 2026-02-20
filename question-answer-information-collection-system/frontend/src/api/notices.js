// frontend/src/api/notices.js
import request from '@/utils/request'

export function getNoticeList(params) {
  return request.get('/api/notices/', { params })
}

export function getNoticeDetail(id) {
  return request.get(`/api/notices/${id}/`)
}

export function createNotice(data) {
  return request.post('/api/notices/', data)
}

export function updateNotice(id, data) {
  return request.patch(`/api/notices/${id}/`, data)
}

export function deleteNotice(id) {
  return request.delete(`/api/notices/${id}/`)
}
