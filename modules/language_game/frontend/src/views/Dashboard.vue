<template>
  <div class="dashboard-container py-4">
    <!-- Header Section -->
    <div class="row mb-5 align-items-center">
      <div class="col-lg-8">
        <h1 class="display-title text-white fw-bold mb-2">Selamat Datang, {{ userStore.name }}!</h1>
        <p class="text-muted fs-5">今天是您在 IWIP 平台精进印尼语的又一天。继续努力，冲击更高的水平！</p>
      </div>
      <div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
        <router-link to="/map" class="btn glass-btn glass-btn-primary py-3 px-5 fw-bold shadow">
          进入学习地图
        </router-link>
      </div>
    </div>

    <!-- Status & Stat Cards -->
    <div class="row g-4 mb-5">
      <!-- Profile Card -->
      <div class="col-lg-4">
        <div class="glass-card h-100 d-flex flex-column justify-content-between">
          <div class="d-flex align-items-center gap-4 mb-4">
            <div class="avatar-large">{{ userStore.name.charAt(0) }}</div>
            <div>
              <h4 class="text-white fw-bold mb-1">{{ userStore.name }}</h4>
              <p class="text-muted mb-0 small">{{ userStore.department }} | 工号: {{ userStore.id }}</p>
            </div>
          </div>
          
          <div class="level-progress-box">
            <div class="d-flex justify-content-between text-white fw-medium mb-2">
              <span>游戏等级: LV.{{ userStore.level }}</span>
              <span>{{ userStore.xp % 100 }} / 100 XP</span>
            </div>
            <div class="progress-bar-container">
              <div class="progress-fill" :style="{ width: (userStore.xp % 100) + '%' }"></div>
            </div>
            <div class="text-muted small mt-2">总获取经验: {{ userStore.xp }} XP</div>
          </div>
        </div>
      </div>

      <!-- Capability Summary Card -->
      <div class="col-lg-4">
        <div class="glass-card h-100 d-flex flex-column justify-content-between">
          <h5 class="text-white fw-bold mb-4">当前语言水平</h5>
          <div class="d-flex align-items-center justify-content-center py-3">
            <div class="language-level-badge glow-text-primary">{{ levelCode }}</div>
          </div>
          <div class="text-center mt-3">
            <p class="text-muted small mb-0">系统将依据您在各章节练习中的正确率自动更新该评级。</p>
          </div>
        </div>
      </div>

      <!-- Practice Statistics Card -->
      <div class="col-lg-4">
        <div class="glass-card h-100 d-flex flex-column justify-content-between">
          <h5 class="text-white fw-bold mb-3">错题及复习</h5>
          <div class="stats-box mb-4">
            <div class="d-flex justify-content-between align-items-center py-2 border-bottom border-light border-opacity-10">
              <span class="text-muted">当前错题本数量</span>
              <span class="badge bg-danger rounded-pill fs-6">{{ wrongQuestionsCount }}</span>
            </div>
            <div class="d-flex justify-content-between align-items-center py-2">
              <span class="text-muted">已获勋章数</span>
              <span class="badge bg-warning text-dark rounded-pill fs-6">{{ earnedBadges.length }} / 7</span>
            </div>
          </div>
          
          <button 
            class="btn glass-btn w-100 py-3 text-white fw-semibold border-danger border-opacity-20 hover-bg-danger"
            @click="handleWrongPractice"
            :disabled="wrongQuestionsCount === 0"
          >
            错题专项强化训练
          </button>
        </div>
      </div>
    </div>

    <!-- Badges Showcase Section -->
    <div class="row">
      <div class="col-12">
        <div class="glass-card">
          <h4 class="text-white display-title fw-semibold mb-4">我的荣誉勋章</h4>
          
          <div v-if="earnedBadges.length === 0" class="text-center py-5">
            <p class="text-muted">您目前还没有获得勋章，快去挑战课程地图吧！</p>
          </div>
          
          <div v-else class="row g-4 justify-content-start">
            <div 
              class="col-6 col-sm-4 col-md-3 col-lg-2 text-center" 
              v-for="badge in earnedBadges" 
              :key="badge.id"
            >
              <div class="badge-item p-3 rounded-4 glass-panel border border-light border-opacity-10 d-flex flex-column align-items-center">
                <div class="badge-icon-box mb-3">
                  🥇
                </div>
                <h6 class="text-white fw-semibold mb-1">{{ badge.badge_details.name }}</h6>
                <p class="text-muted mb-0 small text-center">{{ badge.badge_details.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/store'
import axios from 'axios'

const userStore = useUserStore()
const router = useRouter()

const wrongQuestionsCount = ref(0)
const levelCode = ref('A1')
const earnedBadges = ref([])

const fetchDashboardData = async () => {
  try {
    // 1. Fetch wrong questions
    const wqResponse = await axios.get('/api/wrong-questions')
    wrongQuestionsCount.value = wqResponse.data.length
    
    // 2. Fetch reports (for current language level)
    const repResponse = await axios.get('/api/reports')
    levelCode.value = repResponse.data.radar.level || 'A1'
    
    // 3. Fetch user badges from backend (can query via list reports or profile endpoint)
    // For simplicity, we can fetch from ranking or custom api, let's write a direct query or fetch from profile
    // We can fetch from leaderboard or we simulate/query employee badges
  } catch (err) {
    console.error('Failed to load dashboard metrics:', err)
  }
}

// In the database seeding or API we also link badges
// Let's create a custom action to query employee badges or use list
const fetchBadges = async () => {
  try {
    // We can query wrong questions or use rankings API.
    // Let's request ranking which has employee details, or admin employees list.
    // To make it simple, let's query the wrong-questions to see if it responds,
    // and for badges we can call rankings or load from local/simulate.
    // Let's fetch ranking API:
    const response = await axios.get('/api/rankings')
    // We can also have an endpoint for user profile if we want.
    // Let's query from rankings and set personal level/xp in store:
    if (response.data && response.data.personal) {
      userStore.updateProfile(response.data.personal.xp, response.data.personal.level)
    }
    
    // Fetch employee's specific badges list (we can get it or seed some placeholder list based on XP)
    // To make it robust, we'll simulate loading if database query failed, or fetch it.
    // Let's call /api/wrong-questions, we can mock badges if not implemented or write a quick get endpoint.
    // Since we created models and schemas for employee_badges, let's fetch badges in game or report.
    // We can let report endpoint return badges! Yes, that is very clean!
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  fetchDashboardData()
  fetchBadges()
})

const handleWrongPractice = () => {
  // Direct to custom practice session utilizing wrong questions
  router.push('/game/1?mode=wrong_practice')
}
</script>

<style scoped>
.avatar-large {
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 32px;
  font-weight: bold;
  font-family: 'Outfit', sans-serif;
  border: 3px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.5);
}

.progress-bar-container {
  width: 100%;
  height: 10px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #a855f7);
  box-shadow: 0 0 8px rgba(99, 102, 241, 0.6);
  border-radius: 5px;
  transition: width 0.5s ease;
}

.language-level-badge {
  font-size: 80px;
  font-weight: 900;
  font-family: 'Outfit', sans-serif;
  color: #fff;
  background: linear-gradient(135deg, #6366f1, #06b6d4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 4px 10px rgba(99, 102, 241, 0.3));
}

.badge-icon-box {
  font-size: 36px;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
}

.badge-item {
  transition: transform 0.2s ease;
}
.badge-item:hover {
  transform: scale(1.05);
  border-color: rgba(255, 255, 255, 0.25) !important;
}

.hover-bg-danger:hover {
  background: rgba(239, 68, 68, 0.15) !important;
  border-color: var(--color-danger) !important;
}
</style>
