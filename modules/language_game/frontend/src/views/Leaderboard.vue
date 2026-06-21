<template>
  <div class="leaderboard-container py-4 text-white">
    <div class="mb-5 text-center">
      <h1 class="display-title fw-bold mb-2 text-white glow-text-primary">印尼语光荣榜</h1>
      <p class="text-muted fs-5">看看谁是今天最顶尖的语言达人！</p>
    </div>

    <!-- Personal Rank Card -->
    <div class="glass-card mb-5 border-primary border-opacity-25 bg-primary bg-opacity-5">
      <div class="row align-items-center text-center text-md-start">
        <div class="col-md-3 d-flex justify-content-center justify-content-md-start mb-3 mb-md-0">
          <div class="rank-circle d-flex flex-column align-items-center justify-content-center">
            <span class="text-muted small">我的名次</span>
            <h2 class="text-white fw-bold mb-0">#{{ personalRank }}</h2>
          </div>
        </div>
        
        <div class="col-md-6 mb-3 mb-md-0">
          <h4 class="text-white fw-bold mb-1">{{ userStore.name }}</h4>
          <p class="text-muted mb-0">{{ userStore.department }} | 工号：{{ userStore.id }}</p>
        </div>
        
        <div class="col-md-3 text-md-end">
          <div class="text-muted small">我的总经验</div>
          <h3 class="text-success fw-bold mb-0">{{ userStore.xp }} XP</h3>
          <span class="text-muted small">当前等级: LV.{{ userStore.level }}</span>
        </div>
      </div>
    </div>

    <!-- Rankings Tabs -->
    <div class="row">
      <!-- Company / Individual Ranks -->
      <div class="col-lg-6 mb-4">
        <div class="glass-card h-100">
          <h4 class="text-white fw-bold mb-4 display-title">🏆 个人积分排行榜 (Top 50)</h4>
          
          <div class="table-responsive">
            <table class="table table-dark table-hover align-middle bg-transparent border-0">
              <thead>
                <tr class="text-muted border-bottom border-light border-opacity-10">
                  <th class="py-3 border-0">排名</th>
                  <th class="py-3 border-0">姓名</th>
                  <th class="py-3 border-0">部门</th>
                  <th class="py-3 border-0 text-end">积分 (XP)</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="emp in companyList" 
                  :key="emp.id"
                  class="border-bottom border-light border-opacity-5"
                  :class="{ 'table-active bg-primary bg-opacity-10': emp.id === userStore.id }"
                >
                  <td class="py-3 border-0 fw-bold">
                    <span v-if="emp.rank === 1">🥇</span>
                    <span v-else-if="emp.rank === 2">🥈</span>
                    <span v-else-if="emp.rank === 3">🥉</span>
                    <span v-else>{{ emp.rank }}</span>
                  </td>
                  <td class="py-3 border-0 text-white fw-medium">{{ emp.name }}</td>
                  <td class="py-3 border-0 text-muted small">{{ emp.department }}</td>
                  <td class="py-3 border-0 text-end text-success fw-bold font-monospace">{{ emp.xp }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Department Ranks -->
      <div class="col-lg-6 mb-4">
        <div class="glass-card h-100">
          <h4 class="text-white fw-bold mb-4 display-title">🏢 部门平均积分榜</h4>
          
          <div class="table-responsive">
            <table class="table table-dark table-hover align-middle bg-transparent border-0">
              <thead>
                <tr class="text-muted border-bottom border-light border-opacity-10">
                  <th class="py-3 border-0">排名</th>
                  <th class="py-3 border-0">部门</th>
                  <th class="py-3 border-0">参训人数</th>
                  <th class="py-3 border-0 text-end">平均积分</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="dept in departmentList" 
                  :key="dept.department"
                  class="border-bottom border-light border-opacity-5"
                  :class="{ 'table-active bg-primary bg-opacity-10': dept.department === userStore.department }"
                >
                  <td class="py-3 border-0 fw-bold">
                    <span v-if="dept.rank === 1">🥇</span>
                    <span v-else-if="dept.rank === 2">🥈</span>
                    <span v-else-if="dept.rank === 3">🥉</span>
                    <span v-else>{{ dept.rank }}</span>
                  </td>
                  <td class="py-3 border-0 text-white fw-medium">{{ dept.department }}</td>
                  <td class="py-3 border-0 text-muted font-monospace">{{ dept.emp_count }} 人</td>
                  <td class="py-3 border-0 text-end text-info fw-bold font-monospace">{{ dept.avg_xp }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../store/store'
import axios from 'axios'

const userStore = useUserStore()

const personalRank = ref(0)
const companyList = ref([])
const departmentList = ref([])

const fetchRankings = async () => {
  try {
    const response = await axios.get('/api/rankings')
    personalRank.value = response.data.personal.rank
    companyList.value = response.data.company
    departmentList.value = response.data.department
  } catch (err) {
    console.error('Failed to load rankings:', err)
  }
}

onMounted(() => {
  fetchRankings()
})
</script>

<style scoped>
.rank-circle {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.table th {
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 0.5px;
}

.table tr {
  transition: background-color 0.2s ease;
}

.table-hover tbody tr:hover {
  background-color: rgba(255, 255, 255, 0.03) !important;
}
</style>
