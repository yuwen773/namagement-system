# 薪资导出功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现薪资管理模块的导出功能，支持按月份导出所有员工的薪资数据为 Excel (.xlsx) 文件。

**Architecture:** 在后端添加 export action，前端调用已预留的 API 接口触发下载。

**Tech Stack:** Django 5.2, DRF, openpyxl, Vue 3, Element Plus

---

## Task 1: 安装 openpyxl 依赖

**Files:**
- Modify: `backend/requirements.txt`

**Step 1: 添加 openpyxl 到 requirements.txt**

打开 `backend/requirements.txt`，在末尾添加：

```
openpyxl>=3.1.0
```

**Step 2: 安装依赖**

Run: `pip install openpyxl`
Expected: Successfully installed openpyxl-xxx

**Step 3: 提交代码**

```bash
git add backend/requirements.txt
git commit -m "feat: 添加 openpyxl 依赖用于薪资导出功能

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: 后端添加导出 API

**Files:**
- Modify: `backend/salaries/views.py`

**Step 1: 添加 import 语句**

在 `backend/salaries/views.py` 文件顶部添加：

```python
from django.http import HttpResponse
from openpyxl import Workbook
```

**Step 2: 在 SalaryRecordViewSet 中添加 export action**

在 `SalaryRecordViewSet` 类中，找到 `my-salaries` action（大约第313行），在其后添加：

```python
@action(detail=False, methods=['get'], url_path='export')
def export(self, request):
    """导出薪资数据为 Excel"""
    from salaries.models import SalaryRecord

    year_month = request.query_params.get('year_month')

    if not year_month:
        return Response(
            {'code': 400, 'message': '请指定年份月份'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 查询薪资数据
    queryset = SalaryRecord.objects.filter(year_month=year_month).select_related('employee')

    # 创建 Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "薪资表"

    # 写入表头
    headers = ['序号', '员工姓名', '岗位', '年月', '基本工资', '岗位津贴', '加班费', '扣款', '实发工资', '状态']
    ws.append(headers)

    # 状态和岗位映射
    status_map = {
        'DRAFT': '草稿',
        'PUBLISHED': '已发布',
        'APPEALED': '申诉中',
        'ADJUSTED': '已调整'
    }
    position_map = {
        'CHEF': '厨师',
        'PASTRY': '面点',
        'PREP': '切配',
        'CLEANER': '保洁',
        'SERVER': '服务员',
        'MANAGER': '经理'
    }

    # 写入数据
    for idx, record in enumerate(queryset, 1):
        employee = record.employee
        ws.append([
            idx,
            employee.real_name if employee else '',
            position_map.get(employee.position, employee.position) if employee else '',
            record.year_month,
            float(record.base_salary) if record.base_salary else 0,
            float(record.position_allowance) if record.position_allowance else 0,
            float(record.overtime_pay) if record.overtime_pay else 0,
            float(record.deductions) if record.deductions else 0,
            float(record.total_salary) if record.total_salary else 0,
            status_map.get(record.status, record.status)
        ])

    # 设置列宽
    ws.column_dimensions['A'].width = 8
    ws.column_dimensions['B'].width = 12
    ws.column_dimensions['C'].width = 10
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['E'].width = 12
    ws.column_dimensions['F'].width = 12
    ws.column_dimensions['G'].width = 12
    ws.column_dimensions['H'].width = 12
    ws.column_dimensions['I'].width = 12
    ws.column_dimensions['J'].width = 10

    # 返回文件
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=薪资表_{year_month}.xlsx'
    wb.save(response)
    return response
```

**Step 3: 验证代码语法正确**

Run: `cd backend && python -c "from salaries.views import SalaryRecordViewSet; print('OK')"`
Expected: 输出 OK，无错误

**Step 4: 提交代码**

```bash
git add backend/salaries/views.py
git commit -m "feat: 添加薪资导出 API

- 添加 /salaries/salaries/export/ 接口
- 支持按月份导出薪资数据为 Excel

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: 前端实现导出功能

**Files:**
- Modify: `frontend/src/views/admin/SalaryManageView.vue`

**Step 1: 查找并修改 handleExport 函数**

在 `SalaryManageView.vue` 中找到 `handleExport` 函数（约在第663行），替换为：

```javascript
const handleExport = async () => {
  if (!selectedMonth.value) {
    ElMessage.warning('请先选择月份')
    return
  }

  try {
    const response = await exportSalarySheet({ year_month: selectedMonth.value })
    // 处理 blob 下载
    const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `薪资表_${selectedMonth.value}.xlsx`
    link.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  }
}
```

**Step 2: 验证前端代码无语法错误**

Run: `cd frontend && npm run build 2>&1 | head -20`
Expected: 构建成功，无错误

**Step 3: 提交代码**

```bash
git add frontend/src/views/admin/SalaryManageView.vue
git commit -m "feat: 实现薪资导出功能

- 前端调用导出 API 并触发浏览器下载

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: 测试导出功能

**Step 1: 启动后端服务**

Run: `cd backend && python manage.py runserver`

**Step 2: 测试导出 API**

打开浏览器或使用 curl 访问：
```
http://localhost:8000/api/salaries/salaries/export/?year_month=2026-01
```

Expected: 返回 Excel 文件下载

**Step 3: 启动前端服务**

Run: `cd frontend && npm run dev`

**Step 4: 测试前端导出功能**

1. 登录管理员账号
2. 导航到薪资管理页面
3. 选择月份（确保该月份有薪资数据）
4. 点击"导出工资表"按钮
Expected: 浏览器下载薪资表_2026-01.xlsx 文件

**Step 5: 提交测试结果**

```bash
git commit --allow-empty -m "test: 验证薪资导出功能

- 后端 API 正常返回 Excel 文件
- 前端导出功能正常工作

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```
