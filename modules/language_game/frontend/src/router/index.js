import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../store/store'

import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Map from '../views/Map.vue'
import Game from '../views/Game.vue'
import Reports from '../views/Reports.vue'
import Leaderboard from '../views/Leaderboard.vue'
import Admin from '../views/Admin.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/', name: 'Dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/map', name: 'Map', component: Map, meta: { requiresAuth: true } },
  { path: '/game/:lessonId', name: 'Game', component: Game, meta: { requiresAuth: true } },
  { path: '/reports', name: 'Reports', component: Reports, meta: { requiresAuth: true } },
  { path: '/leaderboard', name: 'Leaderboard', component: Leaderboard, meta: { requiresAuth: true } },
  { path: '/admin', name: 'Admin', component: Admin, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next('/')
  } else {
    next()
  }
})

export default router
