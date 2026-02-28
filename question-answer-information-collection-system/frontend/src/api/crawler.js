import request from '@/utils/request'

// 录制相关
/**
 * 开始录制
 * @param {Object} data - 录制配置
 * @param {string} data.config_id - 配置ID
 */
export function startRecording(data) {
  return request({
    url: '/api/recorder/start/',
    method: 'post',
    data
  })
}

/**
 * 停止录制
 * @param {Object} data - 停止参数
 */
export function stopRecording(data) {
  return request({
    url: '/api/recorder/stop/',
    method: 'post',
    data
  })
}

/**
 * 获取录制步骤列表
 */
export function getRecordingSteps() {
  return request({
    url: '/api/recorder/steps/',
    method: 'get'
  })
}

/**
 * 下载本地录制器
 */
export function downloadRecorder() {
  return request({
    url: '/api/recorder/download/',
    method: 'get',
    responseType: 'blob'
  })
}

/**
 * 上传配置文件
 * @param {FormData} formData - 配置文件 FormData
 */
export function uploadConfig(formData) {
  return request({
    url: '/api/recorder/upload/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

// 配置相关

/**
 * 获取配置列表
 */
export function listConfigs() {
  return request({
    url: '/api/recorder/configs/',
    method: 'get'
  })
}

// 任务相关

/**
 * 获取任务列表
 */
export function listTasks() {
  return request({
    url: '/api/recorder/tasks/',
    method: 'get'
  })
}

/**
 * 创建任务
 * @param {Object} data - 任务数据
 */
export function createTask(data) {
  return request({
    url: '/api/recorder/task/create/',
    method: 'post',
    data
  })
}

/**
 * 获取任务状态
 * @param {number} taskId - 任务ID
 */
export function getTaskStatus(taskId) {
  return request({
    url: `/api/recorder/task/${taskId}/`,
    method: 'get'
  })
}

/**
 * 启动任务
 * @param {number} taskId - 任务ID
 */
export function startTask(taskId) {
  return request({
    url: `/api/recorder/task/${taskId}/start/`,
    method: 'post'
  })
}

/**
 * 暂停任务
 * @param {number} taskId - 任务ID
 */
export function pauseTask(taskId) {
  return request({
    url: `/api/recorder/task/${taskId}/pause/`,
    method: 'post'
  })
}

/**
 * 恢复任务
 * @param {number} taskId - 任务ID
 */
export function resumeTask(taskId) {
  return request({
    url: `/api/recorder/task/${taskId}/resume/`,
    method: 'post'
  })
}

/**
 * 停止任务
 * @param {number} taskId - 任务ID
 */
export function stopTask(taskId) {
  return request({
    url: `/api/recorder/task/${taskId}/stop/`,
    method: 'post'
  })
}
