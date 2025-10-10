<template>
  <div class="cable-explorer">
    <div class="text-subtitle-1 mb-4">Explorer Mode: Click to zoom, hover parts, watch data flow!</div>
    <div class="explorer-container" @click="toggleZoom">
      <svg
        :viewBox="zoomed ? '25 25 50 50' : '0 0 100 100'"
        class="explorer-svg"
        :class="{ zoomed }"
      >
        <!-- Background -->
        <rect width="100" height="100" fill="#f0f0f0" />

        <!-- Render SVG parts -->
        <g v-html="svgContent"></g>

        <!-- Overlay for parts -->
        <g v-for="part in parts" :key="part.name">
          <path
            :d="part.path"
            fill="transparent"
            stroke="none"
            @mouseover="highlightPart(part)"
            @mouseleave="unhighlightPart"
            class="part-overlay"
          />
        </g>

        <!-- Data particles -->
        <circle
          v-for="particle in particles"
          :key="particle.id"
          :cx="particle.x"
          :cy="particle.y"
          r="2"
          fill="#22d3ee"
          class="particle"
        />
      </svg>
    </div>
    <div class="controls mt-4">
      <v-btn @click="startFlow" color="primary" variant="outlined" class="me-2">
        <v-icon icon="mdi-play" class="me-1" />
        Start Data Flow
      </v-btn>
      <v-btn @click="stopFlow" color="error" variant="outlined">
        <v-icon icon="mdi-stop" class="me-1" />
        Stop
      </v-btn>
    </div>
    <div v-if="highlightedPart" class="highlight-info mt-2">
      <v-chip color="accent" variant="elevated">
        {{ highlightedPart.name }}
      </v-chip>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { gsap } from 'gsap'

interface Props {
  era: any
}

const props = defineProps<Props>()

const zoomed = ref(false)
const highlightedPart = ref<any>(null)
const particles = ref<Array<{ id: number; x: number; y: number }>>([])
const particleId = ref(0)
const flowInterval = ref<number | null>(null)

const svgContent = computed(() => props.era?.crossSection?.svg || '')
const parts = computed(() => props.era?.crossSection?.parts || [])

function toggleZoom() {
  zoomed.value = !zoomed.value
  gsap.to('.explorer-svg', {
    scale: zoomed.value ? 2 : 1,
    duration: 0.5,
    ease: 'power2.out'
  })
}

function highlightPart(part: any) {
  highlightedPart.value = part
  // Add glow effect or something
}

function unhighlightPart() {
  highlightedPart.value = null
}

function startFlow() {
  if (flowInterval.value) return
  flowInterval.value = setInterval(() => {
    const newParticle = {
      id: particleId.value++,
      x: 10, // start from left
      y: 50
    }
    particles.value.push(newParticle)

    // Animate particle across
    gsap.to(newParticle, {
      x: 90,
      duration: 3,
      ease: 'none',
      onComplete: () => {
        const index = particles.value.findIndex(p => p.id === newParticle.id)
        if (index > -1) particles.value.splice(index, 1)
      }
    })
  }, 500) // add new particle every 500ms
}

function stopFlow() {
  if (flowInterval.value) {
    clearInterval(flowInterval.value)
    flowInterval.value = null
  }
  particles.value = []
}

onUnmounted(() => {
  stopFlow()
})
</script>

<style scoped>
.cable-explorer { text-align: center; }
.explorer-container { cursor: pointer; display: inline-block; overflow: hidden; border-radius: 8px; border: 1px solid rgba(255,255,255,.1); }
.explorer-svg { width: 400px; height: 400px; transition: transform 0.5s; }
.zoomed { transform: scale(2); }
.part-overlay { cursor: pointer; }
.particle { opacity: 0.8; }
.highlight-info { display: flex; justify-content: center; }
</style>
