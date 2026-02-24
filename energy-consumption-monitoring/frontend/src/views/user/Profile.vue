<template>
  <div class="profile-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="24" cy="16" r="8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M8 42C8 32 16 28 24 28C32 28 40 32 40 42" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="header-text">
          <h1 class="page-title">个人中心</h1>
          <p class="page-subtitle">管理您的个人信息与偏好设置</p>
        </div>
      </div>
      <div class="header-decoration">
        <div class="deco-circle circle-1"></div>
        <div class="deco-circle circle-2"></div>
        <div class="deco-circle circle-3"></div>
      </div>
    </div>

    <!-- Profile Content -->
    <div class="profile-content">
      <!-- Tab Navigation -->
      <div class="tab-navigation">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="['tab-btn', { active: activeTab === tab.key }]"
          @click="switchTab(tab.key)"
        >
          <span class="tab-icon">
            <component :is="tab.icon" />
          </span>
          <span class="tab-label">{{ tab.label }}</span>
        </button>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Basic Info Tab -->
        <transition name="tab-fade" mode="out-in">
          <div v-if="activeTab === 'basic'" key="basic" class="basic-info-tab">
            <!-- Avatar Section -->
            <div class="avatar-section">
              <div class="avatar-wrapper">
                <div class="avatar-container" :class="{ uploading: avatarUploading }">
                  <img v-if="profile.avatar" :src="profile.avatar" alt="Avatar" class="avatar-image" />
                  <el-icon v-else class="avatar-placeholder"><icon-ep-user /></el-icon>
                  <div v-if="avatarUploading" class="avatar-overlay">
                    <el-icon class="is-loading"><icon-ep-loading /></el-icon>
                  </div>
                </div>
                <button class="avatar-upload-btn" @click="selectAvatar">
                  <el-icon><icon-ep-camera /></el-icon>
                  <span>更换头像</span>
                </button>
                <input
                  ref="avatarInputRef"
                  type="file"
                  accept="image/*"
                  style="display: none"
                  @change="handleAvatarChange"
                />
              </div>
              <div class="avatar-tips">
                <p>支持 JPG、PNG 格式，建议尺寸 200x200 像素，文件大小不超过 2MB</p>
              </div>
            </div>

            <!-- Profile Form -->
            <div class="profile-form">
              <el-form
                ref="profileFormRef"
                :model="profile"
                :rules="profileRules"
                label-width="100px"
                label-position="left"
              >
                <div class="form-section">
                  <h3 class="section-title">
                    <span class="title-icon"><icon-ep-user /></span>
                    基本信息
                  </h3>
                  <div class="form-grid">
                    <el-form-item label="用户名" prop="username">
                      <el-input v-model="profile.username" disabled>
                        <template #prefix>
                          <el-icon><icon-ep-user /></el-icon>
                        </template>
                      </el-input>
                    </el-form-item>
                    <el-form-item label="真实姓名" prop="real_name">
                      <el-input v-model="profile.real_name" placeholder="请输入真实姓名">
                        <template #prefix>
                          <el-icon><icon-ep-postcard /></el-icon>
                        </template>
                      </el-input>
                    </el-form-item>
                    <el-form-item label="手机号码" prop="phone">
                      <el-input v-model="profile.phone" placeholder="请输入手机号码" maxlength="11">
                        <template #prefix>
                          <el-icon><icon-ep-phone /></el-icon>
                        </template>
                      </el-input>
                    </el-form-item>
                    <el-form-item label="电子邮箱" prop="email">
                      <el-input v-model="profile.email" placeholder="请输入电子邮箱">
                        <template #prefix>
                          <el-icon><icon-ep-message /></el-icon>
                        </template>
                      </el-input>
                    </el-form-item>
                  </div>
                </div>

                <div class="form-section">
                  <h3 class="section-title">
                    <span class="title-icon"><icon-ep-office-building /></span>
                    附加信息
                  </h3>
                  <div class="form-grid">
                    <el-form-item label="部门" prop="department">
                      <el-input v-model="profile.department" placeholder="请输入所属部门">
                        <template #prefix>
                          <el-icon><icon-ep-office-building /></el-icon>
                        </template>
                      </el-input>
                    </el-form-item>
                    <el-form-item label="职位" prop="position">
                      <el-input v-model="profile.position" placeholder="请输入职位">
                        <template #prefix>
                          <el-icon><icon-ep-briefcase /></el-icon>
                        </template>
                      </el-input>
                    </el-form-item>
                  </div>
                </div>
              </el-form>

              <!-- Form Actions -->
              <div class="form-actions">
                <button class="action-btn secondary" @click="resetProfileForm">
                  <el-icon><icon-ep-refresh-left /></el-icon>
                  重置
                </button>
                <button class="action-btn primary" :class="{ loading: saving }" @click="saveProfile">
                  <el-icon v-if="!saving"><icon-ep-check /></el-icon>
                  <el-icon v-else class="is-loading"><icon-ep-loading /></el-icon>
                  {{ saving ? '保存中...' : '保存修改' }}
                </button>
              </div>
            </div>
          </div>

          <!-- Account Binding Tab -->
          <div v-else-if="activeTab === 'binding'" key="binding" class="binding-tab">
            <div class="binding-header">
              <h3 class="binding-title">已绑定房间</h3>
              <button class="add-room-btn" @click="showBindDialog = true">
                <el-icon><icon-ep-plus /></el-icon>
                添加房间
              </button>
            </div>

            <!-- Room List -->
            <div class="room-list">
              <div
                v-for="room in boundRooms"
                :key="room.id"
                class="room-card"
              >
                <div class="room-icon">
                  <el-icon><icon-ep-house /></el-icon>
                </div>
                <div class="room-info">
                  <h4 class="room-name">{{ room.room_number || room.name }}</h4>
                  <p class="room-detail">
                    <span>{{ room.building_name || room.building }}</span>
                    <span class="separator">·</span>
                    <span>{{ room.floor_name || room.floor }}</span>
                  </p>
                  <p v-if="room.department" class="room-department">{{ room.department }}</p>
                </div>
                <div class="room-actions">
                  <button class="room-action-btn unbind" @click="confirmUnbind(room)">
                    <el-icon><icon-ep-close /></el-icon>
                    解绑
                  </button>
                </div>
              </div>

              <el-empty v-if="boundRooms.length === 0" description="暂无绑定房间">
                <el-button type="primary" @click="showBindDialog = true">
                  绑定房间
                </el-button>
              </el-empty>
            </div>
          </div>

          <!-- Alarm Subscription Tab -->
          <div v-else-if="activeTab === 'alarm'" key="alarm" class="alarm-tab">
            <div class="alarm-header">
              <h3 class="alarm-title">告警订阅</h3>
              <p class="alarm-subtitle">自定义您想接收的告警通知类型</p>
            </div>

            <div class="subscription-list">
              <div
                v-for="(item, key) in subscriptions"
                :key="key"
                class="subscription-card"
              >
                <div class="sub-icon" :class="`sub-${key}`">
                  <el-icon>
                    <icon-ep-wallet v-if="key === 'lowBalance'" />
                    <icon-ep-warning v-else-if="key === 'abnormalUsage'" />
                    <icon-ep-bell v-else />
                  </el-icon>
                </div>
                <div class="sub-content">
                  <h4 class="sub-title">{{ item.title }}</h4>
                  <p class="sub-description">{{ item.description }}</p>
                </div>
                <div class="sub-toggle">
                  <el-switch
                    v-model="item.enabled"
                    :active-color="'#f97316'"
                    @change="updateSubscription(key, item.enabled)"
                  />
                </div>
              </div>
            </div>

            <!-- Save Button -->
            <div class="alarm-actions">
              <button class="action-btn primary" :class="{ loading: savingSubscriptions }" @click="saveSubscriptions">
                <el-icon v-if="!savingSubscriptions"><icon-ep-check /></el-icon>
                <el-icon v-else class="is-loading"><icon-ep-loading /></el-icon>
                {{ savingSubscriptions ? '保存中...' : '保存设置' }}
              </button>
            </div>
          </div>
        </transition>
      </div>
    </div>

    <!-- Bind Room Dialog -->
    <el-dialog
      v-model="showBindDialog"
      title="绑定房间"
      width="500px"
      class="bind-dialog"
      :close-on-click-modal="false"
    >
      <el-form
        ref="bindFormRef"
        :model="bindForm"
        :rules="bindRules"
        label-width="80px"
      >
        <el-form-item label="建筑" prop="building_id">
          <el-select
            v-model="bindForm.building_id"
            placeholder="请选择建筑"
            style="width: 100%"
            @change="onBuildingChange"
          >
            <el-option
              v-for="building in availableBuildings"
              :key="building.id"
              :label="building.name"
              :value="building.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="楼层" prop="floor_id">
          <el-select
            v-model="bindForm.floor_id"
            placeholder="请选择楼层"
            style="width: 100%"
            :disabled="!bindForm.building_id"
            @change="onFloorChange"
          >
            <el-option
              v-for="floor in availableFloors"
              :key="floor.id"
              :label="floor.name"
              :value="floor.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="房间" prop="room_id">
          <el-select
            v-model="bindForm.room_id"
            placeholder="请选择房间"
            style="width: 100%"
            :disabled="!bindForm.floor_id"
          >
            <el-option
              v-for="room in availableRooms"
              :key="room.id"
              :label="room.room_number"
              :value="room.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showBindDialog = false">取消</el-button>
        <el-button type="primary" @click="bindRoom">确认绑定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import {
  getMyProfile,
  updateMyProfile,
  getMyBindRooms,
  bindRoom as bindRoomApi,
  unbindRoom as unbindRoomApi,
  getMyAlarmSubscriptions,
  updateAlarmSubscriptions,
  uploadAvatar,
} from '@/api/profile'
import { getBuildings, getFloors, getRooms } from '@/api/building'

// Store
const userStore = useUserStore()

// State
const activeTab = ref('basic')
const saving = ref(false)
const avatarUploading = ref(false)
const showBindDialog = ref(false)
const savingSubscriptions = ref(false)
const avatarInputRef = ref(null)
const profileFormRef = ref(null)
const bindFormRef = ref(null)

// Tab configuration
const tabs = [
  { key: 'basic', label: '基本资料', icon: 'icon-ep-user' },
  { key: 'binding', label: '账号绑定', icon: 'icon-ep-link' },
  { key: 'alarm', label: '告警订阅', icon: 'icon-ep-bell' },
]

// Profile data
const profile = reactive({
  username: '',
  real_name: '',
  phone: '',
  email: '',
  department: '',
  position: '',
  avatar: '',
})

// Form rules
const profileRules = {
  real_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' },
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' },
  ],
  email: [
    { type: 'email', message: '请输入正确的电子邮箱', trigger: 'blur' },
  ],
}

// Bind form
const bindForm = reactive({
  building_id: null,
  floor_id: null,
  room_id: null,
})

const bindRules = {
  building_id: [{ required: true, message: '请选择建筑', trigger: 'change' }],
  floor_id: [{ required: true, message: '请选择楼层', trigger: 'change' }],
  room_id: [{ required: true, message: '请选择房间', trigger: 'change' }],
}

// Data
const boundRooms = ref([])
const availableBuildings = ref([])
const availableFloors = ref([])
const availableRooms = ref([])

// Subscriptions
const subscriptions = reactive({
  lowBalance: {
    title: '余额不足提醒',
    description: '当账户余额低于设定阈值时接收通知',
    enabled: true,
  },
  abnormalUsage: {
    title: '异常用能提醒',
    description: '当检测到异常能耗情况时接收告警通知',
    enabled: true,
  },
  offlineDevice: {
    title: '设备离线提醒',
    description: '当绑定设备离线超过24小时时接收通知',
    enabled: false,
  },
})

// Methods
function switchTab(tab) {
  activeTab.value = tab
}

function selectAvatar() {
  avatarInputRef.value?.click()
}

async function handleAvatarChange(event) {
  const file = event.target.files?.[0]
  if (!file) return

  // Validate file
  if (!file.type.startsWith('image/')) {
    ElMessage.error('请选择图片文件')
    return
  }

  if (file.size > 2 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过 2MB')
    return
  }

  // Upload avatar
  const formData = new FormData()
  formData.append('avatar', file)

  avatarUploading.value = true
  try {
    const response = await uploadAvatar(formData)
    if (response.code === 0) {
      profile.avatar = response.data.avatar
      // Update store
      userStore.userInfo.avatar = response.data.avatar
      ElMessage.success('头像更新成功')
    }
  } catch (error) {
    console.error('Failed to upload avatar:', error)
    ElMessage.error('头像上传失败')
  } finally {
    avatarUploading.value = false
    // Reset input
    event.target.value = ''
  }
}

async function loadProfile() {
  try {
    const response = await getMyProfile()
    if (response.code === 0 && response.data) {
      Object.assign(profile, response.data)
      // Update store
      userStore.userInfo = { ...userStore.userInfo, ...response.data }
    }
  } catch (error) {
    console.error('Failed to load profile:', error)
    // Use store data as fallback
    if (userStore.userInfo) {
      Object.assign(profile, userStore.userInfo)
    }
  }
}

async function saveProfile() {
  try {
    await profileFormRef.value?.validate()
  } catch {
    return
  }

  saving.value = true
  try {
    const response = await updateMyProfile(profile)
    if (response.code === 0) {
      // Update store
      userStore.userInfo = { ...userStore.userInfo, ...profile }
      ElMessage.success('保存成功')
    }
  } catch (error) {
    console.error('Failed to save profile:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

function resetProfileForm() {
  loadProfile()
}

async function loadBoundRooms() {
  try {
    const response = await getMyBindRooms()
    if (response.code === 0 && response.data) {
      boundRooms.value = response.data
    }
  } catch (error) {
    console.error('Failed to load bound rooms:', error)
    // Mock data for development
    boundRooms.value = [
      { id: 1, room_number: '301', building_name: '学生宿舍A栋', floor_name: '3层', department: '计算机学院' },
    ]
  }
}

async function confirmUnbind(room) {
  try {
    await ElMessageBox.confirm(
      `确定要解绑房间"${room.room_number || room.name}"吗？`,
      '解绑确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    const response = await unbindRoomApi(room.id)
    if (response.code === 0) {
      boundRooms.value = boundRooms.value.filter(r => r.id !== room.id)
      ElMessage.success('解绑成功')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to unbind room:', error)
      ElMessage.error('解绑失败')
    }
  }
}

async function loadAvailableBuildings() {
  try {
    const response = await getBuildings()
    if (response.code === 0 && response.data) {
      availableBuildings.value = response.data
    }
  } catch (error) {
    console.error('Failed to load buildings:', error)
  }
}

async function onBuildingChange(buildingId) {
  bindForm.floor_id = null
  bindForm.room_id = null
  availableFloors.value = []
  availableRooms.value = []

  if (!buildingId) return

  try {
    const response = await getFloors({ building_id: buildingId })
    if (response.code === 0 && response.data) {
      availableFloors.value = response.data
    }
  } catch (error) {
    console.error('Failed to load floors:', error)
  }
}

async function onFloorChange(floorId) {
  bindForm.room_id = null
  availableRooms.value = []

  if (!floorId) return

  try {
    const response = await getRooms({ floor_id: floorId })
    if (response.code === 0 && response.data) {
      availableRooms.value = response.data
    }
  } catch (error) {
    console.error('Failed to load rooms:', error)
  }
}

async function bindRoom() {
  try {
    await bindFormRef.value?.validate()
  } catch {
    return
  }

  try {
    const response = await bindRoomApi({ room_ids: [bindForm.room_id] })
    if (response.code === 0) {
      showBindDialog.value = false
      await loadBoundRooms()
      ElMessage.success('绑定成功')
      // Reset form
      bindForm.building_id = null
      bindForm.floor_id = null
      bindForm.room_id = null
      availableFloors.value = []
      availableRooms.value = []
    }
  } catch (error) {
    console.error('Failed to bind room:', error)
    ElMessage.error('绑定失败')
  }
}

async function loadSubscriptions() {
  try {
    const response = await getMyAlarmSubscriptions()
    if (response.code === 0 && response.data) {
      // Merge with default subscriptions
      Object.keys(subscriptions).forEach(key => {
        if (response.data[key] !== undefined) {
          subscriptions[key].enabled = response.data[key]
        }
      })
    }
  } catch (error) {
    console.error('Failed to load subscriptions:', error)
  }
}

function updateSubscription(key, enabled) {
  subscriptions[key].enabled = enabled
}

async function saveSubscriptions() {
  savingSubscriptions.value = true
  try {
    const data = {}
    Object.keys(subscriptions).forEach(key => {
      data[key] = subscriptions[key].enabled
    })

    const response = await updateAlarmSubscriptions(data)
    if (response.code === 0) {
      ElMessage.success('设置保存成功')
    }
  } catch (error) {
    console.error('Failed to save subscriptions:', error)
    ElMessage.error('保存失败')
  } finally {
    savingSubscriptions.value = false
  }
}

// Lifecycle
onMounted(() => {
  loadProfile()
  loadBoundRooms()
  loadSubscriptions()
  loadAvailableBuildings()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

.profile-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   PAGE HEADER
   ======================================== */
.page-header {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #f97316 0%, #ea580c 50%, #dc2626 100%);
  border-radius: 20px;
  padding: 28px 32px;
  color: white;
  box-shadow: 0 20px 40px rgba(249, 115, 22, 0.25);
}

.header-content {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.header-icon svg {
  width: 28px;
  height: 28px;
  color: white;
}

.header-text .page-title {
  margin: 0 0 4px;
  font-size: 24px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
}

.header-text .page-subtitle {
  margin: 0;
  font-size: 13px;
  opacity: 0.9;
}

.header-decoration {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 16px;
}

.deco-circle {
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.circle-1 {
  width: 80px;
  height: 80px;
  animation: float 3s ease-in-out infinite;
}

.circle-2 {
  width: 50px;
  height: 50px;
  animation: float 3s ease-in-out infinite 0.5s;
}

.circle-3 {
  width: 30px;
  height: 30px;
  animation: float 3s ease-in-out infinite 1s;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* ========================================
   PROFILE CONTENT
   ======================================== */
.profile-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Tab Navigation */
.tab-navigation {
  display: flex;
  gap: 8px;
  background: white;
  padding: 6px;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: transparent;
  border: none;
  border-radius: 10px;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-btn:hover {
  background: #f8fafc;
  color: #f97316;
}

.tab-btn.active {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.tab-icon {
  display: flex;
  align-items: center;
  font-size: 18px;
}

/* Tab Content */
.tab-content {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  padding: 24px;
  min-height: 400px;
}

/* Tab Transition */
.tab-fade-enter-active,
.tab-fade-leave-active {
  transition: all 0.3s ease;
}

.tab-fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.tab-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* ========================================
   BASIC INFO TAB
   ======================================== */
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #fff7ed 0%, #fff 100%);
  border-radius: 16px;
  border: 1px solid rgba(249, 115, 22, 0.2);
  margin-bottom: 24px;
}

.avatar-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.avatar-container {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid white;
  box-shadow: 0 8px 24px rgba(249, 115, 22, 0.2);
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 48px;
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

.avatar-container.uploading {
  pointer-events: none;
}

.avatar-upload-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  color: #64748b;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.avatar-upload-btn:hover {
  border-color: #f97316;
  color: #f97316;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.15);
}

.avatar-tips {
  margin-top: 8px;
}

.avatar-tips p {
  margin: 0;
  font-size: 12px;
  color: #9ca3af;
  text-align: center;
}

/* Profile Form */
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-section {
  padding: 20px;
  background: #f9fafb;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 16px;
  font-size: 14px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

.title-icon {
  display: flex;
  align-items: center;
  color: #f97316;
  font-size: 18px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

/* Form Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.action-btn.secondary {
  background: #f8fafc;
  color: #64748b;
  border: 1px solid #e5e7eb;
}

.action-btn.secondary:hover {
  background: #f1f5f9;
}

.action-btn.primary {
  background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.3);
}

.action-btn.primary:hover {
  box-shadow: 0 6px 20px rgba(249, 115, 22, 0.4);
  transform: translateY(-1px);
}

.action-btn.loading {
  opacity: 0.8;
  cursor: not-allowed;
}

/* ========================================
   BINDING TAB
   ======================================== */
.binding-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.binding-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

.add-room-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-room-btn:hover {
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
  transform: translateY(-1px);
}

/* Room List */
.room-list {
  display: grid;
  gap: 12px;
}

.room-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 18px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  transition: all 0.3s ease;
}

.room-card:hover {
  background: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  border-color: #f97316;
}

.room-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 12px;
  color: #92400e;
  font-size: 20px;
}

.room-info {
  flex: 1;
  min-width: 0;
}

.room-name {
  margin: 0 0 4px;
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.room-detail {
  margin: 0 0 4px;
  font-size: 13px;
  color: #64748b;
}

.room-detail .separator {
  margin: 0 6px;
}

.room-department {
  margin: 0;
  font-size: 12px;
  color: #9ca3af;
}

.room-actions {
  flex-shrink: 0;
}

.room-action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.room-action-btn.unbind {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.room-action-btn.unbind:hover {
  background: #ef4444;
  color: white;
}

/* ========================================
   ALARM TAB
   ======================================== */
.alarm-header {
  margin-bottom: 24px;
}

.alarm-title {
  margin: 0 0 4px;
  font-size: 16px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

.alarm-subtitle {
  margin: 0;
  font-size: 13px;
  color: #64748b;
}

/* Subscription List */
.subscription-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.subscription-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  transition: all 0.3s ease;
}

.subscription-card:hover {
  background: white;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.sub-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  font-size: 20px;
  color: white;
}

.sub-icon.sub-lowBalance {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
}

.sub-icon.sub-abnormalUsage {
  background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
}

.sub-icon.sub-offlineDevice {
  background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
}

.sub-content {
  flex: 1;
}

.sub-title {
  margin: 0 0 4px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.sub-description {
  margin: 0;
  font-size: 12px;
  color: #64748b;
}

.sub-toggle {
  flex-shrink: 0;
}

/* Alarm Actions */
.alarm-actions {
  display: flex;
  justify-content: flex-end;
}

/* ========================================
   BIND DIALOG
   ======================================== */
:deep(.bind-dialog) {
  border-radius: 16px;
}

:deep(.bind-dialog .el-dialog__header) {
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
}

:deep(.bind-dialog .el-dialog__title) {
  font-size: 16px;
  font-weight: 600;
  font-family: 'Noto Sans SC', sans-serif;
  color: #1f2937;
}

:deep(.bind-dialog .el-dialog__body) {
  padding: 24px;
}

:deep(.bind-dialog .el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid #f1f5f9;
}

/* ========================================
   ELEMENT PLUS OVERRIDES
   ======================================== */
:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #fcd34d inset;
}

:deep(.el-input.is-disabled .el-input__wrapper) {
  background: #f8fafc;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #f97316 inset !important;
}

:deep(.el-select .el-input__wrapper) {
  border-radius: 10px;
}

:deep(.el-switch.is-checked .el-switch__core) {
  background-color: #f97316;
}

:deep(.el-select-dropdown__item.is-selected) {
  color: #f97316;
  background: rgba(249, 115, 22, 0.1);
}

:deep(.el-empty) {
  padding: 40px 20px;
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 768px) {
  .page-header {
    padding: 20px;
  }

  .header-decoration {
    display: none;
  }

  .header-text .page-title {
    font-size: 20px;
  }

  .tab-navigation {
    overflow-x: auto;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .room-card {
    flex-wrap: wrap;
  }

  .room-actions {
    width: 100%;
    margin-top: 12px;
  }

  .room-action-btn {
    width: 100%;
    justify-content: center;
  }

  .subscription-card {
    flex-wrap: wrap;
  }

  .sub-toggle {
    width: 100%;
    display: flex;
    justify-content: flex-end;
    margin-top: 12px;
  }
}
</style>
