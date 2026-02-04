/**
 * 常量定义
 */

// 订单状态映射
export const ORDER_STATUS_MAP = {
  pending_payment: { label: '待付款', type: 'warning' },
  pending_shipment: { label: '待发货', type: 'info' },
  shipped: { label: '已发货', type: 'primary' },
  completed: { label: '已完成', type: 'success' },
  cancelled: { label: '已取消', type: 'danger' },
  return_processing: { label: '退款中', type: 'warning' }
}

// 退换货状态映射
export const RETURN_STATUS_MAP = {
  pending: { label: '待审核', type: 'warning' },
  approved: { label: '已同意', type: 'success' },
  rejected: { label: '已拒绝', type: 'danger' },
  processing: { label: '处理中', type: 'primary' },
  completed: { label: '已完成', type: 'success' }
}

// 商品状态映射
export const PRODUCT_STATUS_MAP = {
  draft: { label: '草稿', type: 'info' },
  pending: { label: '待审核', type: 'warning' },
  published: { label: '已发布', type: 'success' },
  archived: { label: '已下架', type: 'danger' }
}

// 优惠券类型映射
export const COUPON_TYPE_MAP = {
  full_reduction: { label: '满减券', type: 'primary' },
  discount: { label: '折扣券', type: 'success' }
}

// 优惠券状态映射
export const COUPON_STATUS_MAP = {
  active: { label: '进行中', type: 'success' },
  inactive: { label: '已停用', type: 'info' },
  expired: { label: '已过期', type: 'danger' }
}

// 用户优惠券状态映射
export const USER_COUPON_STATUS_MAP = {
  unused: { label: '未使用', type: 'success' },
  used: { label: '已使用', type: 'info' },
  expired: { label: '已过期', type: 'danger' }
}

// FAQ 分类
export const FAQ_CATEGORIES = [
  { value: 'order', label: '订单问题' },
  { value: 'payment', label: '支付问题' },
  { value: 'shipping', label: '物流配送' },
  { value: 'product', label: '商品问题' },
  { value: 'return', label: '退换货' },
  { value: 'account', label: '账户问题' }
]

// 每页数量选项
export const PAGE_SIZE_OPTIONS = [10, 20, 50, 100]

// 默认分页大小
export const DEFAULT_PAGE_SIZE = 20

// 本地存储键名
export const STORAGE_KEYS = {
  TOKEN: 'token',
  USER_INFO: 'user_info',
  CART_COUNT: 'cart_count',
  SEARCH_HISTORY: 'search_history'
}
