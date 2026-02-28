// frontend/src/api/feedbacks.js
import request from '@/utils/request'

export function getFeedbackList(params) {
  return request.get('/api/feedbacks/', { params })
}

export function getFeedbackDetail(id) {
  return request.get(`/api/feedbacks/${id}/`)
}

export function createFeedback(data) {
  return request.post('/api/feedbacks/', data)
}

export function updateFeedback(id, data) {
  return request.patch(`/api/feedbacks/${id}/`, data)
}

export function deleteFeedback(id) {
  return request.delete(`/api/feedbacks/${id}/`)
}

export function getFeedbackFilterOptions() {
  return request.get('/api/feedbacks/filter_options/')
}
