<template>
  <div class="login-wrapper d-flex align-items-center justify-content-center">
    <div class="col-12 col-md-5 col-lg-4 px-3">
      <div class="text-center mb-5 float-animation">
        <h1 class="display-title glow-text-primary text-white fw-bold">IWIP INDONESIAN</h1>
        <p class="text-muted fs-5 mt-2">印尼语培训考核游戏系统</p>
      </div>

      <div class="glass-card p-4 shadow-lg border border-light border-opacity-10">
        <h3 class="text-white text-center mb-4 display-title fw-semibold">登录系统</h3>
        
        <form @submit.prevent="handleLogin">
          <div class="mb-4">
            <label class="form-label text-light small fw-medium">工号 / EMPLOYEE ID</label>
            <input 
              type="text" 
              class="form-control glass-input" 
              placeholder="请输入您的工号" 
              v-model="employeeId"
              required
            />
          </div>

          <div class="mb-4">
            <label class="form-label text-light small fw-medium">登录密码 / PASSWORD</label>
            <input 
              type="password" 
              class="form-control glass-input" 
              placeholder="请输入密码" 
              v-model="password"
              required
            />
          </div>

          <div v-if="errorMsg" class="alert alert-danger border-0 bg-danger bg-opacity-25 text-danger rounded-3 py-2 px-3 mb-4 small">
            {{ errorMsg }}
          </div>

          <button 
            type="submit" 
            class="btn w-100 glass-btn glass-btn-primary py-3 fw-bold text-white shadow"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            登 录 / SIGN IN
          </button>
        </form>

        <div class="text-center mt-4">
          <span class="text-muted small">系统默认密码为 admin123，若有疑问请咨询管理员。</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/store'
import axios from 'axios'

const userStore = useUserStore()
const router = useRouter()

const employeeId = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)

const handleLogin = async () => {
  loading.value = true
  errorMsg.value = ''
  
  try {
    const response = await axios.post('/api/login', {
      employee_id: employeeId.value,
      password: password.value
    })
    
    // Set user store state
    userStore.setLogin(response.data)
    
    // Redirect to home dashboard
    router.push('/')
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      errorMsg.value = err.response.data.message
    } else {
      errorMsg.value = '登录服务不可用，请联系管理员'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrapper {
  min-height: 80vh;
}
</style>
