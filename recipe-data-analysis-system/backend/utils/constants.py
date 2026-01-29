"""
常量定义模块

定义系统中使用的各种常量。
"""

# 用户角色常量
class UserRole:
    """用户角色"""
    USER = 'user'
    ADMIN = 'admin'
    CHOICES = [
        (USER, '普通用户'),
        (ADMIN, '管理员'),
    ]


# 分类类型常量
class CategoryType:
    """分类类型"""
    CUISINE = 'cuisine'      # 菜系
    SCENE = 'scene'          # 场景
    CROWD = 'crowd'          # 人群
    DIFFICULTY = 'difficulty'  # 难度
    TASTE = 'taste'          # 口味
    CHOICES = [
        (CUISINE, '菜系'),
        (SCENE, '场景'),
        (CROWD, '人群'),
        (DIFFICULTY, '难度'),
        (TASTE, '口味'),
    ]


# 食材分类常量
class IngredientCategory:
    """食材分类"""
    VEGETABLE = 'vegetable'    # 蔬菜
    MEAT = 'meat'              # 肉类
    SEAFOOD = 'seafood'        # 海鲜
    SEASONING = 'seasoning'    # 调料
    FRUIT = 'fruit'            # 水果
    GRAIN = 'grain'            # 谷物
    DAIRY = 'dairy'            # 乳制品
    OTHER = 'other'            # 其他
    CHOICES = [
        (VEGETABLE, '蔬菜'),
        (MEAT, '肉类'),
        (SEAFOOD, '海鲜'),
        (SEASONING, '调料'),
        (FRUIT, '水果'),
        (GRAIN, '谷物'),
        (DAIRY, '乳制品'),
        (OTHER, '其他'),
    ]


# 用户行为类型常量
class BehaviorType:
    """用户行为类型"""
    LOGIN = 'login'                    # 登录
    SEARCH = 'search'                  # 搜索
    VIEW = 'view'                      # 浏览
    COLLECT = 'collect'                # 收藏
    UNCOLLECT = 'uncollect'            # 取消收藏
    SHARE = 'share'                    # 分享
    CHOICES = [
        (LOGIN, '登录'),
        (SEARCH, '搜索'),
        (VIEW, '浏览'),
        (COLLECT, '收藏'),
        (UNCOLLECT, '取消收藏'),
        (SHARE, '分享'),
    ]


# 分页常量
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


# JWT 配置常量
JWT_ACCESS_TOKEN_LIFETIME = 60 * 24  # 24 小时（分钟）
