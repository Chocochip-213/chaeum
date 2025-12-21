<template>
  <div class="app-container">
    <AppHeader v-if="!route.meta.hideHeader" />
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView, useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'

const route = useRoute()
</script>

<style scoped></style>
