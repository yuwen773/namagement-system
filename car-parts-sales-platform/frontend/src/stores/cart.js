import { defineStore } from 'pinia'
import { getCartApi, addCartItemApi, updateCartItemApi, deleteCartItemApi } from '@/api/modules/cart'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
    isLoading: false,
    totalQuantity: 0,
    totalPrice: 0
  }),

  getters: {
    // 选中的商品
    selectedItems: (state) => state.items.filter(item => item.selected),
    // 选中商品总数量
    selectedQuantity: (state) => state.items.filter(item => item.selected).reduce((sum, item) => sum + item.quantity, 0),
    // 选中商品总价
    selectedPrice: (state) => state.items.filter(item => item.selected).reduce((sum, item) => sum + item.price * item.quantity, 0)
  },

  actions: {
    // 获取购物车
    async fetchCart() {
      this.isLoading = true
      try {
        const data = await getCartApi()
        this.items = data.items || []
        this.totalQuantity = data.total_items || 0
        this.totalPrice = data.total_price || 0
      } finally {
        this.isLoading = false
      }
    },

    // 添加商品到购物车
    async addItem(productId, quantity = 1) {
      try {
        await addCartItemApi({ product_id: productId, quantity })
        await this.fetchCart()
      } catch (error) {
        throw error
      }
    },

    // 更新商品数量
    async updateQuantity(itemId, quantity) {
      try {
        await updateCartItemApi(itemId, { quantity })
        await this.fetchCart()
      } catch (error) {
        throw error
      }
    },

    // 删除商品
    async removeItem(itemId) {
      try {
        await deleteCartItemApi(itemId)
        await this.fetchCart()
      } catch (error) {
        throw error
      }
    },

    // 切换选中状态
    toggleSelect(itemId) {
      const item = this.items.find(i => i.id === itemId)
      if (item) {
        item.selected = !item.selected
      }
    },

    // 全选/取消全选
    toggleSelectAll(selected) {
      this.items.forEach(item => {
        item.selected = selected
      })
    },

    // 清空购物车
    clearCart() {
      this.items = []
      this.totalQuantity = 0
      this.totalPrice = 0
    }
  }
})
