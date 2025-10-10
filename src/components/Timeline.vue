<template>
  <div class="timeline">
    <v-toolbar density="comfortable" color="transparent" flat>
      <v-toolbar-title class="text-h6">Eras</v-toolbar-title>
      <v-spacer />
      <v-btn-toggle v-model="sortOrder" mandatory>
        <v-btn value="old-to-new" size="small" variant="outlined">
          <v-icon size="small" class="me-1">mdi-sort-calendar-ascending</v-icon>
          Old → New
        </v-btn>
        <v-btn value="new-to-old" size="small" variant="outlined">
          <v-icon size="small" class="me-1">mdi-sort-calendar-descending</v-icon>
          New → Old
        </v-btn>
      </v-btn-toggle>
    </v-toolbar>
    <v-divider class="mb-2" />

    <v-timeline side="start" density="compact" line-inset="8" truncate-line="both">
      <v-timeline-item v-for="era in displayedEras" :key="era.id" :dot-color="'secondary'"
        :icon="store.selectedEraId === era.id ? 'mdi-star' : 'mdi-circle'">
        <template #opposite>
          <div class="years-display">
            <div class="year">{{ era.years }}</div>
            <div class="year-marker"></div>
          </div>
        </template>
        <div class="era-card" @click="open(era.id)" @keyup.enter="open(era.id)" role="button" tabindex="0">
          <!-- Year badge in top-left corner -->
          <div class="era-year-badge">{{ era.years }}</div>

          <v-img :src="withBase(era.image)" aspect-ratio="16/9" class="era-img" cover>
            <template #placeholder>
              <div class="skeleton" />
            </template>
          </v-img>
          <div class="era-meta">
            <div class="title">{{ era.title }}</div>
            <div class="advancement" v-if="era.keyAdvancement">{{ era.keyAdvancement }}</div>
            <div class="summary">{{ era.summary }}</div>
            <v-btn size="small" color="accent" variant="tonal" class="mt-2">Explore</v-btn>
          </div>
        </div>
      </v-timeline-item>
    </v-timeline>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMuseumStore } from '@/stores/museum'

const store = useMuseumStore()
const reverseOrder = ref(false)

const displayedEras = computed(() => {
  return reverseOrder.value ? [...store.eras].reverse() : store.eras
})

const sortOrder = computed({
  get: () => reverseOrder.value ? 'new-to-old' : 'old-to-new',
  set: (value: string) => {
    reverseOrder.value = value === 'new-to-old'
  }
})

function withBase(path: string) {
  const base = import.meta.env.BASE_URL || '/'
  return `${base}${path.replace(/^\//, '')}`
}

function open(id: string) { store.openEra(id) }
</script>

<style scoped>
.timeline {
  padding: 12px 12px 24px;
  position: relative;
}

.era-card {
  position: relative;
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 12px;
  align-items: center;
  padding: 10px;
  border-radius: 12px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.02));
  border: 1px solid rgba(255, 255, 255, 0.08);
  cursor: pointer;
  transition: transform .2s ease, box-shadow .2s ease;
}

.era-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, .3);
}

.era-img {
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.era-year-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: rgba(34, 211, 238, 0.9);
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.85rem;
  z-index: 2;
  backdrop-filter: blur(4px);
  font-variant-numeric: tabular-nums;
}

.skeleton {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(255, 255, 255, .06), rgba(255, 255, 255, .12), rgba(255, 255, 255, .06));
  background-size: 200% 100%;
  animation: shimmer 1.2s infinite;
}

.era-meta .title {
  font-weight: 700;
  font-size: 1.05rem;
}

.era-meta .advancement {
  font-size: 0.9rem;
  color: #22d3ee;
  font-weight: 600;
  margin-bottom: 4px;
}

.era-meta .summary {
  opacity: .8;
  font-size: .9rem;
}

.years-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.year {
  font-weight: 700;
  font-size: 1.1rem;
  color: #22d3ee;
  font-variant-numeric: tabular-nums;
  text-align: right;
  min-width: 80px;
}

.year-marker {
  width: 12px;
  height: 12px;
  background: linear-gradient(135deg, #22d3ee, #a78bfa);
  border-radius: 50%;
  opacity: 0.8;
}

@media (max-width: 600px) {
  .era-card {
    grid-template-columns: 1fr;
  }

  .year {
    min-width: 60px;
    font-size: 1rem;
  }

  .years-display {
    justify-content: flex-end;
  }
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }

  100% {
    background-position: -200% 0;
  }
}
</style>
