<template>
  <div class="app-container">
    <!-- Navbar (Hidden on Login screen) -->
    <nav v-if="userStore.isLoggedIn" class="navbar navbar-expand-lg navbar-dark glass-navbar py-3">
      <div class="container">
        <router-link class="navbar-brand display-title fw-bold text-white fs-4 glow-text-primary" to="/">
          IWIP INDONESIAN
        </router-link>
        
        <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0 ms-lg-4 gap-2">
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded text-light" active-class="active-nav-link" to="/map">
                学习地图
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded text-light" active-class="active-nav-link" to="/reports">
                分析报表
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link px-3 rounded text-light" active-class="active-nav-link" to="/leaderboard">
                排行榜
              </router-link>
            </li>
            <li class="nav-item" v-if="userStore.isAdmin">
              <router-link class="nav-link px-3 rounded text-light" active-class="active-nav-link" to="/admin">
                管理中心
              </router-link>
            </li>
          </ul>
          
          <div class="d-flex align-items-center gap-3">
            <div class="text-end d-none d-lg-block">
              <span class="d-block text-white fw-medium">{{ userStore.name }}</span>
              <span class="d-block text-muted small">{{ userStore.department }} | LV.{{ userStore.level }}</span>
            </div>
            
            <router-link to="/" class="avatar-link">
              <div class="user-avatar">
                {{ userStore.name.charAt(0) }}
              </div>
            </router-link>
            
            <button class="btn btn-outline-danger btn-sm border-0 rounded-circle" @click="handleLogout" title="退出登录">
              <i class="bi bi-box-arrow-right">退出</i>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main View Routing Area -->
    <main class="container py-4">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup>
import { useUserStore } from './store/store'
import { useRouter } from 'vue-router'
import axios from 'axios'

const userStore = useUserStore()
const router = useRouter()

// Initialize auth headers if token exists on load
if (userStore.token) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${userStore.token}`
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.active-nav-link {
  background: rgba(255, 255, 255, 0.1);
  color: #fff !important;
  font-weight: 600;
  box-shadow: inset 0 0 4px rgba(255, 255, 255, 0.2);
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-weight: bold;
  font-family: 'Outfit', sans-serif;
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 10px rgba(99, 102, 241, 0.4);
}

.avatar-link {
  text-decoration: none;
}
</style>
