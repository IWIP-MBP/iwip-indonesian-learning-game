<template>
  <div class="map-container py-4 text-white">
    <div class="text-center mb-5">
      <h1 class="display-title fw-bold text-white mb-2 glow-text-primary">IWIP 学习航线图</h1>
      <p class="text-muted fs-5">完成前面的课程，解锁更多场景！</p>
    </div>

    <!-- Thematic Stages -->
    <div class="stage-section mb-5" v-for="stage in stages" :key="stage.name">
      <div class="stage-header d-flex align-items-center gap-3 mb-4">
        <div class="stage-badge">{{ stage.icon }}</div>
        <div>
          <h3 class="display-title fw-bold mb-0 text-white">{{ stage.name }}</h3>
          <p class="text-muted mb-0 small">{{ stage.desc }}</p>
        </div>
      </div>

      <div class="row g-4">
        <div 
          class="col-12 col-md-6 col-lg-4" 
          v-for="lesson in stage.lessons" 
          :key="lesson.id"
        >
          <div 
            class="lesson-card glass-card h-100 d-flex flex-column justify-content-between position-relative overflow-hidden"
            :class="{ 'locked-card': !lesson.unlocked, 'completed-card': lesson.completed }"
          >
            <!-- Lock Overlay for locked lessons -->
            <div v-if="!lesson.unlocked" class="locked-overlay d-flex flex-column align-items-center justify-content-center">
              <span class="fs-1">🔒</span>
              <span class="small fw-semibold mt-2 text-uppercase tracking-wider">未解锁</span>
            </div>

            <div>
              <div class="d-flex justify-content-between align-items-start mb-3">
                <span class="lesson-number">LESSON {{ lesson.id }}</span>
                <span v-if="lesson.completed" class="badge bg-success rounded-pill px-3 py-1 text-white small">已通关</span>
                <span v-else-if="lesson.unlocked" class="badge bg-primary rounded-pill px-3 py-1 text-white small">可学习</span>
              </div>
              
              <h4 class="text-white fw-bold mb-2">{{ cleanTitle(lesson.title) }}</h4>
              <p class="text-muted small mb-4">章节练习：10道题 | Boss挑战：20道随机题 (80分通关)</p>
            </div>

            <div v-if="lesson.unlocked" class="d-flex gap-2 mt-auto">
              <button 
                class="btn glass-btn flex-grow-1 text-white fw-medium"
                @click="startLesson(lesson.id, 'practice')"
              >
                常规练习
              </button>
              <button 
                class="btn glass-btn glass-btn-primary flex-grow-1 text-white fw-bold"
                @click="startLesson(lesson.id, 'boss')"
              >
                BOSS 战
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const lessons = ref([])

const stages = computed(() => {
  if (lessons.value.length === 0) return []
  
  return [
    {
      name: '发音基础阶段',
      desc: '掌握元音、子音拼读与基本数字发音',
      icon: '🎵',
      lessons: lessons.value.filter(l => l.id <= 8)
    },
    {
      name: '日常沟通阶段',
      desc: '基本构句语法、个人爱好、日期与天气',
      icon: '💬',
      lessons: lessons.value.filter(l => l.id >= 9 && l.id <= 13)
    },
    {
      name: '生活与社交场景',
      desc: '在超市、食堂、宿舍等实际情景中的沟通',
      icon: '🏠',
      lessons: lessons.value.filter(l => l.id >= 14 && l.id <= 17)
    },
    {
      name: '职场与安全生产',
      desc: '工作现场、会议、请假、续签以及核心安全规范',
      icon: '🛡️',
      lessons: lessons.value.filter(l => l.id >= 18)
    }
  ]
})

const fetchLessons = async () => {
  try {
    const response = await axios.get('/api/lessons')
    lessons.value = response.data
  } catch (err) {
    console.error('Failed to load lessons:', err)
  }
}

const cleanTitle = (title) => {
  // Removes Pinyin/English if title is long or formats it nicely
  return title.replace("Pelajaran ke-", "Pelajaran ")
}

const startLesson = (lessonId, mode) => {
  router.push(`/game/${lessonId}?mode=${mode}`)
}

onMounted(() => {
  fetchLessons()
})
</script>

<style scoped>
.stage-badge {
  width: 48px;
  height: 48px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.lesson-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.lesson-number {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 12px;
  color: var(--color-primary);
  letter-spacing: 1px;
}

.locked-card {
  filter: brightness(0.6);
  pointer-events: none;
}

.locked-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(13, 15, 24, 0.6);
  backdrop-filter: blur(4px);
  z-index: 10;
}

.completed-card {
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: inset 0 0 10px rgba(16, 185, 129, 0.1);
}
</style>
