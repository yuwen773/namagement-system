# 薪资导出功能设计方案

## 需求背景

薪资管理模块的导出功能已在前端预留接口，但后端尚未实现。用户需要按月份导出所有员工的薪资数据为 Excel 文件。

## 解决方案

在薪资管理模块中添加导出功能，支持按月份导出所有员工的薪资数据为 Excel (.xlsx) 文件。

## 设计方案

### 1. 技术选型

- **Excel 生成库**: openpyxl
- **导出格式**: Excel (.xlsx)
- **API 路径**: `/salaries/salaries/export/`

### 2. 后端实现

#### 2.1 安装依赖

```bash
pip install openpyxl
```

#### 2.2 添加导出 API

在 `backend/salaries/views.py` 的 `SalaryRecordViewSet` 中添加 `export` action：

```python
@action(detail=False, methods=['get'])
def export(self, request):
    """导出薪资数据为 Excel"""
    year_month = request.query_params.get('year_month')

    if not year_month:
        return Response(
            {'code': 400, 'message': '请指定年份月份'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 查询薪资数据
    queryset = self.get_queryset().filter(year_month=year_month).select_related('employee')

    # 创建 Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "薪资表"

    # 写入表头
    headers = ['序号', '员工姓名', '岗位', '年月', '基本工资', '岗位津贴', '加班费', '扣款', '实发工资', '状态']
    ws.append(headers)

    # 写入数据
    for idx, record in enumerate(queryset, 1):
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
        ws.append([
            idx,
            record.employee.real_name if record.employee else '',
            position_map.get(record.employee.position, record.employee.position) if record.employee else '',
            record.year_month,
            float(record.base_salary),
            float(record.position_allowance),
            float(record.overtime_pay),
            float(record.deductions),
            float(record.total_salary),
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

### 3. 前端实现

修改 `frontend/src/views/admin/SalaryManageView.vue` 中的 `handleExport` 函数：

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
    ElMessage.error('导出失败')
  }
}
```

### 4. Excel 表格设计

| 列 | 字段 | 说明 |
|---|---|---|
| A | 序号 | 从 1 开始 |
| B | 员工姓名 | 员工真实姓名 |
| C | 岗位 | 岗位中文名称 |
| D | 年月 | 格式：YYYY-MM |
| E | 基本工资 | 数值 |
| F | 岗位津贴 | 数值 |
| G | 加班费 | 数值 |
| H | 扣款 | 数值 |
| I | 实发工资 | 数值 |
| J | 状态 | 草稿/已发布/申诉中/已调整 |

## 影响范围

- `backend/requirements.txt` - 添加 openpyxl 依赖
- `backend/salaries/views.py` - 添加 export action
- `frontend/src/views/admin/SalaryManageView.vue` - 实现 handleExport

## 测试要点

1. 验证导出功能正常下载 Excel 文件
2. 验证 Excel 内容正确
3. 验证未选择月份时的错误提示
4. 验证无数据时的导出结果
