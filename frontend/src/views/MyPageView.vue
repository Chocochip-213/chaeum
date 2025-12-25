<template>
  <div class="my-page-container">
    <header class="profile-header">
      <div class="profile-avatar-lg">
        {{ nickname.charAt(0) }}
      </div>
      <div class="profile-info">
        <h1 class="profile-name">{{ nickname }}</h1>
        <p class="profile-email">{{ email }}</p>
      </div>
    </header>

    <nav class="tab-nav">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="tab-item"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
        type="button"
      >
        {{ tab.label }}
      </button>
    </nav>

    <main class="tab-content">
      <section v-if="activeTab === 'report'">
        <h2 class="section-title"><BarChart2 :size="20" /> 최근 분석 내역</h2>
        <div v-if="reports.length === 0" class="empty-state">최근 분석 내역이 없습니다.</div>
        <div class="report-list">
          <div
            v-for="report in reports"
            :key="report.id"
            class="report-card"
            @click="router.push(`/analysis/result/${report.id}`)"
          >
            <div class="report-info">
              <h3 class="report-job">
                {{ report.company_name }} · {{ formatDate(report.created_at) }}
              </h3>
              <p class="report-score">
                적합도 {{ report.score }}% · 부족 역량 {{ report.gap_missing_skills.length }}개
              </p>
            </div>
            <button class="arrow-btn" type="button">
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
            type="button"
          >
            내가 쓴 글
          </button>
          <button
            class="filter-btn"
            :class="{ active: activityFilter === 'comments' }"
            @click="activityFilter = 'comments'"
            type="button"
          >
            작성 댓글
          </button>
        </div>

        <div class="activity-list">
          <template v-if="activityFilter === 'posts'">
            <div v-if="myPosts.length === 0" class="empty-state">작성한 게시글이 없습니다.</div>
            <div
              v-else
              v-for="post in myPosts"
              :key="post.id"
              class="activity-card hover-effect"
              @click="router.push(`/community/${post.id}`)"
            >
              <div class="activity-main">
                <h3 class="post-title">{{ post.title }}</h3>
                <span class="post-date">{{ post.date }}</span>
              </div>
              <div class="activity-stats">
                <span class="stat"><Eye :size="14" /> {{ post.views }}</span>
                <span class="stat"><MessageSquare :size="14" /> {{ post.commentCount }}</span>
              </div>
            </div>
          </template>

          <template v-if="activityFilter === 'comments'">
            <div v-if="myComments.length === 0" class="empty-state">작성한 댓글이 없습니다.</div>
            <div
              v-else
              v-for="comment in myComments"
              :key="comment.id"
              class="activity-card"
              @click="router.push(`/community/${comment.post_id}`)"
            >
              <div class="activity-main">
                <h3 class="post-date">{{ comment.post_title }}</h3>
                <h3 class="post-title comment-content">{{ comment.content }}</h3>
                <span class="post-date">{{ formatDate(comment.created_at) }}</span>
              </div>
            </div>
          </template>
        </div>
      </section>

      <section v-if="activeTab === 'settings'">
        <div class="settings-grid">
          <div class="settings-card">
            <h3 class="card-title"><User :size="18" /> 프로필 정보</h3>

            <div class="form-group">
              <label>내 이력서</label>

              <input
                type="file"
                ref="fileInputRef"
                class="hidden-input"
                accept=".pdf"
                @change="handleFileChange"
              />

              <div
                class="upload-zone"
                :class="{ dragging: isDragging, 'has-file': !!resumeFileName }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
                @click="triggerFileInput"
              >
                <div v-if="resumeFileName" class="file-exists-state">
                  <div class="file-icon-wrapper">
                    <FileText :size="24" class="file-icon" />
                  </div>
                  <div class="file-info-text">
                    <span class="file-name">{{ resumeFileName }}</span>
                    <span class="last-update"
                      >마지막 업데이트: {{ formatDate(resumeFileDate) }}</span
                    >
                    <span class="file-action-text">클릭하거나 파일을 드래그하여 변경</span>
                  </div>
                </div>

                <div v-else class="upload-placeholder">
                  <div class="icon-circle">
                    <Upload :size="20" />
                  </div>
                  <p class="upload-main-text">이력서를 드래그하거나 클릭하여 업로드</p>
                  <p class="upload-sub-text">PDF</p>
                </div>
              </div>

              <!-- 샘플 데이터 로드 버튼 추가 -->
              <div class="sample-load-wrapper">
                <button class="text-btn" @click="showSampleModal = true" type="button">
                  <Sparkles :size="14" />
                  체험용 샘플 이력서 불러오기
                </button>
              </div>
            </div>
          </div>

          <div class="settings-card column-card">
            <div>
              <h3 class="card-title"><Settings :size="18" /> 계정 관리</h3>

              <div class="form-group">
                <label>이메일</label>
                <input type="text" :value="email" readonly class="input-readonly" />
              </div>

              <div class="form-group">
                <label>비밀번호</label>
                <button
                  v-if="!isChangingPassword"
                  @click="isChangingPassword = true"
                  class="link-btn"
                  type="button"
                >
                  비밀번호 변경하기
                </button>

                <div v-else class="password-form-container">
                  <input
                    type="password"
                    v-model="passwordForm.current"
                    placeholder="현재 비밀번호"
                    class="input-field"
                  />
                  <input
                    type="password"
                    v-model="passwordForm.new"
                    placeholder="새 비밀번호"
                    class="input-field"
                  />
                  <input
                    type="password"
                    v-model="passwordForm.confirm"
                    placeholder="새 비밀번호 확인"
                    class="input-field"
                    @keydown.enter="handleChangePassword"
                  />
                  <div class="form-actions">
                    <button @click="cancelPasswordChange" class="btn-cancel" type="button">
                      취소
                    </button>
                    <button @click="handleChangePassword" class="btn-save" type="button">
                      변경 완료
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <div class="logout-section">
              <div class="divider"></div>
              <button class="btn-logout" @click="handleLogout" type="button">
                <LogOut :size="16" /> 로그아웃
              </button>
            </div>
          </div>
        </div>

        <div class="danger-zone">
          <div class="danger-header">
            <div class="danger-icon-wrapper">
              <AlertTriangle :size="20" />
            </div>
            <div>
              <h3 class="danger-title">회원 탈퇴</h3>
              <p class="danger-desc">
                탈퇴 시 모든 데이터가 영구적으로 삭제되며 복구할 수 없습니다.
              </p>
            </div>
          </div>
          <button class="btn-danger-fill" @click="handleDeleteAccount" type="button">
            탈퇴하기
          </button>
        </div>
      </section>
    </main>

    <SampleResumeModal
      v-if="showSampleModal"
      @close="showSampleModal = false"
      @success="fetchUserResumes"
    />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import {
  BarChart2,
  ChevronRight,
  MessageSquare,
  User,
  FileText,
  Settings,
  LogOut,
  AlertTriangle,
  Eye,
  Upload,
  Sparkles // 추가
} from 'lucide-vue-next'

import api from '@/api'
import { useUserStore } from '@/stores/user'
import { useAuthStore } from '@/stores/auth'
import SampleResumeModal from '@/components/SampleResumeModal.vue' // 추가

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const authStore = useAuthStore()
const { nickname, email } = storeToRefs(userStore)

const activeTab = ref(route.query.tab || 'settings')
const activityFilter = ref('posts')
const isChangingPassword = ref(false)
const resumeFileDate = ref('')
const resumeFileName = ref('')
const myComments = ref([])
const myPosts = ref([])
const reports = ref([])
const passwordForm = ref({ current: '', new: '', confirm: '' })
const fileInputRef = ref(null)
const isDragging = ref(false)
const showSampleModal = ref(false) // 추가

watch(activeTab, (newTab) => {
  router.replace({ query: { ...route.query, tab: newTab } })
})

const tabs = [
  { id: 'report', label: '분석 리포트' },
  { id: 'activities', label: '내 활동' },
  { id: 'settings', label: '계정 설정' },
]

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

const cancelPasswordChange = () => {
  isChangingPassword.value = false
  passwordForm.value = { current: '', new: '', confirm: '' }
}

const triggerFileInput = () => {
  fileInputRef.value.click()
}

const handleFileChange = (event) => {
  const files = event.target.files
  if (files.length > 0) {
    processFile(files[0])
  }
}

const handleDrop = (event) => {
  isDragging.value = false
  const files = event.dataTransfer.files
  if (files.length > 0) {
    processFile(files[0])
  }
}

const processFile = async (file) => {
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    await api.post('/resumes/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    await fetchUserResumes()
  } catch (error) {
    console.error('이력서 업로드 실패:', error)
    alert('업로드 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.')

    if (fileInputRef.value) fileInputRef.value.value = ''
  }
}

const handleChangePassword = async () => {
  if (!passwordForm.value.current || !passwordForm.value.new || !passwordForm.value.confirm) {
    alert('모든 항목을 입력해주세요.')
    return
  }

  if (passwordForm.value.new != passwordForm.value.confirm) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }

  try {
    await api.post('/users/password/change/', {
      old_password: passwordForm.value.current,
      new_password: passwordForm.value.new,
    })

    alert('비밀번호가 성공적으로 변경되었습니다.')
    cancelPasswordChange()
  } catch (error) {
    console.error('비밀번호 변경 실패', error)

    if (error.response?.data?.old_password) {
      alert('현재 비밀번호가 일치하지 않습니다.')
    } else if (error.response?.data?.new_password?.[0]) {
      alert(error.response.data.new_password[0])
    } else {
      alert('비밀번호 변경 중 오류가 발생했습니다. 입력값을 확인해주세요.')
    }
  }
}

const handleLogout = async () => {
  try {
    const refreshToken = localStorage.getItem('refreshToken')
    if (refreshToken) {
      await api.post('/users/logout/', { refresh: refreshToken })
    }
  } catch (error) {
    console.error('로그아웃 API 호출 실패:', error)
  } finally {
    authStore.logout()
    userStore.$reset()
    router.push({ name: 'home' })
  }
}

const handleDeleteAccount = async () => {
  if (!confirm('정말로 탈퇴하시겠습니까? 이 작업은 되돌릴 수 없습니다.')) {
    return
  }

  try {
    await api.delete('/users/delete/')
    authStore.logout()
    userStore.$reset()
    alert('회원 탈퇴가 완료되었습니다.')
    router.push({ name: 'home' })
  } catch (error) {
    console.error('회원 탈퇴 실패:', error)
    alert('회원 탈퇴 중 오류가 발생했습니다. 다시 시도해 주세요.')
  }
}

const fetchMyPosts = async () => {
  try {
    const response = await api.get('/community/posts/my/')
    myPosts.value = response.data.map((post) => ({
      id: post.id,
      title: post.title,
      date: formatDate(post.created_at),
      views: post.view_count,
      commentCount: post.comments.length,
    }))
  } catch (error) {
    console.error('내 글 조회 중 오류 발생:', error)
  }
}

const fetchUserResumes = async () => {
  try {
    const response = await api.get('/resumes/')
    if (response.data && response.data.length > 0) {
      resumeFileName.value = response.data[0].file_name
      resumeFileDate.value = response.data[0].uploaded_at
    } else {
      resumeFileName.value = ''
    }
  } catch (error) {
    console.error('이력서 조회 중 오류 발생:', error)
  }
}
const fetchMyComments = async () => {
  try {
    const response = await api.get('/community/comments/my/')
    if (response.data) {
      myComments.value = response.data
    }
  } catch (error) {
    console.error('내 댓글 조회 중 오류 발생:', error)
  }
}

const fetchAnalysisHistory = async () => {
  try {
    const response = await api.get('/analysis/history/')
    if (response.data) {
      reports.value = response.data
    }
  } catch (error) {
    console.error('리포트 조회 중 오류 발생:', error)
  }
}

onMounted(() => {
  if (!userStore.userInfo) {
    userStore.fetchUserProfile()
  }
  fetchUserResumes()
  fetchMyComments()
  fetchMyPosts()
  fetchAnalysisHistory()
})
</script>

<style scoped>
.my-page-container {
  max-width: 1024px;
  margin: 0 auto;
  padding: 60px 20px 100px;
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
  cursor: pointer;
}

.report-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
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

.report-card:hover .arrow-btn {
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
  background-color: #fff;
  cursor: pointer;
}

.activity-card.hover-effect {
  cursor: pointer;
  transition: background-color 0.2s;
}

.activity-card.hover-effect:hover {
  background-color: #f9fafb;
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

.comment-content {
  font-weight: 500;
  color: #333;
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

.empty-state {
  text-align: center;
  padding: 40px 0;
  color: #888;
  font-size: 14px;
  background-color: #f9fafb;
  border-radius: 12px;
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
  background-color: white;
}

.column-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
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

.hidden-input {
  display: none;
}

.upload-zone {
  position: relative;
  width: 100%;
  height: 140px;
  border: 1px dashed #d1d5db;
  border-radius: 12px;
  background-color: #f9fafb;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
  overflow: hidden;
  box-sizing: border-box;
}

.upload-zone.dragging {
  border-color: #111;
  background-color: #f3f4f6;
  transform: scale(0.99);
}

.upload-zone.has-file {
  border: 1px solid #e5e7eb;
  background-color: white;
  justify-content: flex-start;
  padding: 0 24px;
}

.upload-placeholder {
  text-align: center;
  pointer-events: none;
}

.icon-circle {
  width: 40px;
  height: 40px;
  background-color: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  color: #666;
}

.upload-main-text {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 4px 0;
}

.upload-sub-text {
  font-size: 12px;
  color: #9ca3af;
  margin: 0;
}

.file-exists-state {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 16px;
}

.file-icon-wrapper {
  width: 48px;
  height: 48px;
}

.sample-load-wrapper {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

.text-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s;
}

.text-btn:hover {
  background-color: #f3f4f6;
  color: #111;
}


.file-info-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex-grow: 1;
  overflow: hidden;
  gap: 2px;
}

.file-name {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.last-update {
  font-size: 13px;
  color: #4b5563;
  margin-bottom: 4px;
}

.file-action-text {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 2px;
}

.file-icon-wrapper {
  width: 52px;
  height: 52px;
  background-color: #f3f4f6;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #374151;
  flex-shrink: 0;
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

.password-form-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background-color: #f9fafb;
  padding: 16px;
  border-radius: 8px;
  margin-top: 8px;
}

.input-field {
  width: 100%;
  padding: 12px;
  border: 1px solid #eee;
  background-color: white;
  border-radius: 6px;
  color: #111;
  font-size: 14px;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.input-field:focus {
  border-color: #111;
}

.form-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.btn-cancel {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  background-color: white;
  color: #666;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.btn-save {
  flex: 1;
  padding: 10px;
  border: 1px solid #111;
  background-color: #111;
  color: white;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.logout-section {
  margin-top: 32px;
}

.divider {
  height: 1px;
  background-color: #eee;
  margin-bottom: 16px;
}

.btn-logout {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background-color: white;
  color: #4b5563;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-logout:hover {
  background-color: #f3f4f6;
  color: #111;
}

.danger-zone {
  background-color: #fff5f5;
  border: 1px solid #fee2e2;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.danger-header {
  display: flex;
  gap: 16px;
  align-items: center;
}

.danger-icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #fee2e2;
  color: #dc2626;
  display: flex;
  align-items: center;
  justify-content: center;
}

.danger-title {
  color: #b91c1c;
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 4px 0;
}

.danger-desc {
  font-size: 14px;
  color: #7f1d1d;
  margin: 0;
}

.btn-danger-fill {
  background-color: #dc2626;
  border: 1px solid #dc2626;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.2s;
}

.btn-danger-fill:hover {
  background-color: #b91c1c;
}

@media (max-width: 768px) {
  .settings-grid {
    grid-template-columns: 1fr;
  }
  .danger-zone {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  .btn-danger-fill {
    width: 100%;
  }
}
</style>
