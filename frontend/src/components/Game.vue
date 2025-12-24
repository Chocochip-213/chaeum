<template>
  <div class="game-container">
    <div class="game-header">
      <h2 class="game-title">분석 중입니다...</h2>
      <p class="game-desc">기다리는 동안 사과를 모아보세요! (현재 점수: {{ localScore }}점)</p>
    </div>
    <canvas ref="gameCanvas" width="600" height="400" class="game-canvas"></canvas>
    <p class="game-guide">마우스나 터치로 바구니를 이동하세요</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['update-score'])

const gameCanvas = ref(null)
const localScore = ref(0)
let animationFrameId = null
let gameLoopActive = false

const basket = { x: 250, y: 350, width: 60, height: 20, speed: 8 }
const apples = []
const appleRadius = 10
const spawnRate = 40
let frameCount = 0

const startGame = () => {
  const canvas = gameCanvas.value
  if (!canvas) return

  canvas.addEventListener('mousemove', handleInput)
  canvas.addEventListener('touchmove', handleInput, { passive: false })
  canvas.addEventListener('touchstart', handleInput, { passive: false })

  gameLoopActive = true
  apples.length = 0
  localScore.value = 0
  basket.x = canvas.width / 2 - basket.width / 2

  gameLoop()
}

const stopGame = () => {
  gameLoopActive = false
  if (animationFrameId) cancelAnimationFrame(animationFrameId)

  const canvas = gameCanvas.value
  if (canvas) {
    canvas.removeEventListener('mousemove', handleInput)
    canvas.removeEventListener('touchmove', handleInput)
    canvas.removeEventListener('touchstart', handleInput)
  }
}

// 마우스와 터치 입력을 통합 처리하는 함수
const handleInput = (e) => {
  const canvas = gameCanvas.value
  if (!canvas) return

  // 모바일에서 게임 조작 중 화면 스크롤 방지
  if (e.type === 'touchmove' || e.type === 'touchstart') {
    e.preventDefault()
  }

  const rect = canvas.getBoundingClientRect()

  // 마우스 또는 터치 좌표 가져오기
  let clientX
  if (e.touches && e.touches.length > 0) {
    clientX = e.touches[0].clientX
  } else {
    clientX = e.clientX
  }

  const scaleX = canvas.width / rect.width

  const canvasX = (clientX - rect.left) * scaleX

  basket.x = canvasX - basket.width / 2

  if (basket.x < 0) basket.x = 0
  if (basket.x + basket.width > canvas.width) basket.x = canvas.width - basket.width
}

const gameLoop = () => {
  if (!gameLoopActive) return
  update()
  draw()
  animationFrameId = requestAnimationFrame(gameLoop)
}

const update = () => {
  const canvas = gameCanvas.value
  if (!canvas) return
  frameCount++

  // 사과 생성
  if (frameCount % spawnRate === 0) {
    const x = Math.random() * (canvas.width - appleRadius * 2) + appleRadius
    apples.push({ x, y: 0, speed: Math.random() * 2 + 2 })
  }

  // 사과 이동 및 충돌 체크
  for (let i = apples.length - 1; i >= 0; i--) {
    const apple = apples[i]
    apple.y += apple.speed

    // 바구니와 충돌
    if (
      apple.y + appleRadius >= basket.y &&
      apple.y - appleRadius <= basket.y + basket.height &&
      apple.x >= basket.x &&
      apple.x <= basket.x + basket.width
    ) {
      localScore.value += 10
      emit('update-score', localScore.value)
      apples.splice(i, 1)
      continue
    }

    // 바닥에 닿음
    if (apple.y > canvas.height) {
      apples.splice(i, 1)
    }
  }
}

const draw = () => {
  const canvas = gameCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  // 배경
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  ctx.fillStyle = '#f9fafb'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  // 바구니
  ctx.fillStyle = '#111'
  ctx.beginPath()
  if (ctx.roundRect) {
    ctx.roundRect(basket.x, basket.y, basket.width, basket.height, 5)
  } else {
    ctx.rect(basket.x, basket.y, basket.width, basket.height)
  }
  ctx.fill()

  // 사과
  ctx.fillStyle = '#ef4444'
  apples.forEach((apple) => {
    ctx.beginPath()
    ctx.arc(apple.x, apple.y, appleRadius, 0, Math.PI * 2)
    ctx.fill()

    // 사과 꼭지
    ctx.strokeStyle = '#374151'
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(apple.x, apple.y - appleRadius)
    ctx.lineTo(apple.x + 3, apple.y - appleRadius - 5)
    ctx.stroke()
  })
}

onMounted(() => {
  startGame()
})

onUnmounted(() => {
  stopGame()
})
</script>

<style scoped>
.game-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #fff;
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  animation: fadeIn 0.3s ease;
}

.game-header {
  text-align: center;
  margin-bottom: 20px;
}

.game-title {
  font-size: 20px;
  font-weight: 700;
  color: #111;
  margin-bottom: 8px;
}

.game-desc {
  color: #666;
  font-size: 15px;
}

.game-canvas {
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  background-color: #f9fafb;
  cursor: none;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);

  width: 100%;
  max-width: 600px;
  height: auto;
  aspect-ratio: 3 / 2;

  touch-action: none;
}

.game-guide {
  margin-top: 16px;
  font-size: 13px;
  color: #9ca3af;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
