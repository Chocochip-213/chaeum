<template>
  <div class="my-page-container">
    <header class="profile-header">
      <div class="profile-avatar-lg">
        {{ userInfo.nickname.charAt(0) }}
      </div>
      <div class="profile-info">
        <h1 class="profile-name">{{ userInfo.nickname }}</h1>
        <p class="profile-email">{{ userInfo.email }}</p>
      </div>
    </header>

    <nav class="tab-nav">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="tab-item"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
      </button>
    </nav>

    <main class="tab-content">
      <section v-if="activeTab === 'report'">
        <h2 class="section-title"><BarChart2 :size="20" /> 최근 분석 내역</h2>

        <div class="report-list">
          <div v-for="report in reports" :key="report.id" class="report-card">
            <div class="report-info">
              <div class="report-meta">
                <span class="company-badge">{{ report.company }}</span>
                <span class="date">{{ report.date }}</span>
              </div>
              <h3 class="report-job">{{ report.jobTitle }}</h3>
              <p class="report-score">
                적합도 {{ report.score }}% · 부족 역량 {{ report.missingSkills }}개
              </p>
            </div>
            <button class="arrow-btn">
              <ChevronRight :size="20" />
            </button>
          </div>
        </div>
      </section>

      <section v-if="activeTab === 'activities'">
        <div class="activity-filters">
          <button
            class="filter-btn"
            :class="{ active: activityFilter === 'posts' }"
            @click="activityFilter = 'posts'"
          >
            내가 쓴 글
          </button>
          <button
            class="filter-btn"
            :class="{ active: activityFilter === 'comments' }"
            @click="activityFilter = 'comments'"
          >
            작성 댓글
          </button>
        </div>

        <div class="activity-list">
          <div v-for="post in myPosts" :key="post.id" class="activity-card">
            <div class="activity-main">
              <h3 class="post-title">{{ post.title }}</h3>
              <span class="post-date">{{ post.date }}</span>
            </div>
            <div class="activity-stats">
              <span class="stat"><Eye :size="14" /> {{ post.likes }}</span>
              <span class="stat"><MessageSquare :size="14" /> {{ post.comments }}</span>
            </div>
          </div>
        </div>
      </section>

      <section v-if="activeTab === 'settings'">
        <div class="settings-grid">
          <div class="settings-card">
            <h3 class="card-title"><User :size="18" /> 프로필 정보</h3>

            <div class="form-group">
              <label>내 이력서</label>
              <div class="file-input-box">
                <div class="file-info">
                  <FileText :size="16" />
                  <span>{{ userInfo.resumeFile }}</span>
                </div>
                <button class="btn-sm">변경</button>
              </div>
            </div>

            <div class="form-group">
              <label>보유 스킬</label>
              <div class="skill-tags">
                <span v-for="skill in userInfo.skills" :key="skill" class="skill-tag">
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>

          <div class="settings-card">
            <h3 class="card-title"><Settings :size="18" /> 계정 관리</h3>

            <div class="form-group">
              <label>이메일</label>
              <input type="text" :value="userInfo.email" readonly class="input-readonly" />
            </div>

            <div class="form-group">
              <label>비밀번호</label>
              <button class="link-btn">비밀번호 변경하기</button>
            </div>
          </div>
        </div>

        <div class="danger-zone">
          <h3 class="danger-title">Danger Zone</h3>
          <div class="danger-actions">
            <button class="btn-danger-outline"><LogOut :size="16" /> 로그아웃</button>
            <button class="btn-danger-fill"><Trash2 :size="16" /> 회원 탈퇴</button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  BarChart2,
  ChevronRight,
  MessageSquare,
  User,
  FileText,
  Settings,
  LogOut,
  Trash2,
  Eye,
} from 'lucide-vue-next'

const activeTab = ref('report') // report, activities, settings
const activityFilter = ref('posts') // posts, comments

const tabs = [
  { id: 'report', label: '분석 리포트' },
  { id: 'activities', label: '내 활동' },
  { id: 'settings', label: '계정 설정' },
]

const userInfo = ref({
  nickname: '김싸피',
  email: 'ssafy@example.com',
  resumeFile: 'kim_resume_v2.pdf',
  skills: ['Java', 'Spring', 'MySQL'],
})

const reports = ref([
  {
    id: 1,
    company: 'Toss',
    date: '2024.05.20',
    jobTitle: '토스(Toss) Frontend Developer',
    score: 72,
    missingSkills: 2,
  },
  {
    id: 2,
    company: 'Naver',
    date: '2024.05.15',
    jobTitle: '네이버(Naver) Backend Engineer',
    score: 65,
    missingSkills: 2,
  },
  {
    id: 3,
    company: 'Karrot',
    date: '2024.05.01',
    jobTitle: '당근마켓 SRE',
    score: 45,
    missingSkills: 2,
  },
])

const myPosts = ref([
  { id: 1, title: '클린코드 3장 함수 요약 정리', date: '2024.05.21', likes: 5, comments: 2 },
  { id: 2, title: '면접 스터디 모집합니다 (서울캠)', date: '2024.05.18', likes: 8, comments: 12 },
])
</script>

<style scoped>
.my-page-container {
  max-width: 1024px;
  margin: 0 auto;
  padding: 60px 20px 100px;
  font-family:
    -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #111;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 40px;
}
.profile-avatar-lg {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  font-weight: 700;
  color: #4b5563;
}
.profile-name {
  font-size: 32px;
  font-weight: 800;
  margin: 0 0 8px 0;
}
.profile-email {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.tab-nav {
  display: flex;
  gap: 32px;
  border-bottom: 1px solid #eee;
  margin-bottom: 40px;
}
.tab-item {
  background: none;
  border: none;
  font-size: 16px;
  font-weight: 600;
  color: #888;
  padding-bottom: 12px;
  cursor: pointer;
  position: relative;
}
.tab-item.active {
  color: #111;
}
.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #111;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
}

.report-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.report-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 24px;
  background-color: white;
  transition: box-shadow 0.2s;
}
.report-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}
.report-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.company-badge {
  background-color: #f3f4f6;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 700;
  color: #333;
}
.date {
  font-size: 13px;
  color: #888;
}
.report-job {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 6px 0;
}
.report-score {
  font-size: 14px;
  color: #666;
  margin: 0;
}
.arrow-btn {
  background: none;
  border: none;
  color: #ccc;
  cursor: pointer;
}
.arrow-btn:hover {
  color: #111;
}

.activity-filters {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}
.filter-btn {
  padding: 8px 16px;
  border-radius: 20px;
  border: 1px solid #eee;
  background-color: white;
  font-size: 14px;
  font-weight: 600;
  color: #666;
  cursor: pointer;
}
.filter-btn.active {
  background-color: #111;
  color: white;
  border-color: #111;
}
.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.activity-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 20px;
}
.post-title {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 6px 0;
}
.post-date {
  font-size: 13px;
  color: #888;
}
.activity-stats {
  display: flex;
  gap: 12px;
  color: #666;
  font-size: 13px;
}
.stat {
  display: flex;
  align-items: center;
  gap: 4px;
}

.settings-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 40px;
}
.settings-card {
  border: 1px solid #eee;
  border-radius: 12px;
  padding: 24px;
}
.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 700;
  margin-bottom: 24px;
  margin-top: 0;
}
.form-group {
  margin-bottom: 24px;
}
.form-group:last-child {
  margin-bottom: 0;
}
.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #666;
  margin-bottom: 8px;
}
.file-input-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f9fafb;
  padding: 12px;
  border-radius: 8px;
}
.file-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #333;
}
.btn-sm {
  font-size: 13px;
  font-weight: 600;
  border: none;
  background: none;
  cursor: pointer;
  color: #111;
}
.skill-tags {
  display: flex;
  gap: 8px;
}
.skill-tag {
  background-color: #f3f4f6;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #333;
}
.input-readonly {
  width: 100%;
  padding: 12px;
  border: 1px solid #eee;
  background-color: #f9fafb;
  border-radius: 8px;
  color: #555;
  outline: none;
  box-sizing: border-box;
}
.link-btn {
  background: none;
  border: none;
  padding: 0;
  font-size: 14px;
  text-decoration: underline;
  cursor: pointer;
  color: #111;
}

.danger-zone {
  background-color: #fef2f2;
  border-radius: 12px;
  padding: 24px;
}
.danger-title {
  color: #b91c1c;
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 16px 0;
}
.danger-actions {
  display: flex;
  gap: 12px;
}
.btn-danger-outline {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: white;
  border: 1px solid #fee2e2;
  color: #ef4444;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
.btn-danger-fill {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background-color: #dc2626;
  border: 1px solid #dc2626;
  color: white;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

@media (max-width: 768px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
}
</style>
