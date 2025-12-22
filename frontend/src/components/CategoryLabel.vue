<template>
  <span>
    <slot></slot>
  </span>
</template>

<script setup></script>

<style scoped>
span {
  padding: 10px 20px;
  color: #5c5c5c;
  font-weight: 500;
  border: 1px solid #e5e5e5;
  font-size: 16px;
  border-radius: 24px;
  background-color: #ffffff;
  cursor: pointer;
}

span:hover {
  color: #1a1a1a;
  border-color: #1a1a1a;
}
</style>
