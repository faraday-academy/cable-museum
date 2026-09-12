<template>
  <v-dialog v-model="store.dialogOpen" max-width="960" transition="dialog-bottom-transition">
    <v-card :color="'surface'" class="era-dialog">
      <v-card-title class="d-flex align-center justify-space-between">
        <div class="d-flex align-center gap-2">
          <v-icon icon="mdi-timeline" class="me-2" />
          <span class="text-h6">{{ store.selectedEra?.title }}</span>
          <span class="years">{{ store.selectedEra?.years }}</span>
        </div>
        <v-btn icon="mdi-close" variant="text" @click="store.closeDialog()" />
      </v-card-title>

      <v-tabs v-model="tab" color="primary">
        <v-tab value="overview">Overview</v-tab>
        <v-tab value="history" :disabled="!history">History</v-tab>
        <v-tab value="cross-section" :disabled="!spec">Cross-Section</v-tab>
        <v-tab value="explorer">Signal Flow</v-tab>
      </v-tabs>

      <v-card-text>
        <v-window v-model="tab">
          <v-window-item value="overview">
            <div class="grid">
              <div class="media">
                <v-img :src="withBase(store.selectedEra?.image || '')" aspect-ratio="16/9" cover class="rounded mb-3" />
                <div v-if="store.selectedEra?.video" class="video rounded">
                  <iframe
                    :src="store.selectedEra?.video"
                    :title="store.selectedEra?.videoTitle || 'Era video'"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowfullscreen
                  />
                </div>
              </div>

              <div class="content">
                <p class="mb-4">{{ store.selectedEra?.summary }}</p>

                <v-expand-transition>
                  <div v-if="store.selectedEra?.facts?.length" class="mb-4">
                    <div class="text-subtitle-1 mb-2">Fun facts</div>
                    <v-chip
                      v-for="(fact, i) in store.selectedEra?.facts"
                      :key="i"
                      size="small"
                      color="secondary"
                      variant="elevated"
                      class="me-2 mb-2"
                    >
                      {{ fact }}
                    </v-chip>
                  </div>
                </v-expand-transition>

                <div v-if="store.selectedEra?.links?.length" class="links">
                  <v-btn
                    v-for="(lnk, i) in store.selectedEra?.links"
                    :key="i"
                    :href="lnk.href"
                    target="_blank"
                    rel="noopener"
                    color="primary"
                    variant="tonal"
                    class="me-2 mb-2"
                  >
                    <v-icon icon="mdi-open-in-new" class="me-1" />
                    {{ lnk.label }}
                  </v-btn>
                </div>

                <div v-if="store.selectedEra?.gallery?.length" class="mt-4">
                  <div class="text-subtitle-1 mb-2">Gallery</div>
                  <div class="gallery">
                    <v-img
                      v-for="(img, i) in store.selectedEra?.gallery"
                      :key="i"
                      :src="withBase(img)"
                      aspect-ratio="16/10"
                      class="rounded"
                      cover
                    />
                  </div>
                </div>
              </div>
            </div>
          </v-window-item>

          <v-window-item value="history">
            <div class="pane">
              <CableHistory v-if="history" :history="history" />
            </div>
          </v-window-item>

          <v-window-item value="cross-section">
            <div class="pane">
              <p class="pane__tagline" v-if="spec">{{ spec.tagline }}</p>
              <CableCrossSection v-if="spec" :spec="spec" :title="store.selectedEra?.title" />
              <p v-else class="pane__empty">No construction data for this exhibit yet.</p>
            </div>
          </v-window-item>

          <v-window-item value="explorer">
            <div class="pane">
              <CableCutaway v-if="spec" :spec="spec" :title="store.selectedEra?.title" />
              <CableExplorer v-else :era="store.selectedEra" />
            </div>
          </v-window-item>
        </v-window>
      </v-card-text>

      <v-card-actions>
        <v-spacer />
        <v-btn v-if="store.selectedEra?.trivia" color="secondary" variant="outlined" @click="manualQuizOpen = true">
          <v-icon icon="mdi-brain" class="me-1" />
          Take Quiz
        </v-btn>
        <v-btn color="accent" variant="elevated" @click="store.closeDialog()">Close</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <TriviaDialog :trivia="store.selectedEra?.trivia" :eraId="store.selectedEra?.id || ''" :open="store.dialogOpen" v-model:manualOpen="manualQuizOpen" />
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useMuseumStore } from '@/stores/museum'
import CableExplorer from './CableExplorer.vue'
import CableCrossSection from './CableCrossSection.vue'
import CableCutaway from './CableCutaway.vue'
import CableHistory from './CableHistory.vue'
import TriviaDialog from './TriviaDialog.vue'

const store = useMuseumStore()
const tab = ref('overview')

/** Construction spec for the open era, if we have one. */
const history = computed(() => store.selectedEra?.history ?? null)

const spec = computed(() => {
  const id = store.selectedEraId
  return id ? store.cableSpecs[id] ?? null : null
})
const manualQuizOpen = ref(false)

function withBase(path: string) {
  const base = import.meta.env.BASE_URL || '/'
  return `${base}${path.replace(/^\//,'')}`
}

// Watch for dialog open to mark era as visited
watch(() => store.dialogOpen, (open: boolean) => {
  if (open && store.selectedEra) {
    store.markEraVisited(store.selectedEra.id)
  }
})
</script>

<style scoped>
.pane { padding: 4px 2px 8px; }

.pane__tagline {
  font-size: 1rem;
  color: var(--text);
  font-weight: 600;
  line-height: 1.5;
  margin: 0 0 18px;
  padding-left: 12px;
  border-left: 3px solid var(--copper);
}

.pane__empty { color: var(--text-muted); }

.grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 20px; }
.video { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border: 1px solid var(--line); }
.video iframe { position: absolute; top:0; left:0; width:100%; height:100%; }
.gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.rounded { border-radius: 10px; overflow: hidden; }
.years { opacity: .65; font-size: .9rem; margin-left: 8px; }
.cross-section { text-align: center; }
.cross-svg { display: inline-block; border: 1px solid var(--line); border-radius: 8px; padding: 20px; background: rgba(0,0,0,.05); }
.parts-list { text-align: left; }
@media (max-width: 940px){ .grid { grid-template-columns: 1fr; } .gallery { grid-template-columns: repeat(2, 1fr); } }
</style>
