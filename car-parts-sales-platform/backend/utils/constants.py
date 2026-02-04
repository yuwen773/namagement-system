"""
常量定义模块
"""
from enum import Enum


class OrderStatus(Enum):
    """订单状态"""
    PENDING_PAYMENT = 'pending_payment'
    PENDING_SHIPMENT = 'pending_shipment'
    SHIPPED = 'shipped'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    @classmethod
    def choices(cls):
        return (
            (cls.PENDING_PAYMENT.value, '待付款'),
            (cls.PENDING_SHIPMENT.value, '待发货'),
            (cls.SHIPPED.value, '已发货'),
            (cls.COMPLETED.value, '已完成'),
            (cls.CANCELLED.value, '已取消'),
        )


class ProductStatus(Enum):
    """商品状态"""
    DRAFT = 'draft'
    PENDING = 'pending'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

    @classmethod
    def choices(cls):
        return (
            (cls.DRAFT.value, '草稿'),
            (cls.PENDING.value, '待审核'),
            (cls.PUBLISHED.value, '已上架'),
            (cls.ARCHIVED.value, '已下架'),
        )


class CouponType(Enum):
    """优惠券类型"""
    FULL_REDUCTION = 'full_reduction'  # 满减
    DISCOUNT = 'discount'  # 折扣

    @classmethod
    def choices(cls):
        return (
            (cls.FULL_REDUCTION.value, '满减券'),
            (cls.DISCOUNT.value, '折扣券'),
        )


class ReturnRequestStatus(Enum):
    """退换货状态"""
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    @classmethod
    def choices(cls):
        return (
            (cls.PENDING.value, '待处理'),
            (cls.APPROVED.value, '已同意'),
            (cls.REJECTED.value, '已拒绝'),
        )


class UserCouponStatus(Enum):
    """用户优惠券状态"""
    UNUSED = 'unused'
    USED = 'used'
    EXPIRED = 'expired'

    @classmethod
    def choices(cls):
        return (
            (cls.UNUSED.value, '未使用'),
            (cls.USED.value, '已使用'),
            (cls.EXPIRED.value, '已过期'),
        )
