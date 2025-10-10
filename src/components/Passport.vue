<template>
  <div class="passport">
    <h1 class="text-h4 mb-4">Museum Passport</h1>
    <p class="text-body-1 mb-6">Track your exploration progress! Visit eras to unlock them in your passport.</p>

    <v-row>
      <v-col cols="12" md="8">
        <v-card class="pa-4" elevation="2">
          <v-card-title>Explored Eras</v-card-title>
          <v-card-text>
            <div class="era-grid">
              <div
                v-for="era in store.eras"
                :key="era.id"
                class="era-stamp"
                :class="{ visited: isVisited(era.id), locked: !isVisited(era.id) }"
                @click="isVisited(era.id) ? openEra(era.id) : null"
              >
                <v-img :src="withBase(era.image)" aspect-ratio="16/9" class="era-img" cover />
                <div class="era-overlay">
                  <div v-if="isVisited(era.id)" class="visited-stamp">
                    <v-icon icon="mdi-check-circle" color="success" size="48" class="stamp-icon" />
                    <div class="stamp-ribbon">Visited</div>
                  </div>
                  <div v-else class="locked-stamp">
                    <v-icon icon="mdi-lock" size="48" class="lock-icon" />
                    <div class="lock-text">Locked</div>
                  </div>
                </div>
                <div class="era-info" :class="{ 'info-hidden': !isVisited(era.id) }">
                  <div class="title">{{ era.title }}</div>
                  <div class="years">{{ era.years }}</div>
                  <div class="advancement" v-if="era.keyAdvancement && isVisited(era.id)">{{ era.keyAdvancement }}</div>
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="pa-4" elevation="2">
          <v-card-title>Progress Stats</v-card-title>
          <v-card-text>
            <div class="stats">
              <div class="stat">
                <v-icon icon="mdi-timeline" class="me-2" />
                <span>{{ store.visitedEras.length }} / {{ store.eras.length }} Eras Visited</span>
              </div>
              <div class="stat">
                <v-icon icon="mdi-brain" class="me-2" />
                <span>{{ totalTriviaAnswered }} Trivia Questions Answered</span>
              </div>
              <div class="stat">
                <v-icon icon="mdi-cable-data" class="me-2" />
                <span>{{ store.savedCables.length }} Cables Designed</span>
              </div>
            </div>
            <v-progress-circular
              :value="(store.visitedEras.length / store.eras.length) * 100"
              color="primary"
              size="80"
              class="mt-4"
            >
              {{ Math.round((store.visitedEras.length / store.eras.length) * 100) }}%
            </v-progress-circular>
          </v-card-text>
        </v-card>

        <v-card class="pa-4 mt-4" elevation="2" v-if="store.savedCables.length > 0">
          <v-card-title>Saved Cables</v-card-title>
          <v-card-text>
            <div class="saved-cables">
              <div v-for="cable in store.savedCables" :key="cable.name" class="cable-item">
                <v-icon icon="mdi-cable-data" class="me-2" />
                {{ cable.name }}
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useMuseumStore } from '@/stores/museum'

const store = useMuseumStore()

const totalTriviaAnswered = computed(() => {
  return Object.values(store.answeredTrivia).reduce((sum, arr) => sum + arr.length, 0)
})

function isVisited(eraId: string): boolean {
  return store.visitedEras.includes(eraId)
}

function openEra(eraId: string) {
  store.openEra(eraId)
}

function withBase(path: string) {
  const base = import.meta.env.BASE_URL || '/'
  return `${base}${path.replace(/^\//,'')}`
}
</script>

<style scoped>
.passport { max-width: 1200px; margin: 0 auto; }
.era-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.era-stamp { position: relative; border-radius: 12px; overflow: hidden; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
.era-stamp:hover { transform: scale(1.05); box-shadow: 0 8px 24px rgba(0,0,0,0.4); }
.era-stamp.visited { border: 3px solid #22d3ee; cursor: pointer; }
.era-stamp.locked { cursor: not-allowed; filter: grayscale(0.7) blur(0.5px); }
.era-overlay { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.6); }
.visited-stamp { position: relative; text-align: center; }
.stamp-icon { animation: bounce 1s ease-in-out; }
.stamp-ribbon { background: linear-gradient(45deg, #22d3ee, #a78bfa); color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; font-size: 0.8rem; margin-top: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.3); }
.locked-stamp { position: relative; text-align: center; }
.lock-icon { color: #666; animation: shake 0.5s ease-in-out; }
.lock-text { color: #999; font-weight: bold; margin-top: 8px; }
.era-info { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.9), transparent); padding: 12px; color: white; transition: opacity 0.3s; }
.era-info.info-hidden { opacity: 0.3; }
.era-info .title { font-weight: 700; font-size: 1rem; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }
.era-info .years { opacity: 0.8; font-size: 0.8rem; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }
.era-info .advancement { font-size: 0.75rem; color: #22d3ee; margin-top: 2px; text-shadow: 0 1px 2px rgba(0,0,0,0.8); }
@keyframes bounce { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
@keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-2px); } 75% { transform: translateX(2px); } }
.stats { display: flex; flex-direction: column; gap: 8px; }
.stat { display: flex; align-items: center; }
.cable-item { display: flex; align-items: center; padding: 4px 0; }
</style>
