import request from '@/utils/request'

/**
 * Recharge API
 */

/**
 * Get recharge records
 * @param {Object} params - Query parameters
 */
export function getRechargeRecords(params) {
  return request({
    url: '/recharges/',
    method: 'get',
    params,
  })
}

/**
 * Simulate recharge (for demo purposes)
 * @param {Object} data - { room_id, amount, payment_method }
 */
export function simulateRecharge(data) {
  return request({
    url: '/recharges/simulate/',
    method: 'post',
    data,
  })
}
