# 用户绑定房间管理员审核功能实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 添加用户绑定房间的管理员审核功能，用户绑定房间需管理员审批后才能生效

**Architecture:** 用户发起绑定申请 → 进入待审核状态 → 管理员审批 → 审批通过后正式生效。需要修改UserProfile模型添加待审核字段，修改ProfileViewSet支持审核流程，并在Admin端添加审核管理页面。

**Tech Stack:** Django + DRF + Vue 3 + Element Plus

---

### Task 1: 修改 UserProfile 模型，添加待审核字段

**Files:**
- Modify: `backend/apps/accounts/models.py:25-30`
- Modify: `backend/apps/accounts/admin.py:7-20`

**Step 1: 修改 UserProfile 模型**

```python
# backend/apps/accounts/models.py 添加两个新字段
bind_rooms = models.JSONField(
    default=list,
    blank=True,
    verbose_name="绑定房间",
)
pending_bind_rooms = models.JSONField(
    default=list,
    blank=True,
    verbose_name="待审核绑定申请",
    help_text="用户发起但待管理员审批的房间ID列表",
)
```

**Step 2: 生成迁移文件**

Run: `cd backend && python manage.py makemigrations accounts`
Expected: 输出包含 `pending_bind_rooms` 字段的迁移文件

**Step 3: 执行迁移**

Run: `cd backend && python manage.py migrate`
Expected: 表结构更新成功

**Step 4: 更新 Admin 显示**

```python
# backend/apps/accounts/admin.py
list_display = (
    "id", "user", "phone", "role",
    "bind_rooms", "pending_bind_rooms",  # 添加此行
    "alarm_subscriptions", "created_at", "updated_at",
)
```

**Step 5: Commit**

```bash
git add backend/apps/accounts/models.py backend/apps/accounts/admin.py backend/apps/accounts/migrations/
git commit -m "feat: add pending_bind_rooms field to UserProfile"
```

---

### Task 2: 修改后端 ProfileViewSet，支持审核流程

**Files:**
- Modify: `backend/apps/system/views.py:381-432`
- Modify: `backend/apps/system/serializers.py`

**Step 1: 修改 ProfileBindRoomsSerializer 添加状态说明**

```python
# backend/apps/system/serializers.py
class ProfileBindRoomsSerializer(serializers.Serializer):
    """用户绑定房间请求"""
    room_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        allow_empty=False,
    )
```

**Step 2: 修改 bind_rooms 方法，POST 时进入待审核状态**

```python
# backend/apps/system/views.py - bind_rooms 方法修改
@action(detail=False, methods=["get", "post", "delete"], url_path="bind-rooms")
def bind_rooms(self, request):
    """GET 获取已绑定; POST 发起绑定申请; DELETE 解绑"""
    profile = self._profile_object()

    if request.method.lower() == "get":
        # 获取已绑定房间
        current_room_ids = sorted(set(int(item) for item in profile.bind_rooms if str(item).isdigit()))
        # ... 现有逻辑 ...

    # POST: 发起绑定申请（进入待审核）
    if request.method.lower() == "post":
        current_pending = sorted(set(int(item) for item in profile.pending_bind_rooms if str(item).isdigit()))
        current_bound = sorted(set(int(item) for item in profile.bind_rooms if str(item).isdigit()))

        # 过滤掉已绑定和已申请的
        new_rooms = [r for r in room_ids if r not in current_bound and r not in current_pending]
        updated_pending = sorted(set(current_pending + new_rooms))

        profile.pending_bind_rooms = updated_pending
        profile.save(update_fields=["pending_bind_rooms", "updated_at"])

        _write_operation_log(request, "bind_room_request", f"rooms:{new_rooms}")
        return Response({
            "message": "绑定申请已提交，等待管理员审批",
            "pending_bind_rooms": updated_pending
        })

    # DELETE: 解绑（直接解绑，不需要审核）
    # ... 现有逻辑 ...
```

**Step 3: 添加获取待审核申请列表的接口**

```python
# backend/apps/system/views.py - ProfileViewSet 中添加
@action(detail=False, methods=["get"], url_path="pending-bind-requests")
def pending_bind_requests(self, request):
    """获取当前用户的待审核绑定申请"""
    profile = self._profile_object()
    pending_ids = sorted(set(int(item) for item in profile.pending_bind_rooms if str(item).isdigit()))

    if not pending_ids:
        return Response([])

    room_map = {
        room.id: room
        for room in Room.objects.select_related("floor", "floor__building").filter(id__in=pending_ids)
    }
    rooms = []
    for room_id in pending_ids:
        room = room_map.get(room_id)
        if room:
            rooms.append({
                "id": room.id,
                "room_number": room.room_number,
                "building_name": room.floor.building.name,
                "floor_name": room.floor.name,
            })
    return Response(rooms)
```

**Step 4: Commit**

```bash
git add backend/apps/system/views.py backend/apps/system/serializers.py
git commit -m "feat: modify bind_rooms to require admin approval"
```

---

### Task 3: 添加管理员审核 API

**Files:**
- Modify: `backend/apps/system/views.py`
- Modify: `backend/apps/system/urls.py`

**Step 1: 添加管理员审核接口**

```python
# backend/apps/system/views.py - 管理员审核绑定申请
@action(detail=False, methods=["post"], url_path="approve-bind-request")
@permission_classes([IsAdmin])
def approve_bind_request(self, request):
    """管理员批准绑定申请"""
    user_id = request.data.get("user_id")
    room_ids = request.data.get("room_ids", [])
    approve = request.data.get("approve", True)

    try:
        profile = UserProfile.objects.get(user_id=user_id)
    except UserProfile.DoesNotExist:
        return Response({"error": "用户不存在"}, status=400)

    pending = set(int(item) for item in profile.pending_bind_rooms if str(item).isdigit())
    current_bound = set(int(item) for item in profile.bind_rooms if str(item).isdigit())

    if approve:
        # 批准：移到已绑定
        new_bound = current_bound.union(room_ids)
        new_pending = pending - set(room_ids)
        profile.bind_rooms = list(new_bound)
        profile.pending_bind_rooms = list(new_pending)
        _write_operation_log(request, "approve_bind_request", f"user:{user_id}, rooms:{room_ids}")
    else:
        # 拒绝：直接从待审核移除
        new_pending = pending - set(room_ids)
        profile.pending_bind_rooms = list(new_pending)
        _write_operation_log(request, "reject_bind_request", f"user:{user_id}, rooms:{room_ids}")

    profile.save()
    return Response({"bind_rooms": profile.bind_rooms, "pending_bind_rooms": profile.pending_bind_rooms})
```

**Step 2: 添加获取所有待审核申请的接口（管理员用）**

```python
# backend/apps/system/views.py
@action(detail=False, methods=["get"], url_path="all-pending-bind-requests")
@permission_classes([IsAdmin])
def all_pending_bind_requests(self, request):
    """获取所有待审核的绑定申请（管理员）"""
    profiles = UserProfile.objects.exclude(pending_bind_rooms=[]).select_related("user")

    results = []
    for profile in profiles:
        pending_ids = [int(item) for item in profile.pending_bind_rooms if str(item).isdigit()]
        if not pending_ids:
            continue

        room_map = {
            room.id: room
            for room in Room.objects.select_related("floor", "floor__building").filter(id__in=pending_ids)
        }

        rooms = []
        for room_id in pending_ids:
            room = room_map.get(room_id)
            if room:
                rooms.append({
                    "id": room.id,
                    "room_number": room.room_number,
                    "building_name": room.floor.building.name,
                    "floor_name": room.floor.name,
                })

        results.append({
            "user_id": profile.user_id,
            "username": profile.user.username,
            "real_name": profile.user.first_name or profile.user.username,
            "rooms": rooms,
            "pending_count": len(rooms),
        })

    return Response(results)
```

**Step 3: 添加 URL 路由**

```python
# backend/apps/system/urls.py
path("profile/approve-bind-request/", ProfileViewSet.as_view({"post": "approve_bind_request"}), name="profile-approve-bind-request"),
path("profile/all-pending-bind-requests/", ProfileViewSet.as_view({"get": "all_pending_bind_requests"}), name="profile-all-pending-bind-requests"),
```

**Step 4: Commit**

```bash
git add backend/apps/system/views.py backend/apps/system/urls.py
git commit -m "feat: add admin approval API for room binding"
```

---

### Task 4: 前端 - 用户端显示待审核状态

**Files:**
- Modify: `frontend/src/api/profile.js`
- Modify: `frontend/src/views/user/Profile.vue`

**Step 1: 添加前端 API**

```javascript
// frontend/src/api/profile.js 添加

/**
 * Get my pending bind requests
 */
export function getMyPendingBindRequests() {
  return request({
    url: '/profile/pending-bind-requests/',
    method: 'get',
  })
}
```

**Step 2: 修改 Profile.vue 显示待审核列表**

在 `boundRooms` 旁边添加 `pendingRooms` 展示：

```vue
<!-- 待审核申请 -->
<div v-if="pendingRooms.length > 0" class="pending-rooms">
  <h4>待审核申请</h4>
  <el-alert type="warning" :closable="false">
    您有 {{ pendingRooms.length }} 个房间绑定申请正在审核中
  </el-alert>
  <div v-for="room in pendingRooms" :key="room.id" class="room-card pending">
    <div class="room-info">
      <h4>{{ room.room_number }}</h4>
      <p>{{ room.building_name }} · {{ room.floor_name }}</p>
    </div>
    <el-tag type="warning">待审核</el-tag>
  </div>
</div>
```

添加数据加载：

```javascript
const pendingRooms = ref([])

// 加载待审核
async function loadPendingRooms() {
  const response = await getMyPendingBindRequests()
  pendingRooms.value = response.data
}

// 页面加载时调用
loadPendingRooms()
```

**Step 3: Commit**

```bash
git add frontend/src/api/profile.js frontend/src/views/user/Profile.vue
git commit -m "feat: show pending bind requests in user profile"
```

---

### Task 5: 前端 - 管理端添加审核页面

**Files:**
- Create: `frontend/src/views/admin/RoomBinding.vue`
- Modify: `frontend/src/api/system.js`
- Modify: `frontend/src/router/index.js`

**Step 1: 添加管理端 API**

```javascript
// frontend/src/api/system.js 添加

/**
 * Get all pending bind requests
 */
export function getAllPendingBindRequests() {
  return request({
    url: '/profile/all-pending-bind-requests/',
    method: 'get',
  })
}

/**
 * Approve or reject bind request
 * @param {Object} data - { user_id, room_ids, approve }
 */
export function approveBindRequest(data) {
  return request({
    url: '/profile/approve-bind-request/',
    method: 'post',
    data,
  })
}
```

**Step 2: 创建审核页面 RoomBinding.vue**

```vue
<template>
  <div class="room-binding-page">
    <div class="page-header">
      <h2>房间绑定审核</h2>
      <p class="page-subtitle">审核用户提交的房间绑定申请</p>
    </div>

    <el-card v-if="pendingRequests.length > 0">
      <el-table :data="pendingRequests" v-loading="loading">
        <el-table-column label="用户" width="180">
          <template #default="{ row }">
            <div class="user-cell">
              <span class="user-name">{{ row.real_name || row.username }}</span>
              <span class="user-username">@{{ row.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="申请房间" min-width="300">
          <template #default="{ row }">
            <el-tag v-for="room in row.rooms" :key="room.id" class="room-tag">
              {{ room.building_name }} - {{ room.floor_name }} - {{ room.room_number }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleApprove(row)">
              批准
            </el-button>
            <el-button type="danger" size="small" @click="handleReject(row)">
              拒绝
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-empty v-else description="暂无待审核的绑定申请" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAllPendingBindRequests, approveBindRequest } from '@/api/system'

const loading = ref(false)
const pendingRequests = ref([])

async function loadPendingRequests() {
  loading.value = true
  try {
    const response = await getAllPendingBindRequests()
    pendingRequests.value = response.data || []
  } catch (error) {
    console.error(error)
    ElMessage.error('加载待审核申请失败')
  } finally {
    loading.value = false
  }
}

async function handleApprove(row) {
  try {
    await ElMessageBox.confirm(`批准用户 "${row.real_name || row.username}" 的绑定申请？`, '确认批准')
    await approveBindRequest({
      user_id: row.user_id,
      room_ids: row.rooms.map(r => r.id),
      approve: true
    })
    ElMessage.success('已批准绑定申请')
    loadPendingRequests()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

async function handleReject(row) {
  try {
    await ElMessageBox.confirm(`拒绝用户 "${row.real_name || row.username}" 的绑定申请？`, '确认拒绝')
    await approveBindRequest({
      user_id: row.user_id,
      room_ids: row.rooms.map(r => r.id),
      approve: false
    })
    ElMessage.success('已拒绝绑定申请')
    loadPendingRequests()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  }
}

onMounted(() => {
  loadPendingRequests()
})
</script>

<style scoped>
.room-binding-page {
  padding: 20px;
}
.page-header {
  margin-bottom: 20px;
}
.page-header h2 {
  margin: 0 0 8px;
}
.page-subtitle {
  color: #909399;
  margin: 0;
}
.user-cell {
  display: flex;
  flex-direction: column;
}
.user-name {
  font-weight: 500;
}
.user-username {
  font-size: 12px;
  color: #909399;
}
.room-tag {
  margin: 2px 4px;
}
</style>
```

**Step 3: 添加路由**

```javascript
// frontend/src/router/index.js
{
  path: '/admin/room-binding',
  component: () => import('@/views/admin/RoomBinding.vue'),
  meta: { roles: ['ADMIN'], title: '房间绑定审核' }
}
```

**Step 4: Commit**

```bash
git add frontend/src/api/system.js frontend/src/views/admin/RoomBinding.vue frontend/src/router/index.js
git commit -m "feat: add room binding approval page in admin"
```

---

### Task 6: 测试验证

**Step 1: 启动后端服务**

Run: `cd backend && python manage.py runserver`

**Step 2: 以普通用户身份发起绑定申请**

- 登录用户端
- 进入 Profile → 账号绑定
- 添加一个房间
- 确认申请提交后，显示"等待管理员审批"

**Step 3: 验证待审核状态**

Run: `curl -H "Authorization: Bearer <admin_token>" http://localhost:8000/api/profile/all-pending-bind-requests/`
Expected: 返回待审核申请列表

**Step 4: 管理员审批**

- 登录管理端
- 进入 房间绑定审核 页面
- 点击"批准"按钮
- 验证用户端房间已成功绑定

**Step 5: 提交最终代码**

```bash
git add .
git commit -m "feat: complete room binding approval workflow"
```

---

## 执行方式

Plan complete and saved to `docs/plans/2026-02-27-room-binding-approval.md`. Two execution options:

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
