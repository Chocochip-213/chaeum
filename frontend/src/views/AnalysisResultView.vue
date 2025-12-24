<template>
  <div class="page-container">
    <div v-if="loading" class="state-container">
      <div class="spinner"></div>
      <p class="state-text">결과를 불러오는 중입니다...</p>
    </div>

    <div v-else-if="error" class="state-container">
      <p class="error-text">{{ error }}</p>
      <button @click="router.push('/')" class="back-link">메인으로 돌아가기</button>
    </div>

    <main v-else class="main-content animate-fade-in">
      <div class="report-header">
        <div class="header-left">
          <h1 class="page-title">분석 리포트</h1>
          <p class="sub-info">
            <span class="badge badge-target">TARGET</span>
            <span class="company-name">{{ analysisData.company_name || '회사명 정보 없음' }}</span>
          </p>
        </div>
        <div class="header-right">
          <button @click="$router.go(-1)" class="text-btn">이전 페이지로 돌아가기</button>
        </div>
      </div>

      <div class="grid-layout">
        <div class="left-column">
          <div class="card score-card">
            <p class="card-label centered"><Target :size="14" /> 직무 적합도</p>
            <div class="score-display">
              <span class="score-number">{{ scoreDisplay }}</span>
              <span class="score-unit">%</span>
            </div>
            <div class="progress-track">
              <div class="progress-fill" :style="{ width: scoreDisplay + '%' }"></div>
            </div>
          </div>

          <div class="card dark-card">
            <div class="dark-content">
              <h3 class="card-title light-text">
                <Brain :size="16" class="icon-yellow" />
                보완 필요 역량
              </h3>
              <ul class="missing-list">
                <li
                  v-for="skill in analysisData.gap_missing_skills"
                  :key="skill"
                  class="missing-item"
                >
                  <div class="dot"></div>
                  {{ skill }}
                </li>
                <li v-if="!analysisData.gap_missing_skills?.length" class="empty-text">
                  발견된 부족 역량이 없습니다.
                </li>
              </ul>
            </div>
            <div class="bg-icon">
              <BarChart2 :size="120" />
            </div>
          </div>

          <div class="card">
            <h3 class="card-title"><CheckCircle :size="16" class="icon-green" /> 보유 역량</h3>
            <div class="tag-container">
              <span
                v-for="skill in analysisData.user_extracted_skills"
                :key="skill"
                class="skill-tag user-tag"
              >
                {{ skill }}
              </span>
            </div>
          </div>

          <div class="card">
            <h3 class="card-title"><List :size="16" class="icon-blue" />채용공고 요구 역량</h3>
            <div class="tag-container">
              <span
                v-for="skill in analysisData.jd_required_skills"
                :key="skill"
                class="skill-tag jd-tag"
              >
                {{ skill }}
              </span>
            </div>
          </div>
        </div>

        <div class="right-column">
          <div class="card detail-card">
            <h2 class="section-title">
              <Briefcase :size="18" class="icon-brown" />
              주요 업무
            </h2>
            <ul class="task-list">
              <li
                v-for="(task, index) in analysisData.jd_main_tasks"
                :key="index"
                class="task-item"
              >
                <Check :size="14" class="check-icon" />
                <span>{{ task }}</span>
              </li>
            </ul>
          </div>

          <div class="card detail-card">
            <h2 class="section-title">
              <FileText :size="18" class="icon-brown" />
              분석 결과 및 피드백
            </h2>
            <div class="reasoning-text">
              {{ analysisData.reasoning }}
            </div>
          </div>

          <div class="card detail-card">
            <h2 class="section-title">
              <span class="badge badge-ai">AI 추천</span>
              맞춤형 학습 로드맵
            </h2>

            <div v-if="analysisData.rag_recommendations?.length" class="rag-container">
              <div
                v-for="(item, index) in analysisData.rag_recommendations"
                :key="index"
                class="rag-topic animate-slide-up"
                :style="{ animationDelay: `${index * 100}ms` }"
              >
                <div class="topic-header">
                  <span class="topic-badge">Topic {{ index + 1 }}</span>
                  <h3 class="topic-title">{{ item.query }}</h3>
                </div>

                <div class="book-list">
                  <div
                    v-for="(rec, rIndex) in item.recommendations"
                    :key="rIndex"
                    class="book-card group"
                    @click="router.push(`/books/${rec.isbn}`)"
                  >
                    <div class="book-content">
                      <div class="book-image-wrapper">
                        <img
                          v-if="bookCache[rec.isbn]?.cover"
                          :src="bookCache[rec.isbn].cover"
                          :alt="bookCache[rec.isbn].title"
                          class="book-cover"
                        />
                        <div v-else class="placeholder-icon">
                          <Book :size="20" />
                        </div>
                      </div>

                      <div class="book-info">
                        <h4 class="book-title">
                          {{ bookCache[rec.isbn]?.title || '도서 정보를 불러오는 중...' }}
                        </h4>

                        <p v-if="bookCache[rec.isbn]" class="book-meta">
                          {{ bookCache[rec.isbn].author }} | {{ bookCache[rec.isbn].publisher }}
                        </p>
                        <p v-else class="isbn-text">ISBN: {{ rec.isbn }}</p>

                        <div class="chapter-row">
                          <Bookmark :size="14" class="bookmark-icon" />
                          <p class="chapter-text" :title="rec.chapter">
                            {{ rec.chapter }}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">추천 도서 정보를 찾을 수 없습니다.</div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import aladinApi from '@/api/aladin'
import {
  Target,
  Brain,
  BarChart2,
  CheckCircle,
  List,
  Briefcase,
  Check,
  FileText,
  Book,
  Bookmark,
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref(null)
const analysisData = ref({})
const scoreDisplay = ref(0)
const bookCache = ref({})

const TTB_KEY = import.meta.env.VITE_ALADIN_TTB_KEY

const fetchAnalysisResult = async () => {
  try {
    const id = route.params.id
    if (!id) throw new Error('분석 ID가 없습니다.')

    const response = await api.get(`/analysis/${id}/`)
    analysisData.value = response.data

    animateScore(response.data.score || 0)

    if (response.data.rag_recommendations) {
      await fetchBookMetadata(response.data.rag_recommendations)
    }
  } catch (err) {
    console.error('결과 조회 실패:', err)
    error.value = '분석 결과를 불러오는데 실패했습니다.'
  } finally {
    loading.value = false
  }
}

const fetchBookMetadata = async (recommendations) => {
  const isbns = new Set()
  recommendations.forEach((topic) => {
    topic.recommendations?.forEach((rec) => {
      if (rec.isbn) isbns.add(rec.isbn)
    })
  })

  const promises = Array.from(isbns).map(async (isbn) => {
    if (bookCache.value[isbn]) return

    try {
      const response = await aladinApi.get('/ItemLookUp.aspx', {
        params: {
          ttbkey: TTB_KEY,
          ItemId: isbn,
          ItemIdType: 'ISBN13',
          output: 'js',
          Version: '20131101',
          Cover: 'Big',
        },
      })

      if (response.data.item && response.data.item.length > 0) {
        const item = response.data.item[0]
        bookCache.value[isbn] = {
          title: item.title,
          cover: item.cover,
          author: item.author,
          publisher: item.publisher,
          link: item.link,
        }
      } else {
        bookCache.value[isbn] = {
          title: '도서 정보를 찾을 수 없습니다',
          author: '-',
          publisher: '-',
          cover: null,
        }
      }
    } catch (e) {
      console.error(`ISBN ${isbn} 조회 실패:`, e)
      bookCache.value[isbn] = {
        title: '정보 로딩 실패',
        author: '-',
        publisher: '-',
        cover: null,
      }
    }
  })

  await Promise.all(promises)
}

const animateScore = (targetScore) => {
  let current = 0
  const duration = 1000
  const intervalTime = 10
  const steps = duration / intervalTime
  const increment = targetScore / steps

  const timer = setInterval(() => {
    current += increment
    if (current >= targetScore) {
      scoreDisplay.value = targetScore
      clearInterval(timer)
    } else {
      scoreDisplay.value = Math.floor(current)
    }
  }, intervalTime)
}

onMounted(() => {
  fetchAnalysisResult()
})
</script>

<style scoped>
.state-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 2px solid #e5e5e5;
  border-bottom-color: #1a1a1a;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.state-text {
  color: #6b7280;
}

.error-text {
  color: #ef4444;
  margin-bottom: 16px;
}

.back-link {
  background: none;
  border: none;
  text-decoration: underline;
  color: #6b7280;
  cursor: pointer;
  font-size: 14px;
}

.back-link:hover {
  color: #1f2937;
}

.main-content {
  max-width: 1024px;
  margin: 0 auto;
  padding: 32px 16px;
  width: 100%;
  flex: 1;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.report-header {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-bottom: 32px;
  gap: 16px;
}

@media (min-width: 768px) {
  .report-header {
    flex-direction: row;
    align-items: center;
  }
}

.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

.sub-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
  font-size: 14px;
  color: #5c5c5c;
}

.badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 700;
}

.badge-target {
  background-color: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #dbeafe;
}

.company-name {
  font-weight: 500;
}

.text-btn {
  background: none;
  border: none;
  border-bottom: 1px solid transparent;
  font-size: 14px;
  font-weight: 500;
  color: #5c5c5c;
  cursor: pointer;
  transition: all 0.2s;
}

.text-btn:hover {
  color: #1a1a1a;
  border-bottom-color: #1a1a1a;
}

.grid-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

@media (min-width: 768px) {
  .grid-layout {
    grid-template-columns: 1fr 2fr;
  }
}

.left-column,
.right-column {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card {
  background-color: white;
  border: 1px solid #e5e5e5;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.detail-card {
  padding: 32px;
}

.card-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 12px;
}

.centered {
  justify-content: center;
}

.score-card {
  text-align: center;
  transition: border-color 0.3s;
}

.score-display {
  margin-bottom: 16px;
  display: inline-block;
  line-height: 1;
}

.score-number {
  font-size: 48px;
  font-weight: 700;
  color: #1a1a1a;
  letter-spacing: -1px;
}

.score-unit {
  font-size: 20px;
  color: #9ca3af;
  margin-left: 2px;
}

.progress-track {
  width: 100%;
  height: 10px;
  background-color: #f3f4f6;
  border-radius: 9999px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background-color: #1a1a1a;
  border-radius: 9999px;
  transition: width 1s ease-out;
}

.dark-card {
  background-color: #2a2a2a;
  color: white;
  position: relative;
  overflow: hidden;
  border: none;
}

.dark-content {
  position: relative;
  z-index: 10;
}

.card-title {
  font-size: 14px;
  font-weight: 700;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1a1a1a;
}

.light-text {
  color: white;
}

.icon-yellow {
  color: #facc15;
}
.icon-green {
  color: #16a34a;
}
.icon-blue {
  color: #2563eb;
}
.icon-brown {
  color: #8d6e63;
}

.missing-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.missing-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 500;
  color: #d1d5db;
}

.dot {
  width: 6px;
  height: 6px;
  background-color: #9ca3af;
  border-radius: 50%;
}

.empty-text {
  font-size: 12px;
  color: #9ca3af;
}

.bg-icon {
  position: absolute;
  bottom: -20px;
  right: -20px;
  color: white;
  opacity: 0.05;
  pointer-events: none;
}

.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.skill-tag {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.user-tag {
  background-color: #f3f4f6;
  color: #4b5563;
  border: 1px solid #e5e7eb;
}

.jd-tag {
  background-color: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #dbeafe;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.task-list {
  list-style: none;
  padding: 20px;
  margin: 0;
  background-color: #f9fafb;
  border-radius: 8px;
  border: 1px solid #f3f4f6;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.task-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 14px;
  color: #374151;
}

.check-icon {
  margin-top: 4px;
  color: #8d6e63;
  flex-shrink: 0;
}

.reasoning-text {
  font-size: 14px;
  line-height: 1.6;
  color: #374151;
  white-space: pre-line;
}

.badge-ai {
  background-color: #fff7ed;
  color: #ea580c;
  border: 1px solid #ffedd5;
}

.rag-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.rag-topic {
  border-bottom: 1px solid #f3f4f6;
  padding-bottom: 32px;
}

.rag-topic:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.topic-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.topic-badge {
  background-color: #f3f4f6;
  color: #4b5563;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
}

.topic-title {
  font-size: 16px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.3;
}

.book-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.book-card {
  background-color: #f9fafb;
  border-radius: 12px;
  border: 1px solid #f3f4f6;
  padding: 16px;
  transition:
    border-color 0.2s,
    transform 0.2s;
  cursor: pointer;
  display: block;
}

.book-card:hover {
  border-color: #8d6e63;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.book-content {
  display: flex;
  gap: 16px;
}

.book-image-wrapper {
  flex-shrink: 0;
  width: 60px;
  height: 86px;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #9ca3af;
  overflow: hidden;
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-icon {
  color: #9ca3af;
}

.book-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.book-title {
  font-size: 15px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 4px 0;
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-meta {
  font-size: 12px;
  color: #6b7280;
  margin: 0 0 8px 0;
}

.isbn-text {
  font-size: 12px;
  color: #9ca3af;
  font-family: monospace;
  margin: 0 0 8px 0;
}

.chapter-row {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  background-color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid #f3f4f6;
  width: fit-content;
}

.bookmark-icon {
  color: #8d6e63;
  margin-top: 3px;
  flex-shrink: 0;
}

.chapter-text {
  font-size: 13px;
  font-weight: 500;
  color: #4b5563;
  margin: 0;
  line-height: 1.4;

  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.empty-state {
  text-align: center;
  padding: 32px 0;
  color: #9ca3af;
  font-size: 14px;
}

.animate-slide-up {
  opacity: 0;
  animation: slideUp 0.5s ease-out forwards;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
