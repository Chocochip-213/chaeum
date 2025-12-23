import api from '@/api'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    isAuthenticated: false,
  }),

  getters: {
    nickname: (state) => (state.userInfo ? state.userInfo.nickname : ''),
    email: (state) => (state.userInfo ? state.userInfo.email : ''),
    id: (state) => (state.userInfo ? state.userInfo.id : ''),
  },

  actions: {
    async fetchUserProfile() {
      try {
        const response = await api.get('/users/profile/')

        this.userInfo = response.data
        this.isAuthenticated = true
      } catch (error) {
        console.error('유저 정보 조회 실패:', error)
        this.userInfo = null
        this.isAuthenticated = false
      }
    },

    clearUser() {
      this.userInfo = null
      this.isAuthenticated = false
    },
  },
})
