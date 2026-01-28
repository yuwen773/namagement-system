"""
常量定义模块

定义项目中使用的各种常量
"""

# 岗位津贴配置（单位：元）
POSITION_ALLOWANCE_MAP = {
    'CHEF': 800,       # 厨师
    'PASTRY': 700,     # 面点
    'PREP': 500,       # 切配
    'CLEANER': 300,    # 保洁
    'SERVER': 400,     # 服务员
    'MANAGER': 1000,   # 经理
}

# 默认基本工资（单位：元）
DEFAULT_BASE_SALARY = 3000

# 薪资计算常量
DAYS_PER_MONTH = 21.75  # 每月工作天数（用于计算日工资）
HOURS_PER_DAY = 8       # 每天工作小时数（用于计算时薪）
OVERTIME_RATE = 1.5     # 加班费倍率

# 扣款金额（单位：元）
LATE_DEDUCTION = 20     # 迟到扣款
MISSING_DEDUCTION = 50  # 缺卡扣款

# 考勤宽限时间（分钟）
GRACE_PERIOD_MINUTES = 5

# 薪资状态
SALARY_STATUS_DRAFT = 'DRAFT'           # 草稿
SALARY_STATUS_PUBLISHED = 'PUBLISHED'   # 已发布
SALARY_STATUS_ADJUSTED = 'ADJUSTED'     # 已调整
SALARY_STATUS_APPEALED = 'APPEALED'     # 申诉中

# 请假状态
LEAVE_STATUS_PENDING = 'PENDING'       # 待审批
LEAVE_STATUS_APPROVED = 'APPROVED'     # 已批准
LEAVE_STATUS_REJECTED = 'REJECTED'     # 已拒绝
LEAVE_STATUS_CANCELLED = 'CANCELLED'   # 已撤销

# 调班申请状态
SWAP_STATUS_PENDING = 'PENDING'       # 待审批
SWAP_STATUS_APPROVED = 'APPROVED'     # 已批准
SWAP_STATUS_REJECTED = 'REJECTED'     # 已拒绝

# 申诉状态
APPEAL_STATUS_PENDING = 'PENDING'     # 待审批
APPEAL_STATUS_APPROVED = 'APPROVED'   # 已批准
APPEAL_STATUS_REJECTED = 'REJECTED'   # 已拒绝

# 员工状态
EMPLOYEE_STATUS_ACTIVE = 'ACTIVE'           # 在职
EMPLOYEE_STATUS_INACTIVE = 'INACTIVE'       # 离职
EMPLOYEE_STATUS_LEAVE_WITHOUT_PAY = 'LEAVE_WITHOUT_PAY'  # 停薪留职

# 用户角色
USER_ROLE_ADMIN = 'ADMIN'       # 管理员
USER_ROLE_EMPLOYEE = 'EMPLOYEE'  # 普通员工
