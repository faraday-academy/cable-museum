<template>
  <div class="timeline">
    <!-- ── Header: title, search, filter, sort — all on one row so
             the controls cost no vertical space ── -->
    <div class="timeline-head">
      <template v-if="!searchOpen">
        <h2 class="timeline-head__title">
          Eras
          <span class="timeline-head__count">{{ displayedEras.length }}<template v-if="isFiltered"> / {{ store.eras.length }}</template></span>
        </h2>
        <v-spacer />
      </template>

      <!-- search grows in place of the title -->
      <div v-else class="search">
        <v-icon icon="mdi-magnify" size="18" class="search__icon" />
        <input
          ref="searchInput"
          v-model="query"
          class="search__input"
          type="search"
          placeholder="Search cables, years, materials…"
          aria-label="Search exhibits"
          @keyup.escape="closeSearch"
        />
        <button type="button" class="icon-btn icon-btn--sm" aria-label="Close search" @click="closeSearch">
          <v-icon icon="mdi-close" size="17" />
        </button>
      </div>

      <button
        v-if="!searchOpen"
        type="button" class="icon-btn" aria-label="Search exhibits" @click="openSearch"
      >
        <v-icon icon="mdi-magnify" size="19" />
      </button>

      <!-- filter popover -->
      <v-menu :close-on-content-click="false" location="bottom end" offset="8">
        <template #activator="{ props: menu }">
          <button
            v-bind="menu"
            type="button"
            class="icon-btn"
            :class="{ 'is-on': activeFilterCount > 0 }"
            :aria-label="`Filter exhibits${activeFilterCount ? `, ${activeFilterCount} active` : ''}`"
          >
            <v-icon icon="mdi-filter-variant" size="19" />
            <span v-if="activeFilterCount" class="icon-btn__badge">{{ activeFilterCount }}</span>
          </button>
        </template>

        <div class="filters">
          <div class="filters__head">
            <span class="eyebrow">Filter</span>
            <button v-if="activeFilterCount" type="button" class="filters__clear" @click="clearFilters">Clear all</button>
          </div>

          <div class="filters__group">
            <span class="filters__label">Era</span>
            <div class="chips">
              <button
                v-for="p in PERIODS" :key="p.id" type="button" class="chip"
                :class="{ 'is-on': periods.includes(p.id) }" @click="toggle(periods, p.id)"
              >{{ p.label }}</button>
            </div>
          </div>

          <div class="filters__group">
            <span class="filters__label">Cable type</span>
            <div class="chips">
              <button
                v-for="f in availableFamilies" :key="f" type="button" class="chip"
                :class="{ 'is-on': families.includes(f) }" @click="toggle(families, f)"
              >{{ FAMILY_LABEL[f] || f }}</button>
            </div>
          </div>

          <div class="filters__group">
            <span class="filters__label">Carries</span>
            <div class="chips">
              <button
                v-for="k in availableSignals" :key="k" type="button" class="chip"
                :class="{ 'is-on': signals.includes(k) }" @click="toggle(signals, k)"
              >{{ SIGNAL_LABEL[k] || k }}</button>
            </div>
          </div>

          <div class="filters__group">
            <label class="switch">
              <input type="checkbox" v-model="withVideo" />
              <span>Has a video</span>
            </label>
          </div>
        </div>
      </v-menu>

      <div class="segmented" role="group" aria-label="Sort eras">
        <button
          type="button" class="segmented__btn" :class="{ 'is-active': !reverseOrder }"
          :aria-pressed="!reverseOrder" title="Oldest first" @click="reverseOrder = false"
        >
          <v-icon size="14" icon="mdi-sort-calendar-ascending" />
        </button>
        <button
          type="button" class="segmented__btn" :class="{ 'is-active': reverseOrder }"
          :aria-pressed="reverseOrder" title="Newest first" @click="reverseOrder = true"
        >
          <v-icon size="14" icon="mdi-sort-calendar-descending" />
        </button>
      </div>
    </div>

    <hr class="rule-fade mb-3" />

    <p v-if="!displayedEras.length" class="timeline-empty">
      <v-icon icon="mdi-cable-data" size="22" />
      No cables match. <button type="button" class="linkish" @click="clearAll">Reset filters</button>
    </p>

    <v-timeline v-else side="start" density="compact" line-inset="8" truncate-line="both">
      <v-timeline-item v-for="era in displayedEras" :key="era.id" :dot-color="store.selectedEraId === era.id ? 'primary' : 'secondary'"
        :icon="store.selectedEraId === era.id ? 'mdi-star' : 'mdi-circle'">
        <template #opposite>
          <div class="years-display">
            <div class="year">{{ era.years }}</div>
            <div class="year-marker"></div>
          </div>
        </template>
        <div class="era-card" @click="open(era.id)" @keyup.enter="open(era.id)" role="button" tabindex="0">
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
            <v-btn size="small" color="primary" variant="tonal" class="mt-2 explore-btn">Explore</v-btn>
          </div>
        </div>
      </v-timeline-item>
    </v-timeline>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, ref } from 'vue'
import { useMuseumStore } from '@/stores/museum'

const store = useMuseumStore()
const reverseOrder = ref(false)

// ── search ──────────────────────────────────────────────────
const query = ref('')
const searchOpen = ref(false)
const searchInput = ref<HTMLInputElement | null>(null)

async function openSearch() {
  searchOpen.value = true
  await nextTick()
  searchInput.value?.focus()
}
function closeSearch() {
  searchOpen.value = false
  query.value = ''
}

// ── filters ─────────────────────────────────────────────────
const PERIODS = [
  { id: 'pre1900', label: 'Before 1900', test: (y: number) => y < 1900 },
  { id: 'p1900', label: '1900–1959', test: (y: number) => y >= 1900 && y < 1960 },
  { id: 'p1960', label: '1960–1989', test: (y: number) => y >= 1960 && y < 1990 },
  { id: 'p1990', label: '1990–2009', test: (y: number) => y >= 1990 && y < 2010 },
  { id: 'p2010', label: '2010 onward', test: (y: number) => y >= 2010 }
]

const FAMILY_LABEL: Record<string, string> = {
  telegraph: 'Telegraph', telephone: 'Telephone', coax: 'Coaxial', fiber: 'Fibre optic',
  twisted: 'Twisted pair', usb: 'USB family', av: 'Display & AV', audio: 'Audio',
  power: 'Power', serial: 'Serial', parallel: 'Parallel', smart: 'Smart / experimental'
}

const SIGNAL_LABEL: Record<string, string> = {
  current: 'Electric current', audio: 'Analogue audio', differential: 'Differential pairs',
  rf: 'RF wave', light: 'Light'
}

const periods = ref<string[]>([])
const families = ref<string[]>([])
const signals = ref<string[]>([])
const withVideo = ref(false)

// The template passes the ref ALREADY UNWRAPPED (Vue does that for
// setup refs), so this receives the reactive array itself — mutate it
// directly rather than reaching for .value.
function toggle(list: string[], id: string) {
  const i = list.indexOf(id)
  if (i === -1) list.push(id)
  else list.splice(i, 1)
}

function clearFilters() {
  periods.value = []
  families.value = []
  signals.value = []
  withVideo.value = false
}
function clearAll() {
  clearFilters()
  closeSearch()
}

const activeFilterCount = computed(() =>
  periods.value.length + families.value.length + signals.value.length + (withVideo.value ? 1 : 0)
)
const isFiltered = computed(() => activeFilterCount.value > 0 || query.value.trim() !== '')

function specOf(id: string) {
  return store.cableSpecs[id]
}

const availableFamilies = computed(() => {
  const set = new Set<string>()
  for (const e of store.eras) {
    const f = specOf(e.id)?.family
    if (f) set.add(f)
  }
  return [...set].sort((a, b) => (FAMILY_LABEL[a] || a).localeCompare(FAMILY_LABEL[b] || b))
})

const availableSignals = computed(() => {
  const set = new Set<string>()
  for (const e of store.eras) {
    const k = specOf(e.id)?.signal?.kind
    if (k) set.add(k)
  }
  return [...set]
})

/** Everything a search query is allowed to match. */
function haystack(era: any) {
  const spec = specOf(era.id)
  return [
    era.title, era.summary, era.keyAdvancement, era.years,
    ...(era.facts ?? []),
    spec?.tagline,
    ...(spec?.layers ?? []).map((l: any) => l.label),
    ...(spec?.connectors ?? []).map((c: any) => c.label),
    ...(spec?.chips ?? []).map((c: any) => c.label)
  ].filter(Boolean).join(' ').toLowerCase()
}

const displayedEras = computed(() => {
  const q = query.value.trim().toLowerCase()
  let list = store.eras.filter(era => {
    const spec = specOf(era.id)
    const year = Number(era.sortYear ?? 9999)

    if (periods.value.length) {
      const ok = PERIODS.filter(p => periods.value.includes(p.id)).some(p => p.test(year))
      if (!ok) return false
    }
    if (families.value.length && !families.value.includes(spec?.family)) return false
    if (signals.value.length && !signals.value.includes(spec?.signal?.kind)) return false
    if (withVideo.value && !era.video) return false
    if (q && !haystack(era).includes(q)) return false
    return true
  })

  if (reverseOrder.value) list = [...list].reverse()
  return list
})

function withBase(path: string) {
  const base = import.meta.env.BASE_URL || '/'
  return `${base}${path.replace(/^\//, '')}`
}

function open(id: string) { store.openEra(id) }
</script>

<style scoped>
.timeline {
  padding: 16px 14px 28px;
  position: relative;
}

.timeline-head {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 2px 2px 12px;
}

.timeline-head__count {
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text-dim);
  margin-left: 8px;
  letter-spacing: 0.02em;
}

/* ── Icon buttons (search / filter) ───────────────────────── */
.icon-btn {
  position: relative;
  appearance: none;
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-muted);
  width: 34px;
  height: 34px;
  border-radius: var(--r-md);
  display: inline-grid;
  place-items: center;
  cursor: pointer;
  flex: none;
  transition: color var(--t-fast) var(--ease),
              background-color var(--t-fast) var(--ease),
              border-color var(--t-fast) var(--ease);
}

.icon-btn:hover {
  color: var(--text);
  background: var(--surface-2);
  border-color: var(--line);
}

.icon-btn.is-on {
  color: var(--copper-bright);
  background: var(--copper-tint);
  border-color: var(--line-copper);
}

.icon-btn--sm { width: 26px; height: 26px; }

.icon-btn__badge {
  position: absolute;
  top: -3px;
  right: -3px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: var(--r-pill);
  background: var(--copper);
  color: var(--text-on-accent);
  font-size: 0.62rem;
  font-weight: 800;
  display: grid;
  place-items: center;
}

/* ── Inline search ────────────────────────────────────────── */
.search {
  flex: 1;
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 8px 5px 10px;
  border-radius: var(--r-pill);
  background: var(--surface-2);
  border: 1px solid var(--line-copper);
  animation: search-in var(--t-med) var(--ease-out);
}

@keyframes search-in {
  from { opacity: 0; transform: translateX(-6px); }
  to { opacity: 1; transform: none; }
}

.search__icon { color: var(--copper); flex: none; }

.search__input {
  flex: 1;
  min-width: 0;
  background: none;
  border: 0;
  outline: none;
  color: var(--text);
  font: inherit;
  font-size: 0.86rem;
}

.search__input::placeholder { color: var(--text-dim); }
.search__input::-webkit-search-cancel-button { display: none; }

/* ── Filter popover ───────────────────────────────────────── */
.filters {
  width: 288px;
  padding: 14px;
  background: var(--surface);
  border: 1px solid var(--line-strong);
  border-radius: var(--r-lg);
  box-shadow: var(--shadow-3);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.filters__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.filters__clear {
  appearance: none;
  border: 0;
  background: none;
  cursor: pointer;
  font: inherit;
  font-size: 0.74rem;
  font-weight: 700;
  color: var(--copper-bright);
}

.filters__clear:hover { text-decoration: underline; }

.filters__group { display: flex; flex-direction: column; gap: 8px; }

.filters__label {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-caps);
  color: var(--text-dim);
}

.chips { display: flex; flex-wrap: wrap; gap: 6px; }

.chip {
  appearance: none;
  cursor: pointer;
  font: inherit;
  font-size: 0.74rem;
  font-weight: 600;
  padding: 5px 10px;
  border-radius: var(--r-pill);
  background: var(--surface-2);
  border: 1px solid var(--line);
  color: var(--text-muted);
  transition: color var(--t-fast) var(--ease),
              background-color var(--t-fast) var(--ease),
              border-color var(--t-fast) var(--ease);
}

.chip:hover { color: var(--text); border-color: var(--line-strong); }

.chip.is-on {
  background: var(--copper-tint);
  border-color: var(--line-copper);
  color: var(--copper-bright);
}

.switch {
  display: flex;
  align-items: center;
  gap: 9px;
  cursor: pointer;
  font-size: 0.82rem;
  color: var(--text-muted);
}

.switch input { accent-color: var(--copper); width: 15px; height: 15px; cursor: pointer; }

/* ── Empty state ──────────────────────────────────────────── */
.timeline-empty {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding: 22px 14px;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.timeline-empty .v-icon { color: var(--text-dim); }

.linkish {
  appearance: none;
  border: 0;
  background: none;
  padding: 0;
  cursor: pointer;
  font: inherit;
  color: var(--copper-bright);
  font-weight: 700;
  text-decoration: underline;
}

.timeline-head__title {
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: var(--tracking-tight);
  margin: 0;
}

.era-card {
  position: relative;
  display: grid;
  grid-template-columns: 132px 1fr;
  gap: 14px;
  align-items: center;
  padding: 10px;
  border-radius: var(--r-lg);
  background: var(--surface);
  border: 1px solid var(--line);
  cursor: pointer;
  transition: transform var(--t-med) var(--ease-out),
              border-color var(--t-fast) var(--ease),
              box-shadow var(--t-med) var(--ease);
}

.era-card:hover {
  transform: translateY(-2px);
  border-color: var(--line-copper);
  box-shadow: var(--shadow-2);
}

.era-card:hover .era-meta .title { color: var(--copper-bright); }

.era-img {
  border-radius: var(--r-md);
  overflow: hidden;
  position: relative;
  background: var(--abyss-deep);
}

.era-year-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: rgba(7, 11, 20, 0.82);
  backdrop-filter: blur(6px);
  color: var(--copper-bright);
  padding: 3px 8px;
  border-radius: var(--r-sm);
  border: 1px solid var(--line-copper);
  font-weight: 700;
  font-size: 0.74rem;
  letter-spacing: 0.02em;
  z-index: 2;
}

.skeleton {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, var(--surface), var(--surface-3), var(--surface));
  background-size: 200% 100%;
  animation: shimmer 1.2s infinite;
}

.era-meta .title {
  font-weight: 700;
  font-size: 1rem;
  line-height: 1.25;
  letter-spacing: var(--tracking-tight);
  transition: color var(--t-fast) var(--ease);
}

.era-meta .advancement {
  font-size: 0.78rem;
  color: var(--teal);
  font-weight: 700;
  letter-spacing: 0.01em;
  margin: 4px 0 5px;
}

.era-meta .summary {
  color: var(--text-muted);
  font-size: 0.86rem;
  line-height: 1.5;
}

.years-display {
  display: flex;
  align-items: center;
  gap: 8px;
}

.year {
  font-weight: 700;
  font-size: 1rem;
  color: var(--text-muted);
  text-align: right;
  min-width: 80px;
  letter-spacing: 0.01em;
}

.year-marker {
  width: 8px;
  height: 8px;
  background: var(--copper);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--copper-glow);
}

@media (max-width: 600px) {
  .era-card { grid-template-columns: 1fr; }
  .year { min-width: 60px; font-size: 0.92rem; }
  .years-display { justify-content: flex-end; }
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
