# 个人中心功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为用户端添加个人中心功能，支持查看和修改个人信息（用户名、邮箱、手机号）以及修改密码。

**Architecture:** 采用现有用户认证体系，在后端 ProfileView 添加 PATCH 方法更新个人信息，前端创建独立个人中心页面，复用现有中国传统文化 UI 风格。

**Tech Stack:** Django + DRF (后端), Vue 3 + Element Plus (前端), Pinia (状态管理)

---

### Task 1: 后端 - 添加更新个人信息 Serializer

**Files:**
- Create: `backend/apps/users/serializers.py` (追加)

**Step 1: 添加 UpdateProfileSerializer**

打开 `backend/apps/users/serializers.py`，在文件末尾追加：

```python
class UpdateProfileSerializer(serializers.Serializer):
    """更新个人资料序列化器"""
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=20, required=False)

    def validate_email(self, value):
        """检查邮箱是否已被其他用户使用"""
        user = self.context['request'].user
        if User.objects.exclude(id=user.id).filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被使用")
        return value
```

**Step 2: 提交**

```bash
git add backend/apps/users/serializers.py
git commit -m "feat(profile): 添加更新个人资料序列化器"
```

---

### Task 2: 后端 - 添加 ProfileView PATCH 方法

**Files:**
- Modify: `backend/apps/users/views.py:95-104`

**Step 1: 添加 patch 方法**

在 `ProfileView` 类中添加 `patch` 方法：

```python
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 现有代码保持不变...
        profile = request.user.profile
        data = {
            "id": request.user.id,
            "username": request.user.username,
            "role": get_user_role(request.user),
            "email": profile.email,
            "phone": profile.phone or "",
            "is_active": profile.is_active,
            "last_login_time": profile.last_login_time,
            "date_joined": request.user.date_joined,
        }
        return success_response(data=data, message="获取成功")

    def patch(self, request):
        """更新当前用户个人信息"""
        serializer = UpdateProfileSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return error_response(
                message=_first_error(serializer.errors),
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        profile = request.user.profile
        validated_data = serializer.validated_data

        if 'email' in validated_data:
            profile.email = validated_data['email']
        if 'phone' in validated_data:
            profile.phone = validated_data['phone']
        profile.save()

        return success_response(
            data={
                "id": request.user.id,
                "username": request.user.username,
                "role": get_user_role(request.user),
                "email": profile.email,
                "phone": profile.phone or "",
            },
            message="更新成功",
        )
```

**Step 2: 添加 Import**

在文件顶部的 import 区域添加：

```python
from .serializers import (
    # ... 现有
    UpdateProfileSerializer,  # 新增
)
```

**Step 3: 提交**

```bash
git add backend/apps/users/views.py
git commit -m "feat(profile): 添加更新个人资料 API"
```

---

### Task 3: 后端 - 添加修改密码 API

**Files:**
- Modify: `backend/apps/users/views.py` (继续)
- Modify: `backend/apps/users/serializers.py`

**Step 1: 添加 ChangePasswordSerializer**

在 `serializers.py` 中添加：

```python
class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate_old_password(self, value):
        """验证旧密码"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码错误")
        return value
```

**Step 2: 在 ProfileView 添加 change_password action**

在 `ProfileView` 类中添加：

```python
@action(methods=["post"], detail=False, url_path="change-password")
def change_password(self, request):
    """修改密码"""
    serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
    if not serializer.is_valid():
        return error_response(
            message=_first_error(serializer.errors),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    request.user.set_password(serializer.validated_data['new_password'])
    request.user.save()

    return success_response(message="密码修改成功，请重新登录")
```

**Step 3: 提交**

```bash
git add backend/apps/users/views.py backend/apps/users/serializers.py
git commit -m "feat(profile): 添加修改密码 API"
```

---

### Task 4: 前端 - 添加个人资料类型定义

**Files:**
- Modify: `frontend/src/types/index.ts`

**Step 1: 添加类型定义**

在 `types/index.ts` 文件末尾添加：

```typescript
// 个人中心相关类型
export interface UserProfile {
  id: number
  username: string
  role: UserRole
  email: string
  phone: string
  is_active: boolean
  last_login_time: string | null
  date_joined: string
}

export interface UpdateProfileRequest {
  email?: string
  phone?: string
}

export interface ChangePasswordRequest {
  old_password: string
  new_password: string
}
```

**Step 2: 提交**

```bash
git add frontend/src/types/index.ts
git commit -m "feat(profile): 添加个人资料类型定义"
```

---

### Task 5: 前端 - 添加 Profile API

**Files:**
- Modify: `frontend/src/api/auth.ts`

**Step 1: 添加 API 函数**

在 `auth.ts` 中添加：

```typescript
import type { UserProfile, UpdateProfileRequest, ChangePasswordRequest } from '@/types'

// 获取当前用户信息
export const getCurrentUser = () => request.get<UserProfile>('/auth/me/')

// 更新个人资料
export const updateProfile = (data: UpdateProfileRequest) =>
  request.patch<UserProfile>('/auth/me/', data)

// 修改密码
export const changePassword = (data: ChangePasswordRequest) =>
  request.post<{ message: string }>('/auth/me/change-password/', data)
```

**Step 2: 提交**

```bash
git add frontend/src/api/auth.ts
git commit -m "feat(profile): 添加个人资料 API"
```

---

### Task 6: 前端 - 创建个人中心页面

**Files:**
- Create: `frontend/src/views/Profile.vue`

**Step 1: 创建页面组件**

```vue
<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span class="title">个人中心</span>
        </div>
      </template>

      <el-tabs v-model="activeTab" class="profile-tabs">
        <!-- 基本信息 Tab -->
        <el-tab-pane label="基本信息" name="profile">
          <el-form
            ref="profileFormRef"
            :model="profileForm"
            :rules="profileRules"
            label-width="100px"
            class="profile-form"
          >
            <el-form-item label="用户名">
              <el-input v-model="profileForm.username" disabled />
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="profileForm.phone" placeholder="请输入手机号" />
            </el-form-item>
            <el-form-item label="角色">
              <el-tag :type="profileForm.role === 'admin' ? 'danger' : 'info'">
                {{ profileForm.role === 'admin' ? '管理员' : '普通用户' }}
              </el-tag>
            </el-form-item>
            <el-form-item label="注册时间">
              <span>{{ formatDate(profileForm.date_joined) }}</span>
            </el-form-item>
            <el-form-item label="最后登录">
              <span>{{ profileForm.last_login_time ? formatDate(profileForm.last_login_time) : '暂无' }}</span>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="saveProfile">
                保存修改
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 修改密码 Tab -->
        <el-tab-pane label="修改密码" name="password">
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="100px"
            class="profile-form"
          >
            <el-form-item label="原密码" prop="old_password">
              <el-input
                v-model="passwordForm.old_password"
                type="password"
                placeholder="请输入原密码"
                show-password
              />
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
              <el-input
                v-model="passwordForm.new_password"
                type="password"
                placeholder="请输入新密码"
                show-password
              />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input
                v-model="passwordForm.confirm_password"
                type="password"
                placeholder="请再次输入新密码"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="changingPwd" @click="changePassword">
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { getCurrentUser, updateProfile, changePassword } from '@/api/auth'
import type { UserProfile } from '@/types'

const activeTab = ref('profile')
const saving = ref(false)
const changingPwd = ref(false)

const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()

const profileForm = reactive<UserProfile>({
  id: 0,
  username: '',
  role: 'user',
  email: '',
  phone: '',
  is_active: true,
  last_login_time: null,
  date_joined: '',
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: '',
})

const profileRules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' },
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号', trigger: 'blur' },
  ],
}

const validateConfirmPwd = (rule: any, value: string, callback: any) => {
  if (value !== passwordForm.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules: FormRules = {
  old_password: [
    { required: true, message: '请输入原密码', trigger: 'blur' },
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少8位', trigger: 'blur' },
  ],
  confirm_password: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirmPwd, trigger: 'blur' },
  ],
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

const loadProfile = async () => {
  try {
    const res = await getCurrentUser()
    Object.assign(profileForm, res.data)
  } catch (error) {
    ElMessage.error('加载个人信息失败')
  }
}

const saveProfile = async () => {
  if (!profileFormRef.value) return

  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        await updateProfile({
          email: profileForm.email,
          phone: profileForm.phone,
        })
        ElMessage.success('保存成功')
      } catch (error: any) {
        ElMessage.error(error.response?.data?.message || '保存失败')
      } finally {
        saving.value = false
      }
    }
  })
}

const changePassword = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      changingPwd.value = true
      try {
        await changePassword({
          old_password: passwordForm.old_password,
          new_password: passwordForm.new_password,
        })
        ElMessage.success('密码修改成功，请重新登录')
        passwordForm.old_password = ''
        passwordForm.new_password = ''
        passwordForm.confirm_password = ''
        // 可选：自动登出
        // logout()
        // router.push('/login')
      } catch (error: any) {
        ElMessage.error(error.response?.data?.message || '修改密码失败')
      } finally {
        changingPwd.value = false
      }
    }
  })
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-card {
  max-width: 600px;
  margin: 0 auto;
}

.card-header .title {
  font-size: 18px;
  font-weight: 600;
  color: #8b4513;
}

.profile-tabs {
  margin-top: 10px;
}

.profile-form {
  max-width: 400px;
  margin: 20px auto;
}
</style>
```

**Step 2: 提交**

```bash
git add frontend/src/views/Profile.vue
git commit -m "feat(profile): 创建个人中心页面"
```

---

### Task 7: 前端 - 添加路由

**Files:**
- Modify: `frontend/src/router/index.ts`

**Step 1: 添加路由**

在路由配置中添加：

```typescript
import Profile from '@/views/Profile.vue'

// 在 routes 数组中添加:
{
  path: '/profile',
  component: Profile,
  meta: { requiresAuth: true },
},
```

**Step 2: 提交**

```bash
git add frontend/src/router/index.ts
git commit -m "feat(profile): 添加个人中心路由"
```

---

### Task 8: 前端 - 添加侧边栏入口

**Files:**
- Modify: `frontend/src/layouts/MainLayout.vue`

**Step 1: 添加菜单项**

在侧边栏菜单中找到 `el-menu` 的 `router` 模式，在合适位置添加：

```vue
<el-menu-item index="/profile">
  <el-icon><User /></el-icon>
  <span>个人中心</span>
</el-menu-item>
```

需要导入 User 图标：

```typescript
import { User } from '@element-plus/icons-vue'
```

**Step 2: 提交**

```bash
git add frontend/src/layouts/MainLayout.vue
git commit -m "feat(profile): 添加侧边栏入口"
```

---

### Task 9: 验证功能

**Step 1: 启动后端和前端**

```bash
# 后端
cd backend
python manage.py runserver

# 前端
cd frontend
npm run dev
```

**Step 2: 测试流程**

1. 登录系统
2. 点击侧边栏"个人中心"菜单
3. 验证基本信息显示正确
4. 修改邮箱/手机号，点击保存
5. 切换到"修改密码"标签
6. 尝试修改密码

**Step 3: 提交**

```bash
git add .
git commit -m "test: 验证个人中心功能"
```

---

## 执行选项

**Plan complete and saved to `docs/plans/2026-02-26-profile-feature.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**
