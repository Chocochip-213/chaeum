<template>
  <div class="community-container">
    <header class="community-header">
      <div class="title-area">
        <h1 class="main-title">AI 커리어 분석</h1>
        <p class="sub-title">
          원하는 공고와 내 이력서를 비교해 합격 확률을 높이는 핵심 포인트를 짚어드려요.
        </p>
      </div>
    </header>

    <main class="analysis-content">
      <section class="analysis-section">
        <h2 class="section-label">1. 내 이력서 등록</h2>
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
              <span class="last-update"> 마지막 업데이트: {{ formatDate(resumeFileDate) }} </span>
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
      </section>

      <section class="analysis-section">
        <h2 class="section-label">2. 채용 공고 분석</h2>
        <div class="url-input-container">
          <div class="input-wrapper" :class="{ focused: isUrlFocused }">
            <LinkIcon :size="20" class="input-icon" />
            <input
              type="text"
              v-model="jobUrl"
              placeholder="채용 플랫폼 URL 입력 (원티드, 점핏)"
              class="url-input"
              @focus="isUrlFocused = true"
              @blur="isUrlFocused = false"
              @keydown.enter="handleEnter"
            />
          </div>
          <button class="analyze-btn" @click="handleAnalyze" :disabled="!jobUrl || !resumeFileName">
            <Sparkles :size="18" />
            분석하기
          </button>
        </div>
        <p class="helper-text">* 이력서가 등록되어 있어야 분석이 가능합니다.</p>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FileText, Upload, Link as LinkIcon, Sparkles } from 'lucide-vue-next'
import api from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const fileInputRef = ref(null)
const isDragging = ref(false)
const resumeFileName = ref('')
const resumeFileDate = ref('')

const jobUrl = ref('')
const isUrlFocused = ref(false)

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

const triggerFileInput = () => {
  fileInputRef.value.click()
}

const handleFileChange = (event) => {
  const files = event.target.files
  if (files.length > 0) processFile(files[0])
}

const handleDrop = (event) => {
  isDragging.value = false
  const files = event.dataTransfer.files
  if (files.length > 0) processFile(files[0])
}

const processFile = async (file) => {
  if (!file) return
  const formData = new FormData()
  formData.append('file', file)

  try {
    await api.post('/resumes/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    await fetchUserResumes()
    alert('이력서가 등록되었습니다.')
  } catch (error) {
    console.error('이력서 업로드 실패:', error)
    alert('업로드 중 오류가 발생했습니다.')
    if (fileInputRef.value) fileInputRef.value.value = ''
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
    console.error('이력서 조회 오류:', error)
  }
}

const checkPlatformUrl = (url) => {
  const targetUrl = url.trim()
  const isJumpit = targetUrl.includes('jumpit.saramin.co.kr/position/')
  const isWanted = targetUrl.includes('wanted.co.kr/wd/')
  return isJumpit || isWanted
}

const handleEnter = (e) => {
  if (e.isComposing) return
  handleAnalyze()
}

const handleAnalyze = async () => {
  if (!resumeFileName.value) {
    alert('먼저 이력서를 등록해주세요.')
    return
  }
  if (!jobUrl.value) {
    alert('채용 공고 URL을 입력해주세요.')
    return
  }

  if (!checkPlatformUrl(jobUrl.value)) {
    alert(
      '지원하지 않는 플랫폼입니다.\n점핏(Jumpit) 또는 원티드(Wanted) 채용 공고 분석 가능합니다.',
    )
    jobUrl.value = ''
    return
  }

  const formData = new FormData()
  formData.append('job_posting_url', jobUrl.value.trim())

  try {
    const response = await api.post('/analysis/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    console.log('분석 결과:', response)

    if (response.data && response.data.id) {
      router.push({ name: 'analysis-result', params: { id: response.data.id } })
    }
  } catch (error) {
    console.error('분석 요청 실패:', error)
  }
}

onMounted(() => {
  fetchUserResumes()
})
</script>

<style scoped>
.community-container {
  max-width: 720px;
  margin: 0 auto;
  padding: 60px 20px 100px;
  position: relative;
}

.community-header {
  margin-bottom: 40px;
}

.main-title {
  font-size: 28px;
  font-weight: 800;
  color: #111;
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.sub-title {
  color: #666;
  font-size: 15px;
  line-height: 1.5;
}

.analysis-content {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.analysis-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-label {
  font-size: 16px;
  font-weight: 700;
  color: #111;
  margin: 0;
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
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.last-update {
  font-size: 13px;
  color: #4b5563;
}

.file-action-text {
  font-size: 12px;
  color: #9ca3af;
}

.url-input-container {
  display: flex;
  gap: 12px;
  height: 52px;
}

.input-wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 0 16px;
  transition: all 0.2s ease;
}

.input-wrapper.focused {
  border-color: #111;
  background-color: #fff;
  box-shadow: 0 0 0 1px #111;
}

.input-icon {
  color: #9ca3af;
  margin-right: 12px;
  flex-shrink: 0;
}

.url-input {
  width: 100%;
  border: none;
  background: none;
  font-size: 15px;
  color: #111;
  outline: none;
}

.url-input::placeholder {
  color: #9ca3af;
}

.analyze-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 24px;
  background-color: #111;
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
}

.analyze-btn:hover:not(:disabled) {
  background-color: #333;
  transform: translateY(-1px);
}

.analyze-btn:disabled {
  background-color: #e5e7eb;
  color: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.helper-text {
  font-size: 13px;
  color: #9ca3af;
  margin: 0;
  padding-left: 4px;
}

@media (max-width: 600px) {
  .url-input-container {
    flex-direction: column;
    height: auto;
  }

  .input-wrapper {
    padding: 16px;
  }

  .analyze-btn {
    width: 100%;
    height: 50px;
    justify-content: center;
  }
}
</style>
