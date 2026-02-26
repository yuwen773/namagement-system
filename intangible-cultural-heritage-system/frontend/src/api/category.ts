import request from '@/utils/request'
import type { ApiResponse, Category, CategoryTree } from '@/types'

// 获取分类列表
export const getCategoryList = (params?: { 
  page?: number
  level?: string
  parent_id?: number | string
  name?: string
}) => {
  return request.get<ApiResponse<Category[]>>('/categories/', { params })
}

// 获取分类树
export const getCategoryTree = () => {
  return request.get<ApiResponse<CategoryTree[]>>('/categories/tree/')
}

// 获取分类详情
export const getCategoryDetail = (id: number) => {
  return request.get<ApiResponse<Category>>(`/categories/${id}/`)
}

// 创建分类
export const createCategory = (data: {
  name: string
  code: string
  level: string
  parent?: number
}) => {
  return request.post<ApiResponse<Category>>('/categories/', data)
}

// 更新分类
export const updateCategory = (id: number, data: Partial<{
  name: string
  code: string
  level: string
  parent?: number
}>) => {
  return request.patch<ApiResponse<Category>>(`/categories/${id}/`, data)
}

// 删除分类
export const deleteCategory = (id: number) => {
  return request.delete<ApiResponse<null>>(`/categories/${id}/`)
}
