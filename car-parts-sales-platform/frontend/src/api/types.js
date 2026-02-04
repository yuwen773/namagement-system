// 通用类型定义

/**
 * API 响应结构
 * @template T
 * @typedef {Object} ApiResponse
 * @property {number} code - 状态码
 * @property {string} message - 消息
 * @property {T} data - 数据
 */

/**
 * 分页响应结构
 * @template T
 * @typedef {Object} PaginatedResponse
 * @property {number} count - 总数量
 * @property {string|null} next - 下一页链接
 * @property {string|null} previous - 上一页链接
 * @property {T[]} results - 数据列表
 */

/**
 * 用户类型
 * @typedef {Object} User
 * @property {number} id - 用户ID
 * @property {string} phone - 手机号
 * @property {string} nickname - 昵称
 * @property {string} avatar - 头像URL
 * @property {number} points - 积分
 * @property {boolean} is_admin - 是否管理员
 * @property {string} created_at - 创建时间
 */

/**
 * 商品类型
 * @typedef {Object} Product
 * @property {number} id - 商品ID
 * @property {string} name - 商品名称
 * @property {string} description - 商品描述
 * @property {number} price - 价格
 * @property {number} stock - 库存
 * @property {string} image - 主图
 * @property {string} status - 状态
 * @property {number} sales - 销量
 * @property {number} views - 浏览量
 * @property {Object} category - 分类
 * @property {Array} images - 图片列表
 * @property {Array} attributes - 属性列表
 */

/**
 * 订单类型
 * @typedef {Object} Order
 * @property {number} id - 订单ID
 * @property {string} order_no - 订单号
 * @property {string} status - 订单状态
 * @property {number} total_amount - 总金额
 * @property {number} discount_amount - 优惠金额
 * @property {number} pay_amount - 支付金额
 * @property {Array} items - 订单商品列表
 */

/**
 * 购物车商品类型
 * @typedef {Object} CartItem
 * @property {number} id - 购物车项ID
 * @property {number} product_id - 商品ID
 * @property {string} product_name - 商品名称
 * @property {string} product_image - 商品图片
 * @property {number} price - 价格
 * @property {number} quantity - 数量
 * @property {boolean} selected - 是否选中
 */

// 分页参数
export class PaginationParams {
  constructor(page = 1, pageSize = 20) {
    this.page = page
    this.page_size = pageSize
  }
}

// API 错误类
export class ApiError extends Error {
  constructor(message, code = 400) {
    super(message)
    this.name = 'ApiError'
    this.code = code
  }
}
