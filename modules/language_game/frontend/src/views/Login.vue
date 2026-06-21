<template>
  <div class="login-wrapper d-flex align-items-center justify-content-center py-5">
    <div class="container px-4">
      <div class="row align-items-stretch g-4 justify-content-center">
        <!-- Application Introduction & Developer Metadata -->
        <div class="col-12 col-md-6 col-lg-6 d-flex">
          <div class="glass-card p-4 p-lg-5 w-100 shadow-lg border border-light border-opacity-10 d-flex flex-column justify-content-between text-start">
            <div>
              <div class="float-animation mb-4">
                <h1 class="display-title glow-text-primary text-white fw-bold mb-1">IWIP INDONESIAN</h1>
                <p class="text-muted fs-5 mt-1">印尼语培训考核游戏系统</p>
              </div>
              
              <div class="intro-section mb-4">
                <h5 class="text-white fw-bold mb-2">💡 系统简介</h5>
                <p class="text-light-muted small lh-lg">
                  本系统紧密结合印尼语教材，打造以游戏化闯关为核心的培训考核模式。涵盖日常对话、安全环保、办公生产等 21 个核心课程章节，动态合成超过 3000 道多样化趣味题库，赋能员工高效掌握印尼语常用交流。
                </p>
              </div>

              <div class="info-section mb-4">
                <h5 class="text-white fw-bold mb-3">🛠️ 系统开发与版本信息</h5>
                <div class="row g-2">
                  <div class="col-6">
                    <div class="p-2 px-3 rounded bg-white bg-opacity-5 border border-light border-opacity-5">
                      <span class="text-muted d-block small">开发人</span>
                      <strong class="text-info">张金刚</strong>
                    </div>
                  </div>
                  <div class="col-6">
                    <div class="p-2 px-3 rounded bg-white bg-opacity-5 border border-light border-opacity-5">
                      <span class="text-muted d-block small">当前版本</span>
                      <strong class="text-success">v1.2.0 (Premium)</strong>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="changelog-section mt-3">
              <h6 class="text-white fw-bold mb-2">📋 v1.2.0 修订内容：</h6>
              <ul class="text-light-muted small ps-3 mb-0 lh-lg">
                <li>🎵 <strong>答题声效反馈</strong>：集成清脆风铃（答对）与警告音效（答错）。</li>
                <li>📥 <strong>动态模板导入</strong>：支持在后台下载 Excel 导入模板，智能创建解析。</li>
                <li>⚙️ <strong>无部门预设管理</strong>：去除硬编码初始部门，支持导入时动态自动生成。</li>
                <li>🔑 <strong>系统播种优化</strong>：修正默认管理员账号加密验证，确保稳定登录。</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Login Panel -->
        <div class="col-12 col-md-6 col-lg-5 d-flex align-items-center">
          <div class="glass-card p-4 p-lg-5 w-100 shadow-lg border border-light border-opacity-10">
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
              <span class="text-muted small">系统默认管理员账号为：admin / admin123</span>
            </div>
          </div>
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
.text-light-muted {
  color: rgba(255, 255, 255, 0.7);
}
</style>
