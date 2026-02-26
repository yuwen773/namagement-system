import request from '@/utils/request'
import type { ApiResponse, Announcement, AnnouncementCreate, AnnouncementListParams } from '@/types'

// 获取公告列表
export const getAnnouncementList = (params?: AnnouncementListParams) => {
  return request.get<ApiResponse<Announcement[]>>('/announcements/', { params })
}

// 获取公告详情
export const getAnnouncementDetail = (id: number) => {
  return request.get<ApiResponse<Announcement>>(`/announcements/${id}/`)
}

// 创建公告
export const createAnnouncement = (data: AnnouncementCreate) => {
  return request.post<ApiResponse<Announcement>>('/announcements/', data)
}

// 更新公告
export const updateAnnouncement = (id: number, data: Partial<AnnouncementCreate>) => {
  return request.patch<ApiResponse<Announcement>>(`/announcements/${id}/`, data)
}

// 删除公告
export const deleteAnnouncement = (id: number) => {
  return request.delete<ApiResponse<null>>(`/announcements/${id}/`)
}
