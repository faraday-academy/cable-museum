<template>
  <div class="hist">
    <!-- ── 1. THREE BEATS — the first thing you see ── -->
    <ol class="beats">
      <li v-for="(b, i) in beats" :key="b.key" class="beat" :style="{ '--i': i }">
        <span class="beat__num">{{ i + 1 }}</span>
        <div class="beat__body">
          <h4 class="beat__head">{{ b.head }}</h4>
          <p class="beat__text">{{ b.text }}</p>
        </div>
      </li>
    </ol>

    <!-- ── 2. MILESTONE SPINE — the cable's whole life ── -->
    <section v-if="milestones.length" class="spine">
      <h4 class="hist__title">
        <v-icon icon="mdi-timeline-clock-outline" size="17" />
        The whole life of this cable
      </h4>

      <div class="spine__rail" role="tablist" aria-label="Milestones">
        <span class="spine__line" aria-hidden="true" />
        <button
          v-for="(m, i) in milestones"
          :key="i"
          type="button"
          role="tab"
          class="spine__stop"
          :class="{ 'is-active': active === i }"
          :aria-selected="active === i"
          @click="active = i"
          @mouseenter="active = i"
        >
          <span class="spine__dot" />
          <span class="spine__year">{{ m.year }}</span>
        </button>
      </div>

      <p class="spine__label" :key="active">
        <strong>{{ milestones[active].year }}</strong>
        {{ milestones[active].label }}
      </p>
    </section>

    <!-- ── 3. STAT STRIP — comparable across every exhibit ── -->
    <section v-if="stats.length" class="stats">
      <div v-for="s in stats" :key="s.label" class="stat">
        <span class="stat__label">{{ s.label }}</span>
        <span class="stat__value">{{ s.value }}</span>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

interface History {
  beats: { problem: string; breakthrough: string; legacy: string }
  milestones: { year: string; label: string }[]
  stats: { label: string; value: string }[]
}

const props = defineProps<{ history: History }>()

const active = ref(0)

const beats = computed(() => [
  { key: 'problem', head: 'The problem', text: props.history.beats.problem },
  { key: 'breakthrough', head: 'The breakthrough', text: props.history.beats.breakthrough },
  { key: 'legacy', head: 'What it changed', text: props.history.beats.legacy }
])

const milestones = computed(() => props.history.milestones ?? [])
const stats = computed(() => props.history.stats ?? [])

watch(() => props.history, () => { active.value = 0 })
</script>

<style scoped>
.hist { display: flex; flex-direction: column; gap: 28px; }

.hist__title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.74rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-caps);
  color: var(--text-dim);
  margin: 0 0 16px;
}

.hist__title .v-icon { color: var(--copper); }

/* ── Three beats ─────────────────────────────────────────── */
.beats {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.beat {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: var(--r-lg);
  background: var(--surface);
  border: 1px solid var(--line);
  position: relative;
  overflow: hidden;
}

/* a copper rule that grows across the three panels, left to right */
.beat::before {
  content: '';
  position: absolute;
  inset: 0 0 auto 0;
  height: 2px;
  background: var(--copper);
  opacity: calc(0.3 + var(--i) * 0.35);
}

.beat__num {
  flex: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--copper-tint);
  border: 1px solid var(--line-copper);
  color: var(--copper-bright);
  font-size: 0.76rem;
  font-weight: 800;
}

.beat__head {
  margin: 2px 0 6px;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-caps);
  color: var(--copper-bright);
}

.beat__text {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.6;
  color: var(--text);
}

/* ── Milestone spine ─────────────────────────────────────── */
.spine__rail {
  position: relative;
  display: flex;
  justify-content: space-between;
  gap: 4px;
  padding: 4px 0 0;
}

.spine__line {
  position: absolute;
  left: 6px;
  right: 6px;
  top: 11px;
  height: 2px;
  background: linear-gradient(90deg, var(--line-strong), var(--line-copper));
  border-radius: var(--r-pill);
}

.spine__stop {
  position: relative;
  appearance: none;
  background: none;
  border: 0;
  cursor: pointer;
  font: inherit;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 0 2px;
  flex: 1;
  min-width: 0;
}

.spine__dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--surface-3);
  border: 2px solid var(--line-strong);
  transition: background-color var(--t-fast) var(--ease),
              border-color var(--t-fast) var(--ease),
              transform var(--t-fast) var(--ease-out),
              box-shadow var(--t-fast) var(--ease);
}

.spine__stop:hover .spine__dot { border-color: var(--copper); }

.spine__stop.is-active .spine__dot {
  background: var(--copper);
  border-color: var(--copper-bright);
  transform: scale(1.25);
  box-shadow: 0 0 12px var(--copper-glow);
}

.spine__year {
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  color: var(--text-dim);
  white-space: nowrap;
  transition: color var(--t-fast) var(--ease);
}

.spine__stop.is-active .spine__year { color: var(--copper-bright); }

.spine__label {
  margin: 16px 0 0;
  padding: 12px 14px;
  border-radius: var(--r-md);
  background: var(--surface);
  border: 1px solid var(--line);
  border-left: 3px solid var(--copper);
  font-size: 0.9rem;
  line-height: 1.55;
  color: var(--text-muted);
  animation: fade-up var(--t-med) var(--ease-out);
}

.spine__label strong {
  color: var(--copper-bright);
  margin-right: 8px;
}

@keyframes fade-up {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: none; }
}

/* ── Stat strip ──────────────────────────────────────────── */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
  gap: 10px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 12px 14px;
  border-radius: var(--r-md);
  background: var(--abyss-deep);
  border: 1px solid var(--line);
}

.stat__label {
  font-size: 0.66rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-caps);
  color: var(--text-dim);
}

.stat__value {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--teal);
}

@media (max-width: 760px) {
  .beats { grid-template-columns: 1fr; }
  .spine__year { font-size: 0.62rem; }
}
</style>
