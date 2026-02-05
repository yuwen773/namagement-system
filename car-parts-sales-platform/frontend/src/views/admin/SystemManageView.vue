<template>
  <div class="system-manage-view">
    <el-tabs v-model="activeTab" class="system-tabs">
      <!-- 系统配置 -->
      <el-tab-pane label="系统配置" name="configs">
        <div class="tab-content">
          <!-- 统计卡片 -->
          <el-row :gutter="16" class="stats-row">
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
                  <el-icon><Setting /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ configStats.total }}</div>
                  <div class="stat-label">总配置数</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
                  <el-icon><Unlock /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ configStats.editable }}</div>
                  <div class="stat-label">可编辑</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)">
                  <el-icon><Lock /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ configStats.readonly }}</div>
                  <div class="stat-label">只读</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ configStats.basic }}</div>
                  <div class="stat-label">基础配置</div>
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- 操作栏 -->
          <div class="toolbar">
            <el-input
              v-model="configSearch"
              placeholder="搜索配置键或描述"
              clearable
              style="width: 250px"
              @clear="fetchConfigs"
              @keyup.enter="fetchConfigs"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-select v-model="configCategoryFilter" placeholder="选择分类" clearable style="width: 150px" @change="fetchConfigs">
              <el-option label="基础配置" value="basic" />
              <el-option label="SEO配置" value="seo" />
              <el-option label="交易配置" value="trade" />
              <el-option label="其他配置" value="other" />
            </el-select>
            <el-select v-model="configEditableFilter" placeholder="编辑权限" clearable style="width: 130px" @change="fetchConfigs">
              <el-option label="可编辑" :value="true" />
              <el-option label="只读" :value="false" />
            </el-select>
            <el-button type="primary" @click="openConfigDialog()">
              <el-icon><Plus /></el-icon>
              新增配置
            </el-button>
          </div>

          <!-- 配置表格 -->
          <el-table :data="configList" stripe v-loading="configLoading">
            <el-table-column prop="key" label="配置键" width="200" />
            <el-table-column prop="value" label="配置值" show-overflow-tooltip />
            <el-table-column prop="description" label="描述" show-overflow-tooltip />
            <el-table-column prop="category" label="分类" width="120">
              <template #default="{ row }">
                <el-tag :type="getConfigCategoryType(row.category)" size="small">
                  {{ getConfigCategoryLabel(row.category) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="is_editable" label="可编辑" width="100" align="center">
              <template #default="{ row }">
                <el-icon v-if="row.is_editable" color="#67c23a"><Unlock /></el-icon>
                <el-icon v-else color="#909399"><Lock /></el-icon>
              </template>
            </el-table-column>
            <el-table-column prop="updated_at" label="更新时间" width="170">
              <template #default="{ row }">
                {{ formatDateTime(row.updated_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button v-if="row.is_editable" type="primary" link size="small" @click="openConfigDialog(row)">编辑</el-button>
                <el-button v-else type="info" link size="small" @click="viewConfig(row)">查看</el-button>
                <el-popconfirm v-if="row.is_editable" title="确定删除此配置吗？" @confirm="deleteConfig(row.id)">
                  <template #reference>
                    <el-button type="danger" link size="small">删除</el-button>
                  </template>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <el-pagination
            v-model:current-page="configPagination.page"
            v-model:page-size="configPagination.page_size"
            :total="configPagination.total"
            :page-sizes="[10, 30, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="fetchConfigs"
            @current-change="fetchConfigs"
          />
        </div>
      </el-tab-pane>

      <!-- 消息通知 -->
      <el-tab-pane label="消息通知" name="messages">
        <div class="tab-content">
          <!-- 统计卡片 -->
          <el-row :gutter="16" class="stats-row">
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
                  <el-icon><Message /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ messageStats.total }}</div>
                  <div class="stat-label">总消息数</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
                  <el-icon><DocumentCopy /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ messageStats.draft }}</div>
                  <div class="stat-label">草稿</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)">
                  <el-icon><Promotion /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ messageStats.sent }}</div>
                  <div class="stat-label">已发送</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)">
                  <el-icon><View /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ messageStats.read }}</div>
                  <div class="stat-label">已读</div>
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- 操作栏 -->
          <div class="toolbar">
            <el-input
              v-model="messageSearch"
              placeholder="搜索消息标题或内容"
              clearable
              style="width: 250px"
              @clear="fetchMessages"
              @keyup.enter="fetchMessages"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-button type="primary" @click="openMessageDialog()">
              <el-icon><Plus /></el-icon>
              发送消息
            </el-button>
          </div>

          <!-- 消息表格 -->
          <el-table :data="messageList" stripe v-loading="messageLoading">
            <el-table-column prop="title" label="标题" width="200" show-overflow-tooltip />
            <el-table-column prop="content" label="内容" show-overflow-tooltip />
            <el-table-column prop="message_type" label="类型" width="110">
              <template #default="{ row }">
                <el-tag :type="getMessageTypeColor(row.message_type)" size="small">
                  {{ getMessageTypeLabel(row.message_type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="recipient_name" label="接收人" width="120">
              <template #default="{ row }">
                {{ row.recipient_name || '全员' }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="90">
              <template #default="{ row }">
                <el-tag :type="getMessageStatusType(row.status)" size="small">
                  {{ getMessageStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="sent_at" label="发送时间" width="170">
              <template #default="{ row }">
                {{ formatDateTime(row.sent_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="viewMessage(row)">查看</el-button>
                <el-button v-if="row.status === 'draft'" type="warning" link size="small" @click="openMessageDialog(row)">编辑</el-button>
                <el-popconfirm title="确定删除此消息吗？" @confirm="deleteMessage(row.id)">
                  <template #reference>
                    <el-button type="danger" link size="small">删除</el-button>
                  </template>
                </el-popconfirm>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <el-pagination
            v-model:current-page="messagePagination.page"
            v-model:page-size="messagePagination.page_size"
            :total="messagePagination.total"
            :page-sizes="[10, 30, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="fetchMessages"
            @current-change="fetchMessages"
          />
        </div>
      </el-tab-pane>

      <!-- 操作日志 -->
      <el-tab-pane label="操作日志" name="logs">
        <div class="tab-content">
          <!-- 统计卡片 -->
          <el-row :gutter="16" class="stats-row">
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ logStats.total }}</div>
                  <div class="stat-label">总日志数</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)">
                  <el-icon><CircleCheck /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ logStats.success }}</div>
                  <div class="stat-label">成功</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
                  <el-icon><CircleClose /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ logStats.failed }}</div>
                  <div class="stat-label">失败</div>
                </div>
              </div>
            </el-col>
            <el-col :xs="12" :sm="8" :md="6">
              <div class="stat-card">
                <div class="stat-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%)">
                  <el-icon><Warning /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ logStats.today }}</div>
                  <div class="stat-label">今日</div>
                </div>
              </div>
            </el-col>
          </el-row>

          <!-- 操作栏 -->
          <div class="toolbar">
            <el-input
              v-model="logSearch"
              placeholder="搜索操作人或详情"
              clearable
              style="width: 250px"
              @clear="fetchLogs"
              @keyup.enter="fetchLogs"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            <el-select v-model="logActionFilter" placeholder="操作类型" clearable style="width: 130px" @change="fetchLogs">
              <el-option label="创建" value="create" />
              <el-option label="更新" value="update" />
              <el-option label="删除" value="delete" />
              <el-option label="登录" value="login" />
              <el-option label="登出" value="logout" />
            </el-select>
            <el-select v-model="logStatusFilter" placeholder="操作状态" clearable style="width: 120px" @change="fetchLogs">
              <el-option label="成功" value="success" />
              <el-option label="失败" value="failed" />
            </el-select>
          </div>

          <!-- 日志表格 -->
          <el-table :data="logList" stripe v-loading="logLoading">
            <el-table-column prop="operator_name" label="操作人" width="120" />
            <el-table-column prop="action_type" label="操作类型" width="90">
              <template #default="{ row }">
                <el-tag :type="getLogActionColor(row.action_type)" size="small">
                  {{ getLogActionLabel(row.action_type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="object_type" label="对象类型" width="120" />
            <el-table-column prop="detail" label="操作详情" show-overflow-tooltip />
            <el-table-column prop="ip_address" label="IP地址" width="140" />
            <el-table-column prop="status" label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="getLogStatusType(row.status)" size="small">
                  {{ getLogStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="操作时间" width="170">
              <template #default="{ row }">
                {{ formatDateTime(row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" link size="small" @click="viewLog(row)">详情</el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <el-pagination
            v-model:current-page="logPagination.page"
            v-model:page-size="logPagination.page_size"
            :total="logPagination.total"
            :page-sizes="[10, 30, 50]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="fetchLogs"
            @current-change="fetchLogs"
          />
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 系统配置弹窗 -->
    <el-dialog
      v-model="configDialogVisible"
      :title="configForm.id ? '编辑配置' : '新增配置'"
      width="600px"
      @close="resetConfigForm"
    >
      <el-form :model="configForm" :rules="configRules" ref="configFormRef" label-width="100px">
        <el-form-item label="配置键" prop="key">
          <el-input v-model="configForm.key" placeholder="请输入配置键（英文，如：site_name）" :disabled="!!configForm.id" />
        </el-form-item>
        <el-form-item label="配置值" prop="value">
          <el-input v-model="configForm.value" type="textarea" :rows="3" placeholder="请输入配置值" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="configForm.description" placeholder="请输入配置描述" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="configForm.category" placeholder="请选择分类" style="width: 100%">
            <el-option label="基础配置" value="basic" />
            <el-option label="SEO配置" value="seo" />
            <el-option label="交易配置" value="trade" />
            <el-option label="其他配置" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="可编辑" prop="is_editable">
          <el-switch v-model="configForm.is_editable" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="configDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveConfig" :loading="configSubmitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- 配置查看弹窗 -->
    <el-dialog v-model="configViewVisible" title="配置详情" width="600px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="配置键">{{ currentConfig.key }}</el-descriptions-item>
        <el-descriptions-item label="配置值">{{ currentConfig.value }}</el-descriptions-item>
        <el-descriptions-item label="描述">{{ currentConfig.description }}</el-descriptions-item>
        <el-descriptions-item label="分类">
          <el-tag :type="getConfigCategoryType(currentConfig.category)">
            {{ getConfigCategoryLabel(currentConfig.category) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="可编辑">
          <el-tag :type="currentConfig.is_editable ? 'success' : 'info'">
            {{ currentConfig.is_editable ? '是' : '否' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDateTime(currentConfig.created_at) }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ formatDateTime(currentConfig.updated_at) }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 消息发送弹窗 -->
    <el-dialog
      v-model="messageDialogVisible"
      :title="messageForm.id ? '编辑消息' : '发送消息'"
      width="600px"
      @close="resetMessageForm"
    >
      <el-form :model="messageForm" :rules="messageRules" ref="messageFormRef" label-width="100px">
        <el-form-item label="接收人" prop="recipient">
          <el-select v-model="messageForm.recipient" placeholder="留空表示全员消息" clearable filterable style="width: 100%">
            <el-option
              v-for="user in userList"
              :key="user.id"
              :label="user.nick_name || user.phone"
              :value="user.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="消息类型" prop="message_type">
          <el-select v-model="messageForm.message_type" placeholder="请选择消息类型" style="width: 100%">
            <el-option label="系统公告" value="announcement" />
            <el-option label="订单通知" value="notification" />
            <el-option label="促销通知" value="promotion" />
            <el-option label="系统通知" value="system" />
          </el-select>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="messageForm.title" placeholder="请输入消息标题" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="messageForm.content" type="textarea" :rows="5" placeholder="请输入消息内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="messageDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveMessage" :loading="messageSubmitting">确定</el-button>
      </template>
    </el-dialog>

    <!-- 消息查看弹窗 -->
    <el-dialog v-model="messageViewVisible" title="消息详情" width="600px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="标题">{{ currentMessage.title }}</el-descriptions-item>
        <el-descriptions-item label="类型">
          <el-tag :type="getMessageTypeColor(currentMessage.message_type)">
            {{ getMessageTypeLabel(currentMessage.message_type) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="接收人">{{ currentMessage.recipient_name || '全员' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getMessageStatusType(currentMessage.status)">
            {{ getMessageStatusLabel(currentMessage.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="内容">
          <div style="white-space: pre-wrap">{{ currentMessage.content }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="发送时间">{{ formatDateTime(currentMessage.sent_at) }}</el-descriptions-item>
        <el-descriptions-item label="阅读时间">{{ formatDateTime(currentMessage.read_at) }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ formatDateTime(currentMessage.created_at) }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 日志详情弹窗 -->
    <el-dialog v-model="logViewVisible" title="日志详情" width="600px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="操作人">{{ currentLog.operator_name }}</el-descriptions-item>
        <el-descriptions-item label="操作类型">
          <el-tag :type="getLogActionColor(currentLog.action_type)">
            {{ getLogActionLabel(currentLog.action_type) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="对象类型">{{ currentLog.object_type }}</el-descriptions-item>
        <el-descriptions-item label="对象ID">{{ currentLog.object_id }}</el-descriptions-item>
        <el-descriptions-item label="操作详情">
          <div style="white-space: pre-wrap">{{ currentLog.detail }}</div>
        </el-descriptions-item>
        <el-descriptions-item label="IP地址">{{ currentLog.ip_address }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getLogStatusType(currentLog.status)">
            {{ getLogStatusLabel(currentLog.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item v-if="currentLog.error_message" label="错误信息">
          <span style="color: #f56c6c">{{ currentLog.error_message }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="操作时间">{{ formatDateTime(currentLog.created_at) }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Setting, Unlock, Lock, Document, Search, Plus, Message, DocumentCopy,
  Promotion, View, CircleCheck, CircleClose, Warning
} from '@element-plus/icons-vue'
import {
  getConfigsListApi, createConfigApi, updateConfigApi, deleteConfigApi,
  getMessagesListApi, createMessageApi, updateMessageApi, deleteMessageApi,
  getLogsListApi,
  getConfigCategoryLabel, getConfigCategoryType,
  getMessageTypeLabel, getMessageTypeColor, getMessageStatusLabel, getMessageStatusType,
  getLogActionLabel, getLogActionColor, getLogStatusLabel, getLogStatusType
} from '@/api/modules/system'
import { getUserListApi } from '@/api/modules/user'

const route = useRoute()

// 当前激活标签
const activeTab = ref('configs')

// 根据路由设置默认 tab
const setTabFromRoute = () => {
  const path = route.path
  if (path.endsWith('/logs')) {
    activeTab.value = 'logs'
  } else if (path.endsWith('/messages')) {
    activeTab.value = 'messages'
  } else {
    activeTab.value = 'configs'
  }
}

// 监听路由变化
watch(() => route.path, () => {
  setTabFromRoute()
}, { immediate: true })

// ==================== 系统配置 ====================
const configList = ref([])
const configLoading = ref(false)
const configSearch = ref('')
const configCategoryFilter = ref('')
const configEditableFilter = ref(null)
const configPagination = reactive({ page: 1, page_size: 20, total: 0 })
const configStats = reactive({ total: 0, editable: 0, readonly: 0, basic: 0 })

const configDialogVisible = ref(false)
const configViewVisible = ref(false)
const configSubmitting = ref(false)
const configFormRef = ref(null)
const configForm = reactive({
  id: null, key: '', value: '', description: '', category: 'basic', is_editable: true
})
const configRules = {
  key: [{ required: true, message: '请输入配置键', trigger: 'blur' }],
  value: [{ required: true, message: '请输入配置值', trigger: 'blur' }],
  description: [{ required: true, message: '请输入描述', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }]
}
const currentConfig = ref({})

// 获取配置列表
async function fetchConfigs() {
  configLoading.value = true
  try {
    const params = {
      page: configPagination.page,
      page_size: configPagination.page_size,
      search: configSearch.value || undefined,
      category: configCategoryFilter.value || undefined,
      is_editable: configEditableFilter.value !== null ? configEditableFilter.value : undefined
    }
    const res = await getConfigsListApi(params)
    configList.value = res.results || []
    configPagination.total = res.count || 0

    // 更新统计
    const results = res.results || []
    configStats.total = res.count || 0
    configStats.editable = results.filter(c => c.is_editable).length
    configStats.readonly = results.filter(c => !c.is_editable).length
    configStats.basic = results.filter(c => c.category === 'basic').length
  } catch (err) {
    ElMessage.error('获取配置列表失败')
  } finally {
    configLoading.value = false
  }
}

// 打开配置弹窗
function openConfigDialog(config = {}) {
  if (config.id) {
    Object.assign(configForm, {
      id: config.id, key: config.key, value: config.value,
      description: config.description, category: config.category, is_editable: config.is_editable
    })
  } else {
    resetConfigForm()
  }
  configDialogVisible.value = true
}

// 重置配置表单
function resetConfigForm() {
  configForm.id = null
  configForm.key = ''
  configForm.value = ''
  configForm.description = ''
  configForm.category = 'basic'
  configForm.is_editable = true
  configFormRef.value?.clearValidate()
}

// 保存配置
async function saveConfig() {
  await configFormRef.value.validate()
  configSubmitting.value = true
  try {
    const data = {
      key: configForm.key, value: configForm.value,
      description: configForm.description, category: configForm.category, is_editable: configForm.is_editable
    }
    if (configForm.id) {
      await updateConfigApi(configForm.id, data)
      ElMessage.success('更新成功')
    } else {
      await createConfigApi(data)
      ElMessage.success('创建成功')
    }
    configDialogVisible.value = false
    fetchConfigs()
  } catch (err) {
    ElMessage.error('保存失败')
  } finally {
    configSubmitting.value = false
  }
}

// 查看配置
function viewConfig(config) {
  currentConfig.value = config
  configViewVisible.value = true
}

// 删除配置
async function deleteConfig(id) {
  try {
    await deleteConfigApi(id)
    ElMessage.success('删除成功')
    fetchConfigs()
  } catch (err) {
    ElMessage.error('删除失败')
  }
}

// ==================== 消息通知 ====================
const messageList = ref([])
const messageLoading = ref(false)
const messageSearch = ref('')
const messagePagination = reactive({ page: 1, page_size: 20, total: 0 })
const messageStats = reactive({ total: 0, draft: 0, sent: 0, read: 0 })

const messageDialogVisible = ref(false)
const messageViewVisible = ref(false)
const messageSubmitting = ref(false)
const messageFormRef = ref(null)
const messageForm = reactive({
  id: null, recipient: null, title: '', content: '', message_type: 'announcement'
})
const messageRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  message_type: [{ required: true, message: '请选择消息类型', trigger: 'change' }]
}
const currentMessage = ref({})
const userList = ref([])

// 获取消息列表
async function fetchMessages() {
  messageLoading.value = true
  try {
    const params = {
      page: messagePagination.page,
      page_size: messagePagination.page_size,
      search: messageSearch.value || undefined
    }
    const res = await getMessagesListApi(params)
    messageList.value = res.results || []
    messagePagination.total = res.count || 0

    // 更新统计
    const results = res.results || []
    messageStats.total = res.count || 0
    messageStats.draft = results.filter(m => m.status === 'draft').length
    messageStats.sent = results.filter(m => m.status === 'sent').length
    messageStats.read = results.filter(m => m.status === 'read').length
  } catch (err) {
    ElMessage.error('获取消息列表失败')
  } finally {
    messageLoading.value = false
  }
}

// 打开消息弹窗
function openMessageDialog(message = {}) {
  if (message.id) {
    Object.assign(messageForm, {
      id: message.id, recipient: message.recipient, title: message.title,
      content: message.content, message_type: message.message_type
    })
  } else {
    resetMessageForm()
  }
  messageDialogVisible.value = true
}

// 重置消息表单
function resetMessageForm() {
  messageForm.id = null
  messageForm.recipient = null
  messageForm.title = ''
  messageForm.content = ''
  messageForm.message_type = 'announcement'
  messageFormRef.value?.clearValidate()
}

// 保存消息
async function saveMessage() {
  await messageFormRef.value.validate()
  messageSubmitting.value = true
  try {
    const data = {
      recipient: messageForm.recipient, title: messageForm.title,
      content: messageForm.content, message_type: messageForm.message_type
    }
    if (messageForm.id) {
      await updateMessageApi(messageForm.id, data)
      ElMessage.success('更新成功')
    } else {
      await createMessageApi(data)
      ElMessage.success('发送成功')
    }
    messageDialogVisible.value = false
    fetchMessages()
  } catch (err) {
    ElMessage.error('保存失败')
  } finally {
    messageSubmitting.value = false
  }
}

// 查看消息
function viewMessage(message) {
  currentMessage.value = message
  messageViewVisible.value = true
}

// 删除消息
async function deleteMessage(id) {
  try {
    await deleteMessageApi(id)
    ElMessage.success('删除成功')
    fetchMessages()
  } catch (err) {
    ElMessage.error('删除失败')
  }
}

// ==================== 操作日志 ====================
const logList = ref([])
const logLoading = ref(false)
const logSearch = ref('')
const logActionFilter = ref('')
const logStatusFilter = ref('')
const logPagination = reactive({ page: 1, page_size: 20, total: 0 })
const logStats = reactive({ total: 0, success: 0, failed: 0, today: 0 })

const logViewVisible = ref(false)
const currentLog = ref({})

// 获取日志列表
async function fetchLogs() {
  logLoading.value = true
  try {
    const params = {
      page: logPagination.page,
      page_size: logPagination.page_size,
      search: logSearch.value || undefined,
      action_type: logActionFilter.value || undefined,
      status: logStatusFilter.value || undefined
    }
    const res = await getLogsListApi(params)
    logList.value = res.results || []
    logPagination.total = res.count || 0

    // 更新统计
    const results = res.results || []
    logStats.total = res.count || 0
    logStats.success = results.filter(l => l.status === 'success').length
    logStats.failed = results.filter(l => l.status === 'failed').length
    // 简单统计今日日志
    const today = new Date().toDateString()
    logStats.today = results.filter(l => new Date(l.created_at).toDateString() === today).length
  } catch (err) {
    ElMessage.error('获取日志列表失败')
  } finally {
    logLoading.value = false
  }
}

// 查看日志
function viewLog(log) {
  currentLog.value = log
  logViewVisible.value = true
}

// ==================== 工具函数 ====================
function formatDateTime(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

// ==================== 初始化 ====================
onMounted(async () => {
  fetchConfigs()
  fetchMessages()
  fetchLogs()

  // 获取用户列表（用于消息接收人选择）
  try {
    const res = await getUserListApi({ page: 1, page_size: 1000 })
    userList.value = res.results || []
  } catch (err) {
    console.error('获取用户列表失败', err)
  }
})
</script>

<style scoped>
.system-manage-view {
  padding: 20px;
}

.system-tabs {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
}

.tab-content {
  min-height: 500px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-icon .el-icon {
  font-size: 28px;
  color: #fff;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 8px;
}

.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 20px;
  align-items: center;
}

.el-table {
  margin-bottom: 20px;
}

.el-pagination {
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .system-manage-view {
    padding: 10px;
  }

  .system-tabs {
    padding: 10px;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .toolbar > * {
    width: 100% !important;
  }

  .stat-card {
    margin-bottom: 12px;
  }
}
</style>
