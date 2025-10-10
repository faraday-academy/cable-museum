<template>
  <div class="cable-builder">
    <h1 class="text-h4 mb-4">Cable Builder</h1>
    <p class="text-body-1 mb-6">Design your own custom cable by selecting components below. See a live preview and specs summary.</p>

    <v-row>
      <v-col cols="12" md="4">
        <v-card class="pa-4" elevation="2">
          <v-card-title>Components</v-card-title>
          <v-card-text>
            <v-select
              v-model="selectedWire"
              :items="wireOptions"
              label="Wire"
              item-title="name"
              item-value="id"
              clearable
              @update:model-value="onSelect('wire', $event)"
            />
            <v-select
              v-model="selectedInsulation"
              :items="insulationOptions"
              label="Insulation"
              item-title="name"
              item-value="id"
              clearable
              @update:model-value="onSelect('insulation', $event)"
            />
            <v-select
              v-model="selectedConnector"
              :items="connectorOptions"
              label="Connector"
              item-title="name"
              item-value="id"
              clearable
              @update:model-value="onSelect('connector', $event)"
            />
            <v-text-field v-model="cableName" label="Cable Name" class="mt-4" />
            <v-btn
              block
              color="primary"
              :disabled="!store.assembledCable || !cableName.trim()"
              @click="saveCable"
              class="mt-2"
            >
              Save Cable
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="pa-4" elevation="2">
          <v-card-title>Preview</v-card-title>
          <v-card-text class="d-flex justify-center">
            <CablePreview :cable="store.assembledCable" />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card class="pa-4" elevation="2">
          <v-card-title>Specs Summary</v-card-title>
          <v-card-text>
            <div v-if="store.assembledCable">
              <v-chip
                v-for="(spec, key) in store.assembledCable.totalSpecs"
                :key="key"
                size="small"
                color="secondary"
                class="me-1 mb-1"
              >
                {{ key }}: {{ spec }}
              </v-chip>
            </div>
            <p v-else class="text-body-2 text-medium-emphasis">Select all components to see specs</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="store.savedCables.length > 0">
      <v-col cols="12">
        <v-card class="pa-4" elevation="2">
          <v-card-title>Saved Cables</v-card-title>
          <v-card-text>
            <v-row>
              <v-col v-for="saved in store.savedCables" :key="saved.name" cols="12" md="6" lg="4">
                <v-card variant="outlined" class="pa-3">
                  <v-card-title class="text-h6">{{ saved.name }}</v-card-title>
                  <v-card-text>
                    <div class="saved-cable-parts">
                      <div v-if="saved.cable.wire" class="part">
                        <v-icon icon="mdi-cable-data" size="16" class="me-1" />
                        {{ saved.cable.wire.name }}
                      </div>
                      <div v-if="saved.cable.insulation" class="part">
                        <v-icon icon="mdi-shield" size="16" class="me-1" />
                        {{ saved.cable.insulation.name }}
                      </div>
                      <div v-if="saved.cable.connector" class="part">
                        <v-icon icon="mdi-connection" size="16" class="me-1" />
                        {{ saved.cable.connector.name }}
                      </div>
                    </div>
                  </v-card-text>
                  <v-card-actions>
                    <v-btn size="small" color="primary" @click="loadCable(saved)">Load</v-btn>
                    <v-spacer />
                    <v-btn size="small" color="error" variant="text" @click="deleteCable(saved)">Delete</v-btn>
                  </v-card-actions>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useMuseumStore, type CablePart } from '@/stores/museum'
import CablePreview from './CablePreview.vue'

const store = useMuseumStore()
const cableName = ref('')

const selectedWire = computed({
  get: () => store.selectedCable.wire?.id || null,
  set: (id: string | null) => store.selectPart('wire', findPart(id))
})

const selectedInsulation = computed({
  get: () => store.selectedCable.insulation?.id || null,
  set: (id: string | null) => store.selectPart('insulation', findPart(id))
})

const selectedConnector = computed({
  get: () => store.selectedCable.connector?.id || null,
  set: (id: string | null) => store.selectPart('connector', findPart(id))
})

const wireOptions = computed(() => store.cableParts.filter(p => p.type === 'wire'))
const insulationOptions = computed(() => store.cableParts.filter(p => p.type === 'insulation'))
const connectorOptions = computed(() => store.cableParts.filter(p => p.type === 'connector'))

function findPart(id: string | null): CablePart | null {
  return id ? store.cableParts.find(p => p.id === id) || null : null
}

function onSelect(type: 'wire' | 'insulation' | 'connector', id: string | null) {
  store.selectPart(type, findPart(id))
}

function saveCable() {
  if (store.assembledCable && cableName.value.trim()) {
    store.saveCable(cableName.value.trim())
    cableName.value = ''
    // Could add a snackbar notification here
  }
}

function loadCable(saved: { name: string; cable: any }) {
  store.selectedCable = { ...saved.cable }
}

function deleteCable(saved: { name: string; cable: any }) {
  const index = store.savedCables.findIndex(c => c.name === saved.name)
  if (index > -1) {
    store.savedCables.splice(index, 1)
  }
}
</script>

<style scoped>
.cable-builder { max-width: 1200px; margin: 0 auto; }
.saved-cable-parts .part { display: flex; align-items: center; margin-bottom: 4px; font-size: 0.9rem; }
</style>
