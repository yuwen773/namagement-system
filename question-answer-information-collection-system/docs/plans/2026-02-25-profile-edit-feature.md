# 个人中心编辑资料功能实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**目标:** 为用户端个人中心添加编辑资料功能，允许用户修改用户名和邮箱

**架构设计:** 在现有的 Profile.vue 页面中添加"编辑资料"按钮，点击后弹出 Element Plus Dialog 模态框，内嵌表单进行编辑。表单提交成功后调用 updateUserInfo API，然后刷新 Pinia store 中的用户信息并更新界面显示。

**技术栈:** Vue 3 Composition API, Element Plus Dialog/Form, Pinia store, Axios

---

## 任务概览

| 任务 | 描述 | 预计时间 |
|------|------|----------|
| Task 1 | 添加编辑资料模态框结构到 Profile.vue | 10分钟 |
| Task 2 | 实现表单验证规则 | 10分钟 |
| Task 3 | 实现表单提交逻辑 | 15分钟 |
| Task 4 | 修改成功后更新用户信息 | 10分钟 |
| Task 5 | 测试功能完整性 | 10分钟 |

---

## Task 1: 添加编辑资料模态框结构

**文件:**
- Modify: `frontend/src/views/Profile.vue`

**Step 1: 在 template 中添加编辑按钮**

找到账户信息卡片的 card-header 部分，在标题后添加编辑按钮。

在 `profile-card user-card` 的 `card-header` div 中，在 `h2.card-title` 后添加：

```vue
<button class="edit-btn" @click="openEditDialog">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
  </svg>
  编辑资料
</button>
```

**Step 2: 添加编辑资料模态框**

在 template 的最后，在 `</main>` 后添加：

```vue
<!-- Edit Profile Dialog -->
<el-dialog
  v-model="editDialogVisible"
  title="编辑资料"
  width="500px"
  :close-on-click-modal="false"
  class="edit-dialog"
>
  <el-form
    ref="editFormRef"
    :model="editForm"
    :rules="editRules"
    label-position="top"
    class="edit-form"
  >
    <el-form-item label="用户名" prop="username">
      <el-input
        v-model="editForm.username"
        placeholder="请输入用户名"
        maxlength="50"
        show-word-limit
      />
    </el-form-item>

    <el-form-item label="邮箱" prop="email">
      <el-input
        v-model="editForm.email"
        placeholder="请输入邮箱（可选）"
        type="email"
      />
    </el-form-item>
  </el-form>

  <template #footer>
    <div class="dialog-footer">
      <button class="cancel-btn" @click="editDialogVisible = false">取消</button>
      <button class="confirm-btn" @click="handleEditSubmit" :disabled="editLoading">
        <span v-if="!editLoading">保存修改</span>
        <span v-else class="loading-text">
          <span class="spinner"></span>
          保存中...
        </span>
      </button>
    </div>
  </template>
</el-dialog>
```

**Step 3: 在 script setup 中添加响应式状态**

在 `<script setup>` 中现有的 `submitLoading` 后添加：

```javascript
// Edit profile dialog
const editDialogVisible = ref(false)
const editFormRef = ref(null)
const editLoading = ref(false)

const editForm = reactive({
  username: '',
  email: ''
})
```

**Step 4: 添加打开模态框方法**

在 methods 区域（`togglePassword` 方法后）添加：

```javascript
const openEditDialog = () => {
  // Pre-fill form with current user info
  editForm.username = authStore.userInfo?.username || ''
  editForm.email = authStore.userInfo?.email || ''
  editDialogVisible = true
}
```

**Step 5: 添加模态框相关样式**

在 style 区域末尾、`</style>` 前添加：

```css
/* Edit Button */
.edit-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(13, 148, 136, 0.1);
  border: 1px solid rgba(13, 148, 136, 0.2);
  border-radius: 8px;
  color: #0d9488;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-left: auto;
}

.edit-btn:hover {
  background: rgba(13, 148, 136, 0.15);
  border-color: rgba(13, 148, 136, 0.3);
  transform: translateY(-1px);
}

.edit-btn svg {
  width: 16px;
  height: 16px;
}

/* Dialog Styles */
.edit-dialog :deep(.el-dialog__header) {
  padding: 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.edit-dialog :deep(.el-dialog__title) {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
}

.edit-dialog :deep(.el-dialog__body) {
  padding: 1.5rem;
}

.edit-dialog :deep(.el-dialog__footer) {
  padding: 1rem 1.5rem;
  border-top: 1px solid #f1f5f9;
}

/* Edit Form */
.edit-form :deep(.el-form-item__label) {
  color: #475569;
  font-size: 0.875rem;
  font-weight: 500;
  padding-bottom: 0.5rem;
}

.edit-form :deep(.el-input__wrapper) {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  box-shadow: none;
  padding: 0.5rem 0.75rem;
  height: 44px;
}

.edit-form :deep(.el-input__wrapper:hover) {
  border-color: rgba(13, 148, 136, 0.5);
}

.edit-form :deep(.el-input__wrapper.is-focus) {
  border-color: #0d9488;
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.edit-form :deep(.el-input__inner) {
  color: #1e293b;
  font-size: 0.9rem;
}

.edit-form :deep(.el-input__inner::placeholder) {
  color: #94a3b8;
}

/* Dialog Footer */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.cancel-btn {
  padding: 0.625rem 1.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  color: #64748b;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-btn:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

.confirm-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1.5rem;
  background: linear-gradient(135deg, #0d9488 0%, #14b8a6 100%);
  border: none;
  border-radius: 10px;
  color: #ffffff;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
}

.confirm-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.loading-text .spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
```

**Step 6: 运行开发服务器验证 UI**

```bash
cd frontend
npm run dev
```

访问 http://localhost:5173/profile，点击"编辑资料"按钮，验证模态框正常显示。

**Step 7: 提交变更**

```bash
cd D:/work/code/personal/namagement-system/question-answer-information-collection-system
git add frontend/src/views/Profile.vue
git commit -m "feat: 添加编辑资料模态框UI结构"
```

---

## Task 2: 实现表单验证规则

**文件:**
- Modify: `frontend/src/views/Profile.vue`

**Step 1: 导入 API 方法**

确保 script setup 顶部已有导入（应该已存在）：

```javascript
import { updateUserInfo } from '@/api/users'
```

**Step 2: 添加验证规则**

在 `passwordRules` 定义后、`// Methods` 注释前添加：

```javascript
// Edit form validation rules
const validateUsername = (rule, value, callback) => {
  if (!value || value.trim() === '') {
    callback(new Error('用户名不能为空'))
  } else if (value.length < 2) {
    callback(new Error('用户名至少2个字符'))
  } else if (value.length > 50) {
    callback(new Error('用户名不能超过50个字符'))
  } else if (!/^[a-zA-Z0-9_\u4e00-\u9fa5]+$/.test(value)) {
    callback(new Error('用户名只能包含字母、数字、下划线和中文'))
  } else {
    callback()
  }
}

const validateEmail = (rule, value, callback) => {
  if (!value || value.trim() === '') {
    // Email is optional
    callback()
  } else {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(value)) {
      callback(new Error('请输入有效的邮箱地址'))
    } else {
      callback()
    }
  }
}

const editRules = {
  username: [
    { required: true, validator: validateUsername, trigger: 'blur' }
  ],
  email: [
    { validator: validateEmail, trigger: 'blur' }
  ]
}
```

**Step 3: 测试验证规则**

在浏览器中打开编辑模态框，尝试：
1. 清空用户名 → 应显示"用户名不能为空"
2. 输入单个字符 → 应显示"用户名至少2个字符"
3. 输入无效邮箱如 "test" → 应显示"请输入有效的邮箱地址"

**Step 4: 提交变更**

```bash
git add frontend/src/views/Profile.vue
git commit -m "feat: 添加编辑资料表单验证规则"
```

---

## Task 3: 实现表单提交逻辑

**文件:**
- Modify: `frontend/src/views/Profile.vue`

**Step 1: 实现表单提交处理方法**

在 `handlePasswordSubmit` 方法后添加：

```javascript
const handleEditSubmit = async () => {
  if (!editFormRef.value) return

  try {
    await editFormRef.value.validate()
  } catch {
    return
  }

  editLoading.value = true

  try {
    const res = await updateUserInfo({
      username: editForm.username.trim(),
      email: editForm.email.trim() || null
    })

    if (res.code === 0) {
      ElMessage.success('资料修改成功')
      editDialogVisible = false
      // Refresh user info will be handled in Task 4
      await authStore.fetchUserInfo()
    } else {
      ElMessage.error(res.message || '修改失败，请稍后重试')
    }
  } catch (e) {
    const errorMsg = e.response?.data?.message || e.response?.data?.username?.[0] || e.response?.data?.email?.[0] || '修改失败，请稍后重试'
    ElMessage.error(errorMsg)
  } finally {
    editLoading.value = false
  }
}
```

**Step 2: 检查 auth store 是否有 fetchUserInfo 方法**

读取 `frontend/src/stores/auth.js`：

```bash
cat frontend/src/stores/auth.js
```

如果不存在 `fetchUserInfo` 方法，需要在 Task 4 中添加。

**Step 3: 测试表单提交**

在浏览器中：
1. 打开编辑模态框
2. 修改用户名或邮箱
3. 点击"保存修改"
4. 检查 Network 面板确认请求发送到 `/api/auth/me/`

**Step 4: 提交变更**

```bash
git add frontend/src/views/Profile.vue
git commit -m "feat: 实现编辑资料表单提交逻辑"
```

---

## Task 4: 确保用户信息更新后刷新界面

**文件:**
- Check: `frontend/src/stores/auth.js`
- Modify: `frontend/src/stores/auth.js` (如果需要)

**Step 1: 检查 auth store 结构**

```bash
cat frontend/src/stores/auth.js
```

**Step 2: 如果缺少 fetchUserInfo 方法，则添加**

在 auth store 中添加（如果不存在）：

```javascript
// 在 actions 中添加
async fetchUserInfo() {
  try {
    const res = await getUserInfo()
    if (res.code === 0) {
      this.userInfo = res.data
      // Update localStorage
      localStorage.setItem('userInfo', JSON.stringify(res.data))
    }
  } catch (error) {
    console.error('Failed to fetch user info:', error)
  }
}
```

确保已导入 `getUserInfo`：

```javascript
import { getUserInfo } from '@/api/users'
```

**Step 3: 测试信息刷新流程**

1. 修改用户名
2. 保存成功
3. 验证页面显示的用户名已更新
4. 验证侧边栏用户名（如果有）也已更新

**Step 4: 提交变更**

```bash
git add frontend/src/stores/auth.js
git commit -m "feat: 添加用户信息刷新方法"
```

---

## Task 5: 功能完整测试

**文件:**
- Test: `frontend/src/views/Profile.vue`

**Step 1: 测试正常修改流程**

1. 登录系统
2. 进入个人中心
3. 点击"编辑资料"按钮
4. 修改用户名为新值（如 "testuser01"）
5. 填写邮箱（如 "test@example.com"）
6. 点击"保存修改"
7. 验证：页面显示新用户名和邮箱
8. 退出并重新登录，验证信息持久化

**Step 2: 测试验证规则**

1. 打开编辑模态框
2. 清空用户名 → 应显示错误提示
3. 输入无效邮箱 "abc" → 应显示错误提示
4. 确认无法提交表单

**Step 3: 测试取消操作**

1. 修改表单内容
2. 点击"取消"按钮
3. 验证模态框关闭，数据未保存

**Step 4: 测试网络错误处理**

1. 修改后端代码临时返回错误（或断开网络）
2. 尝试提交
3. 验证显示错误提示信息

**Step 5: 测试用户名冲突**

1. 尝试修改为已存在的用户名
2. 验证显示友好的错误提示

**Step 6: 跨浏览器测试**

在 Chrome 和 Firefox 中重复上述测试。

**Step 7: 提交最终版本**

```bash
git add frontend/src/views/Profile.vue
git commit -m "test: 完成编辑资料功能测试"
```

---

## 相关文档

- **PRD:** `memory-bank/PRD.md` - 第 3.1 节"认证与个人中心模块"
- **架构文档:** `memory-bank/architecture.md`
- **API 标准:** 响应格式 `{ code: 0, data: {...} }`
- **用户模型:** `backend/apps/accounts/models.py` - User 模型

---

## 验收标准

- [ ] 个人中心页面显示"编辑资料"按钮
- [ ] 点击按钮弹出编辑模态框
- [ ] 表单预填充当前用户信息
- [ ] 用户名必填，邮箱选填
- [ ] 表单验证正常工作（非空、格式）
- [ ] 提交成功后界面实时更新用户信息
- [ ] 错误提示友好（网络错误、用户名冲突等）
- [ ] 模态框样式与现有设计风格一致
- [ ] 响应式布局在移动端正常显示

---

## 备注

- 后端 API 已存在，无需修改后端代码
- 使用 Element Plus 的 Dialog 和 Form 组件
- 保持与现有 Profile 页面的视觉风格一致
- 用户名修改后无需强制重新登录（JWT 包含 user ID，不依赖 username）
