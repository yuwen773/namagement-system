"""
统计分析视图

提供人员、考勤、薪资等统计数据的 API 接口
数据格式适配 ECharts 渲染
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Count, Q, Sum, Avg
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from decimal import Decimal

from employees.models import EmployeeProfile
from attendance.models import AttendanceRecord
from salaries.models import SalaryRecord
from schedules.models import Schedule
from leaves.models import LeaveRequest


@api_view(["GET"])
@permission_classes([AllowAny])
def employee_statistics(request):
    """
    人员统计接口

    返回：
    - 总人数
    - 岗位分布（用于饼图）
    - 持证率统计
    - 入职状态分布
    """
    try:
        # 获取所有在职员工
        active_employees = EmployeeProfile.objects.filter(status="ACTIVE")

        # 总人数
        total_count = active_employees.count()

        # 岗位分布统计
        position_stats = active_employees.values("position").annotate(
            count=Count("id")
        ).order_by("-count")

        # 岗位分布数据（用于 ECharts 饼图）
        position_labels = []
        position_data = []
        position_mapping = {
            "CHEF": "厨师",
            "PASTRY": "面点",
            "PREP": "切配",
            "CLEANER": "保洁",
            "SERVER": "服务员",
            "MANAGER": "经理"
        }
        for item in position_stats:
            label = position_mapping.get(item["position"], item["position"])
            position_labels.append(label)
            position_data.append(item["count"])

        # 持证率统计
        health_cert_count = active_employees.filter(
            health_certificate_no__isnull=False
        ).exclude(health_certificate_no="").count()

        chef_cert_count = active_employees.filter(
            chef_certificate_level__isnull=False
        ).exclude(chef_certificate_level="").count()

        health_cert_rate = round(
            (health_cert_count / total_count * 100) if total_count > 0 else 0, 2
        )
        chef_cert_rate = round(
            (chef_cert_count / total_count * 100) if total_count > 0 else 0, 2
        )

        # 入职状态分布
        status_stats = EmployeeProfile.objects.values("status").annotate(
            count=Count("id")
        ).order_by("-count")

        status_mapping = {
            "ACTIVE": "在职",
            "INACTIVE": "离职",
            "LEAVE_WITHOUT_PAY": "停薪留职"
        }
        status_labels = []
        status_data = []
        for item in status_stats:
            label = status_mapping.get(item["status"], item["status"])
            status_labels.append(label)
            status_data.append(item["count"])

        return Response({
            "code": 200,
            "message": "获取人员统计数据成功",
            "data": {
                # 总览数据
                "overview": {
                    "total_count": total_count,
                    "health_cert_rate": health_cert_rate,
                    "chef_cert_rate": chef_cert_rate
                },
                # 岗位分布（饼图数据）
                "position_distribution": {
                    "labels": position_labels,
                    "data": position_data
                },
                # 持证统计
                "certificates": {
                    "health_cert_count": health_cert_count,
                    "chef_cert_count": chef_cert_count,
                    "health_cert_rate": health_cert_rate,
                    "chef_cert_rate": chef_cert_rate
                },
                # 入职状态分布（饼图数据）
                "status_distribution": {
                    "labels": status_labels,
                    "data": status_data
                }
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "code": 500,
            "message": f"获取人员统计数据失败：{str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def attendance_statistics(request):
    """
    考勤统计接口

    查询参数：
    - start_date: 开始日期 (YYYY-MM-DD)
    - end_date: 结束日期 (YYYY-MM-DD)
    - days: 最近N天 (默认7天)

    返回：
    - 出勤率统计
    - 迟到次数统计
    - 缺卡次数统计
    - 加班时长统计
    - 日期维度的考勤趋势（用于折线图）
    """
    try:
        # 获取查询参数
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        days = request.query_params.get("days", 7)

        # 确定日期范围
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=int(days))

        # 获取日期范围内的排班记录（用于计算应出勤次数）
        schedules_in_range = Schedule.objects.filter(
            work_date__gte=start_date,
            work_date__lte=end_date
        )
        total_should_attend = schedules_in_range.count()

        # 获取日期范围内的考勤记录
        attendance_records = AttendanceRecord.objects.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )

        # 统计各种考勤状态
        total_records = attendance_records.count()
        normal_count = attendance_records.filter(status="NORMAL").count()
        late_count = attendance_records.filter(status="LATE").count()
        early_leave_count = attendance_records.filter(status="EARLY_LEAVE").count()
        missing_count = attendance_records.filter(status="MISSING").count()
        abnormal_count = attendance_records.filter(status="ABNORMAL").count()

        # 实际出勤天数（正常 + 迟到 + 早退都算出勤）
        present_count = normal_count + late_count + early_leave_count

        # 出勤率
        attendance_rate = round(
            (present_count / total_should_attend * 100) if total_should_attend > 0 else 0, 2
        )

        # 加班统计
        overtime_records = attendance_records.filter(
            clock_out_time__isnull=False
        )
        total_overtime_hours = sum(
            record.calculate_overtime_hours() or 0
            for record in overtime_records
        )
        total_overtime_hours = round(total_overtime_hours, 2)

        # 日期维度的考勤趋势（用于折线图）
        daily_stats = []
        current_date = start_date
        while current_date <= end_date:
            day_records = AttendanceRecord.objects.filter(
                created_at__date=current_date
            )

            day_normal = day_records.filter(status="NORMAL").count()
            day_late = day_records.filter(status="LATE").count()
            day_early = day_records.filter(status="EARLY_LEAVE").count()
            day_missing = day_records.filter(status="MISSING").count()

            daily_stats.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "normal": day_normal,
                "late": day_late,
                "early_leave": day_early,
                "missing": day_missing,
                "total": day_records.count()
            })

            current_date += timedelta(days=1)

        # 岗位维度的考勤统计
        position_attendance = []
        position_mapping = {
            "CHEF": "厨师",
            "PASTRY": "面点",
            "PREP": "切配",
            "CLEANER": "保洁",
            "SERVER": "服务员",
            "MANAGER": "经理"
        }
        for position_code, position_name in position_mapping.items():
            employees = EmployeeProfile.objects.filter(position=position_code)
            position_records = attendance_records.filter(employee__in=employees)

            if position_records.exists():
                position_late = position_records.filter(status="LATE").count()
                position_missing = position_records.filter(status="MISSING").count()
                position_overtime = sum(
                    record.calculate_overtime_hours() or 0
                    for record in position_records.filter(clock_out_time__isnull=False)
                )

                position_attendance.append({
                    "position": position_name,
                    "late_count": position_late,
                    "missing_count": position_missing,
                    "overtime_hours": round(position_overtime, 2)
                })

        return Response({
            "code": 200,
            "message": "获取考勤统计数据成功",
            "data": {
                # 总览数据
                "overview": {
                    "total_should_attend": total_should_attend,
                    "total_records": total_records,
                    "attendance_rate": attendance_rate,
                    "present_count": present_count,
                    "late_count": late_count,
                    "early_leave_count": early_leave_count,
                    "missing_count": missing_count,
                    "abnormal_count": abnormal_count,
                    "total_overtime_hours": total_overtime_hours
                },
                # 状态分布（用于饼图）
                "status_distribution": {
                    "labels": ["正常", "迟到", "早退", "缺卡", "异常"],
                    "data": [normal_count, late_count, early_leave_count, missing_count, abnormal_count]
                },
                # 日期趋势（用于折线图）
                "daily_trend": daily_stats,
                # 岗位维度统计
                "position_stats": position_attendance
            }
        }, status=status.HTTP_200_OK)

    except ValueError as e:
        return Response({
            "code": 400,
            "message": f"日期格式错误：{str(e)}",
            "data": None
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            "code": 500,
            "message": f"获取考勤统计数据失败：{str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def salary_statistics(request):
    """
    薪资统计接口

    查询参数：
    - months: 最近N个月 (默认12个月)

    返回：
    - 月度薪资支出趋势（用于折线图）
    - 岗位薪资对比（用于柱状图）
    - 薪资构成统计
    """
    try:
        months = request.query_params.get("months", 12)

        # 计算日期范围
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * int(months))

        # 获取薪资记录
        salary_records = SalaryRecord.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date,
            status__in=["PUBLISHED", "ADJUSTED"]  # 只统计已发布的薪资
        ).order_by("year_month")

        if not salary_records.exists():
            return Response({
                "code": 200,
                "message": "暂无薪资数据",
                "data": {
                    "monthly_trend": [],
                    "position_comparison": [],
                    "composition": {}
                }
            }, status=status.HTTP_200_OK)

        # 月度薪资支出趋势（用于折线图）
        monthly_data = {}
        for record in salary_records:
            year_month = record.year_month
            if year_month not in monthly_data:
                monthly_data[year_month] = {
                    "year_month": year_month,
                    "total_salary": Decimal("0.00"),
                    "base_salary": Decimal("0.00"),
                    "position_allowance": Decimal("0.00"),
                    "overtime_pay": Decimal("0.00"),
                    "deductions": Decimal("0.00"),
                    "count": 0
                }

            monthly_data[year_month]["total_salary"] += record.total_salary or Decimal("0.00")
            monthly_data[year_month]["base_salary"] += record.base_salary or Decimal("0.00")
            monthly_data[year_month]["position_allowance"] += record.position_allowance or Decimal("0.00")
            monthly_data[year_month]["overtime_pay"] += record.overtime_pay or Decimal("0.00")
            monthly_data[year_month]["deductions"] += record.deductions or Decimal("0.00")
            monthly_data[year_month]["count"] += 1

        # 转换为列表并排序
        monthly_trend = [
            {
                "year_month": v["year_month"],
                "total_salary": float(v["total_salary"]),
                "base_salary": float(v["base_salary"]),
                "position_allowance": float(v["position_allowance"]),
                "overtime_pay": float(v["overtime_pay"]),
                "deductions": float(v["deductions"]),
                "avg_salary": float(v["total_salary"] / v["count"]) if v["count"] > 0 else 0,
                "count": v["count"]
            }
            for v in sorted(monthly_data.values(), key=lambda x: x["year_month"])
        ]

        # 岗位薪资对比（用于柱状图）
        position_mapping = {
            "CHEF": "厨师",
            "PASTRY": "面点",
            "PREP": "切配",
            "CLEANER": "保洁",
            "SERVER": "服务员",
            "MANAGER": "经理"
        }

        position_data = []
        for position_code, position_name in position_mapping.items():
            employees = EmployeeProfile.objects.filter(position=position_code)
            position_salaries = salary_records.filter(employee__in=employees)

            if position_salaries.exists():
                total = sum(s.total_salary or Decimal("0.00") for s in position_salaries)
                avg_salary = total / position_salaries.count()

                position_data.append({
                    "position": position_name,
                    "total_salary": float(total),
                    "avg_salary": float(avg_salary),
                    "count": position_salaries.count()
                })

        # 薪资构成统计
        total_base = sum(s.base_salary or Decimal("0.00") for s in salary_records)
        total_allowance = sum(s.position_allowance or Decimal("0.00") for s in salary_records)
        total_overtime = sum(s.overtime_pay or Decimal("0.00") for s in salary_records)
        total_deductions = sum(s.deductions or Decimal("0.00") for s in salary_records)
        grand_total = sum(s.total_salary or Decimal("0.00") for s in salary_records)

        composition = {
            "base_salary": float(total_base),
            "position_allowance": float(total_allowance),
            "overtime_pay": float(total_overtime),
            "deductions": float(total_deductions),
            "total_salary": float(grand_total),
            "distribution": {
                "labels": ["基本工资", "岗位津贴", "加班费", "扣款"],
                "data": [
                    float(total_base),
                    float(total_allowance),
                    float(total_overtime),
                    abs(float(total_deductions))  # 扣款取绝对值显示
                ]
            }
        }

        return Response({
            "code": 200,
            "message": "获取薪资统计数据成功",
            "data": {
                # 月度趋势（用于折线图）
                "monthly_trend": monthly_trend,
                # 岗位对比（用于柱状图）
                "position_comparison": position_data,
                # 薪资构成（用于饼图）
                "composition": composition
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "code": 500,
            "message": f"获取薪资统计数据失败：{str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def overview_statistics(request):
    """
    总览统计接口（Dashboard 首页）

    返回：
    - 今日概览数据
    - 待办事项统计
    - 快捷统计卡片
    """
    try:
        today = datetime.now().date()

        # 今日排班统计
        today_schedules = Schedule.objects.filter(work_date=today)
        today_should_attend = today_schedules.count()

        # 今日考勤统计
        today_attendance = AttendanceRecord.objects.filter(
            created_at__date=today
        )
        today_present = today_attendance.filter(
            status__in=["NORMAL", "LATE", "EARLY_LEAVE"]
        ).count()
        today_late = today_attendance.filter(status="LATE").count()
        today_missing = today_attendance.filter(status="MISSING").count()

        # 今日请假
        today_leaves = LeaveRequest.objects.filter(
            start_time__lte=today,
            end_time__gte=today,
            status="APPROVED"
        ).count()

        # 今日异常考勤
        today_abnormal = today_attendance.filter(
            status__in=["LATE", "EARLY_LEAVE", "MISSING", "ABNORMAL"]
        ).count()

        # 待办事项统计
        pending_leaves = LeaveRequest.objects.filter(status="PENDING").count()
        pending_attendance_appeals = AttendanceRecord.objects.filter(
            correction_remark__isnull=False
        ).count()  # 有更正备注的考勤记录
        pending_salaries = SalaryRecord.objects.filter(status="DRAFT").count()

        # 总览统计
        total_employees = EmployeeProfile.objects.filter(status="ACTIVE").count()
        total_positions = EmployeeProfile.objects.filter(
            status="ACTIVE"
        ).values("position").distinct().count()

        # 本月考勤统计
        from datetime import timedelta
        month_start = today.replace(day=1)
        month_attendance = AttendanceRecord.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lte=today
        )
        month_late = month_attendance.filter(status="LATE").count()
        month_missing = month_attendance.filter(status="MISSING").count()

        return Response({
            "code": 200,
            "message": "获取总览统计数据成功",
            "data": {
                # 今日概览
                "today": {
                    "should_attend": today_should_attend,
                    "present": today_present,
                    "late": today_late,
                    "missing": today_missing,
                    "leaves": today_leaves,
                    "abnormal": today_abnormal,
                    "attendance_rate": round(
                        (today_present / today_should_attend * 100) if today_should_attend > 0 else 0, 2
                    )
                },
                # 待办事项
                "pending": {
                    "leaves": pending_leaves,
                    "attendance_corrections": pending_attendance_appeals,
                    "salary_generation": pending_salaries
                },
                # 总览统计
                "overview": {
                    "total_employees": total_employees,
                    "total_positions": total_positions
                },
                # 本月考勤
                "month_attendance": {
                    "late_count": month_late,
                    "missing_count": month_missing
                }
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "code": 500,
            "message": f"获取总览统计数据失败：{str(e)}",
            "data": None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
