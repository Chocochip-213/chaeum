<template>
  <component :is="layout">
    <RouterView />
  </component>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import EmptyLayout from '@/layouts/EmptyLayout.vue'

const route = useRoute()

const layout = computed(() => {
  // 라우트 정보가 아직 로딩 중일 경우 레이아웃을 그리지 않도록 null 반환
  if (!route.name) return null

  // 라우트 정보가 확인된 후에 올바른 레이아웃을 반환
  return route.meta.layout === 'empty' ? EmptyLayout : DefaultLayout
})

</script>
