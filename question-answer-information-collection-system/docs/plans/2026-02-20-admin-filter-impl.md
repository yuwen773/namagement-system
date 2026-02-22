# 管理端筛选功能实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为管理端的用户管理、公告管理、数据中心三个页面添加高级筛选功能，同时修改后端 API 支持筛选参数。

**Architecture:** 后端修改 ViewSet 的 list 方法添加筛选逻辑，前端添加筛选栏组件，使用 Element Plus 的 Select 和 DatePicker 组件。

**Tech Stack:** Django REST Framework + Vue 3 + Element Plus

---

## 阶段一：后端 API 修改

### Task 1: 修改用户管理 API

**Files:**
- Modify: `backend/apps/accounts/views.py:66-74`

**Step 1: 修改 UserListView.list 方法，添加分页和筛选支持**

```python
def list(self, request):
    """GET /api/auth/users/ - 获取用户列表（支持分页和筛选）"""
    queryset = self.get_queryset()

    # 搜索
    search = request.query_params.get('search', '')
    if search:
        queryset = queryset.filter(username__icontains=search)

    # 角色筛选
    role = request.query_params.get('role', '')
    if role:
        queryset = queryset.filter(role=role)

    # 状态筛选
    is_active = request.query_params.get('is_active')
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active.lower() == 'true')

    # 创建时间范围筛选
    created_at_after = request.query_params.get('created_at_after')
    created_at_before = request.query_params.get('created_at_before')
    if created_at_after:
        queryset = queryset.filter(created_at__gte=created_at_after)
    if created_at_before:
        queryset = queryset.filter(created_at__lte=created_at_before)

    # 排序
    ordering = request.query_params.get('ordering', '-created_at')
    if ordering in ['created_at', '-created_at', 'username', '-username']:
        queryset = queryset.order_by(ordering)

    # 分页
    try:
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        page_size = min(page_size, 100)
    except (ValueError, TypeError):
        page, page_size = 1, 20

    total = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    queryset = queryset[start:end]

    serializer = self.get_serializer(queryset, many=True)
    return Response({
        'code': 0,
        'data': serializer.data,
        'total': total
    })
```

**Step 2: 测试 API**
```bash
curl "http://localhost:8000/api/auth/users/?page=1&page_size=10&role=admin&is_active=true"
```

---

### Task 2: 修改公告管理 API

**Files:**
- Modify: `backend/apps/notices/views.py:27-35`

**Step 1: 修改 NoticeViewSet.get_queryset 和 list 方法**

```python
def get_queryset(self):
    """根据用户角色返回不同范围的公告"""
    user = self.request.user
    if hasattr(user, 'role') and user.role == 'admin':
        # 管理员可以看到全部公告
        return Notice.objects.all()
    # 普通用户只看启用公告
    return Notice.objects.filter(is_active=True)

def list(self, request, *args, **kwargs):
    """获取公告列表（支持分页和筛选）"""
    queryset = self.get_queryset()

    # 搜索
    search = request.query_params.get('search', '')
    if search:
        queryset = queryset.filter(title__icontains=search)

    # 状态筛选
    is_active = request.query_params.get('is_active')
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active.lower() == 'true')

    # 创建时间范围筛选
    created_at_after = request.query_params.get('created_at_after')
    created_at_before = request.query_params.get('created_at_before')
    if created_at_after:
        queryset = queryset.filter(created_at__gte=created_at_after)
    if created_at_before:
        queryset = queryset.filter(created_at__lte=created_at_before)

    # 排序
    ordering = request.query_params.get('ordering', '-created_at')
    if ordering in ['created_at', '-created_at', 'title', '-title']:
        queryset = queryset.order_by(ordering)

    # 分页
    try:
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        page_size = min(page_size, 100)
    except (ValueError, TypeError):
        page, page_size = 1, 20

    total = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    queryset = queryset[start:end]

    serializer = self.get_serializer(queryset, many=True)
    return Response({
        'code': 0,
        'data': serializer.data,
        'total': total
    })
```

**Step 2: 测试 API**
```bash
curl "http://localhost:8000/api/notices/?page=1&page_size=10&is_active=true"
```

---

### Task 3: 修改数据中心 API（问答筛选）

**Files:**
- Modify: `backend/apps/api/views.py:548-616`

**Step 1: 修改 QuestionViewSet.list 方法，添加更多筛选参数**

在现有 list 方法中添加以下筛选逻辑：

```python
# 分类筛选
category = request.query_params.get('category', '')
if category:
    queryset = queryset.filter(category=category)

# 地理位置筛选
location = request.query_params.get('location', '')
if location:
    queryset = queryset.filter(location=location)

# 发布时间范围筛选
publish_time_after = request.query_params.get('publish_time_after')
publish_time_before = request.query_params.get('publish_time_before')
if publish_time_after:
    queryset = queryset.filter(publish_time__gte=publish_time_after)
if publish_time_before:
    queryset = queryset.filter(publish_time__lte=publish_time_before)

# 回答数量范围筛选
answer_count_min = request.query_params.get('answer_count_min')
answer_count_max = request.query_params.get('answer_count_max')
if answer_count_min:
    queryset = queryset.filter(answer_count__gte=int(answer_count_min))
if answer_count_max:
    queryset = queryset.filter(answer_count__lte=int(answer_count_max))

# 更新排序选项
ordering = request.query_params.get('ordering', '-created_at')
valid_orderings = ['created_at', '-created_at', 'publish_time', '-publish_time', 'answer_count', '-answer_count']
if ordering in valid_orderings:
    queryset = queryset.order_by(ordering)
```

**Step 2: 添加获取可选分类/位置的 API**

在 `backend/apps/api/views.py` 末尾添加新视图：

```python
class QuestionFilterOptionsView(APIView):
    """获取问答筛选选项"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """获取可选的分类和位置列表"""
        # 获取所有不同的分类
        categories = Question.objects.filter(
            category__isnull=False
        ).exclude(category='').values_list('category', flat=True).distinct()

        # 获取所有不同的位置
        locations = Question.objects.filter(
            location__isnull=False
        ).exclude(location='').values_list('location', flat=True).distinct()

        return Response(
            make_response(code=0, data={
                'categories': list(categories),
                'locations': list(locations)
            })
        )
```

**Step 3: 注册新 URL**

在 `backend/apps/api/urls.py` 添加：

```python
path('questions/filter-options/', QuestionFilterOptionsView.as_view(), name='question-filter-options'),
```

**Step 4: 测试 API**
```bash
curl "http://localhost:8000/api/questions/?category=影视&location=广东&answer_count_min=1"
curl "http://localhost:8000/api/questions/filter-options/"
```

---

## 阶段二：前端筛选组件

### Task 4: 用户管理页面添加筛选

**Files:**
- Modify: `frontend/src/views/UserManagement.vue`

**Step 1: 在 control-bar 添加筛选下拉框**

在搜索框后添加：

```vue
<!-- 角色筛选 -->
<el-select
  v-model="filters.role"
  placeholder="角色"
  clearable
  class="filter-select"
  @change="handleFilterChange"
>
  <el-option label="全部" value="" />
  <el-option label="管理员" value="admin" />
  <el-option label="普通用户" value="user" />
</el-select>

<!-- 状态筛选 -->
<el-select
  v-model="filters.is_active"
  placeholder="状态"
  clearable
  class="filter-select"
  @change="handleFilterChange"
>
  <el-option label="全部" value="" />
  <el-option label="正常" value="true" />
  <el-option label="禁用" value="false" />
</el-select>
```

**Step 2: 添加筛选状态和方法**

```javascript
// 筛选状态
const filters = reactive({
  role: '',
  is_active: ''
})

// 修改 fetchData 方法
const fetchData = async () => {
  tableLoading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchKeyword.value || undefined,
      role: filters.role || undefined,
      is_active: filters.is_active || undefined
    }
    const res = await request.get('/api/auth/users/', { params })
    // ... 原有逻辑
  } finally {
    tableLoading.value = false
  }
}

// 筛选变化时重置页码
const handleFilterChange = () => {
  currentPage.value = 1
  fetchData()
}
```

---

### Task 5: 公告管理页面添加筛选

**Files:**
- Modify: `frontend/src/views/NoticeManagement.vue`

**Step 1: 添加筛选下拉框**

```vue
<!-- 状态筛选 -->
<el-select
  v-model="filters.is_active"
  placeholder="状态"
  clearable
  class="filter-select"
  @change="handleFilterChange"
>
  <el-option label="全部" value="" />
  <el-option label="启用" value="true" />
  <el-option label="禁用" value="false" />
</el-select>

<!-- 时间范围筛选 -->
<el-date-picker
  v-model="filters.dateRange"
  type="daterange"
  range-separator="至"
  start-placeholder="开始日期"
  end-placeholder="结束日期"
  value-format="YYYY-MM-DD"
  class="filter-date-range"
  @change="handleFilterChange"
/>
```

**Step 2: 添加筛选状态和方法**

```javascript
const filters = reactive({
  is_active: '',
  dateRange: null
})

const fetchData = async () => {
  tableLoading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchKeyword.value || undefined,
      is_active: filters.is_active || undefined,
      created_at_after: filters.dateRange?.[0] || undefined,
      created_at_before: filters.dateRange?.[1] || undefined
    }
    const res = await getNoticeList(params)
    // ... 原有逻辑
  } finally {
    tableLoading.value = false
  }
}
```

---

### Task 6: 数据中心页面添加筛选

**Files:**
- Modify: `frontend/src/views/DataCenter.vue`

**Step 1: 添加筛选下拉框**

```vue
<!-- 分类筛选 -->
<el-select
  v-model="filters.category"
  placeholder="分类"
  clearable
  class="filter-select"
  @change="handleFilterChange"
>
  <el-option label="全部" value="" />
  <el-option
    v-for="cat in filterOptions.categories"
    :key="cat"
    :label="cat"
    :value="cat"
  />
</el-select>

<!-- 位置筛选 -->
<el-select
  v-model="filters.location"
  placeholder="位置"
  clearable
  class="filter-select"
  @change="handleFilterChange"
>
  <el-option label="全部" value="" />
  <el-option
    v-for="loc in filterOptions.locations"
    :key="loc"
    :label="loc"
    :value="loc"
  />
</el-select>

<!-- 回答数筛选 -->
<el-select
  v-model="filters.answerCount"
  placeholder="回答数"
  clearable
  class="filter-select"
  @change="handleFilterChange"
>
  <el-option label="全部" value="" />
  <el-option label="0" value="0" />
  <el-option label="1-3" value="1-3" />
  <el-option label="3以上" value="3+" />
</el-select>

<!-- 发布时间筛选 -->
<el-date-picker
  v-model="filters.dateRange"
  type="daterange"
  range-separator="至"
  start-placeholder="开始日期"
  end-placeholder="结束日期"
  value-format="YYYY-MM-DD"
  class="filter-date-range"
  @change="handleFilterChange"
/>
```

**Step 2: 添加筛选状态和获取选项方法**

```javascript
// 筛选状态
const filters = reactive({
  category: '',
  location: '',
  answerCount: '',
  dateRange: null
})

// 筛选选项
const filterOptions = reactive({
  categories: [],
  locations: []
})

// 获取筛选选项
const fetchFilterOptions = async () => {
  try {
    const res = await request.get('/api/questions/filter-options/')
    if (res.code === 0) {
      filterOptions.categories = res.data.categories || []
      filterOptions.locations = res.data.locations || []
    }
  } catch (e) {
    console.error('Failed to fetch filter options:', e)
  }
}

// 修改 fetchData 方法
const fetchData = async () => {
  tableLoading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: searchKeyword.value || undefined,
      category: filters.category || undefined,
      location: filters.location || undefined,
      publish_time_after: filters.dateRange?.[0] || undefined,
      publish_time_before: filters.dateRange?.[1] || undefined
    }

    // 处理回答数筛选
    if (filters.answerCount) {
      if (filters.answerCount === '0') {
        params.answer_count_min = 0
        params.answer_count_max = 0
      } else if (filters.answerCount === '1-3') {
        params.answer_count_min = 1
        params.answer_count_max = 3
      } else if (filters.answerCount === '3+') {
        params.answer_count_min = 3
      }
    }

    const res = await getQuestions(params)
    // ... 原有逻辑
  } finally {
    tableLoading.value = false
  }
}

// 在 onMounted 中调用
onMounted(() => {
  fetchData()
  fetchFilterOptions()
})
```

**Step 3: 添加筛选样式**

```css
.filter-select {
  width: 相关140px;
}

.filter-date-range {
  width: 240px;
}
```

---

## 验收测试

### 后端 API 测试

1. 用户管理 API
```bash
# 测试分页
curl "http://localhost:8000/api/auth/users/?page=1&page_size=5"
# 测试角色筛选
curl "http://localhost:8000/api/auth/users/?role=admin"
# 测试状态筛选
curl "http://localhost:8000/api/auth/users/?is_active=true"
```

2. 公告管理 API
```bash
# 测试管理员查看全部公告
curl "http://localhost:8000/api/notices/?is_active=false"
# 测试时间筛选
curl "http://localhost:8000/api/notices/?created_at_after=2026-01-01"
```

3. 数据中心 API
```bash
# 测试分类筛选
curl "http://localhost:8000/api/questions/?category=影视"
# 测试位置筛选
curl "http://localhost:8000/api/questions/?location=广东"
# 测试回答数筛选
curl "http://localhost:8000/api/questions/?answer_count_min=3"
# 测试获取筛选选项
curl "http://localhost:8000/api/questions/filter-options/"
```

### 前端测试

1. 打开用户管理页面，测试角色和状态下拉筛选
2. 打开公告管理页面，测试状态和时间范围筛选
3. 打开数据中心页面，测试分类、位置、回答数、发布时间筛选
4. 验证筛选后列表正确更新
5. 验证分页在筛选状态下正常工作

---

## 实现顺序

1. Task 1: 后端用户管理 API
2. Task 2: 后端公告管理 API
3. Task 3: 后端数据中心 API
4. Task 4: 前端用户管理筛选
5. Task 5: 前端公告管理筛选
6. Task 6: 前端数据中心筛选

每个 Task 完成后建议提交一次：
```bash
git add -A
git commit -m "feat: 添加用户管理 API 筛选功能"
```
