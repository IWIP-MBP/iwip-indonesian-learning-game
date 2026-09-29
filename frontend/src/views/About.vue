<template>
  <div class="about-page">
    <!-- Hero Header -->
    <div class="about-hero">
      <div class="hero-glow"></div>
      <div class="hero-content text-center">
        <div class="hero-badge mb-3">
          <span class="badge-icon">🇮🇩</span>
          <span class="badge-label">IWIP Indonesian Learning</span>
        </div>
        <h1 class="hero-title">学习介绍</h1>
        <p class="hero-subtitle">了解您的学习旅程、等级体系与荣誉勋章</p>
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-num">21</span>
            <span class="stat-label">课程章节</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">3150+</span>
            <span class="stat-label">练习题目</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">7</span>
            <span class="stat-label">荣誉勋章</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Section: Language Levels -->
    <div class="section-container">
      <div class="section-header">
        <div class="section-icon">📊</div>
        <h2 class="section-title">印尼语等级说明</h2>
        <p class="section-desc">根据欧洲语言共同参考框架（CEFR）体系，印尼语分为以下等级</p>
      </div>

      <div class="levels-grid">
        <div
          v-for="level in languageLevels"
          :key="level.code"
          class="level-card"
          :class="'level-' + level.color"
          @mouseenter="hoveredLevel = level.code"
          @mouseleave="hoveredLevel = null"
        >
          <div class="level-badge">
            <span class="level-code">{{ level.code }}</span>
            <span class="level-flag">{{ level.flag }}</span>
          </div>
          <div class="level-info">
            <h3 class="level-name">{{ level.name }}</h3>
            <p class="level-desc">{{ level.description }}</p>
            <div class="level-skills">
              <span v-for="skill in level.skills" :key="skill" class="skill-tag">{{ skill }}</span>
            </div>
          </div>
          <div class="level-progress-bar">
            <div class="level-progress-fill" :style="{ width: level.progress + '%' }"></div>
          </div>
          <div class="level-course-note" v-if="level.courseNote">
            <span class="note-icon">📚</span> {{ level.courseNote }}
          </div>
        </div>
      </div>
    </div>

    <!-- Section: Learning Roadmap -->
    <div class="section-container alt-bg">
      <div class="section-header">
        <div class="section-icon">🗺️</div>
        <h2 class="section-title">学习路线图</h2>
        <p class="section-desc">本课程共21节课，分4个阶段循序渐进掌握印尼语</p>
      </div>

      <div class="roadmap">
        <div v-for="(stage, idx) in learningStages" :key="stage.id" class="roadmap-stage">
          <div class="stage-connector" v-if="idx < learningStages.length - 1"></div>
          <div class="stage-card" :class="'stage-' + stage.color">
            <div class="stage-header">
              <div class="stage-number">{{ stage.id }}</div>
              <div class="stage-icon">{{ stage.icon }}</div>
            </div>
            <h3 class="stage-name">{{ stage.name }}</h3>
            <p class="stage-lessons">第 {{ stage.lessons }} 课</p>
            <p class="stage-desc">{{ stage.description }}</p>
            <div class="stage-goals">
              <div v-for="goal in stage.goals" :key="goal" class="goal-item">
                <span class="goal-check">✓</span> {{ goal }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section: XP & Levels System -->
    <div class="section-container">
      <div class="section-header">
        <div class="section-icon">⚡</div>
        <h2 class="section-title">积分与等级系统</h2>
        <p class="section-desc">通过学习获取 XP 经验值，不断升级成长</p>
      </div>

      <div class="xp-system">
        <div class="xp-earn-section">
          <h3 class="subsection-title">如何获取 XP</h3>
          <div class="xp-sources">
            <div v-for="src in xpSources" :key="src.action" class="xp-source-card">
              <span class="xp-source-icon">{{ src.icon }}</span>
              <div class="xp-source-info">
                <span class="xp-source-action">{{ src.action }}</span>
                <span class="xp-source-amount">+{{ src.xp }} XP</span>
              </div>
            </div>
          </div>
        </div>

        <div class="level-tiers-section">
          <h3 class="subsection-title">等级阶梯</h3>
          <div class="level-tiers">
            <div
              v-for="tier in levelTiers"
              :key="tier.level"
              class="tier-item"
              :class="{ 'tier-highlight': tier.highlight }"
            >
              <div class="tier-level">
                <span class="tier-icon">{{ tier.icon }}</span>
                <span class="tier-lv">LV.{{ tier.level }}</span>
              </div>
              <div class="tier-bar-wrap">
                <div class="tier-bar">
                  <div class="tier-bar-fill" :style="{ width: (tier.xp / 2000 * 100) + '%' }"></div>
                </div>
                <span class="tier-xp">{{ tier.xp }} XP</span>
              </div>
              <span class="tier-title">{{ tier.title }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Section: Badges -->
    <div class="section-container alt-bg">
      <div class="section-header">
        <div class="section-icon">🏅</div>
        <h2 class="section-title">荣誉勋章</h2>
        <p class="section-desc">完成特定成就，解锁专属荣誉勋章，展示您的学习实力</p>
      </div>

      <div class="badges-grid">
        <div
          v-for="badge in badges"
          :key="badge.name"
          class="badge-card"
          :class="{ 'badge-locked': badge.locked }"
        >
          <div class="badge-glow"></div>
          <div class="badge-icon-wrap">
            <span class="badge-emoji">{{ badge.icon }}</span>
          </div>
          <h4 class="badge-name">{{ badge.name }}</h4>
          <p class="badge-desc">{{ badge.description }}</p>
          <div class="badge-condition">
            <span class="condition-label">解锁条件：</span>
            <span class="condition-text">{{ badge.condition }}</span>
          </div>
          <div class="badge-rarity" :class="'rarity-' + badge.rarity">
            {{ rarityLabel[badge.rarity] }}
          </div>
        </div>
      </div>
    </div>

    <!-- Section: FAQ -->
    <div class="section-container">
      <div class="section-header">
        <div class="section-icon">💡</div>
        <h2 class="section-title">学习小贴士</h2>
        <p class="section-desc">让学习更高效的方法</p>
      </div>
      <div class="tips-grid">
        <div v-for="tip in tips" :key="tip.title" class="tip-card">
          <span class="tip-icon">{{ tip.icon }}</span>
          <h4 class="tip-title">{{ tip.title }}</h4>
          <p class="tip-body">{{ tip.body }}</p>
        </div>
      </div>
    </div>

    <!-- CTA -->
    <div class="cta-section">
      <div class="cta-content">
        <h2 class="cta-title">准备好开始学习了吗？</h2>
        <p class="cta-desc">打开学习地图，从第一课开始您的印尼语学习之旅！</p>
        <router-link to="/map" class="cta-btn">
          <span>开始学习</span>
          <span class="btn-arrow">→</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const hoveredLevel = ref(null)

const rarityLabel = {
  common: '普通',
  rare: '稀有',
  epic: '史诗',
  legendary: '传说'
}

const languageLevels = [
  {
    code: 'A1',
    name: '初级入门',
    flag: '🌱',
    color: 'green',
    progress: 20,
    description: '掌握基础发音、问候、简单词汇和日常短句，能进行最简单的自我介绍。',
    skills: ['基础发音', '日常问候', '数字与颜色', '简单自我介绍'],
    courseNote: '对应本课程第 1-8 课（发音基础篇）'
  },
  {
    code: 'A2',
    name: '初级应用',
    flag: '🌿',
    color: 'teal',
    progress: 40,
    description: '能进行简单的日常对话，描述自己的工作、爱好、家庭，在熟悉场景中进行基本沟通。',
    skills: ['日常对话', '工作场景', '描述事物', '基本购物'],
    courseNote: '对应本课程第 9-15 课（主题应用篇）'
  },
  {
    code: 'B1',
    name: '中级交流',
    flag: '🌳',
    color: 'blue',
    progress: 60,
    description: '能理解清晰的标准印尼语，应对大多数旅行和工作情境，表达个人观点和简单意见。',
    skills: ['复杂句子', '工作汇报', '意见表达', '新闻理解'],
    courseNote: '对应本课程第 16-21 课（进阶综合篇）'
  },
  {
    code: 'B2',
    name: '中高级',
    flag: '🦅',
    color: 'purple',
    progress: 80,
    description: '能流利地进行工作和社交场合的对话，理解复杂文章，写出清晰详细的文章。',
    skills: ['流利交流', '商务谈判', '复杂写作', '文化理解'],
    courseNote: '超出本课程范围，需进一步专项学习'
  },
  {
    code: 'C1',
    name: '高级流利',
    flag: '🏆',
    color: 'gold',
    progress: 90,
    description: '能在各种社交、学术和职业场合灵活、有效地使用印尼语，表达流利自然。',
    skills: ['学术表达', '高阶写作', '细腻语感', '幽默理解'],
    courseNote: '母语接近水平，需长期沉浸式学习'
  }
]

const learningStages = [
  {
    id: 1, icon: '🔤', color: 'green', name: '发音基础',
    lessons: '1-8',
    description: '系统学习印尼语26个字母的发音规则，掌握特殊字母组合与声调节奏。',
    goals: ['掌握5个元音发音', '掌握特殊辅音组合', '能正确拼读任意印尼语单词']
  },
  {
    id: 2, icon: '📖', color: 'blue', name: '语法核心',
    lessons: '9',
    description: '学习印尼语基本句型结构，理解语法逻辑，为后续主题学习打好基础。',
    goals: ['理解主谓宾结构', '掌握否定与疑问句', '学会时态辅助词用法']
  },
  {
    id: 3, icon: '🗣️', color: 'purple', name: '主题词汇',
    lessons: '10-18',
    description: '围绕日常生活主题（爱好、日期、天气、购物、食堂等）学习实用词汇和对话。',
    goals: ['掌握900+核心词汇', '能在9个生活场景对话', '读懂日常印尼语文章']
  },
  {
    id: 4, icon: '🏭', color: 'gold', name: '职场应用',
    lessons: '19-21',
    description: '专注工厂、职场场景的印尼语应用，学习安全规定、工厂用语和跨文化沟通。',
    goals: ['掌握工厂安全用语', '能进行工作汇报对话', '理解职场文化差异']
  }
]

const xpSources = [
  { icon: '✅', action: '完成一道练习题', xp: 10 },
  { icon: '🎯', action: '连续答对5题', xp: 25 },
  { icon: '⚡', action: '完成一个课程章节', xp: 100 },
  { icon: '🏆', action: '通过 BOSS 关卡', xp: 200 },
  { icon: '🔥', action: '每日登录连续学习', xp: 30 },
  { icon: '💯', action: '章节满分完成', xp: 50 }
]

const levelTiers = [
  { level: 1, xp: 0,    icon: '🌱', title: '萌新学员',    highlight: false },
  { level: 2, xp: 200,  icon: '📖', title: '初级学者',    highlight: false },
  { level: 3, xp: 500,  icon: '⭐', title: '语言探索者',  highlight: false },
  { level: 4, xp: 800,  icon: '🔥', title: '进阶学员',    highlight: false },
  { level: 5, xp: 1200, icon: '💎', title: '精英学者',    highlight: true  },
  { level: 6, xp: 1600, icon: '🏆', title: '语言达人',    highlight: false },
  { level: 7, xp: 2000, icon: '👑', title: '印尼语大师',  highlight: false }
]

const badges = [
  {
    icon: '🌟',
    name: '初心者',
    description: '开始您的印尼语学习之旅',
    condition: '完成第一个课程章节',
    rarity: 'common',
    locked: false
  },
  {
    icon: '🔥',
    name: '七日连胜',
    description: '坚持就是胜利！',
    condition: '连续7天完成学习',
    rarity: 'rare',
    locked: false
  },
  {
    icon: '🎯',
    name: '完美挑战者',
    description: 'BOSS战绝对不失误',
    condition: 'BOSS 战卡中获得100%正确率',
    rarity: 'rare',
    locked: false
  },
  {
    icon: '📚',
    name: '词汇达人',
    description: '积累是成功的关键',
    condition: '累计学习500+个词汇',
    rarity: 'epic',
    locked: false
  },
  {
    icon: '🏆',
    name: '全课通关',
    description: '征服所有21课的传说！',
    condition: '完成全部21个课程章节',
    rarity: 'legendary',
    locked: false
  },
  {
    icon: '⚡',
    name: '速度之星',
    description: '快如闪电的学习达人',
    condition: '30秒内连续答对10道题',
    rarity: 'epic',
    locked: false
  },
  {
    icon: '💎',
    name: '精英学者',
    description: '学习是永无止境的',
    condition: '累计获得1000 XP经验值',
    rarity: 'legendary',
    locked: false
  }
]

const tips = [
  {
    icon: '⏰',
    title: '每日坚持',
    body: '每天学习15-20分钟效果远好于每周一次长时间学习。养成习惯是语言学习的关键。'
  },
  {
    icon: '🔁',
    title: '间隔重复',
    body: '利用游戏中的复习模式，在适当时间回顾之前章节，巩固记忆，防止遗忘。'
  },
  {
    icon: '🗣️',
    title: '大声朗读',
    body: '学到新单词和句子时，大声朗读几遍。听觉和口腔记忆相结合，效果事半功倍。'
  },
  {
    icon: '📝',
    title: '实际应用',
    body: '尝试在工作中使用学到的印尼语词汇。即使一天说一句，也能大幅提升实际运用能力。'
  },
  {
    icon: '🎮',
    title: '享受学习',
    body: '把每道题当成小挑战，把每个勋章当作成就感。享受学习过程，就不容易放弃。'
  },
  {
    icon: '👥',
    title: '和同事练习',
    body: '找到同样在学习印尼语的同事，互相出题、互相交流，学习效果翻倍。'
  }
]
</script>

<style scoped>
/* ── Base ──────────────────────────────────────────────────── */
.about-page {
  min-height: 100vh;
  color: #e2e8f0;
}

/* ── Hero ──────────────────────────────────────────────────── */
.about-hero {
  position: relative;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
  padding: 80px 20px 60px;
  overflow: hidden;
  text-align: center;
}

.hero-glow {
  position: absolute;
  top: -100px; left: 50%;
  transform: translateX(-50%);
  width: 600px; height: 600px;
  background: radial-gradient(ellipse, rgba(139, 92, 246, 0.3) 0%, transparent 70%);
  pointer-events: none;
}

.hero-content { position: relative; z-index: 1; max-width: 700px; margin: 0 auto; }

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 50px;
  padding: 6px 18px;
  font-size: 0.85rem;
  backdrop-filter: blur(10px);
}

.badge-icon { font-size: 1.1rem; }
.badge-label { color: #c4b5fd; font-weight: 600; }

.hero-title {
  font-size: clamp(2.2rem, 5vw, 3.5rem);
  font-weight: 900;
  background: linear-gradient(135deg, #fff 30%, #a78bfa 70%, #60a5fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 16px 0 12px;
  line-height: 1.1;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: rgba(255,255,255,0.65);
  margin-bottom: 40px;
}

.hero-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 20px 40px;
  backdrop-filter: blur(10px);
  display: inline-flex;
}

.stat-item { text-align: center; padding: 0 30px; }
.stat-num { display: block; font-size: 2rem; font-weight: 900; color: #a78bfa; }
.stat-label { font-size: 0.8rem; color: rgba(255,255,255,0.5); }
.stat-divider { width: 1px; height: 50px; background: rgba(255,255,255,0.15); }

/* ── Section Layout ────────────────────────────────────────── */
.section-container {
  padding: 60px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-container.alt-bg {
  background: rgba(255,255,255,0.02);
  max-width: 100%;
  padding: 60px 20px;
}

.section-container.alt-bg > * {
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.section-header { text-align: center; margin-bottom: 48px; }
.section-icon { font-size: 2.5rem; margin-bottom: 12px; display: block; }
.section-title {
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  font-weight: 800;
  color: #f1f5f9;
  margin-bottom: 12px;
}
.section-desc { color: rgba(255,255,255,0.55); max-width: 600px; margin: 0 auto; }
.subsection-title { font-size: 1.1rem; font-weight: 700; color: #c4b5fd; margin-bottom: 20px; }

/* ── Language Levels ───────────────────────────────────────── */
.levels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.level-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 24px;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
  cursor: default;
}

.level-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.4);
}

.level-green  { border-color: rgba(34,197,94,0.3); }
.level-green:hover  { border-color: rgba(34,197,94,0.7); box-shadow: 0 12px 40px rgba(34,197,94,0.15); }
.level-teal   { border-color: rgba(20,184,166,0.3); }
.level-teal:hover   { border-color: rgba(20,184,166,0.7); box-shadow: 0 12px 40px rgba(20,184,166,0.15); }
.level-blue   { border-color: rgba(59,130,246,0.3); }
.level-blue:hover   { border-color: rgba(59,130,246,0.7); box-shadow: 0 12px 40px rgba(59,130,246,0.15); }
.level-purple { border-color: rgba(139,92,246,0.3); }
.level-purple:hover { border-color: rgba(139,92,246,0.7); box-shadow: 0 12px 40px rgba(139,92,246,0.15); }
.level-gold   { border-color: rgba(234,179,8,0.3); }
.level-gold:hover   { border-color: rgba(234,179,8,0.7); box-shadow: 0 12px 40px rgba(234,179,8,0.15); }

.level-badge {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.level-code {
  font-size: 1.6rem;
  font-weight: 900;
  font-family: 'Outfit', monospace;
  color: #fff;
}

.level-flag { font-size: 1.8rem; }

.level-name { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; margin-bottom: 8px; }
.level-desc { font-size: 0.85rem; color: rgba(255,255,255,0.55); line-height: 1.6; margin-bottom: 14px; }

.level-skills { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
.skill-tag {
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 6px;
  padding: 2px 10px;
  font-size: 0.75rem;
  color: #c4b5fd;
}

.level-progress-bar {
  height: 4px;
  background: rgba(255,255,255,0.08);
  border-radius: 2px;
  margin-bottom: 12px;
  overflow: hidden;
}

.level-progress-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 1s ease;
}

.level-green  .level-progress-fill { background: linear-gradient(90deg, #22c55e, #16a34a); }
.level-teal   .level-progress-fill { background: linear-gradient(90deg, #14b8a6, #0d9488); }
.level-blue   .level-progress-fill { background: linear-gradient(90deg, #3b82f6, #2563eb); }
.level-purple .level-progress-fill { background: linear-gradient(90deg, #8b5cf6, #7c3aed); }
.level-gold   .level-progress-fill { background: linear-gradient(90deg, #eab308, #ca8a04); }

.level-course-note {
  font-size: 0.78rem;
  color: rgba(255,255,255,0.4);
  background: rgba(255,255,255,0.04);
  border-radius: 6px;
  padding: 6px 10px;
}

/* ── Roadmap ───────────────────────────────────────────────── */
.roadmap {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  position: relative;
}

.roadmap-stage { position: relative; }

.stage-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px;
  padding: 28px 24px;
  height: 100%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stage-card:hover { transform: translateY(-4px); }

.stage-green  { border-color: rgba(34,197,94,0.3); }
.stage-green:hover  { box-shadow: 0 12px 30px rgba(34,197,94,0.1); }
.stage-blue   { border-color: rgba(59,130,246,0.3); }
.stage-blue:hover   { box-shadow: 0 12px 30px rgba(59,130,246,0.1); }
.stage-purple { border-color: rgba(139,92,246,0.3); }
.stage-purple:hover { box-shadow: 0 12px 30px rgba(139,92,246,0.1); }
.stage-gold   { border-color: rgba(234,179,8,0.3); }
.stage-gold:hover   { box-shadow: 0 12px 30px rgba(234,179,8,0.1); }

.stage-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }

.stage-number {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 1.1rem;
  color: white;
}

.stage-icon { font-size: 2rem; }
.stage-name { font-size: 1.1rem; font-weight: 800; color: #f1f5f9; margin-bottom: 4px; }
.stage-lessons { font-size: 0.78rem; color: #a78bfa; font-weight: 600; margin-bottom: 12px; }
.stage-desc { font-size: 0.85rem; color: rgba(255,255,255,0.55); line-height: 1.6; margin-bottom: 16px; }

.goal-item { font-size: 0.82rem; color: rgba(255,255,255,0.65); display: flex; align-items: flex-start; gap: 8px; margin-bottom: 6px; }
.goal-check { color: #22c55e; font-weight: 700; flex-shrink: 0; }

/* ── XP System ─────────────────────────────────────────────── */
.xp-system {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
}

@media (max-width: 768px) { .xp-system { grid-template-columns: 1fr; } }

.xp-sources { display: flex; flex-direction: column; gap: 12px; }

.xp-source-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 14px 18px;
  transition: all 0.2s ease;
}

.xp-source-card:hover {
  background: rgba(255,255,255,0.07);
  transform: translateX(4px);
}

.xp-source-icon { font-size: 1.4rem; }
.xp-source-info { display: flex; justify-content: space-between; align-items: center; flex: 1; }
.xp-source-action { font-size: 0.9rem; color: rgba(255,255,255,0.7); }
.xp-source-amount { font-weight: 800; color: #a78bfa; font-size: 1rem; }

.level-tiers { display: flex; flex-direction: column; gap: 10px; }

.tier-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 16px;
  border-radius: 10px;
  background: rgba(255,255,255,0.03);
  border: 1px solid transparent;
  transition: all 0.2s ease;
}

.tier-item:hover { background: rgba(255,255,255,0.06); }
.tier-highlight { background: rgba(139,92,246,0.1); border-color: rgba(139,92,246,0.3); }

.tier-level { display: flex; align-items: center; gap: 8px; min-width: 80px; }
.tier-icon { font-size: 1.2rem; }
.tier-lv { font-weight: 800; font-size: 0.9rem; color: #c4b5fd; }

.tier-bar-wrap { flex: 1; display: flex; align-items: center; gap: 10px; }
.tier-bar { flex: 1; height: 6px; background: rgba(255,255,255,0.08); border-radius: 3px; overflow: hidden; }
.tier-bar-fill { height: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6); border-radius: 3px; }
.tier-xp { font-size: 0.75rem; color: rgba(255,255,255,0.4); min-width: 55px; text-align: right; }

.tier-title { font-size: 0.82rem; color: rgba(255,255,255,0.65); min-width: 90px; text-align: right; }

/* ── Badges ────────────────────────────────────────────────── */
.badges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

.badge-card {
  position: relative;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 28px 24px;
  text-align: center;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.badge-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 20px 50px rgba(139,92,246,0.2);
  border-color: rgba(139,92,246,0.4);
}

.badge-glow {
  position: absolute;
  top: -50px; left: 50%;
  transform: translateX(-50%);
  width: 200px; height: 200px;
  background: radial-gradient(ellipse, rgba(139,92,246,0.12), transparent 70%);
  pointer-events: none;
}

.badge-icon-wrap {
  width: 70px; height: 70px;
  background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(99,102,241,0.1));
  border: 2px solid rgba(139,92,246,0.3);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  font-size: 2rem;
  transition: transform 0.3s ease;
}

.badge-card:hover .badge-icon-wrap { transform: scale(1.1) rotate(5deg); }

.badge-name { font-size: 1rem; font-weight: 800; color: #f1f5f9; margin-bottom: 8px; }
.badge-desc { font-size: 0.82rem; color: rgba(255,255,255,0.5); line-height: 1.6; margin-bottom: 14px; }

.badge-condition {
  font-size: 0.78rem;
  background: rgba(255,255,255,0.04);
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 12px;
  text-align: left;
}

.condition-label { color: rgba(255,255,255,0.35); }
.condition-text { color: rgba(255,255,255,0.65); }

.badge-rarity {
  display: inline-block;
  border-radius: 20px;
  padding: 3px 14px;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.rarity-common    { background: rgba(100,100,100,0.2); color: #9ca3af; border: 1px solid rgba(100,100,100,0.3); }
.rarity-rare      { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.rarity-epic      { background: rgba(139,92,246,0.15); color: #a78bfa; border: 1px solid rgba(139,92,246,0.3); }
.rarity-legendary { background: rgba(234,179,8,0.15); color: #fbbf24; border: 1px solid rgba(234,179,8,0.3); }

/* ── Tips ──────────────────────────────────────────────────── */
.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.tip-card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 24px;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.tip-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.3);
  border-color: rgba(255,255,255,0.15);
}

.tip-icon { font-size: 2rem; display: block; margin-bottom: 12px; }
.tip-title { font-size: 1rem; font-weight: 700; color: #f1f5f9; margin-bottom: 8px; }
.tip-body { font-size: 0.85rem; color: rgba(255,255,255,0.55); line-height: 1.7; margin: 0; }

/* ── CTA ───────────────────────────────────────────────────── */
.cta-section {
  background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.15));
  border-top: 1px solid rgba(139,92,246,0.2);
  border-bottom: 1px solid rgba(139,92,246,0.2);
  padding: 70px 20px;
  text-align: center;
}

.cta-content { max-width: 560px; margin: 0 auto; }
.cta-title {
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  font-weight: 900;
  color: #f1f5f9;
  margin-bottom: 12px;
}
.cta-desc { color: rgba(255,255,255,0.55); font-size: 1.05rem; margin-bottom: 32px; }

.cta-btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  text-decoration: none;
  padding: 14px 36px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 1.05rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 20px rgba(99,102,241,0.4);
}

.cta-btn:hover {
  background: linear-gradient(135deg, #7c7ff3, #9f7aea);
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(99,102,241,0.5);
  color: white;
}

.btn-arrow {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.cta-btn:hover .btn-arrow { transform: translateX(4px); }
</style>
