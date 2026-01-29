"""
Django管理命令：生成测试数据
清空所有业务表，为9个业务表每个生成100条符合业务逻辑的测试数据
"""
import random
from datetime import datetime, timedelta, time, date
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from django.utils.timezone import make_aware

from accounts.models import SystemSettings, User
from employees.models import EmployeeProfile
from schedules.models import Shift, Schedule, ShiftSwapRequest
from attendance.models import AttendanceRecord
from leaves.models import LeaveRequest
from salaries.models import SalaryRecord, Appeal


class Command(BaseCommand):
    help = '生成100条测试数据到所有业务表'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='每个表生成的记录数量（默认100）'
        )
        parser.add_argument(
            '--skip-clear',
            action='store_true',
            help='跳过清空数据步骤'
        )

    # ==================== 数据源 ====================

    # 中文姓名库
    SURNAMES = [
        '王', '李', '张', '刘', '陈', '杨', '赵', '黄', '周', '吴',
        '徐', '孙', '胡', '朱', '高', '林', '何', '郭', '马', '罗',
        '梁', '宋', '郑', '谢', '韩', '唐', '冯', '于', '董', '萧',
        '程', '曹', '袁', '邓', '许', '傅', '沈', '曾', '彭', '吕',
        '苏', '卢', '蒋', '蔡', '贾', '丁', '魏', '薛', '叶', '阎'
    ]

    GIVEN_NAMES = [
        '伟', '芳', '娜', '敏', '静', '丽', '强', '磊', '军', '洋',
        '勇', '艳', '杰', '娟', '涛', '明', '超', '秀英', '华', '红',
        '建国', '建军', '志强', '国庆', '春梅', '春华', '秋菊', '秀兰', '桂英', '玉兰',
        '海燕', '丽丽', '小红', '晓华', '晓丽', '建华', '建平', '文静', '文博', '志明',
        '秀珍', '海英', '瑞敏', '瑞华', '光辉', '光华', '保华', '保国', '爱华', '爱民',
        '永强', '永刚', '晓明', '晓红', '晓东', '晓燕', '晓军', '晓梅', '晓芳', '晓娟',
        '玉兰', '玉英', '玉珍', '玉华', '玉芬', '玉莲', '春梅', '春兰', '春花', '春霞',
        '秀珍', '秀兰', '秀芬', '秀华', '秀英', '秀荣', '秀琴', '秀云', '秀芳', '秀娟',
        '丽华', '丽丽', '丽娜', '丽红', '丽萍', '丽娟', '丽芳', '丽梅', '丽英', '丽霞',
        '建华', '建平', '建国', '建军', '建新', '建文', '建武', '建国', '建华', '建平'
    ]

    # 请假原因库
    LEAVE_REASONS = [
        '身体不适，需要休息',
        '家中有事需要处理',
        '医院检查',
        '陪伴家人就医',
        '家庭聚会',
        '个人私事',
        '调休补休',
        '加班调休',
        '外出办事',
        '照顾生病家人',
        '孩子学校有事',
        '参加婚礼',
        '办理证件',
        '房屋装修',
        '搬家',
        '探亲访友',
        '参加培训',
        '驾照考试',
        '银行办事',
        '参加社区活动'
    ]

    # 调班原因库
    SWAP_REASONS = [
        '个人临时有事',
        '家庭安排调整',
        '医生预约',
        '接送孩子',
        '照顾老人',
        '参加重要聚会',
        '办理证件',
        '房屋维修',
        '其他个人原因',
        '与其他员工协商调班',
        '临时加班安排',
        '培训学习',
        '体检预约',
        '学校家长会',
        '重要约会'
    ]

    # 申诉原因库
    APPEAL_REASONS_ATTENDANCE = [
        '实际正常上班，系统误判迟到',
        '因公外出导致缺卡',
        '系统故障导致打卡失败',
        '网络问题打卡未成功',
        '替同事打卡忘记签退',
        '会议延迟导致迟到',
        '接待客户导致迟到',
        '加班后忘记签退',
        '考勤机故障',
        '指纹识别问题'
    ]

    APPEAL_REASONS_SALARY = [
        '加班费计算有误',
        '扣款金额不正确',
        '出勤天数统计错误',
        '基本工资与合同不符',
        '岗位津贴未发放',
        '绩效工资计算错误',
        '加班时长统计不准',
        '请假扣款计算错误',
        '奖金未计入',
        '其他薪资问题'
    ]

    # 打卡地点库
    CLOCK_LOCATIONS = [
        '食堂大厅',
        '后厨操作间',
        '一楼餐厅',
        '二楼餐厅',
        '员工入口',
        '后厨入口',
        '配菜间',
        '面点间',
        '洗碗间',
        '仓库'
    ]

    # 审批意见库
    APPROVAL_REMARKS = [
        '同意',
        '批准',
        '同意申请',
        '情况属实，同意',
        '按规定处理，同意',
        '核实无误，批准',
        '特殊情况，同意',
        '经核实，同意批准',
        '申请合理，同意',
        '已确认，批准'
    ]

    REJECT_REMARKS = [
        '理由不充分，不同意',
        '请提供更多证明材料',
        '申请不符合规定',
        '时机不合适，请调整',
        '影响正常工作安排',
        '已有类似申请，不同意',
        '请重新核对信息',
        '不符合调班条件',
        '请假时间过长',
        '请与主管沟通后再申请'
    ]

    # ==================== 辅助方法 ====================

    def random_date(self, start_date, end_date):
        """生成两个日期之间的随机日期"""
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)

    def random_datetime(self, start_date, end_date):
        """生成两个日期之间的随机日期时间"""
        return make_aware(datetime.combine(
            self.random_date(start_date, end_date),
            time(random.randint(0, 23), random.randint(0, 59))
        ))

    def random_phone(self):
        """生成随机手机号"""
        return f'13{random.randint(0, 9)}{random.randint(10000000, 99999999)}'

    def random_id_card(self):
        """生成随机身份证号"""
        return f'{random.randint(110000, 659999)}{random.randint(1970, 2005)}{random.randint(1, 12):02d}{random.randint(1, 28):02d}{random.randint(100, 999)}'

    def random_chinese_name(self):
        """生成随机中文姓名"""
        surname = random.choice(self.SURNAMES)
        given_name = random.choice(self.GIVEN_NAMES)
        return f'{surname}{given_name}'

    # ==================== 数据清空 ====================

    def clear_all_data(self):
        """按依赖顺序清空所有业务表数据"""
        self.stdout.write(self.style.WARNING('开始清空所有业务表数据...'))

        # 按依赖关系反向删除
        models_to_clear = [
            ('appeals', Appeal),
            ('salary_records', SalaryRecord),
            ('leave_requests', LeaveRequest),
            ('attendance_records', AttendanceRecord),
            ('shift_swap_requests', ShiftSwapRequest),
            ('schedules', Schedule),
            ('users', User),
            ('shifts', Shift),
            ('employee_profiles', EmployeeProfile),
        ]

        for name, model in models_to_clear:
            count = model.objects.count()
            if count > 0:
                model.objects.all().delete()
                self.stdout.write(f'  [OK] 已清空 {name}: {count} 条')

        self.stdout.write(self.style.SUCCESS('数据清空完成！'))

    # ==================== 数据生成 ====================

    def generate_employees(self, count):
        """生成员工档案"""
        self.stdout.write(f'生成员工档案 ({count}条)...')

        # 岗位分布
        positions_dist = {
            EmployeeProfile.Position.CHEF: 15,
            EmployeeProfile.Position.PASTRY: 12,
            EmployeeProfile.Position.PREP: 20,
            EmployeeProfile.Position.CLEANER: 25,
            EmployeeProfile.Position.SERVER: 20,
            EmployeeProfile.Position.MANAGER: 8,
        }

        employees = []
        today = date.today()

        for position, num in positions_dist.items():
            for i in range(num):
                # 生成入职日期（2022-2025年）
                entry_date = self.random_date(date(2022, 1, 1), date(2025, 12, 31))

                # 状态分布：90% ACTIVE, 5% INACTIVE, 5% LEAVE_WITHOUT_PAY
                status_rand = random.random()
                if status_rand < 0.90:
                    status = EmployeeProfile.Status.ACTIVE
                elif status_rand < 0.95:
                    status = EmployeeProfile.Status.INACTIVE
                else:
                    status = EmployeeProfile.Status.LEAVE_WITHOUT_PAY

                # 健康证信息
                health_cert_no = f'H{random.randint(10000000, 99999999)}'
                health_expiry = today + timedelta(days=random.randint(365, 1095))

                employee = EmployeeProfile(
                    name=self.random_chinese_name(),
                    gender=random.choice([EmployeeProfile.Gender.MALE, EmployeeProfile.Gender.FEMALE]),
                    phone=self.random_phone(),
                    id_card=self.random_id_card() if random.random() > 0.1 else None,
                    address=f'{random.choice(["北京市", "上海市", "广州市", "深圳市"])}某区某街道某号' if random.random() > 0.3 else None,
                    position=position,
                    entry_date=entry_date,
                    status=status,
                    health_certificate_no=health_cert_no,
                    health_certificate_expiry=health_expiry,
                    chef_certificate_level=self._get_chef_cert(position) if position in [EmployeeProfile.Position.CHEF, EmployeeProfile.Position.PASTRY] else None
                )
                employees.append(employee)

        EmployeeProfile.objects.bulk_create(employees)
        self.stdout.write(f'  [OK] 成功生成 {len(employees)} 条员工档案')
        return employees

    def _get_chef_cert(self, position):
        """根据岗位生成厨师证"""
        if random.random() > 0.3:  # 70%有证书
            certs = ['高级技师', '技师', '高级', '中级', '初级']
            return random.choice(certs)
        return None

    def generate_shifts(self, count):
        """生成班次定义"""
        self.stdout.write(f'生成班次定义 ({count}条)...')

        # 班次类型定义
        shift_types = [
            ('早餐班', time(5, 30), time(10, 0), 20),
            ('中餐班', time(10, 0), time(14, 30), 20),
            ('晚餐班', time(16, 0), time(20, 30), 20),
            ('早中连班', time(5, 30), time(14, 30), 15),
            ('中晚连班', time(10, 0), time(20, 30), 15),
            ('全天班', time(8, 0), time(20, 0), 10),
        ]

        shifts = []
        for shift_type, start_t, end_t, num in shift_types:
            for i in range(1, num + 1):
                shift = Shift(
                    name=f'{shift_type}{i}',
                    start_time=start_t,
                    end_time=end_t
                )
                shifts.append(shift)

        Shift.objects.bulk_create(shifts)
        self.stdout.write(f'  [OK] 成功生成 {len(shifts)} 条班次定义')
        return shifts

    def generate_users(self, count):
        """生成用户账号"""
        self.stdout.write(f'生成用户账号 ({count}条)...')

        employees = list(EmployeeProfile.objects.all())
        active_employees = [e for e in employees if e.status == EmployeeProfile.Status.ACTIVE]

        users = []

        # 生成10个管理员
        for i in range(10):
            user = User(
                username=f'admin{i+1:03d}',
                password='123456',  # 开发阶段明文
                employee_id=random.choice(active_employees).id if active_employees else None,
                role=User.Role.ADMIN,
                status=User.Status.ENABLED if random.random() > 0.05 else User.Status.DISABLED
            )
            users.append(user)

        # 生成90个普通员工账号
        for i in range(90):
            # 80%关联到员工，20%独立
            if random.random() < 0.8 and active_employees:
                employee_id = random.choice(active_employees).id
            else:
                employee_id = None

            user = User(
                username=f'user{i+1:03d}',
                password='123456',  # 开发阶段明文
                employee_id=employee_id,
                role=User.Role.EMPLOYEE,
                status=User.Status.ENABLED if random.random() > 0.05 else User.Status.DISABLED
            )
            users.append(user)

        User.objects.bulk_create(users)
        self.stdout.write(f'  [OK] 成功生成 {len(users)} 条用户账号')
        return users

    def generate_schedules(self, count):
        """生成排班计划"""
        self.stdout.write(f'生成排班计划 ({count}条)...')

        employees = list(EmployeeProfile.objects.filter(status=EmployeeProfile.Status.ACTIVE))
        shifts = list(Shift.objects.all())

        if not employees or not shifts:
            self.stdout.write(self.style.ERROR('  [X] 缺少员工或班次数据'))
            return []

        # 时间范围：2026-01-01 至 2026-03-31
        start_date = date(2026, 1, 1)
        end_date = date(2026, 3, 31)

        schedules = []
        used_combinations = set()  # 防止重复

        attempts = 0
        max_attempts = count * 10

        while len(schedules) < count and attempts < max_attempts:
            attempts += 1

            employee = random.choice(employees)
            shift = random.choice(shifts)
            work_date = self.random_date(start_date, end_date)

            # 确保日期在入职日期之后
            if work_date < employee.entry_date:
                continue

            # 确保唯一性
            combo = (employee.id, work_date)
            if combo in used_combinations:
                continue

            schedule = Schedule(
                employee=employee,
                shift=shift,
                work_date=work_date
            )
            schedules.append(schedule)
            used_combinations.add(combo)

        Schedule.objects.bulk_create(schedules)
        self.stdout.write(f'  [OK] 成功生成 {len(schedules)} 条排班计划')
        return schedules

    def generate_swap_requests(self, count):
        """生成调班申请"""
        self.stdout.write(f'生成调班申请 ({count}条)...')

        schedules = list(Schedule.objects.all())
        shifts = list(Shift.objects.all())
        managers = list(EmployeeProfile.objects.filter(position=EmployeeProfile.Position.MANAGER))

        if not schedules:
            self.stdout.write(self.style.ERROR('  [X] 缺少排班数据'))
            return []

        requests = []

        for i in range(count):
            schedule = random.choice(schedules)

            # 生成目标日期（原日期前后7天内）
            days_offset = random.randint(-7, 7)
            target_date = schedule.work_date + timedelta(days=days_offset)
            if target_date < schedule.employee.entry_date:
                target_date = schedule.work_date + timedelta(days=random.randint(1, 7))

            # 选择不同的班次
            target_shift = random.choice(shifts)
            while target_shift.id == schedule.shift.id and len(shifts) > 1:
                target_shift = random.choice(shifts)

            # 状态分布
            status_rand = random.random()
            if status_rand < 0.40:
                status = ShiftSwapRequest.Status.PENDING
                approver = None
                approval_remark = None
            elif status_rand < 0.75:
                status = ShiftSwapRequest.Status.APPROVED
                approver = random.choice(managers) if managers else None
                approval_remark = random.choice(self.APPROVAL_REMARKS)
            else:
                status = ShiftSwapRequest.Status.REJECTED
                approver = random.choice(managers) if managers else None
                approval_remark = random.choice(self.REJECT_REMARKS)

            request = ShiftSwapRequest(
                requester=schedule.employee,
                original_schedule=schedule,
                target_date=target_date,
                target_shift=target_shift,
                reason=random.choice(self.SWAP_REASONS),
                status=status,
                approver=approver,
                approval_remark=approval_remark
            )
            requests.append(request)

        ShiftSwapRequest.objects.bulk_create(requests)
        self.stdout.write(f'  [OK] 成功生成 {len(requests)} 条调班申请')
        return requests

    def generate_attendance(self, count):
        """生成考勤记录"""
        self.stdout.write(f'生成考勤记录 ({count}条)...')

        schedules = list(Schedule.objects.all())

        if not schedules:
            self.stdout.write(self.style.ERROR('  [X] 缺少排班数据'))
            return []

        attendance_records = []

        for i in range(count):
            schedule = random.choice(schedules)
            shift = schedule.shift
            work_date = schedule.work_date

            # 构建班次时间
            shift_start = make_aware(datetime.combine(work_date, shift.start_time))
            shift_end = make_aware(datetime.combine(work_date, shift.end_time))

            # 状态分布
            status_rand = random.random()
            grace_period = timedelta(minutes=5)

            if status_rand < 0.60:  # NORMAL
                clock_in = shift_start - timedelta(minutes=random.randint(0, 5))
                clock_out = shift_end + timedelta(minutes=random.randint(0, 180))
                status = AttendanceRecord.Status.NORMAL
            elif status_rand < 0.80:  # LATE
                clock_in = shift_start + timedelta(minutes=random.randint(6, 30))
                clock_out = shift_end + timedelta(minutes=random.randint(0, 180))
                status = AttendanceRecord.Status.LATE
            elif status_rand < 0.90:  # EARLY_LEAVE
                clock_in = shift_start - timedelta(minutes=random.randint(0, 5))
                clock_out = shift_end - timedelta(minutes=random.randint(6, 30))
                status = AttendanceRecord.Status.EARLY_LEAVE
            else:  # MISSING
                if random.random() < 0.5:
                    clock_in = shift_start - timedelta(minutes=random.randint(0, 5))
                    clock_out = None
                else:
                    clock_in = None
                    clock_out = shift_end + timedelta(minutes=random.randint(0, 30))
                status = AttendanceRecord.Status.MISSING

            # 计算加班时长
            if clock_out and clock_out > shift_end:
                overtime_hours = round((clock_out - shift_end).total_seconds() / 3600, 2)
            else:
                overtime_hours = 0

            record = AttendanceRecord(
                employee=schedule.employee,
                schedule=schedule,
                clock_in_time=clock_in,
                clock_in_location=random.choice(self.CLOCK_LOCATIONS) if clock_in else '未打卡',
                clock_out_time=clock_out,
                clock_out_location=random.choice(self.CLOCK_LOCATIONS) if clock_out else '未打卡',
                status=status
            )
            attendance_records.append(record)

        AttendanceRecord.objects.bulk_create(attendance_records)
        self.stdout.write(f'  [OK] 成功生成 {len(attendance_records)} 条考勤记录')
        return attendance_records

    def generate_leaves(self, count):
        """生成请假申请"""
        self.stdout.write(f'生成请假申请 ({count}条)...')

        employees = list(EmployeeProfile.objects.all())
        managers = list(EmployeeProfile.objects.filter(position=EmployeeProfile.Position.MANAGER))

        if not employees:
            self.stdout.write(self.style.ERROR('  [X] 缺少员工数据'))
            return []

        leaves = []

        for i in range(count):
            employee = random.choice(employees)

            # 请假类型
            leave_type_rand = random.random()
            if leave_type_rand < 0.40:
                leave_type = LeaveRequest.LeaveType.SICK
            elif leave_type_rand < 0.80:
                leave_type = LeaveRequest.LeaveType.PERSONAL
            else:
                leave_type = LeaveRequest.LeaveType.COMPENSATORY

            # 生成时间范围（2026-01-01 至 2026-03-31）
            start_time = make_aware(datetime.combine(
                self.random_date(date(2026, 1, 1), date(2026, 3, 25)),
                time(9, 0)
            ))
            duration_days = random.randint(1, 7)
            end_time = start_time + timedelta(days=duration_days - 1, hours=8)

            # 状态分布
            status_rand = random.random()
            if status_rand < 0.30:
                status = LeaveRequest.Status.PENDING
                approver = None
                approval_remark = ''
            elif status_rand < 0.80:
                status = LeaveRequest.Status.APPROVED
                approver = random.choice(managers) if managers else None
                approval_remark = random.choice(self.APPROVAL_REMARKS)
            else:
                status = LeaveRequest.Status.REJECTED
                approver = random.choice(managers) if managers else None
                approval_remark = random.choice(self.REJECT_REMARKS)

            leave = LeaveRequest(
                employee=employee,
                leave_type=leave_type,
                start_time=start_time,
                end_time=end_time,
                reason=random.choice(self.LEAVE_REASONS),
                status=status,
                approver=approver,
                approval_remark=approval_remark
            )
            leaves.append(leave)

        LeaveRequest.objects.bulk_create(leaves)
        self.stdout.write(f'  [OK] 成功生成 {len(leaves)} 条请假申请')
        return leaves

    def generate_salaries(self, count):
        """生成薪资记录"""
        self.stdout.write(f'生成薪资记录 ({count}条)...')

        employees = list(EmployeeProfile.objects.all())

        if not employees:
            self.stdout.write(self.style.ERROR('  [X] 缺少员工数据'))
            return []

        # 岗位基本工资范围
        position_salary_range = {
            EmployeeProfile.Position.MANAGER: (8000, 12000),
            EmployeeProfile.Position.CHEF: (6000, 9000),
            EmployeeProfile.Position.PASTRY: (5000, 7000),
            EmployeeProfile.Position.PREP: (4000, 5500),
            EmployeeProfile.Position.SERVER: (3500, 5000),
            EmployeeProfile.Position.CLEANER: (3000, 4500),
        }

        # 月份范围
        months = ['2025-10', '2025-11', '2025-12', '2026-01']

        salaries = []
        used_combinations = set()  # 防止同一员工同一月份重复

        attempts = 0
        max_attempts = count * 10

        while len(salaries) < count and attempts < max_attempts:
            attempts += 1

            employee = random.choice(employees)
            year_month = random.choice(months)

            # 确保唯一性
            combo = (employee.id, year_month)
            if combo in used_combinations:
                continue

            # 获取岗位工资范围
            salary_range = position_salary_range.get(employee.position, (3000, 12000))
            base_salary = Decimal(str(random.randint(salary_range[0], salary_range[1])))

            # 岗位津贴
            position_allowance = Decimal(str(random.randint(500, 2000)))

            # 统计数据
            work_days = random.randint(20, 23)
            late_count = random.randint(0, 5)
            missing_count = random.randint(0, 3)
            overtime_hours = Decimal(str(random.randint(0, 40) + random.random()))

            # 计算加班费：时薪 × 1.5 × 加班小时
            daily_wage = base_salary / Decimal('21.75')
            hourly_wage = daily_wage / Decimal('8')
            overtime_pay = (hourly_wage * Decimal('1.5') * overtime_hours).quantize(Decimal('0.01'))

            # 扣款：迟到×20 + 缺卡×50
            deductions = Decimal(str(late_count * 20 + missing_count * 50 + random.randint(0, 100)))

            # 实发工资
            total_salary = base_salary + position_allowance + overtime_pay - deductions

            # 状态
            status = random.choice([
                SalaryRecord.Status.DRAFT,
                SalaryRecord.Status.PUBLISHED,
                SalaryRecord.Status.APPEALED,
                SalaryRecord.Status.ADJUSTED
            ])

            salary = SalaryRecord(
                employee=employee,
                year_month=year_month,
                base_salary=base_salary,
                position_allowance=position_allowance,
                overtime_pay=overtime_pay,
                deductions=deductions,
                total_salary=total_salary,
                work_days=work_days,
                late_count=late_count,
                missing_count=missing_count,
                overtime_hours=overtime_hours,
                status=status
            )
            salaries.append(salary)
            used_combinations.add(combo)

        SalaryRecord.objects.bulk_create(salaries)
        self.stdout.write(f'  [OK] 成功生成 {len(salaries)} 条薪资记录')
        return salaries

    def generate_appeals(self, count):
        """生成申诉"""
        self.stdout.write(f'生成申诉 ({count}条)...')

        employees = list(EmployeeProfile.objects.all())
        attendance_records = list(AttendanceRecord.objects.all())
        salary_records = list(SalaryRecord.objects.all())
        managers = list(EmployeeProfile.objects.filter(position=EmployeeProfile.Position.MANAGER))

        if not employees:
            self.stdout.write(self.style.ERROR('  [X] 缺少员工数据'))
            return []

        appeals = []

        for i in range(count):
            employee = random.choice(employees)

            # 申诉类型
            if random.random() < 0.5 and attendance_records:
                appeal_type = Appeal.AppealType.ATTENDANCE
                target_id = random.choice(attendance_records).id
                reason = random.choice(self.APPEAL_REASONS_ATTENDANCE)
            elif salary_records:
                appeal_type = Appeal.AppealType.SALARY
                target_id = random.choice(salary_records).id
                reason = random.choice(self.APPEAL_REASONS_SALARY)
            else:
                continue

            # 状态分布
            status_rand = random.random()
            if status_rand < 0.40:
                status = Appeal.Status.PENDING
                approver = None
                approval_remark = None
            elif status_rand < 0.75:
                status = Appeal.Status.APPROVED
                approver = random.choice(managers) if managers else None
                approval_remark = random.choice(self.APPROVAL_REMARKS)
            else:
                status = Appeal.Status.REJECTED
                approver = random.choice(managers) if managers else None
                approval_remark = random.choice(self.REJECT_REMARKS)

            appeal = Appeal(
                appeal_type=appeal_type,
                employee=employee,
                target_id=target_id,
                reason=reason,
                status=status,
                approver=approver,
                approval_remark=approval_remark
            )
            appeals.append(appeal)

        Appeal.objects.bulk_create(appeals)
        self.stdout.write(f'  [OK] 成功生成 {len(appeals)} 条申诉')
        return appeals

    # ==================== 验证方法 ====================

    def verify_data(self):
        """验证生成的数据"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('数据验证结果：')
        self.stdout.write('='*50)

        models_to_check = [
            ('employee_profiles', EmployeeProfile, 100),
            ('shifts', Shift, 100),
            ('users', User, 100),
            ('schedules', Schedule, 100),
            ('shift_swap_requests', ShiftSwapRequest, 100),
            ('attendance_records', AttendanceRecord, 100),
            ('leave_requests', LeaveRequest, 100),
            ('salary_records', SalaryRecord, 100),
            ('appeals', Appeal, 100),
        ]

        all_ok = True
        for name, model, expected in models_to_check:
            actual = model.objects.count()
            status = '[OK]' if actual == expected else '[X]'
            if actual != expected:
                all_ok = False
            self.stdout.write(f'  {status} {name}: {actual}/{expected}')

        # 验证外键关系
        self.stdout.write('\n外键关系验证：')

        # 检查User的employee_id是否有效
        invalid_users = User.objects.filter(employee_id__isnull=False).exclude(
            employee_id__in=EmployeeProfile.objects.values_list('id', flat=True)
        ).count()
        self.stdout.write(f'  {"[OK]" if invalid_users == 0 else "[X]"} User.employee_id 引用: {invalid_users} 个无效引用')

        # 检查薪资计算
        self.stdout.write('\n薪资计算验证：')
        salaries = SalaryRecord.objects.all()
        calc_errors = 0
        for salary in salaries:
            expected_total = (salary.base_salary + salary.position_allowance +
                            salary.overtime_pay - salary.deductions)
            if salary.total_salary != expected_total:
                calc_errors += 1
        self.stdout.write(f'  {"[OK]" if calc_errors == 0 else "[X]"} 薪资计算正确: {calc_errors} 个错误')

        # 检查考勤状态
        self.stdout.write('\n考勤状态验证：')
        attendance = AttendanceRecord.objects.all()
        status_errors = 0
        for record in attendance:
            if record.status != record._calculate_status():
                status_errors += 1
        self.stdout.write(f'  {"[OK]" if status_errors == 0 else "[X]"} 考勤状态正确: {status_errors} 个错误')

        self.stdout.write('='*50)

        if all_ok:
            self.stdout.write(self.style.SUCCESS('\n[OK] 所有数据验证通过！'))
        else:
            self.stdout.write(self.style.WARNING('\n[!] 部分数据验证未通过，请检查'))

        return all_ok

    # ==================== 主方法 ====================

    @transaction.atomic
    def handle(self, *args, **options):
        count = options['count']
        skip_clear = options['skip_clear']

        self.stdout.write('\n' + '='*50)
        self.stdout.write('食堂管理系统 - 测试数据生成工具')
        self.stdout.write('='*50 + '\n')

        # 确保系统设置存在
        SystemSettings.get_settings()
        self.stdout.write('[OK] 系统设置已就绪\n')

        # 清空数据
        if not skip_clear:
            self.clear_all_data()
            self.stdout.write('')

        # 生成数据（按依赖顺序）
        self.stdout.write('开始生成测试数据...\n')

        self.generate_employees(count)
        self.generate_shifts(count)
        self.generate_users(count)
        self.generate_schedules(count)
        self.generate_swap_requests(count)
        self.generate_attendance(count)
        self.generate_leaves(count)
        self.generate_salaries(count)
        self.generate_appeals(count)

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('测试数据生成完成！'))

        # 验证数据
        self.verify_data()
