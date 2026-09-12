<template>
  <section class="ladder">
    <header class="ladder__head">
      <div>
        <p class="eyebrow">The whole museum, one scale</p>
        <h2 class="ladder__title">175 years of getting faster</h2>
      </div>
      <p class="ladder__note">
        Each rung is one cable. The scale is logarithmic — every gridline is
        <strong>1000×</strong> the one before it.
      </p>
    </header>

    <!-- decade gridlines -->
    <div class="ladder__axis" aria-hidden="true">
      <span v-for="t in TICKS" :key="t.v" class="ladder__tick" :style="{ left: pct(t.v) + '%' }">
        {{ t.label }}
      </span>
    </div>

    <ol class="ladder__rows">
      <li
        v-for="row in rows"
        :key="row.id"
        class="rung"
        :class="{ 'is-active': row.id === store.selectedEraId }"
      >
        <button type="button" class="rung__btn" @click="store.openEra(row.id)" :title="`${row.title} — ${row.speedLabel}`">
          <span class="rung__year">{{ row.year }}</span>
          <span class="rung__track">
            <span class="rung__bar" :style="{ width: pct(row.bitrate) + '%', background: row.color }" />
            <span class="rung__dot" :style="{ left: pct(row.bitrate) + '%', background: row.color }" />
            <span class="rung__name" :style="{ left: `calc(${pct(row.bitrate)}% + 12px)` }">{{ row.title }}</span>
          </span>
          <span class="rung__speed">{{ row.speedLabel }}</span>
        </button>
      </li>
    </ol>

    <p v-if="powerOnly.length" class="ladder__foot">
      <v-icon icon="mdi-flash" size="15" />
      {{ powerOnly.map(e => e.title.split(':')[0]).join(', ') }} carries power, not data — so it has no place on this scale.
    </p>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useMuseumStore } from '@/stores/museum'

const store = useMuseumStore()

const MIN = 4          // bit/s — below the slowest telegraph
const MAX = 2e12       // 2 Tb/s — headroom above 800G

const TICKS = [
  { v: 1e1, label: '10 b/s' },
  { v: 1e4, label: '10 kb/s' },
  { v: 1e7, label: '10 Mb/s' },
  { v: 1e10, label: '10 Gb/s' },
  { v: 1e12, label: '1 Tb/s' }
]

const FAMILY_COLOR: Record<string, string> = {
  telegraph: '#b87333', telephone: '#e8913a', audio: '#f5d06f',
  coax: '#9aa7b4', twisted: '#46c98b', fiber: '#3fbfd4',
  serial: '#c3ccd8', parallel: '#8b98a8', usb: '#ffae5c',
  av: '#9a86d4', power: '#ef5f5f', smart: '#7fe3c0'
}

function pct(bits: number) {
  const lo = Math.log10(MIN)
  const hi = Math.log10(MAX)
  const v = Math.log10(Math.max(MIN, bits))
  return Math.min(100, Math.max(0, ((v - lo) / (hi - lo)) * 100))
}

function speedLabel(b: number) {
  if (b >= 1e12) return `${(b / 1e12).toFixed(1).replace(/\.0$/, '')} Tb/s`
  if (b >= 1e9) return `${(b / 1e9).toFixed(0)} Gb/s`
  if (b >= 1e6) return `${(b / 1e6).toFixed(0)} Mb/s`
  if (b >= 1e3) return `${(b / 1e3).toFixed(0)} kb/s`
  return `${b} b/s`
}

const rows = computed(() =>
  store.eras
    .filter(e => typeof (e as any).bitrate === 'number')
    .map(e => {
      const spec = store.cableSpecs[e.id]
      const bitrate = (e as any).bitrate as number
      return {
        id: e.id,
        title: e.title.split(':')[0].replace(/\s*\(.*\)$/, ''),
        year: e.years,
        bitrate,
        speedLabel: speedLabel(bitrate),
        color: FAMILY_COLOR[spec?.family] ?? '#93a1b5'
      }
    })
    .sort((a, b) => a.bitrate - b.bitrate)
)

const powerOnly = computed(() => store.eras.filter(e => typeof (e as any).bitrate !== 'number'))
</script>

<style scoped>
.ladder {
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  background: var(--surface);
  padding: 18px 20px 16px;
}

.ladder__head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 18px;
  flex-wrap: wrap;
  margin-bottom: 18px;
}

.ladder__head .eyebrow { margin: 0 0 4px; color: var(--copper); }

.ladder__title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 800;
  letter-spacing: var(--tracking-tight);
}

.ladder__note {
  margin: 0;
  font-size: 0.78rem;
  color: var(--text-muted);
  max-width: 34ch;
  line-height: 1.5;
}

.ladder__note strong { color: var(--teal); }

/* ── axis ─────────────────────────────────────────────────── */
.ladder__axis {
  position: relative;
  height: 16px;
  margin-left: 58px;
  margin-right: 74px;
  border-bottom: 1px solid var(--line);
}

.ladder__tick {
  position: absolute;
  top: 0;
  transform: translateX(-50%);
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: var(--text-dim);
  white-space: nowrap;
}

.ladder__tick::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 15px;
  width: 1px;
  height: 1000px;
  background: var(--line);
  opacity: 0.5;
}

/* ── rungs ────────────────────────────────────────────────── */
.ladder__rows {
  list-style: none;
  margin: 0;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.rung__btn {
  display: grid;
  grid-template-columns: 58px 1fr 74px;
  align-items: center;
  gap: 0;
  width: 100%;
  appearance: none;
  border: 0;
  background: none;
  cursor: pointer;
  font: inherit;
  padding: 0;
  height: 20px;
  border-radius: var(--r-xs);
  transition: background-color var(--t-fast) var(--ease);
}

.rung__btn:hover { background: var(--surface-2); }

.rung.is-active .rung__btn {
  background: var(--copper-tint);
  box-shadow: inset 0 0 0 1px var(--line-copper);
}

.rung__year {
  font-size: 0.62rem;
  font-weight: 700;
  color: var(--text-dim);
  text-align: right;
  padding-right: 10px;
  white-space: nowrap;
}

.rung__track {
  position: relative;
  height: 100%;
  display: block;
}

.rung__bar {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  height: 2px;
  border-radius: var(--r-pill);
  opacity: 0.32;
}

.rung__dot {
  position: absolute;
  top: 50%;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  transform: translate(-50%, -50%);
}

.rung__name {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--text-muted);
  white-space: nowrap;
  pointer-events: none;
  transition: color var(--t-fast) var(--ease);
}

.rung__btn:hover .rung__name,
.rung.is-active .rung__name { color: var(--text); }

.rung__speed {
  font-size: 0.62rem;
  font-weight: 700;
  color: var(--text-dim);
  text-align: right;
  white-space: nowrap;
}

.rung.is-active .rung__speed,
.rung.is-active .rung__year { color: var(--copper-bright); }

.ladder__foot {
  margin: 14px 0 0;
  padding-top: 12px;
  border-top: 1px solid var(--line);
  font-size: 0.75rem;
  color: var(--text-dim);
  display: flex;
  align-items: center;
  gap: 7px;
}

.ladder__foot .v-icon { color: var(--warning); }

@media (max-width: 700px) {
  .rung__name { display: none; }
}
</style>
