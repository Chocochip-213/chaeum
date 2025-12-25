<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h3 class="modal-title">데모용 샘플 이력서 선택</h3>
        <button class="close-btn" @click="$emit('close')">
          <X :size="24" />
        </button>
      </div>

      <p class="modal-desc">
        테스트하고 싶은 직무의 샘플 이력서를 선택해주세요.<br />
        선택 시 기존 이력서는 대체됩니다.
      </p>

      <div class="sample-list">
        <button
          v-for="sample in samples"
          :key="sample.id"
          class="sample-item"
          :class="{ loading: loadingId === sample.id }"
          @click="loadSample(sample.id)"
          :disabled="!!loadingId"
        >
          <div class="sample-icon">
            <component :is="sample.icon" :size="20" />
          </div>
          <span class="sample-name">{{ sample.name }}</span>
          <Loader2 v-if="loadingId === sample.id" class="spinner" :size="16" />
          <ChevronRight v-else class="arrow" :size="16" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  X,
  ChevronRight,
  Server,
  Layout,
  Smartphone,
  BrainCircuit,
  Database,
  Loader2
} from 'lucide-vue-next'
import api from '@/api'

const emit = defineEmits(['close', 'success'])

const loadingId = ref(null)

const samples = [
  { id: 87, name: '백엔드 개발자 샘플', icon: Server },
  { id: 88, name: '프론트엔드 개발자 샘플', icon: Layout },
  { id: 89, name: '안드로이드 개발자 샘플', icon: Smartphone },
  { id: 90, name: 'AI 엔지니어 샘플', icon: BrainCircuit },
  { id: 91, name: '데이터 엔지니어 샘플', icon: Database },
]

const loadSample = async (id) => {
  if (loadingId.value) return
  loadingId.value = id

  try {
    await api.post('/resumes/sample/', { sample_id: id })
    alert('샘플 이력서가 성공적으로 로드되었습니다.')
    emit('success')
    emit('close')
  } catch (error) {
    console.error('샘플 로드 실패:', error)
    alert('샘플 데이터를 불러오는 중 오류가 발생했습니다.')
  } finally {
    loadingId.value = null
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center; /* 모달이 좀 더 위에 뜨도록 조정 가능하지만 중앙 정렬이 기본 */
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modal-content {
  background-color: white;
  border-radius: 20px;
  width: 90%;
  max-width: 400px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  position: relative;
  animation: slideUp 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: #111;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #9ca3af;
  padding: 4px;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #111;
}

.modal-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 24px;
  line-height: 1.5;
}

.sample-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sample-item {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 16px;
  border: 1px solid #eee;
  border-radius: 12px;
  background-color: white;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.sample-item:hover {
  border-color: #111;
  background-color: #f9fafb;
}

.sample-item.loading {
  opacity: 0.7;
  cursor: wait;
}

.sample-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background-color: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4b5563;
  margin-right: 16px;
}

.sample-name {
  flex-grow: 1;
  font-size: 15px;
  font-weight: 600;
  color: #374151;
}

.arrow {
  color: #cbd5e1;
}

.spinner {
  color: #111;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
