import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    id: localStorage.getItem('employee_id') || '',
    name: localStorage.getItem('employee_name') || '',
    department: localStorage.getItem('employee_department') || '',
    role: localStorage.getItem('employee_role') || 'employee',
    xp: parseInt(localStorage.getItem('employee_xp') || '0'),
    level: parseInt(localStorage.getItem('employee_level') || '1')
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.role === 'admin',
    authHeader: (state) => state.token ? `Bearer ${state.token}` : ''
  },
  actions: {
    setLogin(userData) {
      this.token = userData.token
      this.id = userData.id
      this.name = userData.name
      this.department = userData.department
      this.role = userData.role
      this.xp = userData.xp || 0
      this.level = userData.level || 1

      localStorage.setItem('token', this.token)
      localStorage.setItem('employee_id', this.id)
      localStorage.setItem('employee_name', this.name)
      localStorage.setItem('employee_department', this.department)
      localStorage.setItem('employee_role', this.role)
      localStorage.setItem('employee_xp', this.xp)
      localStorage.setItem('employee_level', this.level)
      
      // Configure default axios header
      axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
    },
    updateProfile(xp, level) {
      this.xp = xp
      this.level = level
      localStorage.setItem('employee_xp', this.xp)
      localStorage.setItem('employee_level', this.level)
    },
    logout() {
      this.token = ''
      this.id = ''
      this.name = ''
      this.department = ''
      this.role = 'employee'
      this.xp = 0
      this.level = 1

      localStorage.removeItem('token')
      localStorage.removeItem('employee_id')
      localStorage.removeItem('employee_name')
      localStorage.removeItem('employee_department')
      localStorage.removeItem('employee_role')
      localStorage.removeItem('employee_xp')
      localStorage.removeItem('employee_level')
      
      delete axios.defaults.headers.common['Authorization']
    }
  }
})
