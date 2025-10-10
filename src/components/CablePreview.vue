<template>
  <svg width="300" height="150" viewBox="0 0 300 150" class="cable-preview">
    <defs>
      <linearGradient id="wireGrad" x1="0%" y1="0%" x2="100%" y3="0%">
        <stop offset="0%" :stop-color="wireColor" />
        <stop offset="100%" :stop-color="wireColor" stop-opacity="0.7" />
      </linearGradient>
    </defs>

    <!-- Connector -->
    <rect v-if="connector" x="10" y="60" width="40" height="30" rx="5" :fill="connector.color || '#c0c0c0'" />
    <text x="30" y="78" text-anchor="middle" fill="white" font-size="10">{{ connector?.name.split(' ')[0] }}</text>

    <!-- Cable body -->
    <rect v-if="insulation" x="50" y="55" width="200" height="40" rx="20" :fill="insulation.color || '#ffa500'" />
    <rect v-if="wire" x="60" y="65" width="180" height="20" rx="10" fill="url(#wireGrad)" />

    <!-- Wire label -->
    <text v-if="wire" x="150" y="78" text-anchor="middle" fill="white" font-size="12" font-weight="bold">
      {{ wire.name }}
    </text>

    <!-- Insulation label -->
    <text v-if="insulation" x="150" y="45" text-anchor="middle" fill="#333" font-size="10">
      {{ insulation.name }}
    </text>
  </svg>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  cable: any
}

const props = defineProps<Props>()

const wire = computed(() => props.cable?.parts.find((p: any) => p.type === 'wire'))
const insulation = computed(() => props.cable?.parts.find((p: any) => p.type === 'insulation'))
const connector = computed(() => props.cable?.parts.find((p: any) => p.type === 'connector'))

const wireColor = computed(() => wire.value?.color || '#b87333')
</script>

<style scoped>
.cable-preview { border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; background: rgba(0,0,0,0.05); }
</style>
