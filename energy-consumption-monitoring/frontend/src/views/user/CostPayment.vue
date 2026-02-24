<template>
  <div class="cost-payment-page">
    <!-- Page Header -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-info">
          <h1 class="page-title">
            <span class="title-icon"><icon-ep-wallet /></span>
            费用与充值
          </h1>
          <p class="page-subtitle">管理您的能源费用，便捷充值</p>
        </div>
        <div class="balance-card">
          <div class="balance-label">账户余额</div>
          <div class="balance-value">
            <span class="balance-currency">¥</span>
            <span class="balance-amount">{{ balance }}</span>
          </div>
          <el-button type="primary" size="small" @click="showRechargeDialog = true">
            <el-icon><icon-ep-plus /></el-icon>
            立即充值
          </el-button>
        </div>
      </div>
      <div class="header-coins">
        <div class="coin coin-1">💰</div>
        <div class="coin coin-2">💵</div>
        <div class="coin coin-3">💳</div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="quick-stats">
      <div v-for="(stat, index) in quickStats" :key="index" class="stat-item">
        <div class="stat-icon" :style="{ background: stat.color + '15', color: stat.color }">
          <component :is="stat.icon" />
        </div>
        <div class="stat-info">
          <span class="stat-label">{{ stat.label }}</span>
          <span class="stat-value">{{ stat.value }}</span>
        </div>
      </div>
    </div>

    <!-- Main Tabs -->
    <div class="tabs-container">
      <el-tabs v-model="activeTab" class="custom-tabs">
        <!-- Bills Tab -->
        <el-tab-pane label="我的账单" name="bills">
          <div class="tab-content">
            <!-- Bills Filter -->
            <div class="content-header">
              <div class="filter-group">
                <el-select v-model="billStatus" placeholder="全部状态" style="width: 140px">
                  <el-option label="全部状态" value="" />
                  <el-option label="未支付" value="unpaid" />
                  <el-option label="已支付" value="paid" />
                </el-select>
                <el-date-picker
                  v-model="billMonth"
                  type="month"
                  placeholder="选择月份"
                  style="width: 160px"
                />
                <el-button type="primary" @click="loadBills">
                  <el-icon><icon-ep-search /></el-icon>
                  查询
                </el-button>
              </div>
              <div class="header-actions">
                <span class="total-amount">
                  应付总额: <strong>¥{{ totalAmount.toFixed(2) }}</strong>
                </span>
                <el-button type="success" :disabled="!hasUnpaidBills" @click="payAllBills">
                  <el-icon><icon-ep-check /></el-icon>
                  一键支付
                </el-button>
              </div>
            </div>

            <!-- Bills List -->
            <div class="bills-grid">
              <div
                v-for="bill in filteredBills"
                :key="bill.id"
                class="bill-card"
                :class="{ 'is-overdue': bill.is_overdue, 'is-paid': bill.status === 'paid' }"
              >
                <div class="bill-header">
                  <div class="bill-period">
                    <el-icon><icon-ep-calendar /></el-icon>
                    {{ bill.period }}
                  </div>
                  <el-tag :type="bill.status === 'paid' ? 'success' : bill.is_overdue ? 'danger' : 'warning'" size="small">
                    {{ bill.status === 'paid' ? '已支付' : bill.is_overdue ? '已逾期' : '未支付' }}
                  </el-tag>
                </div>
                <div class="bill-body">
                  <div class="bill-info">
                    <div class="bill-room">
                      <span class="room-icon"><icon-ep-house /></span>
                      {{ bill.room }}
                    </div>
                    <div class="bill-items">
                      <div v-for="(item, idx) in bill.items" :key="idx" class="bill-item">
                        <span class="item-dot" :style="{ background: item.color }"></span>
                        <span class="item-name">{{ item.name }}</span>
                        <span class="item-usage">{{ item.usage }}</span>
                        <span class="item-cost">¥{{ item.cost.toFixed(2) }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="bill-amount">
                    <span class="amount-label">账单金额</span>
                    <span class="amount-value">¥{{ bill.amount.toFixed(2) }}</span>
                  </div>
                </div>
                <div class="bill-footer">
                  <el-button text type="primary" @click="viewBillDetail(bill)">
                    <el-icon><icon-ep-view /></el-icon>
                    查看详情
                  </el-button>
                  <el-button
                    v-if="bill.status === 'unpaid'"
                    type="primary"
                    @click="payBill(bill)"
                  >
                    <el-icon><icon-ep-wallet /></el-icon>
                    立即支付
                  </el-button>
                </div>
              </div>

              <!-- Empty State -->
              <div v-if="filteredBills.length === 0" class="empty-state">
                <div class="empty-icon"><icon-ep-document /></div>
                <p>暂无账单记录</p>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- Recharge Records Tab -->
        <el-tab-pane label="充值记录" name="recharge">
          <div class="tab-content">
            <div class="content-header">
              <h3 class="section-title">充值历史</h3>
              <el-button type="primary" @click="showRechargeDialog = true">
                <el-icon><icon-ep-plus /></el-icon>
                模拟充值
              </el-button>
            </div>

            <!-- Recharge Table -->
            <div class="table-wrapper">
              <el-table
                :data="rechargeRecords"
                style="width: 100%"
                stripe
                :header-cell-style="{ background: '#fef7f0', color: '#1f2937' }"
              >
                <el-table-column prop="time" label="充值时间" width="180" />
                <el-table-column label="充值方式" width="140">
                  <template #default="{ row }">
                    <div class="payment-method">
                      <span class="method-icon">{{ getPaymentIcon(row.method) }}</span>
                      <span>{{ getPaymentLabel(row.method) }}</span>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column prop="amount" label="充值金额" width="140">
                  <template #default="{ row }">
                    <span class="amount-text income">+¥{{ row.amount.toFixed(2) }}</span>
                  </template>
                </el-table-column>
                <el-table-column prop="room" label="充值房间" />
                <el-table-column label="状态" width="100">
                  <template #default="{ row }">
                    <el-tag :type="row.status === 'success' ? 'success' : 'warning'" size="small">
                      {{ row.status === 'success' ? '成功' : '处理中' }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="order_no" label="订单号" width="200" />
              </el-table>

              <!-- Pagination -->
              <div class="pagination-wrapper">
                <el-pagination
                  v-model:current-page="currentPage"
                  v-model:page-size="pageSize"
                  :page-sizes="[10, 20, 50]"
                  :total="rechargeTotal"
                  layout="total, sizes, prev, pager, next"
                  @size-change="loadRechargeRecords"
                  @current-change="loadRechargeRecords"
                />
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- Calculator Tab -->
        <el-tab-pane label="费用计算器" name="calculator">
          <div class="tab-content calculator-content">
            <div class="calculator-layout">
              <!-- Input Section -->
              <div class="calculator-inputs">
                <h3 class="section-title">
                  <span class="title-icon"><icon-ep-calculator /></span>
                  输入用量
                </h3>

                <div class="input-grid">
                  <div
                    v-for="(energy, index) in energyInputs"
                    :key="index"
                    class="energy-input-card"
                    :style="{ borderColor: energy.color + '40' }"
                  >
                    <div class="input-header" :style="{ background: energy.color + '10' }">
                      <span class="input-dot" :style="{ background: energy.color }"></span>
                      <span class="input-label">{{ energy.label }}</span>
                      <span class="input-unit">({{ energy.unit }})</span>
                    </div>
                    <div class="input-body">
                      <el-input-number
                        v-model="energy.value"
                        :min="0"
                        :max="10000"
                        :precision="2"
                        :controls="false"
                        size="large"
                        class="usage-input"
                        @change="calculateCost"
                      />
                      <div class="rate-info">
                        <span class="rate-label">单价</span>
                        <span class="rate-value">¥{{ energy.rate }}/{{ energy.unit }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Quick Presets -->
                <div class="quick-presets">
                  <span class="presets-label">快捷预设:</span>
                  <el-button
                    v-for="preset in presets"
                    :key="preset.name"
                    size="small"
                    @click="applyPreset(preset)"
                  >
                    {{ preset.name }}
                  </el-button>
                </div>
              </div>

              <!-- Result Section -->
              <div class="calculator-results">
                <div class="result-card">
                  <div class="result-header">
                    <h3>费用估算</h3>
                    <el-button text type="primary" @click="resetCalculator">
                      <el-icon><icon-ep-refresh /></el-icon>
                      重置
                    </el-button>
                  </div>

                  <div class="result-breakdown">
                    <div
                      v-for="(energy, index) in energyInputs"
                      :key="index"
                      class="breakdown-item"
                      :style="{ borderColor: energy.color + '30' }"
                    >
                      <span class="breakdown-dot" :style="{ background: energy.color }"></span>
                      <span class="breakdown-label">{{ energy.label }}</span>
                      <span class="breakdown-usage">{{ energy.value }} {{ energy.unit }}</span>
                      <span class="breakdown-cost">¥{{ (energy.value * energy.rate).toFixed(2) }}</span>
                    </div>
                  </div>

                  <div class="result-total">
                    <div class="total-row">
                      <span class="total-label">预计总费用</span>
                      <span class="total-amount">¥{{ totalCost.toFixed(2) }}</span>
                    </div>
                    <div class="total-tip">
                      <el-icon><icon-ep-info-filled /></el-icon>
                      <span>实际费用以账单为准，仅供参考</span>
                    </div>
                  </div>

                  <!-- Energy Tips -->
                  <div class="energy-tips">
                    <h4>
                      <span class="tips-icon">💡</span>
                      节能建议
                    </h4>
                    <ul>
                      <li v-for="(tip, index) in energyTips" :key="index">
                        {{ tip }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- Recharge Dialog -->
    <el-dialog
      v-model="showRechargeDialog"
      title="账户充值"
      width="450px"
      class="recharge-dialog"
    >
      <div class="recharge-content">
        <div class="current-balance">
          <span class="balance-label">当前余额</span>
          <span class="balance-amount">¥{{ balance }}</span>
        </div>

        <div class="amount-selector">
          <label class="selector-label">选择充值金额</label>
          <div class="preset-amounts">
            <div
              v-for="amount in presetAmounts"
              :key="amount"
              class="amount-preset"
              :class="{ active: rechargeAmount === amount }"
              @click="rechargeAmount = amount"
            >
              ¥{{ amount }}
            </div>
          </div>
          <el-input-number
            v-model="rechargeAmount"
            :min="1"
            :max="10000"
            :precision="0"
            :step="10"
            size="large"
            style="width: 100%; margin-top: 12px"
            placeholder="自定义金额"
          />
        </div>

        <div class="payment-methods">
          <label class="selector-label">支付方式</label>
          <div class="method-options">
            <div
              v-for="method in paymentMethods"
              :key="method.value"
              class="method-option"
              :class="{ active: selectedPaymentMethod === method.value }"
              @click="selectedPaymentMethod = method.value"
            >
              <span class="method-icon">{{ method.icon }}</span>
              <span class="method-label">{{ method.label }}</span>
              <el-icon v-if="selectedPaymentMethod === method.value" class="check-icon">
                <icon-ep-check />
              </el-icon>
            </div>
          </div>
        </div>

        <div class="room-selector">
          <label class="selector-label">充值房间</label>
          <el-select v-model="rechargeRoom" placeholder="选择房间" style="width: 100%">
            <el-option
              v-for="room in boundRooms"
              :key="room.id"
              :label="room.name"
              :value="room.id"
            />
          </el-select>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showRechargeDialog = false">取消</el-button>
          <el-button type="primary" :loading="recharging" @click="handleRecharge">
            <el-icon><icon-ep-wallet /></el-icon>
            确认充值 ¥{{ rechargeAmount }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- Bill Detail Dialog -->
    <el-dialog
      v-model="showBillDetail"
      :title="`账单详情 - ${selectedBill?.period}`"
      width="500px"
      class="bill-detail-dialog"
    >
      <div v-if="selectedBill" class="bill-detail-content">
        <div class="detail-section">
          <h4>基本信息</h4>
          <div class="detail-row">
            <span class="row-label">账单周期</span>
            <span class="row-value">{{ selectedBill.period }}</span>
          </div>
          <div class="detail-row">
            <span class="row-label">房间号</span>
            <span class="row-value">{{ selectedBill.room }}</span>
          </div>
          <div class="detail-row">
            <span class="row-label">账单状态</span>
            <el-tag :type="selectedBill.status === 'paid' ? 'success' : 'warning'" size="small">
              {{ selectedBill.status === 'paid' ? '已支付' : '未支付' }}
            </el-tag>
          </div>
        </div>

        <div class="detail-section">
          <h4>费用明细</h4>
          <div class="detail-items">
            <div v-for="(item, index) in selectedBill.items" :key="index" class="detail-item">
              <span class="item-dot" :style="{ background: item.color }"></span>
              <span class="item-name">{{ item.name }}</span>
              <span class="item-usage">{{ item.usage }}</span>
              <span class="item-cost">¥{{ item.cost.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <div class="detail-total">
          <span class="total-label">应付总额</span>
          <span class="total-amount">¥{{ selectedBill.amount.toFixed(2) }}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getMyBills } from '@/api/system'
import { getRechargeRecords, simulateRecharge } from '@/api/recharge'
import { getMyBindRooms } from '@/api/profile'

// Data
const activeTab = ref('bills')
// TODO: 用户余额目前是静态数据，需要后端提供余额管理 API
// 后端需要在 UserProfile 模型中添加 balance 字段，并提供:
// - GET /api/profile/balance/ - 获取余额
// - POST /api/recharges/ - 充值接口（已存在）
const balance = ref('358.60')
const billStatus = ref('')
const billMonth = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const rechargeTotal = ref(0)

// Bills data
const bills = ref([])
const rechargeRecords = ref([])
const boundRooms = ref([])

// Quick stats - 部分数据从 API 计算，部分需要后端支持
const quickStats = ref([
  {
    label: '本月费用',
    value: '¥0', // Will be calculated from bills
    icon: 'icon-ep-wallet',
    color: '#f97316',
  },
  {
    label: '未支付账单',
    value: '0', // Will be calculated from bills
    icon: 'icon-ep-document',
    color: '#eab308',
  },
  {
    label: '累计充值',
    value: '¥0', // Will be calculated from recharge records
    icon: 'icon-ep-coin',
    color: '#22c55e',
  },
  {
    label: '节能奖励',
    value: '¥0', // TODO: 需要后端提供节能奖励 API
    icon: 'icon-ep-medal',
    color: '#3b82f6',
  },
])
const quickStats = ref([
  {
    label: '本月费用',
    value: '¥186.50',
    icon: 'icon-ep-wallet',
    color: '#f97316',
  },
  {
    label: '未支付账单',
    value: '2',
    icon: 'icon-ep-document',
    color: '#eab308',
  },
  {
    label: '累计充值',
    value: '¥1,200',
    icon: 'icon-ep-coin',
    color: '#22c55e',
  },
  {
    label: '节能奖励',
    value: '¥25',
    icon: 'icon-ep-medal',
    color: '#3b82f6',
  },
])

// Calculator
const energyInputs = ref([
  { label: '电', value: 150, unit: 'kWh', rate: 0.52, color: '#eab308' },
  { label: '水', value: 8, unit: 'm³', rate: 3.5, color: '#3b82f6' },
  { label: '气', value: 3, unit: 'm³', rate: 2.8, color: '#ef4444' },
])

const presets = [
  { name: '单人月均', values: [120, 6, 2] },
  { name: '双人月均', values: [200, 10, 4] },
  { name: '高用量', values: [350, 20, 8] },
]

// Recharge
const showRechargeDialog = ref(false)
const rechargeAmount = ref(50)
const rechargeRoom = ref(null)
const selectedPaymentMethod = ref('wechat')
const recharging = ref(false)

const presetAmounts = [10, 20, 50, 100, 200, 500]

const paymentMethods = [
  { label: '微信支付', value: 'wechat', icon: '💚' },
  { label: '支付宝', value: 'alipay', icon: '💙' },
  { label: '银行卡', value: 'card', icon: '💳' },
]

// Bill detail
const showBillDetail = ref(false)
const selectedBill = ref(null)

// Computed
const filteredBills = computed(() => {
  let result = bills.value
  if (billStatus.value) {
    result = result.filter(b => b.status === billStatus.value)
  }
  return result
})

const totalAmount = computed(() => {
  return filteredBills.value
    .filter(b => b.status === 'unpaid')
    .reduce((sum, b) => sum + b.amount, 0)
})

const hasUnpaidBills = computed(() => {
  return filteredBills.value.some(b => b.status === 'unpaid')
})

const totalCost = computed(() => {
  return energyInputs.value.reduce((sum, item) => {
    return sum + (item.value || 0) * item.rate
  }, 0)
})

const energyTips = computed(() => {
  const tips = []
  const electricity = energyInputs.value[0].value
  const water = energyInputs.value[1].value

  if (electricity > 200) {
    tips.push('您的用电量偏高，建议使用节能电器和LED灯')
  }
  if (water > 10) {
    tips.push('您的用水量较高，注意节约用水，及时关闭水龙头')
  }
  if (tips.length === 0) {
    tips.push('您的能耗处于合理范围，继续保持！')
  }
  return tips
})

// Load bills
async function loadBills() {
  try {
    const response = await getMyBills()
    if (response.code === 0 && response.data) {
      bills.value = response.data.map(bill => ({
        id: bill.id,
        period: bill.bill_period || '2024-01',
        room: bill.room_name || '301宿舍',
        amount: bill.amount || 0,
        status: bill.status || 'unpaid',
        is_overdue: new Date(bill.due_date) < new Date() && bill.status !== 'paid',
        items: [
          { name: '电', usage: `${(bill.amount * 0.6 / 0.52).toFixed(1)} kWh`, cost: bill.amount * 0.6, color: '#eab308' },
          { name: '水', usage: `${(bill.amount * 0.25 / 3.5).toFixed(1)} m³`, cost: bill.amount * 0.25, color: '#3b82f6' },
          { name: '气', usage: `${(bill.amount * 0.15 / 2.8).toFixed(1)} m³`, cost: bill.amount * 0.15, color: '#ef4444' },
        ],
      }))
    }
  } catch (error) {
    console.error('Failed to load bills:', error)
    // Mock data
    bills.value = [
      {
        id: 1,
        period: '2024-01',
        room: '301宿舍',
        amount: 186.50,
        status: 'unpaid',
        is_overdue: false,
        items: [
          { name: '电', usage: '215.2 kWh', cost: 111.90, color: '#eab308' },
          { name: '水', usage: '13.3 m³', cost: 46.55, color: '#3b82f6' },
          { name: '气', usage: '10.0 m³', cost: 28.05, color: '#ef4444' },
        ],
      },
      {
        id: 2,
        period: '2023-12',
        room: '301宿舍',
        amount: 165.80,
        status: 'paid',
        is_overdue: false,
        items: [
          { name: '电', usage: '192.5 kWh', cost: 100.10, color: '#eab308' },
          { name: '水', usage: '11.5 m³', cost: 40.25, color: '#3b82f6' },
          { name: '气', usage: '9.0 m³', cost: 25.45, color: '#ef4444' },
        ],
      },
    ]
  }
}

// Load recharge records
async function loadRechargeRecords() {
  try {
    const response = await getRechargeRecords({
      page: currentPage.value,
      page_size: pageSize.value,
    })
    if (response.code === 0 && response.data) {
      rechargeRecords.value = response.data.map(record => ({
        time: record.recharge_time || new Date().toISOString(),
        method: record.payment_method || 'wechat',
        amount: record.amount || 0,
        room: record.room_name || '301宿舍',
        status: record.status || 'success',
        order_no: record.order_no || `RCH${Date.now()}`,
      }))
      rechargeTotal.value = response.total || rechargeRecords.value.length
    }
  } catch (error) {
    console.error('Failed to load recharge records:', error)
    // Mock data
    rechargeRecords.value = [
      {
        time: '2024-01-15 14:32:05',
        method: 'wechat',
        amount: 100,
        room: '301宿舍',
        status: 'success',
        order_no: 'RCH20240115143205',
      },
      {
        time: '2024-01-08 09:15:22',
        method: 'alipay',
        amount: 200,
        room: '301宿舍',
        status: 'success',
        order_no: 'RCH20240108091522',
      },
    ]
    rechargeTotal.value = 2
  }
}

// Load bound rooms
async function loadBoundRooms() {
  try {
    const response = await getMyBindRooms()
    if (response.code === 0 && response.data) {
      boundRooms.value = response.data.map(room => ({
        id: room.id,
        name: room.room_number || `房间${room.id}`,
      }))
      if (boundRooms.value.length > 0 && !rechargeRoom.value) {
        rechargeRoom.value = boundRooms.value[0].id
      }
    }
  } catch (error) {
    console.error('Failed to load rooms:', error)
    boundRooms.value = [
      { id: 1, name: '301宿舍' },
      { id: 2, name: '实验室201' },
    ]
    if (!rechargeRoom.value) {
      rechargeRoom.value = boundRooms.value[0].id
    }
  }
}

// Handle recharge
async function handleRecharge() {
  if (!rechargeRoom.value) {
    ElMessage.warning('请选择充值房间')
    return
  }

  recharging.value = true
  try {
    const response = await simulateRecharge({
      room_id: rechargeRoom.value,
      amount: rechargeAmount.value,
      payment_method: selectedPaymentMethod.value,
    })

    if (response.code === 0) {
      // Update balance
      const currentBalance = parseFloat(balance.value)
      balance.value = (currentBalance + rechargeAmount.value).toFixed(2)

      ElMessage.success(`充值成功！已充值 ¥${rechargeAmount.value}`)
      showRechargeDialog.value = false

      // Reload records
      loadRechargeRecords()
    } else {
      ElMessage.error(response.message || '充值失败，请重试')
    }
  } catch (error) {
    console.error('Recharge failed:', error)
    // Simulate success for demo
    const currentBalance = parseFloat(balance.value)
    balance.value = (currentBalance + rechargeAmount.value).toFixed(2)
    ElMessage.success(`模拟充值成功！已充值 ¥${rechargeAmount.value}`)
    showRechargeDialog.value = false
  } finally {
    recharging.value = false
  }
}

// Pay bill
async function payBill(bill) {
  try {
    await ElMessageBox.confirm(
      `确认支付账单 ¥${bill.amount.toFixed(2)}？`,
      '支付确认',
      {
        confirmButtonText: '确认支付',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    // Simulate payment
    bill.status = 'paid'
    ElMessage.success('支付成功！')

    // Update balance
    const currentBalance = parseFloat(balance.value)
    balance.value = (currentBalance - bill.amount).toFixed(2)
  } catch {
    // User cancelled
  }
}

// Pay all bills
async function payAllBills() {
  const unpaidBills = filteredBills.value.filter(b => b.status === 'unpaid')
  const total = unpaidBills.reduce((sum, b) => sum + b.amount, 0)

  try {
    await ElMessageBox.confirm(
      `确认支付全部未支付账单，共 ¥${total.toFixed(2)}？`,
      '批量支付确认',
      {
        confirmButtonText: '确认支付',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    // Simulate payment
    unpaidBills.forEach(b => b.status = 'paid')
    ElMessage.success(`支付成功！共支付 ¥${total.toFixed(2)}`)

    // Update balance
    const currentBalance = parseFloat(balance.value)
    balance.value = (currentBalance - total).toFixed(2)
  } catch {
    // User cancelled
  }
}

// View bill detail
function viewBillDetail(bill) {
  selectedBill.value = bill
  showBillDetail.value = true
}

// Calculate cost
function calculateCost() {
  // Trigger reactivity
}

// Apply preset
function applyPreset(preset) {
  energyInputs.value.forEach((item, index) => {
    item.value = preset.values[index]
  })
  calculateCost()
}

// Reset calculator
function resetCalculator() {
  energyInputs.value.forEach(item => item.value = 0)
}

// Get payment icon
function getPaymentIcon(method) {
  const icons = {
    wechat: '💚',
    alipay: '💙',
    card: '💳',
  }
  return icons[method] || '💰'
}

// Get payment label
function getPaymentLabel(method) {
  const labels = {
    wechat: '微信支付',
    alipay: '支付宝',
    card: '银行卡',
  }
  return labels[method] || '未知'
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    loadBills(),
    loadRechargeRecords(),
    loadBoundRooms(),
  ])
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;600;700&family=Orbitron:wght@400;500;600;700&display=swap');

.cost-payment-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* ========================================
   PAGE HEADER
   ======================================== */
.page-header {
  position: relative;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  border-radius: 20px;
  padding: 28px 32px;
  color: white;
  overflow: hidden;
}

.header-content {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-info .page-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0 0 8px;
  font-size: 26px;
  font-weight: 700;
  font-family: 'Noto Sans SC', sans-serif;
}

.title-icon {
  display: flex;
  font-size: 24px;
}

.page-subtitle {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

.balance-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 20px 24px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  min-width: 200px;
}

.balance-label {
  font-size: 13px;
  opacity: 0.9;
}

.balance-value {
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.balance-currency {
  font-size: 18px;
  font-weight: 600;
}

.balance-amount {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 32px;
  font-weight: 700;
}

.header-coins {
  position: absolute;
  right: 250px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  gap: 16px;
  opacity: 0.3;
}

.coin {
  font-size: 48px;
  animation: float 3s ease-in-out infinite;
}

.coin-2 { animation-delay: 0.5s; }
.coin-3 { animation-delay: 1s; }

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* ========================================
   QUICK STATS
   ======================================== */
.quick-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  animation: fadeInUp 0.5s ease-out 0.1s both;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
  background: white;
  border-radius: 14px;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  font-size: 20px;
}

.stat-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
  color: #1f2937;
}

/* ========================================
   TABS CONTAINER
   ======================================== */
.tabs-container {
  animation: fadeInUp 0.5s ease-out 0.2s both;
}

.custom-tabs {
  background: white;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.custom-tabs :deep(.el-tabs__header) {
  margin: 0;
  padding: 0 20px;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
}

.custom-tabs :deep(.el-tabs__nav-wrap::after) {
  display: none;
}

.custom-tabs :deep(.el-tabs__item) {
  height: 52px;
  line-height: 52px;
  padding: 0 24px;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  border: none;
}

.custom-tabs :deep(.el-tabs__item.is-active) {
  color: #22c55e;
  background: white;
}

.custom-tabs :deep(.el-tabs__active-bar) {
  background: #22c55e;
  height: 3px;
  border-radius: 2px;
}

.tab-content {
  padding: 24px;
}

/* ========================================
   CONTENT HEADER
   ======================================== */
.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-group {
  display: flex;
  gap: 12px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.total-amount {
  font-size: 14px;
  color: #64748b;
}

.total-amount strong {
  color: #22c55e;
  font-size: 18px;
}

.section-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
}

/* ========================================
   BILLS GRID
   ======================================== */
.bills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
}

.bill-card {
  background: #f9fafb;
  border-radius: 14px;
  border: 2px solid transparent;
  overflow: hidden;
  transition: all 0.3s ease;
}

.bill-card:hover {
  border-color: #22c55e;
  box-shadow: 0 8px 24px rgba(34, 197, 94, 0.15);
}

.bill-card.is-overdue {
  border-color: #ef4444;
  background: linear-gradient(135deg, #fef2f2 0%, #f9fafb 100%);
}

.bill-card.is-paid {
  opacity: 0.7;
}

.bill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.bill-period {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.bill-body {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  gap: 16px;
}

.bill-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.bill-item {
  display: grid;
  grid-template-columns: 8px auto 1fr auto;
  gap: 8px;
  align-items: center;
  font-size: 13px;
}

.item-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.item-name {
  color: #64748b;
}

.item-usage {
  color: #9ca3af;
  font-size: 12px;
}

.item-cost {
  font-weight: 600;
  color: #1f2937;
}

.bill-amount {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: center;
  padding-left: 16px;
  border-left: 1px solid #e5e7eb;
}

.amount-label {
  font-size: 11px;
  color: #64748b;
}

.amount-value {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #22c55e;
}

.bill-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: white;
  border-top: 1px solid #e5e7eb;
}

.bill-room {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #64748b;
  margin-bottom: 8px;
}

.room-icon {
  color: #f97316;
}

/* ========================================
   TABLE
   ======================================== */
.table-wrapper {
  background: #f9fafb;
  border-radius: 12px;
  padding: 16px;
}

.payment-method {
  display: flex;
  align-items: center;
  gap: 8px;
}

.method-icon {
  font-size: 18px;
}

.amount-text {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-weight: 600;
}

.amount-text.income {
  color: #22c55e;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding-top: 16px;
}

/* ========================================
   CALCULATOR
   ======================================== */
.calculator-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 24px;
}

.calculator-inputs {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.energy-input-card {
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.energy-input-card:hover {
  border-color: #22c55e;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.1);
}

.input-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
}

.input-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.input-label {
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}

.input-unit {
  font-size: 11px;
  color: #64748b;
}

.input-body {
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.usage-input {
  width: 100%;
}

.usage-input :deep(.el-input__wrapper) {
  border-radius: 10px;
}

.rate-info {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}

.rate-label {
  color: #64748b;
}

.rate-value {
  font-weight: 600;
  color: #1f2937;
}

.quick-presets {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 12px;
}

.presets-label {
  font-size: 13px;
  font-weight: 500;
  color: #64748b;
}

.calculator-results {
  position: sticky;
  top: 20px;
  height: fit-content;
}

.result-card {
  background: linear-gradient(135deg, #f0fdf4 0%, #fff 100%);
  border-radius: 16px;
  border: 1px solid rgba(34, 197, 94, 0.2);
  padding: 20px;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.08);
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.result-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.result-breakdown {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.breakdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: white;
  border-radius: 10px;
  border: 1px solid transparent;
}

.breakdown-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.breakdown-label {
  flex: 1;
  font-size: 13px;
  color: #64748b;
}

.breakdown-usage {
  font-size: 12px;
  color: #9ca3af;
}

.breakdown-cost {
  font-weight: 600;
  color: #1f2937;
}

.result-total {
  padding: 16px;
  background: rgba(34, 197, 94, 0.1);
  border-radius: 12px;
  margin-bottom: 16px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.total-label {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
}

.total-amount {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #22c55e;
}

.total-tip {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #64748b;
}

.energy-tips {
  padding: 14px;
  background: white;
  border-radius: 10px;
}

.energy-tips h4 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 10px;
  font-size: 13px;
  font-weight: 600;
  color: #1f2937;
}

.tips-icon {
  font-size: 16px;
}

.energy-tips ul {
  margin: 0;
  padding-left: 18px;
  list-style: disc;
}

.energy-tips li {
  font-size: 12px;
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 4px;
}

/* ========================================
   RECHARGE DIALOG
   ======================================== */
.recharge-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.current-balance {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 12px;
}

.balance-label {
  font-size: 14px;
  color: #64748b;
}

.balance-amount {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #22c55e;
}

.amount-selector,
.payment-methods,
.room-selector {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.selector-label {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
}

.preset-amounts {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.amount-preset {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.amount-preset:hover {
  border-color: #22c55e;
  color: #22c55e;
}

.amount-preset.active {
  background: #22c55e;
  border-color: #22c55e;
  color: white;
}

.method-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.method-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 14px 10px;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
}

.method-option:hover {
  border-color: #22c55e;
}

.method-option.active {
  border-color: #22c55e;
  background: rgba(34, 197, 94, 0.05);
}

.method-icon {
  font-size: 28px;
}

.method-label {
  font-size: 12px;
  font-weight: 500;
  color: #64748b;
}

.method-option.active .method-label {
  color: #22c55e;
}

.check-icon {
  position: absolute;
  top: 4px;
  right: 4px;
  color: #22c55e;
  font-size: 14px;
}

/* ========================================
   BILL DETAIL DIALOG
   ======================================== */
.bill-detail-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-section h4 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.row-label {
  color: #64748b;
}

.row-value {
  font-weight: 500;
  color: #1f2937;
}

.detail-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-item {
  display: grid;
  grid-template-columns: 8px auto 1fr auto;
  gap: 10px;
  align-items: center;
  padding: 10px 12px;
  background: #f9fafb;
  border-radius: 8px;
  font-size: 13px;
}

.detail-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 12px;
}

.total-label {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.total-amount {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: #22c55e;
}

/* ========================================
   EMPTY STATE
   ======================================== */
.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: #f9fafb;
  border-radius: 14px;
  border: 2px dashed #e5e7eb;
}

.empty-icon {
  font-size: 48px;
  color: #d1d5db;
  margin-bottom: 12px;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
  color: #64748b;
}

/* ========================================
   ANIMATIONS
   ======================================== */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========================================
   RESPONSIVE
   ======================================== */
@media (max-width: 1200px) {
  .calculator-layout {
    grid-template-columns: 1fr;
  }

  .calculator-results {
    position: static;
  }
}

@media (max-width: 768px) {
  .quick-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .bills-grid {
    grid-template-columns: 1fr;
  }

  .input-grid {
    grid-template-columns: 1fr;
  }

  .content-header {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-group {
    flex-wrap: wrap;
  }

  .header-actions {
    justify-content: space-between;
  }

  .header-content {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .balance-card {
    width: 100%;
  }
}

/* ========================================
   ELEMENT PLUS OVERRIDES
   ======================================== */
:deep(.el-input__wrapper) {
  border-radius: 10px;
}

:deep(.el-select .el-input__wrapper) {
  border-radius: 10px;
}

:deep(.el-button) {
  border-radius: 10px;
}

:deep(.el-dialog) {
  border-radius: 16px;
}

:deep(.el-dialog__header) {
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
}

:deep(.el-dialog__body) {
  padding: 24px;
}

:deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid #f1f5f9;
}
</style>
