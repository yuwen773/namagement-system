import axios from './axios'

// 签到
export function checkIn() {
  return axios.post('/attendance/check-in/')
}

// 签退
export function checkOut() {
  return axios.post('/attendance/check-out/')
}

// 获取今日考勤
export function getTodayAttendance() {
  return axios.get('/attendance/today/')
}

// 获取考勤记录列表
export function getAttendanceRecords(params) {
  return axios.get('/attendance/', { params })
}

// 获取考勤统计
export function getAttendanceStats(month) {
  return axios.get('/attendance/stats/', { params: { month } })
}
