// API 统一导出

// 认证相关
export * from './modules/auth'
export * from './modules/user'
export * from './modules/product'
export * from './modules/cart'
export * from './modules/order'
export * from './modules/marketing'

// 请求方法
export { default as request } from './request'
export { get, post, put, patch, del } from './request'

// 类型定义
export * from './types'
