<template>
  <div class="special-study-container py-4">
    <div class="container">
      
      <!-- 1. Chapter/Category Selection Mode -->
      <div v-if="currentScreen === 'select'" class="animate-fade-in">
        <div class="text-center mb-5">
          <h1 class="display-title text-white fw-bold glow-text-primary mb-2">常用词汇专项学习</h1>
          <p class="text-muted fs-5">突破印尼语核心词汇，支持对照学习与听、读、写三维测试</p>
        </div>

        <!-- Categories Grid -->
        <div class="row g-4 row-cols-2 row-cols-md-3 row-cols-lg-4">
          <div class="col" v-for="cat in categories" :key="cat.id">
            <div class="glass-card category-card p-4 text-center h-100 border border-light border-opacity-10 d-flex flex-column justify-content-between align-items-center" @click="selectCategory(cat)">
              <div class="category-icon-wrapper mb-3">
                <span class="category-emoji">{{ getCategoryEmoji(cat.name) }}</span>
              </div>
              <div>
                <h5 class="text-white fw-bold mb-1">{{ cat.name }}</h5>
                <span class="badge bg-primary bg-opacity-25 text-info px-2 py-1 rounded-pill small" style="font-size: 11px;">
                  {{ cat.word_count }} 词汇
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Word Review / Study List Screen (对照学习) -->
      <div v-else-if="currentScreen === 'review'" class="animate-fade-in col-12 col-lg-8 mx-auto">
        <div class="glass-card p-4 p-md-5 shadow-lg border border-light border-opacity-10 rounded-4">
          <div class="d-flex justify-content-between align-items-center mb-4 pb-2 border-bottom border-light border-opacity-10">
            <div>
              <span class="fs-4 me-2">{{ getCategoryEmoji(selectedCategory?.name) }}</span>
              <h2 class="text-white fw-bold d-inline-block mb-0">{{ selectedCategory?.name }} · 对照学习</h2>
            </div>
            <button class="btn btn-outline-light btn-sm px-3 rounded-pill border-light border-opacity-20" @click="returnToSelect">返回章节选择</button>
          </div>

          <p class="text-muted mb-4">请先通过下表对照记忆印尼语单词和中文含义，点击发音喇叭收听标准发音，准备好后点击底部按钮进行测试。</p>

          <!-- Vocabulary Study Table -->
          <div class="word-list-box mb-5">
            <div class="row g-3">
              <div class="col-12" v-for="(item, idx) in reviewWords" :key="item.id">
                <div class="word-review-row p-3 rounded-3 glass-panel border border-light border-opacity-10 d-flex align-items-center justify-content-between">
                  <div class="d-flex align-items-center gap-3">
                    <span class="fs-5">{{ getCategoryEmoji(selectedCategory?.name) }}</span>
                    <div>
                      <h4 class="text-white fw-bold mb-0 font-monospace" style="letter-spacing: 0.5px;">{{ item.word }}</h4>
                      <div class="text-info small mt-1 font-monospace" style="opacity: 0.85;">印尼语</div>
                    </div>
                  </div>
                  
                  <div class="d-flex align-items-center gap-4">
                    <button class="speak-row-btn" @click="speakWord(item.word)" title="收听发音">
                      🔊
                    </button>
                    <div class="text-end">
                      <h5 class="text-success fw-semibold mb-0" style="font-size: 16px;">{{ item.translation }}</h5>
                      <div class="text-muted small mt-1">中文释义</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Bottom Actions -->
          <div class="text-center pt-2 d-flex gap-3 justify-content-center">
            <button class="btn glass-btn py-3 px-4 text-white fw-semibold rounded-pill" @click="returnToSelect">返回</button>
            <button class="btn glass-btn glass-btn-primary py-3 px-5 text-white fw-bold rounded-pill shadow float-animation" @click="showModeSelector = true">
              🎯 我已学完，开始挑战
            </button>
          </div>
        </div>
      </div>

      <!-- Mode Selection Slide-up Panel (Modal) -->
      <div v-if="showModeSelector" class="modal-overlay d-flex justify-content-center align-items-end align-items-md-center animate-fade-in" @click.self="showModeSelector = false">
        <div class="glass-card mode-selector-card p-4 p-md-5 border border-light border-opacity-10 w-100 rounded-top-5 rounded-md-4 animate-slide-up" style="max-width: 600px;">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h3 class="text-white fw-bold mb-0">选择测试模式：{{ selectedCategory?.name }}</h3>
            <button class="btn btn-outline-light border-0 rounded-circle py-1 px-2" @click="showModeSelector = false">✕</button>
          </div>
          
          <p class="text-muted mb-4">针对当前章节的词汇，为您生成 10 道随机强化考试题。</p>

          <div class="d-flex flex-column gap-3">
            <button class="btn glass-btn mode-btn p-3 text-start d-flex align-items-center justify-content-between text-white rounded-3" @click="startStudy('listening')">
              <div class="d-flex align-items-center gap-3">
                <span class="fs-2">🔊</span>
                <div>
                  <h5 class="fw-bold mb-0">听力专项测试 (听)</h5>
                  <p class="text-muted small mb-0 mt-1">听单词发音，选择正确的中文翻译</p>
                </div>
              </div>
              <span class="arrow-icon">➔</span>
            </button>

            <button class="btn glass-btn mode-btn p-3 text-start d-flex align-items-center justify-content-between text-white rounded-3" @click="startStudy('reading')">
              <div class="d-flex align-items-center gap-3">
                <span class="fs-2">📖</span>
                <div>
                  <h5 class="fw-bold mb-0">认读联想测试 (读)</h5>
                  <p class="text-muted small mb-0 mt-1">中印互译选择，巩固字面记忆</p>
                </div>
              </div>
              <span class="arrow-icon">➔</span>
            </button>

            <button class="btn glass-btn mode-btn p-3 text-start d-flex align-items-center justify-content-between text-white rounded-3" @click="startStudy('writing')">
              <div class="d-flex align-items-center gap-3">
                <span class="fs-2">✍️</span>
                <div>
                  <h5 class="fw-bold mb-0">词汇拼写测试 (写)</h5>
                  <p class="text-muted small mb-0 mt-1">根据中文释义，拼写写出对应的印尼语单词</p>
                </div>
              </div>
              <span class="arrow-icon">➔</span>
            </button>
          </div>
        </div>
      </div>

      <!-- 3. Active Study Session Screen (考试做题) -->
      <div v-if="currentScreen === 'study'" class="col-12 col-lg-8 mx-auto px-3 animate-fade-in">
        <div class="glass-card p-4 p-md-5 shadow-lg position-relative border border-light border-opacity-10 rounded-4">
          <!-- Top Status Bar -->
          <div class="d-flex justify-content-between align-items-center mb-4">
            <button class="btn btn-sm btn-outline-light border-0 text-muted" @click="quitStudy">✕ 退出</button>
            
            <div class="progress-bar-wrapper flex-grow-1 mx-4">
              <div class="progress-bar-bg">
                <div class="progress-bar-fill" :style="{ width: ((currentIndex + 1) / questions.length * 100) + '%' }"></div>
              </div>
            </div>
            
            <span class="text-white small fw-bold font-monospace">{{ currentIndex + 1 }} / {{ questions.length }}</span>
          </div>

          <!-- Session Headers -->
          <div class="d-flex justify-content-between align-items-center mb-4 px-2">
            <div class="text-muted small">
              章节：<span class="text-white fw-semibold">{{ selectedCategory?.name }}</span>
            </div>
            <div class="badge bg-info bg-opacity-25 text-info px-3 py-1 rounded-pill">
              {{ currentModeText }}
            </div>
          </div>

          <!-- Question Display Area -->
          <div class="question-container py-4 mb-4 text-center">
            <!-- Listening TTS Auto-player -->
            <div v-if="studyMode === 'listening'" class="audio-quiz-box mb-4">
              <div class="d-flex flex-column align-items-center">
                <button class="play-btn mb-3" @click="speakCurrentWord" title="播放发音">
                  🔊
                </button>
                <div class="text-muted small">点击按钮重新播放单词原音</div>
              </div>
            </div>

            <!-- Main Question Prompt -->
            <div class="d-flex flex-column align-items-center justify-content-center gap-3">
              <h3 class="text-white fw-bold lh-base mb-0 text-center" v-html="currentQuestion.content"></h3>
              <!-- Read Word pronunciation for Reading / Writing fallback -->
              <button 
                v-if="studyMode === 'reading' && currentQuestion.type === 'reading_indo_to_cn'" 
                class="btn btn-sm btn-outline-light rounded-pill px-3 py-2 border border-light border-opacity-20 float-animation mt-2" 
                @click="speakWord(stripHtml(currentQuestion.content))"
                title="播放发音"
                style="font-size: 13px;"
              >
                🔊 播放原音
              </button>
            </div>
          </div>

          <!-- Interaction Panels -->
          <div class="answers-container">
            <!-- Mode 1 & 2: Multiple Choice Selection (Listening & Reading) -->
            <div v-if="studyMode === 'listening' || studyMode === 'reading'" class="row g-3">
              <div class="col-12 col-md-6" v-for="(opt, oIdx) in currentQuestion.options" :key="oIdx">
                <button 
                  class="btn glass-btn text-start p-4 w-100 border border-light border-opacity-10 text-white rounded-4 option-btn d-flex justify-content-between align-items-center"
                  :class="getOptionClass(opt)"
                  @click="selectOption(opt)"
                  :disabled="answered"
                >
                  <div>
                    <span class="opt-letter me-3">{{ getLetter(oIdx) }}.</span>
                    <span>{{ opt.text }}</span>
                  </div>
                </button>
              </div>
            </div>

            <!-- Mode 3: Spelling/Writing Input Field -->
            <div v-else-if="studyMode === 'writing'" class="writing-input-wrapper py-3">
              <div class="mb-4">
                <input 
                  type="text" 
                  class="form-control glass-input text-center text-white py-3 px-4 rounded-3 fs-4 border border-light border-opacity-20"
                  placeholder="在此输入印尼语单词..."
                  v-model="writingInput"
                  :disabled="answered"
                  @keyup.enter="checkWritingAnswer"
                  ref="spellingInput"
                  autofocus
                  autocomplete="off"
                  autocorrect="off"
                  autocapitalize="off"
                  spellcheck="false"
                />
              </div>
              <div v-if="!answered" class="text-center">
                <button 
                  class="btn glass-btn glass-btn-primary px-5 py-3 text-white fw-bold rounded-pill"
                  @click="checkWritingAnswer"
                  :disabled="!writingInput.trim()"
                >
                  提 交 拼 写
                </button>
              </div>
            </div>
          </div>

          <!-- Bottom Slide-up Correct/Incorrect Panel -->
          <div v-if="answered" class="explanation-panel mt-5 p-4 rounded-4 animate-slide-up" :class="answeredCorrectly ? 'bg-success bg-opacity-10 border border-success border-opacity-25' : 'bg-danger bg-opacity-10 border border-danger border-opacity-25'">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="fw-bold" :class="answeredCorrectly ? 'text-success' : 'text-danger'">
                {{ answeredCorrectly ? '✓ 回答正确！' : '✕ 回答错误' }}
              </h5>
            </div>
            
            <p class="text-light mb-4 small">
              {{ currentQuestion.explanation }}
            </p>
            
            <div class="text-end">
              <button class="btn glass-btn glass-btn-primary px-5 py-3 text-white fw-bold" @click="nextQuestion">
                {{ currentIndex + 1 === questions.length ? '查看成绩' : '下一题' }}
              </button>
            </div>
          </div>

        </div>
      </div>

      <!-- 4. Final Score Summary Screen -->
      <div v-if="currentScreen === 'result'" class="col-12 col-lg-8 mx-auto px-3 animate-fade-in">
        <div class="glass-card p-5 text-center shadow-lg border border-light border-opacity-10 rounded-4">
          <span class="emoji-large mb-3 d-inline-block">{{ scorePercent >= 80 ? '🎉' : '💪' }}</span>
          <h2 class="display-title text-white fw-bold mb-3">测试完成</h2>
          
          <p class="text-muted fs-5 mb-5">
            {{ scorePercent >= 80 ? '太棒了！您非常出色地掌握了这一章节的词汇！' : '测试成绩未达标，建议返回对照表多加练习。' }}
          </p>

          <!-- Metrics -->
          <div class="row g-4 mb-5 justify-content-center">
            <div class="col-6 col-sm-4">
              <div class="metric-card p-3 rounded-4 glass-panel border border-light border-opacity-10">
                <span class="d-block text-muted small">正确题数</span>
                <h3 class="text-white fw-bold mt-1 mb-0">{{ correctCount }} / {{ questions.length }}</h3>
              </div>
            </div>
            <div class="col-6 col-sm-4">
              <div class="metric-card p-3 rounded-4 glass-panel border border-light border-opacity-10">
                <span class="d-block text-muted small">正确率</span>
                <h3 class="fw-bold mt-1 mb-0" :class="scorePercent >= 80 ? 'text-success' : 'text-warning'">{{ scorePercent }}%</h3>
              </div>
            </div>
          </div>

          <!-- Wrong Questions Review -->
          <div v-if="wrongAnswersReview.length > 0" class="text-start mb-5">
            <h4 class="text-white fw-bold mb-3 display-title">错题解析</h4>
            <div class="d-flex flex-column gap-3">
              <div class="p-3 rounded-3 glass-panel border border-danger border-opacity-10" v-for="(item, idx) in wrongAnswersReview" :key="idx">
                <div class="text-danger fw-semibold small mb-1">题目 {{ idx + 1 }}</div>
                <div class="text-white mb-2" v-html="item.content"></div>
                <div class="text-success small fw-medium">正确答案：{{ item.correct_answer }}</div>
                <div class="text-muted small mt-2">解析：{{ item.explanation }}</div>
              </div>
            </div>
          </div>

          <div class="d-flex gap-3 justify-content-center">
            <button class="btn glass-btn py-3 px-5 text-white fw-semibold" @click="returnToReview">返回对照学习</button>
            <button class="btn glass-btn glass-btn-primary py-3 px-5 text-white fw-bold shadow" @click="restartStudy">重新测试</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import axios from 'axios'

// Component Screens
const currentScreen = ref('select') // 'select', 'review', 'study', 'result'
const categories = ref([])
const loading = ref(true)

// Selection settings
const selectedCategory = ref(null)
const showModeSelector = ref(false)
const studyMode = ref('reading') // 'listening', 'reading', 'writing'

// Review state
const reviewWords = ref([])

// Study session state
const questions = ref([])
const currentIndex = ref(0)
const answered = ref(false)
const answeredCorrectly = ref(false)
const selectedOptionText = ref(null)
const writingInput = ref('')
const spellingInput = ref(null)

// Stats tracking
const correctCount = ref(0)
const wrongAnswersReview = ref([])

const currentQuestion = computed(() => {
  return questions.value[currentIndex.value] || {}
})

const scorePercent = computed(() => {
  if (questions.value.length === 0) return 0
  return Math.round((correctCount.value / questions.value.length) * 100)
})

const currentModeText = computed(() => {
  if (studyMode.value === 'listening') return '听力测试'
  if (studyMode.value === 'writing') return '拼写测试'
  return '认读测试'
})

// Fetch all special categories
const fetchCategories = async () => {
  loading.value = true
  try {
    const response = await axios.get('/api/special/categories')
    categories.value = response.data
  } catch (err) {
    console.error('Failed to load categories:', err)
  } finally {
    loading.value = false
  }
}

// Select a category to study (Fetches clean word list and opens review screen)
const selectCategory = async (category) => {
  selectedCategory.value = category
  loading.value = true
  try {
    const response = await axios.get(`/api/special/words/${category.id}`)
    reviewWords.value = response.data
    currentScreen.value = 'review'
  } catch (err) {
    console.error('Failed to load review words:', err)
    alert('无法加载当前词汇表。')
  } finally {
    loading.value = false
  }
}

// Launch a dynamic quiz session
const startStudy = async (mode) => {
  studyMode.value = mode
  showModeSelector.value = false
  loading.value = true
  
  try {
    const response = await axios.get(`/api/special/questions/${selectedCategory.value.id}?mode=${mode}`)
    questions.value = response.data
    currentIndex.value = 0
    correctCount.value = 0
    wrongAnswersReview.value = []
    
    currentScreen.value = 'study'
    setupCurrentQuestion()
  } catch (err) {
    console.error('Failed to load questions:', err)
    alert('未能准备好该章节的词汇测试，请稍后重试。')
  } finally {
    loading.value = false
  }
}

// Setup the current question
const setupCurrentQuestion = () => {
  answered.value = false
  answeredCorrectly.value = false
  selectedOptionText.value = null
  writingInput.value = ''
  
  const q = currentQuestion.value
  
  // Play TTS voice instantly in listening mode
  if (studyMode.value === 'listening') {
    setTimeout(() => {
      speakWord(q.content)
    }, 400)
  }
  
  // Focus text input in writing mode on next UI tick
  if (studyMode.value === 'writing') {
    nextTick(() => {
      if (spellingInput.value) {
        spellingInput.value.focus()
      }
    })
  }
}

// Audio Pronunciation Synthesis
const speakCurrentWord = () => {
  speakWord(currentQuestion.value.content)
}

const speakWord = (word) => {
  if ('speechSynthesis' in window) {
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel()
    }
    const utterance = new SpeechSynthesisUtterance(word)
    utterance.lang = 'id-ID' // Standard Indonesian
    utterance.rate = 0.82 // learning rate
    
    // Choose appropriate voice
    const voices = window.speechSynthesis.getVoices()
    const idVoice = voices.find(v => v.lang.startsWith('id') || v.lang.startsWith('in'))
    if (idVoice) {
      utterance.voice = idVoice
    }
    window.speechSynthesis.speak(utterance)
  }
}

// Clean HTML tags from content
const stripHtml = (html) => {
  const tmp = document.createElement("DIV")
  tmp.innerHTML = html
  const text = tmp.textContent || tmp.innerText || ""
  // extract word inside quotes if present
  const m = text.match(/“([^”]+)”/)
  if (m && m[1]) return m[1]
  return text
}

// Option button classes
const getOptionClass = (opt) => {
  if (!answered.value) return ''
  if (opt.is_correct) {
    return 'opt-correct border-success'
  }
  if (selectedOptionText.value === opt.text && !opt.is_correct) {
    return 'opt-wrong border-danger'
  }
  return 'opt-muted'
}

// Select option event
const selectOption = (opt) => {
  if (answered.value) return
  
  answered.value = true
  selectedOptionText.value = opt.text
  answeredCorrectly.value = opt.is_correct
  playSound(opt.is_correct)
  
  // Auto-speak in reading mode if the correct option is the Indonesian word
  if (studyMode.value === 'reading' && currentQuestion.value.type === 'reading_cn_to_indo' && opt.is_correct) {
    speakWord(opt.text)
  }
  
  if (opt.is_correct) {
    correctCount.value++
  } else {
    const correctOpt = currentQuestion.value.options.find(o => o.is_correct)
    wrongAnswersReview.value.push({
      content: currentQuestion.value.content,
      correct_answer: correctOpt ? correctOpt.text : '',
      explanation: currentQuestion.value.explanation
    })
  }
}

// Submit writing spelling answer
const checkWritingAnswer = () => {
  if (answered.value || !writingInput.value.trim()) return
  
  const userText = writingInput.value.trim().toLowerCase()
  const correctText = currentQuestion.value.correct_answer.trim().toLowerCase()
  
  // Clean punctuation
  const cleanStr = (s) => s.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?"'“]/g, "").trim()
  const isCorrect = cleanStr(userText) === cleanStr(correctText)
  
  answered.value = true
  answeredCorrectly.value = isCorrect
  playSound(isCorrect)
  speakWord(currentQuestion.value.correct_answer)
  
  if (isCorrect) {
    correctCount.value++
  } else {
    wrongAnswersReview.value.push({
      content: currentQuestion.value.content,
      correct_answer: currentQuestion.value.correct_answer,
      explanation: currentQuestion.value.explanation
    })
  }
}

// Synthesis of sound feedback (Beep sound chimes)
const playSound = (isCorrect) => {
  try {
    const AudioContext = window.AudioContext || window.webkitAudioContext
    if (!AudioContext) return
    const ctx = new AudioContext()
    
    const playWaves = () => {
      const now = ctx.currentTime
      const gain = ctx.createGain()
      const osc = ctx.createOscillator()
      
      if (isCorrect) {
        osc.type = 'sine'
        osc.frequency.setValueAtTime(587.33, now) // D5
        osc.frequency.setValueAtTime(880, now + 0.08) // A5
        gain.gain.setValueAtTime(0.06, now)
        gain.gain.linearRampToValueAtTime(0, now + 0.35)
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.35)
      } else {
        osc.type = 'sawtooth'
        osc.frequency.setValueAtTime(180, now)
        osc.frequency.linearRampToValueAtTime(110, now + 0.25)
        gain.gain.setValueAtTime(0.08, now)
        gain.gain.linearRampToValueAtTime(0, now + 0.3)
        osc.connect(gain)
        gain.connect(ctx.destination)
        osc.start(now)
        osc.stop(now + 0.3)
      }
    }

    if (ctx.state === 'suspended') {
      ctx.resume().then(playWaves)
    } else {
      playWaves()
    }
  } catch (err) {
    console.warn('Audio feedback blocked by browser:', err)
  }
}

const getLetter = (idx) => {
  return String.fromCharCode(65 + idx)
}

// Move to next question or show results
const nextQuestion = () => {
  if (currentIndex.value + 1 < questions.value.length) {
    currentIndex.value++
    setupCurrentQuestion()
  } else {
    currentScreen.value = 'result'
  }
}

const restartStudy = () => {
  startStudy(studyMode.value)
}

const returnToSelect = () => {
  currentScreen.value = 'select'
}

const returnToReview = () => {
  currentScreen.value = 'review'
}

const quitStudy = () => {
  if (confirm('确认要退出当前测试吗？您的答题进度将不会保存。')) {
    currentScreen.value = 'review'
  }
}

// Emoji Mapping Helper for the 49 Chapters
const getCategoryEmoji = (name) => {
  const map = {
    '字母': '🔤', '颜色': '🎨', '代词': '🙋‍♂️', '问候': '💬', '数字': '🔢',
    '房子': '🏠', '卧室': '🛏️', '浴室': '🚿', '学习室': '📖', '家庭': '👨‍👩‍👧‍👦',
    '人们': '👥', '形容词': '📝', '动词': '🏃‍♂️', '时间': '🕒', '星期': '📅',
    '月': '📆', '四季': '🍂', '动物': '🦁', '水生动物': '🐬', '自然': '🌲',
    '客厅': '🛋️', '厨房': '🍳', '洗衣店': '🧺', '孩子们': '👶', '食物': '🍔',
    '饮料': '🥤', '早餐': '🍳', '衣物': '👕', '配件': '🕶️', '身体': '💪',
    '职业': '💼', '地方': '📍', '交通': '🚗', '地点': '🧭', '肉类': '🥩',
    '电子产品': '💻', '互联网': '🌐', '社交媒体': '📱', '电子游戏': '🎮',
    '水果': '🍎', '蔬菜': '🥦', '运动': '⚽', '天气': '☀️', '材料': '🧱',
    '购物': '🛒', '超市': '🏬', '情感': '❤️',
    '宿管管理': '🛌', '食堂管理': '🍚', '车辆管理': '🚐', '物资管理': '📦', '办公室管理': '👔'
  }
  return map[name] || '📚'
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.special-study-container {
  min-height: 80vh;
}

.category-card {
  cursor: pointer;
  background: rgba(255, 255, 255, 0.03);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.category-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2) !important;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.category-icon-wrapper {
  width: 70px;
  height: 70px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.category-emoji {
  font-size: 36px;
}

/* Modal Selector */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  z-index: 1050;
}

.mode-selector-card {
  background: rgba(18, 20, 32, 0.85);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
}

.mode-btn {
  background: rgba(255, 255, 255, 0.04);
  transition: all 0.2s ease;
}

.mode-btn:hover {
  background: rgba(255, 255, 255, 0.09);
  border-color: rgba(255, 255, 255, 0.25) !important;
  transform: translateX(4px);
}

.arrow-icon {
  font-size: 20px;
  color: var(--color-primary);
  opacity: 0.7;
}

/* Progress bar */
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

.play-btn {
  width: 90px;
  height: 90px;
  font-size: 36px;
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

/* Word Review Row styling */
.word-review-row {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  transition: all 0.25s ease;
}

.word-review-row:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(99, 102, 241, 0.35) !important;
  transform: scale(1.01);
}

.speak-row-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.05);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.speak-row-btn:hover {
  transform: scale(1.1);
  background: rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 241, 0.4);
  box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
}

/* Standard Choice Buttons */
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
  opacity: 0.4;
}

.opt-letter {
  font-weight: 800;
  color: var(--color-primary);
}

/* Writing/Spelling Input */
.glass-input {
  background: rgba(255, 255, 255, 0.04) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
  font-family: 'Outfit', sans-serif;
  letter-spacing: 1px;
}

.glass-input:focus {
  background: rgba(255, 255, 255, 0.07) !important;
  border-color: rgba(99, 102, 241, 0.5) !important;
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.2) !important;
}

.explanation-panel {
  backdrop-filter: blur(8px);
}

/* Results metrics */
.emoji-large {
  font-size: 80px;
  filter: drop-shadow(0 8px 16px rgba(0,0,0,0.3));
}

.metric-card {
  background: rgba(255, 255, 255, 0.03);
}

/* Animations */
.animate-fade-in {
  animation: fadeIn 0.4s ease-out;
}

.animate-slide-up {
  animation: slide-up 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.97); }
  to { opacity: 1; transform: scale(1); }
}

@keyframes slide-up {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@media (max-width: 576px) {
  .category-card {
    padding: 1rem !important;
  }
  .category-icon-wrapper {
    width: 55px;
    height: 55px;
  }
  .category-emoji {
    font-size: 28px;
  }
}
</style>
