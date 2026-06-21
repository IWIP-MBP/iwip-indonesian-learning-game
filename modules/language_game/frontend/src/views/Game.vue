<template>
  <div class="game-wrapper d-flex justify-content-center align-items-center py-4">
    <div class="col-12 col-lg-8 px-3">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary fs-3" role="status"></div>
        <p class="text-muted mt-3">正在为您准备题库...</p>
      </div>

      <!-- End Game Screen -->
      <div v-else-if="gameOver" class="glass-card p-5 text-center shadow-lg border border-light border-opacity-10 animate-fade-in">
        <span class="emoji-large mb-3 d-inline-block">{{ accuracy >= 0.8 ? '🎉' : '💪' }}</span>
        <h2 class="display-title text-white fw-bold mb-3">
          {{ mode === 'boss' ? 'BOSS 挑战结束' : '练习完成' }}
        </h2>
        
        <p class="text-muted fs-5 mb-5">
          {{ accuracy >= 0.8 ? '恭喜您成功通关！分数已记入KPI系统。' : '未达到80分通关线，别灰心，再练一次吧！' }}
        </p>

        <div class="row g-4 mb-5 justify-content-center">
          <div class="col-6 col-sm-3">
            <div class="metric-card p-3 rounded-4 glass-panel border border-light border-opacity-10">
              <span class="d-block text-muted small">最终得分</span>
              <h3 class="text-white fw-bold mt-1 mb-0">{{ Math.round(accuracy * 100) }} 分</h3>
            </div>
          </div>
          <div class="col-6 col-sm-3">
            <div class="metric-card p-3 rounded-4 glass-panel border border-light border-opacity-10">
              <span class="d-block text-muted small">获取经验</span>
              <h3 class="text-success fw-bold mt-1 mb-0">+{{ xpGained }} XP</h3>
            </div>
          </div>
          <div class="col-6 col-sm-3">
            <div class="metric-card p-3 rounded-4 glass-panel border border-light border-opacity-10">
              <span class="d-block text-muted small">最高连击</span>
              <h3 class="text-warning fw-bold mt-1 mb-0">{{ maxCombo }} Combo</h3>
            </div>
          </div>
        </div>

        <!-- Earned Badges Alert -->
        <div v-if="earnedBadges.length > 0" class="badge-alert-box mb-5 p-4 rounded-4 border border-warning border-opacity-25 bg-warning bg-opacity-10 animate-bounce">
          <h5 class="text-warning fw-bold mb-3">🏆 恭喜您荣获新勋章！</h5>
          <div class="d-flex justify-content-center gap-4 flex-wrap">
            <div class="badge-tag px-3 py-2 rounded-pill bg-dark text-white fw-semibold" v-for="b in earnedBadges" :key="b.id">
              🥇 {{ b.name }}
            </div>
          </div>
        </div>

        <!-- Wrong Answers Review List -->
        <div v-if="sessionWrongAnswers.length > 0" class="text-start mb-5">
          <h4 class="text-white fw-bold mb-3 display-title">错题回顾与解析</h4>
          <div class="d-flex flex-column gap-3">
            <div class="p-3 rounded-3 glass-panel border border-danger border-opacity-10" v-for="(wq, index) in sessionWrongAnswers" :key="index">
              <div class="text-danger fw-semibold small mb-1">题目 {{ index + 1 }} | {{ wq.type_text }}</div>
              <div class="text-white mb-2" v-html="wq.content"></div>
              <div class="text-success small fw-medium">正确答案：{{ wq.correct_answer }}</div>
              <div class="text-muted small mt-2">解析：{{ wq.explanation }}</div>
            </div>
          </div>
        </div>

        <div class="d-flex gap-3 justify-content-center">
          <button class="btn glass-btn py-3 px-5 text-white fw-semibold" @click="goBack">返回地图</button>
          <button class="btn glass-btn glass-btn-primary py-3 px-5 text-white fw-bold shadow" @click="restartGame">再来一次</button>
        </div>
      </div>

      <!-- Active Game / Quiz Screen -->
      <div v-else class="glass-card p-4 shadow-lg position-relative border border-light border-opacity-10">
        <!-- Top Status Bar -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <button class="btn btn-sm btn-outline-light border-0 text-muted" @click="quitGame">✕ 退出</button>
          
          <div class="progress-bar-wrapper flex-grow-1 mx-4">
            <div class="progress-bar-bg">
              <div class="progress-bar-fill" :style="{ width: ((currentIndex + 1) / questions.length * 100) + '%' }"></div>
            </div>
          </div>
          
          <span class="text-white small fw-bold font-monospace">{{ currentIndex + 1 }} / {{ questions.length }}</span>
        </div>

        <!-- Game Info & Combo -->
        <div class="d-flex justify-content-between align-items-center mb-4 px-2">
          <div class="text-muted small">
            模式：<span class="text-white fw-semibold">{{ modeText }}</span>
          </div>
          
          <!-- Combo Counter -->
          <div v-if="combo > 0" class="combo-badge float-animation">
            x{{ combo }}
          </div>
        </div>

        <!-- Question Panel -->
        <div class="question-container py-4 mb-4 text-center">
          <!-- Audio TTS player for Audio Quiz -->
          <div v-if="currentQuestion.type === 'audio'" class="audio-quiz-box mb-4">
            <div class="d-flex flex-column align-items-center">
              <button class="play-btn mb-3" @click="speakCurrentWord" title="播放发音">
                🔊
              </button>
              
              <!-- Voice Gender Selector -->
              <div class="d-flex gap-2 justify-content-center mt-2 glass-panel p-2 rounded-pill border border-light border-opacity-10">
                <button 
                  type="button" 
                  class="btn btn-sm px-3 rounded-pill text-white border-0"
                  :class="ttsGender === 'female' ? 'bg-primary' : 'bg-transparent'"
                  @click="ttsGender = 'female'"
                >
                  👩‍🦰 女声
                </button>
                <button 
                  type="button" 
                  class="btn btn-sm px-3 rounded-pill text-white border-0"
                  :class="ttsGender === 'male' ? 'bg-primary' : 'bg-transparent'"
                  @click="ttsGender = 'male'"
                >
                  👨‍🦱 男声
                </button>
              </div>
            </div>
          </div>

          <!-- Picture Question Image Display -->
          <div v-if="currentQuestion.type === 'picture'" class="picture-quiz-box mb-4">
            <div class="img-frame rounded-4 border border-light border-opacity-10 mx-auto overflow-hidden shadow">
              <!-- We render beautiful clean illustrations using letter or standard icons if img loading fails -->
              <div class="img-fallback d-flex align-items-center justify-content-center fs-1">
                🖼️
              </div>
            </div>
          </div>

          <h3 class="text-white fw-bold lh-base" v-html="currentQuestion.content"></h3>
        </div>

        <!-- Answers / Interactive Widgets -->
        <div class="answers-container">
          <!-- 1. Drag Match (Click-to-match fallback) -->
          <div v-if="currentQuestion.type === 'drag_match'" class="drag-match-wrapper py-3">
            <div class="row g-3">
              <div class="col-6 d-flex flex-column gap-2">
                <button 
                  class="btn glass-btn text-start p-3 w-100 border border-light border-opacity-10 text-white rounded-3 select-box"
                  v-for="word in matchLeft" 
                  :key="word"
                  :class="{ 'match-selected': selectedLeft === word, 'match-done': isMatchCompleted(word, 'left') }"
                  @click="clickLeft(word)"
                >
                  {{ word }}
                </button>
              </div>
              <div class="col-6 d-flex flex-column gap-2">
                <button 
                  class="btn glass-btn text-start p-3 w-100 border border-light border-opacity-10 text-white rounded-3 select-box"
                  v-for="mean in matchRight" 
                  :key="mean"
                  :class="{ 'match-selected': selectedRight === mean, 'match-done': isMatchCompleted(mean, 'right') }"
                  @click="clickRight(mean)"
                >
                  {{ mean }}
                </button>
              </div>
            </div>
            
            <div class="text-center mt-4">
              <button 
                class="btn glass-btn glass-btn-primary px-5 py-3 text-white fw-bold"
                @click="checkMatchAnswer"
                :disabled="matchPairs.length < matchLeft.length"
              >
                提 交 匹 配
              </button>
            </div>
          </div>

          <!-- 2. Choices (For vocab_choice, cn_to_indo, indo_to_cn, audio, picture, fill_blank, dialogue) -->
          <div v-else class="row g-3">
            <div 
              class="col-12 col-md-6" 
              v-for="(opt, oIdx) in currentQuestion.options" 
              :key="oIdx"
            >
              <button 
                class="btn glass-btn text-start p-4 w-100 border border-light border-opacity-10 text-white rounded-4 option-btn"
                :class="getOptionClass(opt)"
                @click="selectOption(opt)"
                :disabled="answered"
              >
                <span class="opt-letter me-3">{{ getLetter(oIdx) }}.</span>
                <span>{{ opt.option_text }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Explanation Modal (Sticky/Slide-up at bottom) -->
        <div v-if="answered" class="explanation-panel mt-4 p-4 rounded-4 animate-slide-up" :class="answeredCorrectly ? 'bg-success bg-opacity-10 border border-success border-opacity-25' : 'bg-danger bg-opacity-10 border border-danger border-opacity-25'">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <h5 class="fw-bold" :class="answeredCorrectly ? 'text-success' : 'text-danger'">
              {{ answeredCorrectly ? '✓ 回答正确！' : '✕ 回答错误' }}
            </h5>
            <span class="text-muted small font-monospace">+{{ currentXpAward }} XP</span>
          </div>
          
          <p class="text-light mb-4 small">{{ currentQuestion.explanation }}</p>
          
          <div class="text-end">
            <button class="btn glass-btn glass-btn-primary px-5 py-3 text-white fw-bold" @click="nextQuestion">
              {{ currentIndex + 1 === questions.length ? '查看结果' : '下一题' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../store/store'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const lessonId = parseInt(route.params.lessonId)
const mode = route.query.mode || 'practice' // 'practice', 'boss', 'wrong_practice'

const loading = ref(true)
const gameOver = ref(false)
const currentIndex = ref(0)
const questions = ref([])

// Stats tracking
const score = ref(0)
const correctCount = ref(0)
const maxCombo = ref(0)
const combo = ref(0)
const xpGained = ref(0)
const ttsGender = ref('female') // 'female' or 'male'

// Question state
const answered = ref(false)
const answeredCorrectly = ref(false)
const selectedOptionId = ref(null)
const currentXpAward = ref(0)

// Game tracking lists
const wrongQuestionIds = ref([])
const correctQuestionIds = ref([])
const sessionWrongAnswers = ref([])
const earnedBadges = ref([])

// Drag match states
const matchLeft = ref([])
const matchRight = ref([])
const selectedLeft = ref(null)
const selectedRight = ref(null)
const matchPairs = ref([]) // [{"left": "saya", "right": "我"}]

const modeText = computed(() => {
  if (mode === 'boss') return 'BOSS 终极挑战'
  if (mode === 'wrong_practice') return '错题专项训练'
  return '普通章节练习'
})

const currentQuestion = computed(() => {
  return questions.value[currentIndex.value] || {}
})

const accuracy = computed(() => {
  if (questions.value.length === 0) return 0
  return correctCount.value / questions.value.length
})

const loadQuestions = async () => {
  loading.value = true
  try {
    let url = `/api/questions/${lessonId}?mode=${mode}`
    if (mode === 'wrong_practice') {
      url = '/api/wrong-questions'
    }
    
    const response = await axios.get(url)
    let fetched = response.data
    
    if (mode === 'wrong_practice') {
      // Wrong practice parses questions inside the wrong_questions format: wq.question_details
      fetched = response.data.map(item => item.question_details).filter(q => q !== null)
      if (fetched.length === 0) {
        alert('您的错题本是空的！')
        router.push('/')
        return
      }
    }
    
    questions.value = fetched
    setupCurrentQuestion()
  } catch (err) {
    console.error('Failed to retrieve quiz bank:', err)
  } finally {
    loading.value = false
  }
}

const setupCurrentQuestion = () => {
  answered.value = false
  selectedOptionId.value = null
  selectedLeft.value = null
  selectedRight.value = null
  matchPairs.value = []
  
  const q = currentQuestion.value
  
  if (q.type === 'drag_match') {
    const rawPairs = JSON.parse(q.content)
    matchLeft.value = rawPairs.map(p => p.indo)
    matchRight.value = rawPairs.map(p => p.cn)
    
    // Shuffle the lists so they are not aligned
    randomizeArray(matchLeft.value)
    randomizeArray(matchRight.value)
  }
  
  // Speak the word automatically if it is audio quiz
  if (q.type === 'audio') {
    setTimeout(() => {
      speakWord(q.content)
    }, 500)
  }
}

const randomizeArray = (arr) => {
  arr.sort(() => Math.random() - 0.5)
}

// Web Speech API Pronunciation
const speakCurrentWord = () => {
  speakWord(currentQuestion.value.content)
}

const speakWord = (word) => {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel() // Stop any current speech
    
    const utterance = new SpeechSynthesisUtterance(word)
    utterance.lang = 'id-ID' // Standard Indonesian
    
    // Attempt to load Indonesian voices
    const voices = window.speechSynthesis.getVoices()
    const idVoices = voices.filter(v => v.lang.startsWith('id'))
    
    if (idVoices.length > 0) {
      // Pick voice matching gender selection
      const matchingVoice = idVoices.find(v => {
        const name = v.name.toLowerCase()
        if (ttsGender.value === 'male') {
          return name.includes('male') || name.includes('ardi') || name.includes('david')
        } else {
          return name.includes('female') || name.includes('gadis') || name.includes('zira')
        }
      })
      utterance.voice = matchingVoice || idVoices[0]
    }
    
    window.speechSynthesis.speak(utterance)
  } else {
    console.warn('Speech synthesis not supported in this browser.')
  }
}

// Match interactions
const clickLeft = (word) => {
  if (isMatchCompleted(word, 'left')) return
  selectedLeft.value = word
  triggerMatchIfPossible()
}

const clickRight = (mean) => {
  if (isMatchCompleted(mean, 'right')) return
  selectedRight.value = mean
  triggerMatchIfPossible()
}

const triggerMatchIfPossible = () => {
  if (selectedLeft.value && selectedRight.value) {
    matchPairs.value.push({
      left: selectedLeft.value,
      right: selectedRight.value
    })
    selectedLeft.value = null
    selectedRight.value = null
  }
}

const isMatchCompleted = (val, side) => {
  return matchPairs.value.some(p => p[side] === val)
}

const playSound = (isCorrect) => {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext
    if (!AudioContext) return
    const ctx = new AudioContext()
    
    if (isCorrect) {
      const now = ctx.currentTime
      const osc1 = ctx.createOscillator()
      const gain1 = ctx.createGain()
      osc1.type = 'sine'
      osc1.frequency.setValueAtTime(659.25, now)
      osc1.frequency.setValueAtTime(880, now + 0.08)
      
      gain1.gain.setValueAtTime(0.08, now)
      gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.3)
      
      osc1.connect(gain1)
      gain1.connect(ctx.destination)
      osc1.start(now)
      osc1.stop(now + 0.3)
    } else {
      const now = ctx.currentTime
      const osc2 = ctx.createOscillator()
      const gain2 = ctx.createGain()
      osc2.type = 'triangle'
      osc2.frequency.setValueAtTime(150, now)
      osc2.frequency.linearRampToValueAtTime(90, now + 0.25)
      
      gain2.gain.setValueAtTime(0.12, now)
      gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.3)
      
      osc2.connect(gain2)
      gain2.connect(ctx.destination)
      osc2.start(now)
      osc2.stop(now + 0.3)
    }
  } catch (err) {
    console.warn('Audio feedback blocked by browser policies or unsupported:', err)
  }
}

const checkMatchAnswer = () => {
  // Validate match pairs
  const q = currentQuestion.value
  const rawPairs = JSON.parse(q.content)
  const truthMap = {}
  rawPairs.forEach(p => {
    truthMap[p.indo] = p.cn
  })
  
  let allCorrect = true
  matchPairs.value.forEach(p => {
    if (truthMap[p.left] !== p.right) {
      allCorrect = false
    }
  })
  
  answered.value = true
  answeredCorrectly.value = allCorrect
  playSound(allCorrect)
  
  if (allCorrect) {
    correctCount.value++
    combo.value++
    if (combo.value > maxCombo.value) {
      maxCombo.value = combo.value
    }
    currentXpAward.value = 10 + (combo.value * 2)
    xpGained.value += currentXpAward.value
    correctQuestionIds.value.push(q.id)
  } else {
    combo.value = 0
    currentXpAward.value = 0
    wrongQuestionIds.value.push(q.id)
    
    // Log wrong answers for review
    sessionWrongAnswers.value.push({
      type_text: '连线匹配',
      content: '多项印尼语及中文词意匹配',
      correct_answer: rawPairs.map(p => `${p.indo} = ${p.cn}`).join('; '),
      explanation: q.explanation
    })
  }
}

// Option selection
const selectOption = (opt) => {
  if (answered.value) return
  
  answered.value = true
  selectedOptionId.value = opt.id
  answeredCorrectly.value = opt.is_correct
  playSound(opt.is_correct)
  
  const q = currentQuestion.value
  
  if (opt.is_correct) {
    correctCount.value++
    combo.value++
    if (combo.value > maxCombo.value) {
      maxCombo.value = combo.value
    }
    currentXpAward.value = 10 + (combo.value * 2)
    xpGained.value += currentXpAward.value
    correctQuestionIds.value.push(q.id)
  } else {
    combo.value = 0
    currentXpAward.value = 0
    wrongQuestionIds.value.push(q.id)
    
    // Log details of wrong answer
    const correctOpt = q.options.find(o => o.is_correct)
    sessionWrongAnswers.value.push({
      type_text: getTypeText(q.type),
      content: q.content,
      correct_answer: correctOpt ? correctOpt.option_text : '',
      explanation: q.explanation
    })
  }
}

const getTypeText = (type) => {
  const map = {
    'vocab_choice': '词汇释义',
    'cn_to_indo': '中文译印尼语',
    'indo_to_cn': '印尼语译中文',
    'audio': '听力发音',
    'picture': '图片辨词',
    'fill_blank': '句子填空',
    'dialogue': '对话补全',
    'drag_match': '连线匹配'
  }
  return map[type] || '课后考核'
}

const getOptionClass = (opt) => {
  if (!answered.value) return ''
  
  if (opt.is_correct) {
    return 'opt-correct border-success'
  }
  
  if (selectedOptionId.value === opt.id && !opt.is_correct) {
    return 'opt-wrong border-danger'
  }
  
  return 'opt-muted'
}

const getLetter = (idx) => {
  return String.fromCharCode(65 + idx)
}

const nextQuestion = () => {
  if (currentIndex.value + 1 < questions.value.length) {
    currentIndex.value++
    setupCurrentQuestion()
  } else {
    submitQuizResults()
  }
}

const submitQuizResults = async () => {
  loading.value = true
  try {
    const response = await axios.post('/api/game/submit', {
      lesson_id: lessonId,
      correct_count: correctCount.value,
      total_count: questions.value.length,
      time_spent: 120, // simulate
      max_combo: maxCombo.value,
      mode: mode,
      wrong_question_ids: wrongQuestionIds.value,
      correct_question_ids: correctQuestionIds.value
    })
    
    xpGained.value = response.data.xp_gained
    earnedBadges.value = response.data.new_badges || []
    
    // Sync local store
    userStore.updateProfile(response.data.new_level_xp || userStore.xp + xpGained.value, response.data.new_level || userStore.level)
    
    gameOver.value = true
  } catch (err) {
    console.error('Failed to submit results:', err)
    gameOver.value = true // Show client calculations on network error
  } finally {
    loading.value = false
  }
}

const restartGame = () => {
  gameOver.value = false
  currentIndex.value = 0
  score.value = 0
  correctCount.value = 0
  combo.value = 0
  maxCombo.value = 0
  xpGained.value = 0
  wrongQuestionIds.value = []
  correctQuestionIds.value = []
  sessionWrongAnswers.value = []
  earnedBadges.value = []
  
  loadQuestions()
}

const goBack = () => {
  router.push('/map')
}

const quitGame = () => {
  if (confirm('确定要退出当前练习吗？您的答题记录将不会被保存。')) {
    router.push('/map')
  }
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.game-wrapper {
  min-height: 80vh;
}

.progress-bar-wrapper {
  height: 8px;
}

.progress-bar-bg {
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #06b6d4);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.emoji-large {
  font-size: 80px;
  filter: drop-shadow(0 8px 16px rgba(0,0,0,0.3));
}

.metric-card {
  background: rgba(255, 255, 255, 0.03);
}

.play-btn {
  width: 80px;
  height: 80px;
  font-size: 32px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(168, 85, 247, 0.2));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
  transition: all 0.2s ease;
}

.play-btn:hover {
  transform: scale(1.05);
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(168, 85, 247, 0.3));
  border-color: rgba(255,255,255,0.4);
}

.img-frame {
  width: 200px;
  height: 200px;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
}

.img-fallback {
  opacity: 0.5;
}

.option-btn {
  background: rgba(255, 255, 255, 0.04);
  font-size: 16px;
  transition: all 0.2s ease;
}

.option-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.25);
  transform: scale(1.02);
}

.opt-correct {
  background: rgba(16, 185, 129, 0.15) !important;
  color: #10b981 !important;
  font-weight: 600;
  box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
}

.opt-wrong {
  background: rgba(239, 68, 68, 0.15) !important;
  color: #ef4444 !important;
  font-weight: 600;
  box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
}

.opt-muted {
  opacity: 0.5;
}

.select-box {
  background: rgba(255, 255, 255, 0.04);
  transition: all 0.2s ease;
}

.match-selected {
  background: rgba(99, 102, 241, 0.2) !important;
  border-color: var(--color-primary) !important;
  box-shadow: 0 0 12px var(--color-primary-glow);
}

.match-done {
  background: rgba(16, 185, 129, 0.2) !important;
  border-color: var(--color-success) !important;
  color: var(--color-success) !important;
  opacity: 0.7;
  pointer-events: none;
}

.opt-letter {
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  color: var(--color-primary);
}

.animate-slide-up {
  animation: slide-up 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slide-up {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
