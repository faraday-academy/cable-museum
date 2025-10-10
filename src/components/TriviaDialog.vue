<template>
  <v-dialog v-model="show" max-width="500" persistent>
    <v-card>
      <v-card-title class="text-h6">Cable Trivia!</v-card-title>
      <v-card-text>
        <div v-if="!answered" class="question">
          <p class="mb-4">{{ currentTrivia?.question }}</p>
          <v-btn
            v-for="(option, index) in currentTrivia?.options"
            :key="index"
            block
            class="mb-2"
            @click="selectAnswer(index)"
          >
            {{ option }}
          </v-btn>
        </div>
        <div v-else class="result">
          <v-icon :color="isCorrect ? 'success' : 'error'" size="48" class="mb-2">
            {{ isCorrect ? 'mdi-check-circle' : 'mdi-close-circle' }}
          </v-icon>
          <p class="text-h6 mb-2">{{ isCorrect ? 'Correct!' : 'Not quite!' }}</p>
          <p>{{ currentTrivia?.fact }}</p>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn v-if="answered" color="primary" @click="close">Got it!</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useMuseumStore } from '@/stores/museum'

interface Trivia {
  question: string
  options: string[]
  correct: number
  fact: string
}

interface Props {
  trivia: Trivia[] | undefined
  eraId: string
  open: boolean
  manualOpen: boolean
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:manualOpen': [value: boolean]
}>()

const store = useMuseumStore()
const show = ref(false)
const answered = ref(false)
const selectedIndex = ref<number | null>(null)
const currentTrivia = ref<Trivia | null>(null)
const currentIndex = ref<number | null>(null)

const isCorrect = computed(() => selectedIndex.value === currentTrivia.value?.correct)

function selectTrivia(allowAnswered = false) {
  if (!props.trivia || props.trivia.length === 0) return

  let available = props.trivia
  if (!allowAnswered) {
    // Filter to unanswered
    available = props.trivia
      .map((_, index) => index)
      .filter(index => !store.isTriviaAnswered(props.eraId, index))
      .map(index => props.trivia![index])
  }

  if (available.length === 0) return // No trivia available

  const randomIndex = Math.floor(Math.random() * available.length)
  const selectedTrivia = allowAnswered ? available[randomIndex] : props.trivia[randomIndex]
  const selectedTriviaIndex = allowAnswered ? props.trivia.indexOf(selectedTrivia) : randomIndex

  currentTrivia.value = selectedTrivia
  currentIndex.value = selectedTriviaIndex
  answered.value = false
  selectedIndex.value = null
}

function selectAnswer(index: number) {
  selectedIndex.value = index
  answered.value = true
  // Mark as answered
  if (currentIndex.value !== null) {
    store.markTriviaAnswered(props.eraId, currentIndex.value)
  }
}

function close() {
  show.value = false
  answered.value = false
}

// Watch for open prop to trigger trivia
watch(() => props.open, (newVal: boolean) => {
  if (newVal) {
    setTimeout(() => {
      selectTrivia(false) // Only unanswered for auto
      if (currentTrivia.value) {
        show.value = true
      }
    }, 1000) // Delay 1 second after dialog opens
  }
})

// Watch for manual open
watch(() => props.manualOpen, (newVal: boolean) => {
  if (newVal) {
    selectTrivia(true) // Allow answered for manual
    show.value = true
    emit('update:manualOpen', false) // Reset
  }
})
</script>

<style scoped>
.question { text-align: center; }
.result { text-align: center; }
</style>
