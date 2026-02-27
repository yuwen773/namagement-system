<template>
  <div class="notices-admin-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-meta">
          <div class="meta-tag">ADMIN</div>
          <span class="meta-date">{{ currentDate }}</span>
        </div>
        <h1 class="page-title">公告与知识</h1>
        <p class="page-subtitle">统一管理通知公告与节能知识内容</p>
      </div>
      <div class="header-decoration">
        <div class="deco-line"></div>
        <div class="deco-square"></div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card stat-notice">
        <div class="stat-header">
          <span class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
          </span>
          <span class="stat-trend up">+{{ noticeStats.todayNew }}</span>
        </div>
        <div class="stat-value">{{ noticeStats.total }}</div>
        <div class="stat-label">公告总数</div>
      </div>
      <div class="stat-card stat-published">
        <div class="stat-header">
          <span class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
          </span>
          <span class="stat-trend">{{ Math.round(noticeStats.published / noticeStats.total * 100) || 0 }}%</span>
        </div>
        <div class="stat-value">{{ noticeStats.published }}</div>
        <div class="stat-label">已发布</div>
      </div>
      <div class="stat-card stat-tip">
        <div class="stat-header">
          <span class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" y1="16" x2="12" y2="12"/>
              <line x1="12" y1="8" x2="12.01" y2="8"/>
            </svg>
          </span>
          <span class="stat-trend up">+{{ tipStats.todayNew }}</span>
        </div>
        <div class="stat-value">{{ tipStats.total }}</div>
        <div class="stat-label">知识条目</div>
      </div>
      <div class="stat-card stat-draft">
        <div class="stat-header">
          <span class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
              <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
            </svg>
          </span>
        </div>
        <div class="stat-value">{{ noticeStats.draft + tipStats.draft }}</div>
        <div class="stat-label">草稿</div>
      </div>
    </div>

    <!-- Tab Navigation -->
    <div class="tab-container">
      <div class="tab-nav">
        <button
          v-for="tab in tabs"
          :key="tab.key"
          :class="['tab-btn', { active: activeTab === tab.key }]"
          @click="activeTab = tab.key"
        >
          <span class="tab-icon" v-html="tab.icon"></span>
          <span class="tab-label">{{ tab.label }}</span>
          <span class="tab-count">{{ tab.key === 'notices' ? paginatedNotices.length : paginatedTips.length }}</span>
        </button>
      </div>

      <!-- Content Area -->
      <div class="tab-content">
        <!-- Notices Tab -->
        <div v-show="activeTab === 'notices'" class="content-panel notices-panel">
          <!-- Action Bar -->
          <div class="action-bar">
            <div class="search-wrapper">
              <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
              <input
                v-model="noticeFilters.search"
                type="text"
                placeholder="搜索公告标题或内容..."
                class="search-input"
                @input="applyNoticeFilters"
              />
            </div>
            <div class="filter-group">
              <select v-model="noticeFilters.type" class="filter-select" @change="applyNoticeFilters">
                <option value="">全部类型</option>
                <option value="NOTICE">通知</option>
                <option value="ANNOUNCEMENT">公告</option>
              </select>
              <select v-model="noticeFilters.status" class="filter-select" @change="applyNoticeFilters">
                <option value="">全部状态</option>
                <option value="published">已发布</option>
                <option value="draft">草稿</option>
              </select>
            </div>
            <div class="action-spacer"></div>
            <button class="btn btn-secondary" @click="loadNotices">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 4 23 10 17 10"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
              刷新
            </button>
            <button class="btn btn-primary" @click="openNoticeDialog()">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              新增公告
            </button>
          </div>

          <!-- Table -->
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th style="width: 50px">#</th>
                  <th>标题</th>
                  <th style="width: 100px">类型</th>
                  <th style="width: 90px">优先级</th>
                  <th style="width: 90px">目标</th>
                  <th style="width: 160px">发布时间</th>
                  <th style="width: 90px">状态</th>
                  <th style="width: 140px">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in paginatedNotices" :key="row.id" class="table-row">
                  <td class="row-index">{{ (noticePagination.page - 1) * noticePagination.pageSize + index + 1 }}</td>
                  <td class="row-title">
                    <span class="title-text">{{ row.title || '--' }}</span>
                    <span class="title-category">{{ row.category || '未分类' }}</span>
                  </td>
                  <td>
                    <span :class="['type-badge', `type-${row.notice_type}`]">
                      {{ noticeTypeLabel(row.notice_type) }}
                    </span>
                  </td>
                  <td>
                    <span :class="['priority-badge', `priority-${row.priority?.toLowerCase()}`]">
                      {{ priorityLabel(row.priority) }}
                    </span>
                  </td>
                  <td>
                    <span class="target-badge">{{ targetRoleLabel(row.target_role) }}</span>
                  </td>
                  <td class="row-time">{{ formatTime(row.publish_time) }}</td>
                  <td>
                    <span :class="['status-badge', row.is_published ? 'published' : 'draft']">
                      {{ row.is_published ? '已发布' : '草稿' }}
                    </span>
                  </td>
                  <td class="row-actions">
                    <button class="action-btn" @click="openNoticeDialog(row)" title="编辑">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                      </svg>
                    </button>
                    <button class="action-btn danger" @click="handleDeleteNotice(row)" title="删除">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                      </svg>
                    </button>
                  </td>
                </tr>
                <tr v-if="paginatedNotices.length === 0">
                  <td colspan="8" class="empty-cell">
                    <div class="empty-state">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
                        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
                      </svg>
                      <span>暂无公告数据</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="pagination-bar">
            <div class="pagination-info">
              共 <span class="highlight">{{ noticePagination.total }}</span> 条记录，
              第 <span class="highlight">{{ noticePagination.page }}</span> / {{ Math.ceil(noticePagination.total / noticePagination.pageSize) || 1 }} 页
            </div>
            <div class="pagination-controls">
              <button
                class="page-btn"
                :disabled="noticePagination.page === 1"
                @click="noticePagination.page--"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="15 18 9 12 15 6"/>
                </svg>
              </button>
              <span class="page-indicator">{{ noticePagination.page }}</span>
              <button
                class="page-btn"
                :disabled="noticePagination.page >= Math.ceil(noticePagination.total / noticePagination.pageSize)"
                @click="noticePagination.page++"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="9 18 15 12 9 6"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Tips Tab -->
        <div v-show="activeTab === 'tips'" class="content-panel tips-panel">
          <!-- Action Bar -->
          <div class="action-bar">
            <div class="search-wrapper">
              <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
              </svg>
              <input
                v-model="tipFilters.search"
                type="text"
                placeholder="搜索知识标题或内容..."
                class="search-input"
                @input="applyTipFilters"
              />
            </div>
            <div class="filter-group">
              <select v-model="tipFilters.category" class="filter-select" @change="applyTipFilters">
                <option value="">全部分类</option>
                <option v-for="cat in tipCategoryOptions" :key="cat" :value="cat">{{ cat }}</option>
              </select>
              <select v-model="tipFilters.status" class="filter-select" @change="applyTipFilters">
                <option value="">全部状态</option>
                <option value="published">已发布</option>
                <option value="draft">草稿</option>
              </select>
            </div>
            <div class="action-spacer"></div>
            <button class="btn btn-secondary" @click="loadTips">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23 4 23 10 17 10"/>
                <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
              </svg>
              刷新
            </button>
            <button class="btn btn-primary" @click="openTipDialog()">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              新增知识
            </button>
          </div>

          <!-- Table -->
          <div class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th style="width: 50px">#</th>
                  <th>标题</th>
                  <th style="width: 200px">内容摘要</th>
                  <th style="width: 120px">分类</th>
                  <th style="width: 90px">目标</th>
                  <th style="width: 160px">发布时间</th>
                  <th style="width: 90px">状态</th>
                  <th style="width: 140px">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in paginatedTips" :key="row.id" class="table-row">
                  <td class="row-index">{{ (tipPagination.page - 1) * tipPagination.pageSize + index + 1 }}</td>
                  <td class="row-title">
                    <span class="title-text">{{ row.title || '--' }}</span>
                  </td>
                  <td class="row-content">{{ shortText(row.content) }}</td>
                  <td>
                    <span class="category-tag">{{ row.category || '未分类' }}</span>
                  </td>
                  <td>
                    <span class="target-badge">{{ targetRoleLabel(row.target_role) }}</span>
                  </td>
                  <td class="row-time">{{ formatTime(row.publish_time) }}</td>
                  <td>
                    <span :class="['status-badge', row.is_published ? 'published' : 'draft']">
                      {{ row.is_published ? '已发布' : '草稿' }}
                    </span>
                  </td>
                  <td class="row-actions">
                    <button class="action-btn" @click="openTipDialog(row)" title="编辑">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                      </svg>
                    </button>
                    <button class="action-btn danger" @click="handleDeleteTip(row)" title="删除">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"/>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                      </svg>
                    </button>
                  </td>
                </tr>
                <tr v-if="paginatedTips.length === 0">
                  <td colspan="8" class="empty-cell">
                    <div class="empty-state">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="16" x2="12" y2="12"/>
                        <line x1="12" y1="8" x2="12.01" y2="8"/>
                      </svg>
                      <span>暂无知识数据</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div class="pagination-bar">
            <div class="pagination-info">
              共 <span class="highlight">{{ tipPagination.total }}</span> 条记录，
              第 <span class="highlight">{{ tipPagination.page }}</span> / {{ Math.ceil(tipPagination.total / tipPagination.pageSize) || 1 }} 页
            </div>
            <div class="pagination-controls">
              <button
                class="page-btn"
                :disabled="tipPagination.page === 1"
                @click="tipPagination.page--"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="15 18 9 12 15 6"/>
                </svg>
              </button>
              <span class="page-indicator">{{ tipPagination.page }}</span>
              <button
                class="page-btn"
                :disabled="tipPagination.page >= Math.ceil(tipPagination.total / tipPagination.pageSize)"
                @click="tipPagination.page++"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="9 18 15 12 9 6"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Notice Dialog -->
    <div class="dialog-overlay" v-show="noticeDialog.visible" @click.self="noticeDialog.visible = false">
      <div class="dialog-panel">
        <div class="dialog-header">
          <h3 class="dialog-title">{{ noticeDialog.isEdit ? '编辑公告' : '新增公告' }}</h3>
          <button class="dialog-close" @click="noticeDialog.visible = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="dialog-body">
          <div class="form-group">
            <label class="form-label">标题 <span class="required">*</span></label>
            <input
              v-model="noticeDialog.form.title"
              type="text"
              class="form-input"
              placeholder="请输入公告标题"
              maxlength="200"
            />
          </div>
          <div class="form-group">
            <label class="form-label">内容 <span class="required">*</span></label>
            <textarea
              v-model="noticeDialog.form.content"
              class="form-textarea"
              placeholder="请输入公告内容"
              rows="5"
              maxlength="5000"
            ></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">分类</label>
              <input
                v-model="noticeDialog.form.category"
                type="text"
                class="form-input"
                placeholder="如：系统维护"
                maxlength="32"
              />
            </div>
            <div class="form-group">
              <label class="form-label">类型</label>
              <select v-model="noticeDialog.form.notice_type" class="form-select">
                <option value="NOTICE">通知</option>
                <option value="ANNOUNCEMENT">公告</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">优先级</label>
              <select v-model="noticeDialog.form.priority" class="form-select">
                <option value="LOW">低</option>
                <option value="MEDIUM">中</option>
                <option value="HIGH">高</option>
                <option value="URGENT">紧急</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">目标角色</label>
              <select v-model="noticeDialog.form.target_role" class="form-select">
                <option value="ALL">全部</option>
                <option value="ADMIN">仅管理员</option>
                <option value="USER">仅用户</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">发布状态</label>
              <label class="toggle-switch">
                <input type="checkbox" v-model="noticeDialog.form.is_published" />
                <span class="toggle-slider"></span>
                <span class="toggle-label">{{ noticeDialog.form.is_published ? '已发布' : '草稿' }}</span>
              </label>
            </div>
            <div class="form-group">
              <label class="form-label">发布时间</label>
              <input
                v-model="noticeDialog.form.publish_time"
                type="datetime-local"
                class="form-input"
              />
            </div>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn btn-secondary" @click="noticeDialog.visible = false">取消</button>
          <button class="btn btn-primary" :class="{ loading: noticeDialog.loading }" @click="submitNotice">
            <svg v-if="noticeDialog.loading" class="spinner" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="30 60"/>
            </svg>
            {{ noticeDialog.isEdit ? '保存' : '创建' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Tip Dialog -->
    <div class="dialog-overlay" v-show="tipDialog.visible" @click.self="tipDialog.visible = false">
      <div class="dialog-panel">
        <div class="dialog-header">
          <h3 class="dialog-title">{{ tipDialog.isEdit ? '编辑知识' : '新增知识' }}</h3>
          <button class="dialog-close" @click="tipDialog.visible = false">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        <div class="dialog-body">
          <div class="form-group">
            <label class="form-label">标题 <span class="required">*</span></label>
            <input
              v-model="tipDialog.form.title"
              type="text"
              class="form-input"
              placeholder="请输入知识标题"
              maxlength="200"
            />
          </div>
          <div class="form-group">
            <label class="form-label">内容 <span class="required">*</span></label>
            <textarea
              v-model="tipDialog.form.content"
              class="form-textarea"
              placeholder="请输入知识内容"
              rows="5"
              maxlength="5000"
            ></textarea>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">分类</label>
              <input
                v-model="tipDialog.form.category"
                type="text"
                class="form-input"
                placeholder="如：节电/节水/节气"
                maxlength="32"
              />
            </div>
            <div class="form-group">
              <label class="form-label">目标角色</label>
              <select v-model="tipDialog.form.target_role" class="form-select">
                <option value="ALL">全部</option>
                <option value="ADMIN">仅管理员</option>
                <option value="USER">仅用户</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label class="form-label">发布状态</label>
              <label class="toggle-switch">
                <input type="checkbox" v-model="tipDialog.form.is_published" />
                <span class="toggle-slider"></span>
                <span class="toggle-label">{{ tipDialog.form.is_published ? '已发布' : '草稿' }}</span>
              </label>
            </div>
            <div class="form-group">
              <label class="form-label">发布时间</label>
              <input
                v-model="tipDialog.form.publish_time"
                type="datetime-local"
                class="form-input"
              />
            </div>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn btn-secondary" @click="tipDialog.visible = false">取消</button>
          <button class="btn btn-primary" :class="{ loading: tipDialog.loading }" @click="submitTip">
            <svg v-if="tipDialog.loading" class="spinner" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" fill="none" stroke-dasharray="30 60"/>
            </svg>
            {{ tipDialog.isEdit ? '保存' : '创建' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getNotices, getTips, createNotice, updateNotice, deleteNotice, createTip, updateTip, deleteTip } from '@/api/system'

// Current date
const currentDate = new Date().toLocaleDateString('zh-CN', {
  year: 'numeric',
  month: 'long',
  day: 'numeric'
})

// Tab configuration
const tabs = [
  {
    key: 'notices',
    label: '通知公告',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>'
  },
  {
    key: 'tips',
    label: '节能知识',
    icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>'
  }
]

const activeTab = ref('notices')

// Stats
const noticeStats = ref({ total: 0, published: 0, draft: 0, todayNew: 0 })
const tipStats = ref({ total: 0, published: 0, draft: 0, todayNew: 0 })

// Data
const notices = ref([])
const tips = ref([])

// Filters
const noticeFilters = ref({ search: '', type: '', status: '' })
const tipFilters = ref({ search: '', category: '', status: '' })

// Pagination
const noticePagination = ref({ page: 1, pageSize: 10, total: 0 })
const tipPagination = ref({ page: 1, pageSize: 10, total: 0 })

// Loading states
const noticeLoading = ref(false)
const tipLoading = ref(false)

// Tip category options
const tipCategoryOptions = ['节电', '节水', '节气', '日常', '安全', '环保']

// Dialog states
const noticeDialog = ref({
  visible: false,
  isEdit: false,
  loading: false,
  form: {
    id: null,
    title: '',
    content: '',
    category: '',
    notice_type: 'NOTICE',
    priority: 'MEDIUM',
    target_role: 'ALL',
    is_published: false,
    publish_time: ''
  }
})

const tipDialog = ref({
  visible: false,
  isEdit: false,
  loading: false,
  form: {
    id: null,
    title: '',
    content: '',
    category: '',
    target_role: 'ALL',
    is_published: false,
    publish_time: ''
  }
})

// Computed filtered data
const filteredNotices = computed(() => {
  let result = notices.value

  if (noticeFilters.value.search) {
    const keyword = noticeFilters.value.search.toLowerCase()
    result = result.filter(n =>
      n.title?.toLowerCase().includes(keyword) ||
      n.content?.toLowerCase().includes(keyword)
    )
  }

  if (noticeFilters.value.type) {
    result = result.filter(n => n.notice_type === noticeFilters.value.type)
  }

  if (noticeFilters.value.status) {
    const isPublished = noticeFilters.value.status === 'published'
    result = result.filter(n => n.is_published === isPublished)
  }

  return result
})

const filteredTips = computed(() => {
  let result = tips.value

  if (tipFilters.value.search) {
    const keyword = tipFilters.value.search.toLowerCase()
    result = result.filter(t =>
      t.title?.toLowerCase().includes(keyword) ||
      t.content?.toLowerCase().includes(keyword)
    )
  }

  if (tipFilters.value.category) {
    result = result.filter(t => t.category === tipFilters.value.category)
  }

  if (tipFilters.value.status) {
    const isPublished = tipFilters.value.status === 'published'
    result = result.filter(t => t.is_published === isPublished)
  }

  return result
})

// Paginated data
const paginatedNotices = computed(() => {
  const start = (noticePagination.value.page - 1) * noticePagination.value.pageSize
  const end = start + noticePagination.value.pageSize
  noticePagination.value.total = filteredNotices.value.length
  return filteredNotices.value.slice(start, end)
})

const paginatedTips = computed(() => {
  const start = (tipPagination.value.page - 1) * tipPagination.value.pageSize
  const end = start + tipPagination.value.pageSize
  tipPagination.value.total = filteredTips.value.length
  return filteredTips.value.slice(start, end)
})

// Methods
function noticeTypeLabel(type) {
  const labels = { NOTICE: '通知', ANNOUNCEMENT: '公告' }
  return labels[type] || '通知'
}

function priorityLabel(priority) {
  const labels = { LOW: '低', MEDIUM: '中', HIGH: '高', URGENT: '紧急' }
  return labels[priority] || '中'
}

function targetRoleLabel(role) {
  const labels = { ALL: '全部', ADMIN: '管理员', USER: '用户' }
  return labels[role] || '全部'
}

function priorityTagType(priority) {
  const types = { LOW: 'info', MEDIUM: 'warning', HIGH: 'danger', URGENT: 'danger' }
  return types[priority] || 'info'
}

function formatTime(timeStr) {
  if (!timeStr) return '--'
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function shortText(text, maxLength = 60) {
  if (!text) return '--'
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

function applyNoticeFilters() {
  noticePagination.value.page = 1
}

function applyTipFilters() {
  tipPagination.value.page = 1
}

async function loadNotices() {
  noticeLoading.value = true
  try {
    const response = await getNotices()
    if (response.code === 0 && response.data) {
      notices.value = response.data
      updateNoticeStats()
    }
  } catch (error) {
    console.error('Failed to load notices:', error)
    // Mock data for development
    notices.value = [
      {
        id: 1,
        title: '系统维护通知',
        content: '因系统升级，明日2:00-6:00暂停服务。',
        notice_type: 'NOTICE',
        priority: 'HIGH',
        category: '系统维护',
        target_role: 'ALL',
        is_published: true,
        publish_time: new Date().toISOString()
      }
    ]
    updateNoticeStats()
  } finally {
    noticeLoading.value = false
  }
}

async function loadTips() {
  tipLoading.value = true
  try {
    const response = await getTips()
    if (response.code === 0 && response.data) {
      tips.value = response.data
      updateTipStats()
    }
  } catch (error) {
    console.error('Failed to load tips:', error)
    // Mock data for development
    tips.value = [
      {
        id: 1,
        title: '空调省电小妙招',
        content: '空调温度设置在26℃最省电，每升高1℃可省电约7%。',
        category: '节电',
        target_role: 'ALL',
        is_published: true,
        publish_time: new Date().toISOString()
      }
    ]
    updateTipStats()
  } finally {
    tipLoading.value = false
  }
}

function updateNoticeStats() {
  const today = new Date().toDateString()
  noticeStats.value = {
    total: notices.value.length,
    published: notices.value.filter(n => n.is_published).length,
    draft: notices.value.filter(n => !n.is_published).length,
    todayNew: notices.value.filter(n => new Date(n.publish_time).toDateString() === today).length
  }
}

function updateTipStats() {
  const today = new Date().toDateString()
  tipStats.value = {
    total: tips.value.length,
    published: tips.value.filter(t => t.is_published).length,
    draft: tips.value.filter(t => !t.is_published).length,
    todayNew: tips.value.filter(t => new Date(t.publish_time).toDateString() === today).length
  }
}

function openNoticeDialog(row = null) {
  if (row) {
    noticeDialog.value.isEdit = true
    noticeDialog.value.form = { ...row }
  } else {
    noticeDialog.value.isEdit = false
    noticeDialog.value.form = {
      id: null,
      title: '',
      content: '',
      category: '',
      notice_type: 'NOTICE',
      priority: 'MEDIUM',
      target_role: 'ALL',
      is_published: false,
      publish_time: ''
    }
  }
  noticeDialog.value.visible = true
}

function openTipDialog(row = null) {
  if (row) {
    tipDialog.value.isEdit = true
    tipDialog.value.form = { ...row }
  } else {
    tipDialog.value.isEdit = false
    tipDialog.value.form = {
      id: null,
      title: '',
      content: '',
      category: '',
      target_role: 'ALL',
      is_published: false,
      publish_time: ''
    }
  }
  tipDialog.value.visible = true
}

async function submitNotice() {
  if (!noticeDialog.value.form.title || !noticeDialog.value.form.content) {
    ElMessage.warning('请填写标题和内容')
    return
  }

  noticeDialog.value.loading = true
  try {
    const data = { ...noticeDialog.value.form }
    if (data.publish_time) {
      data.publish_time = new Date(data.publish_time).toISOString()
    }

    if (noticeDialog.value.isEdit) {
      await updateNotice(data.id, data)
      ElMessage.success('公告更新成功')
    } else {
      await createNotice(data)
      ElMessage.success('公告创建成功')
    }
    noticeDialog.value.visible = false
    await loadNotices()
  } catch (error) {
    console.error('Failed to submit notice:', error)
    ElMessage.error('操作失败，请重试')
  } finally {
    noticeDialog.value.loading = false
  }
}

async function submitTip() {
  if (!tipDialog.value.form.title || !tipDialog.value.form.content) {
    ElMessage.warning('请填写标题和内容')
    return
  }

  tipDialog.value.loading = true
  try {
    const data = { ...tipDialog.value.form }
    if (data.publish_time) {
      data.publish_time = new Date(data.publish_time).toISOString()
    }

    if (tipDialog.value.isEdit) {
      await updateTip(data.id, data)
      ElMessage.success('知识更新成功')
    } else {
      await createTip(data)
      ElMessage.success('知识创建成功')
    }
    tipDialog.value.visible = false
    await loadTips()
  } catch (error) {
    console.error('Failed to submit tip:', error)
    ElMessage.error('操作失败，请重试')
  } finally {
    tipDialog.value.loading = false
  }
}

async function handleDeleteNotice(row) {
  try {
    await ElMessageBox.confirm(`确定要删除公告"${row.title}"吗？`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteNotice(row.id)
    ElMessage.success('公告已删除')
    await loadNotices()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete notice:', error)
      ElMessage.error('删除失败，请重试')
    }
  }
}

async function handleDeleteTip(row) {
  try {
    await ElMessageBox.confirm(`确定要删除知识"${row.title}"吗？`, '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteTip(row.id)
    ElMessage.success('知识已删除')
    await loadTips()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete tip:', error)
      ElMessage.error('删除失败，请重试')
    }
  }
}

// Lifecycle
onMounted(async () => {
  await Promise.all([loadNotices(), loadTips()])
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

.notices-admin-page {
  --primary: #0d9488;
  --primary-light: #14b8a6;
  --primary-dark: #0f766e;
  --accent: #f59e0b;
  --accent-light: #fbbf24;
  --danger: #ef4444;
  --danger-light: #f87171;
  --success: #22c55e;
  --warning: #f59e0b;
  --info: #6366f1;

  --bg-primary: #fafafa;
  --bg-secondary: #ffffff;
  --bg-tertiary: #f5f5f5;

  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-muted: #94a3b8;

  --border-light: #e2e8f0;
  --border-medium: #cbd5e1;

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -1px rgba(0, 0, 0, 0.04);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);

  font-family: 'IBM Plex Sans', 'Noto Sans SC', sans-serif;
  color: var(--text-primary);
  background: var(--bg-primary);
  min-height: 100vh;
  padding: 24px;
}

/* ========================================
   PAGE HEADER - Editorial Style
   ======================================== */
.page-header {
  position: relative;
  background: var(--bg-secondary);
  border-radius: 16px;
  padding: 32px 40px;
  margin-bottom: 24px;
  border: 1px solid var(--border-light);
  overflow: hidden;
}

.header-content {
  position: relative;
  z-index: 1;
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.meta-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  background: var(--text-primary);
  color: white;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
  border-radius: 4px;
}

.meta-date {
  font-size: 13px;
  color: var(--text-muted);
}

.page-title {
  margin: 0 0 8px;
  font-family: 'Noto Serif SC', serif;
  font-size: 32px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}

.page-subtitle {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.header-decoration {
  position: absolute;
  right: 40px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  align-items: center;
  gap: 16px;
}

.deco-line {
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, var(--primary), transparent);
}

.deco-square {
  width: 12px;
  height: 12px;
  background: var(--primary);
  transform: rotate(45deg);
}

/* ========================================
   STATS GRID
   ======================================== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--border-light);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--bg-tertiary);
}

.stat-icon svg {
  width: 18px;
  height: 18px;
}

.stat-notice .stat-icon {
  background: rgba(13, 148, 136, 0.1);
  color: var(--primary);
}

.stat-published .stat-icon {
  background: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.stat-tip .stat-icon {
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent);
}

.stat-draft .stat-icon {
  background: rgba(99, 102, 241, 0.1);
  color: var(--info);
}

.stat-trend {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
}

.stat-trend.up {
  color: var(--success);
}

.stat-value {
  font-family: 'Noto Serif SC', serif;
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}

/* ========================================
   TAB NAVIGATION
   ======================================== */
.tab-container {
  background: var(--bg-secondary);
  border-radius: 16px;
  border: 1px solid var(--border-light);
  overflow: hidden;
}

.tab-nav {
  display: flex;
  border-bottom: 1px solid var(--border-light);
  background: var(--bg-tertiary);
}

.tab-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 24px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.5);
}

.tab-btn.active {
  color: var(--primary);
  background: var(--bg-secondary);
  border-bottom-color: var(--primary);
}

.tab-icon {
  display: flex;
  align-items: center;
}

.tab-icon svg {
  width: 18px;
  height: 18px;
}

.tab-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 6px;
  background: var(--border-light);
  border-radius: 10px;
  font-size: 11px;
  font-weight: 600;
}

.tab-btn.active .tab-count {
  background: var(--primary);
  color: white;
}

/* ========================================
   ACTION BAR
   ======================================== */
.action-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
}

.search-wrapper {
  position: relative;
  flex: 1;
  max-width: 320px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--text-muted);
}

.search-input {
  width: 100%;
  padding: 10px 12px 10px 38px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  font-size: 13px;
  color: var(--text-primary);
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  background: var(--bg-secondary);
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.filter-group {
  display: flex;
  gap: 8px;
}

.filter-select {
  padding: 10px 32px 10px 12px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  font-size: 13px;
  color: var(--text-primary);
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  transition: all 0.2s ease;
}

.filter-select:focus {
  outline: none;
  border-color: var(--primary);
}

.action-spacer {
  flex: 1;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn svg {
  width: 16px;
  height: 16px;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark);
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: 1px solid var(--border-light);
}

.btn-secondary:hover {
  background: var(--border-light);
  color: var(--text-primary);
}

/* ========================================
   DATA TABLE
   ======================================== */
.table-wrapper {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  padding: 14px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-light);
}

.data-table td {
  padding: 14px 16px;
  font-size: 13px;
  border-bottom: 1px solid var(--border-light);
}

.table-row {
  transition: background 0.15s ease;
}

.table-row:hover {
  background: rgba(13, 148, 136, 0.03);
}

.row-index {
  color: var(--text-muted);
  font-weight: 500;
}

.row-title {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.title-text {
  font-weight: 500;
  color: var(--text-primary);
}

.title-category {
  font-size: 11px;
  color: var(--text-muted);
}

.row-content {
  color: var(--text-secondary);
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.row-time {
  color: var(--text-secondary);
  font-size: 12px;
}

/* Badges */
.type-badge,
.priority-badge,
.status-badge,
.target-badge,
.category-tag {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 500;
}

.type-badge.type-NOTICE {
  background: rgba(99, 102, 241, 0.1);
  color: var(--info);
}

.type-badge.type-ANNOUNCEMENT {
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent);
}

.priority-badge.priority-low {
  background: rgba(100, 116, 139, 0.1);
  color: var(--text-secondary);
}

.priority-badge.priority-medium {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning);
}

.priority-badge.priority-high {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger);
}

.priority-badge.priority-urgent {
  background: rgba(239, 68, 68, 0.15);
  color: var(--danger);
  font-weight: 600;
}

.status-badge.published {
  background: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.status-badge.draft {
  background: rgba(100, 116, 139, 0.1);
  color: var(--text-secondary);
}

.target-badge {
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.category-tag {
  background: rgba(245, 158, 11, 0.1);
  color: var(--accent);
}

/* Action Buttons */
.row-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--bg-tertiary);
  border: none;
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn svg {
  width: 14px;
  height: 14px;
}

.action-btn:hover {
  background: var(--primary);
  color: white;
}

.action-btn.danger:hover {
  background: var(--danger);
}

/* Empty State */
.empty-cell {
  padding: 60px 16px !important;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  color: var(--text-muted);
}

.empty-state svg {
  width: 48px;
  height: 48px;
  opacity: 0.5;
}

/* ========================================
   PAGINATION
   ======================================== */
.pagination-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  border-top: 1px solid var(--border-light);
}

.pagination-info {
  font-size: 13px;
  color: var(--text-secondary);
}

.pagination-info .highlight {
  color: var(--text-primary);
  font-weight: 600;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-light);
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.page-btn svg {
  width: 14px;
  height: 14px;
}

.page-btn:hover:not(:disabled) {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-indicator {
  min-width: 32px;
  text-align: center;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

/* ========================================
   DIALOG
   ======================================== */
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.dialog-panel {
  width: 100%;
  max-width: 560px;
  background: var(--bg-secondary);
  border-radius: 16px;
  box-shadow: var(--shadow-lg);
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-light);
}

.dialog-title {
  margin: 0;
  font-family: 'Noto Serif SC', serif;
  font-size: 18px;
  font-weight: 600;
}

.dialog-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  border-radius: 8px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
}

.dialog-close svg {
  width: 18px;
  height: 18px;
}

.dialog-close:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.dialog-body {
  padding: 24px;
  max-height: 60vh;
  overflow-y: auto;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-light);
}

/* Form */
.form-group {
  margin-bottom: 20px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-primary);
}

.form-label .required {
  color: var(--danger);
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: 10px 12px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-light);
  border-radius: 8px;
  font-size: 13px;
  color: var(--text-primary);
  transition: all 0.2s ease;
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  background: var(--bg-secondary);
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 100px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* Toggle Switch */
.toggle-switch {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.toggle-switch input {
  display: none;
}

.toggle-slider {
  position: relative;
  width: 44px;
  height: 24px;
  background: var(--border-medium);
  border-radius: 12px;
  transition: all 0.2s ease;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}

.toggle-switch input:checked + .toggle-slider {
  background: var(--primary);
}

.toggle-switch input:checked + .toggle-slider::before {
  transform: translateX(20px);
}

.toggle-label {
  font-size: 13px;
  color: var(--text-secondary);
}

/* Loading spinner */
.btn.loading {
  pointer-events: none;
  opacity: 0.7;
}

.spinner {
  width: 16px;
  height: 16px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .notices-admin-page {
    padding: 16px;
  }

  .page-header {
    padding: 24px;
  }

  .page-title {
    font-size: 24px;
  }

  .header-decoration {
    display: none;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .action-bar {
    flex-wrap: wrap;
  }

  .search-wrapper {
    max-width: 100%;
    order: -1;
    flex-basis: 100%;
    margin-bottom: 12px;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .dialog-panel {
    margin: 16px;
    max-height: calc(100vh - 32px);
  }
}
</style>
