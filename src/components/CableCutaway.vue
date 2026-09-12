<template>
  <div class="cut">
    <div class="cut__stage">
      <svg :viewBox="`0 0 ${W} ${H}`" class="cut__svg" role="img" :aria-label="`Cut-away of ${title}, showing how signal travels`">
        <defs>
          <linearGradient id="cut-sheen" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#fff" stop-opacity="0.16" />
            <stop offset="45%" stop-color="#fff" stop-opacity="0.02" />
            <stop offset="100%" stop-color="#000" stop-opacity="0.26" />
          </linearGradient>
          <filter id="cut-glow" x="-60%" y="-60%" width="220%" height="220%">
            <feGaussianBlur stdDeviation="3.2" result="b" />
            <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
          <clipPath id="cut-core">
            <rect :x="X0" :y="CY - coreH" :width="X1 - X0" :height="coreH * 2" />
          </clipPath>
        </defs>

        <!-- ── the cable, stripped back layer by layer ── -->
        <g>
          <g v-for="(ly, i) in layersOuterFirst" :key="ly.label + i">
            <rect
              :x="layerX(i)" :y="CY - layerH(ly)" :width="X1 - layerX(i)" :height="layerH(ly) * 2"
              :fill="mat(ly.material).fill" :stroke="mat(ly.material).edge" stroke-width="1"
            />
            <!-- rounded cut face, so it reads as a tube not a bar -->
            <ellipse
              :cx="layerX(i)" :cy="CY" :rx="7" :ry="layerH(ly)"
              :fill="mat(ly.material).edge" :stroke="mat(ly.material).edge" stroke-width="1"
            />
            <ellipse :cx="layerX(i)" :cy="CY" :rx="4" :ry="layerH(ly) * 0.78" :fill="mat(ly.material).hi" opacity="0.25" />

            <!-- construction texture along the run -->
            <g v-if="ly.pattern === 'armour'" :opacity="0.85">
              <path
                v-for="k in armourCount(i)" :key="'a' + k"
                :d="armourPath(i, k - 1)"
                :stroke="mat(ly.material).hi" stroke-width="3.5" fill="none" stroke-linecap="round" opacity="0.55"
              />
            </g>
            <g v-else-if="ly.pattern === 'braid'" :opacity="0.7">
              <path :d="braidPath(i, 1)" :stroke="mat(ly.material).hi" stroke-width="2" fill="none" opacity="0.55" />
              <path :d="braidPath(i, -1)" :stroke="mat(ly.material).hi" stroke-width="2" fill="none" opacity="0.55" />
            </g>
            <g v-else-if="ly.pattern === 'weave'" :opacity="0.5">
              <path :d="braidPath(i, 1)" :stroke="mat(ly.material).hi" stroke-width="2.5" fill="none" opacity="0.4" />
            </g>
            <rect
              :x="layerX(i)" :y="CY - layerH(ly)" :width="X1 - layerX(i)" :height="layerH(ly) * 2"
              fill="url(#cut-sheen)" pointer-events="none"
            />
            <!-- label with a leader up to the layer's cut face -->
            <g class="cut__callout">
              <line :x1="layerX(i) + 2" :y1="CY - layerH(ly)" :x2="layerX(i) + 2" :y2="calloutY(i)" :stroke="mat(ly.material).hi" stroke-width="1" opacity="0.55" />
              <circle :cx="layerX(i) + 2" :cy="calloutY(i)" r="2.5" :fill="mat(ly.material).hi" />
              <text :x="layerX(i) + 9" :y="calloutY(i) + 3.5" class="cut__label" :fill="mat(ly.material).hi">{{ ly.label }}</text>
            </g>
          </g>
        </g>

        <!-- ── return current on the shield (coax only) ── -->
        <g v-if="spec.signal.kind === 'rf' && playing" opacity="0.9">
          <g v-for="(p, i) in returnFlow" :key="'rt' + i">
            <path
              :d="`M${p.x} ${CY - shieldY} l10 0`" stroke="#c9d4de" stroke-width="2.5" stroke-linecap="round" opacity="0.55"
            />
            <path
              :d="`M${p.x} ${CY + shieldY} l10 0`" stroke="#c9d4de" stroke-width="2.5" stroke-linecap="round" opacity="0.55"
            />
          </g>
          <text :x="X0 + 14" :y="CY - shieldY - 8" class="cut__mini" fill="#c9d4de">← return current flows back along the shield</text>
        </g>

        <!-- ── the signal itself ── -->
        <g clip-path="url(#cut-core)">
          <!-- fibre: the light path bounces off the cladding -->
          <path
            v-if="spec.signal.kind === 'light' && playing"
            :d="bouncePath" fill="none" stroke="#8fd8e8" stroke-width="1.5" opacity="0.28" stroke-dasharray="4 5"
          />
          <!-- rf: a travelling wave in the dielectric -->
          <path
            v-if="spec.signal.kind === 'rf' && playing"
            :d="wavePath" fill="none" stroke="#6fd9ea" stroke-width="2.5" opacity="0.85" filter="url(#cut-glow)"
          />

          <g v-for="p in particles" :key="p.id">
            <!-- differential: same pulse twice, one inverted -->
            <template v-if="spec.signal.kind === 'differential'">
              <circle :cx="p.x" :cy="CY - pairGap" :r="p.r" fill="#e8913a" filter="url(#cut-glow)" :opacity="p.a" />
              <circle :cx="p.x" :cy="CY + pairGap" :r="p.r" fill="#3fbfd4" filter="url(#cut-glow)" :opacity="p.a" />
            </template>
            <template v-else-if="spec.signal.kind === 'light'">
              <circle :cx="p.x" :cy="p.y" :r="p.r" fill="#d3f4fb" filter="url(#cut-glow)" :opacity="p.a" />
            </template>
            <template v-else-if="spec.signal.kind !== 'rf'">
              <circle :cx="p.x" :cy="p.y" :r="p.r" :fill="signalColor" filter="url(#cut-glow)" :opacity="p.a" />
            </template>
          </g>

          <!-- the field front: what actually moves fast down a wire -->
          <rect
            v-if="playing && ['current', 'audio'].includes(spec.signal.kind)"
            :x="frontX" :y="CY - coreH" width="3" :height="coreH * 2"
            :fill="signalColor" opacity="0.55" filter="url(#cut-glow)"
          />
        </g>

        <!-- ── chips living inside the cable ── -->
        <g v-for="(chip, i) in spec.chips" :key="'c' + i">
          <g :transform="`translate(${chipX(i)},${CY})`" class="cut__chip" :class="{ 'is-hot': chipHot[i] }">
            <rect x="-26" y="-19" width="52" height="38" rx="4" fill="#2f3e52" stroke="#f5d06f" stroke-width="1.4" />
            <rect v-for="k in 4" :key="'l' + k" x="-31" :y="-13 + (k - 1) * 8" width="5" height="4" fill="#f5d06f" />
            <rect v-for="k in 4" :key="'r' + k" x="26" :y="-13 + (k - 1) * 8" width="5" height="4" fill="#f5d06f" />
            <circle cx="0" cy="0" r="9" fill="#f5d06f" :opacity="chipHot[i] ? 0.85 : 0.35" />
            <text x="0" y="3.5" text-anchor="middle" class="cut__chiptext">IC</text>
          </g>
          <line :x1="chipX(i)" :y1="CY - 20" :x2="chipX(i)" :y2="CY - 58" stroke="#f5d06f" stroke-width="1" opacity="0.5" />
          <text :x="chipX(i)" :y="CY - 64" text-anchor="middle" class="cut__label" fill="#f5d06f">{{ chip.label }}</text>
        </g>

        <!-- ── connectors at both ends ── -->
        <CableConnector :kind="connKind" :x="X0 + 6" :y="CY" :s="66" flip :live="leftLive" />
        <CableConnector :kind="connKind" :x="X1 - 6" :y="CY" :s="66" :live="rightLive" />

        <!-- signal leaving the far connector -->
        <g v-for="b in bursts" :key="'b' + b.id">
          <circle :cx="X1 + 26" :cy="CY" :r="6 + b.t * 34" fill="none" :stroke="signalColor" :stroke-width="2.5 * (1 - b.t)" :opacity="1 - b.t" />
          <g v-for="k in 6" :key="'s' + k">
            <circle
              :cx="X1 + 26 + Math.cos(((k - 1) / 6) * Math.PI * 2) * b.t * 40"
              :cy="CY + Math.sin(((k - 1) / 6) * Math.PI * 2) * b.t * 40"
              :r="2.4 * (1 - b.t)" :fill="signalColor" :opacity="1 - b.t"
            />
          </g>
        </g>

        <text :x="X0 + 6" :y="H - 10" class="cut__mini" fill="#93a1b5">{{ spec.connectors[0]?.label }}</text>
        <text :x="X1 - 6" :y="H - 10" text-anchor="end" class="cut__mini" fill="#93a1b5">signal out →</text>
      </svg>
    </div>

    <!-- ── controls + explanation ── -->
    <div class="cut__bar">
      <button type="button" class="cut__play" :class="{ 'is-on': playing }" @click="toggle">
        <v-icon :icon="playing ? 'mdi-pause' : 'mdi-play'" size="18" />
        {{ playing ? 'Pause signal' : 'Send a signal' }}
      </button>

      <div class="segmented" role="group" aria-label="Playback speed">
        <button
          v-for="opt in SPEEDS" :key="opt.v" type="button" class="segmented__btn"
          :class="{ 'is-active': rate === opt.v }" @click="rate = opt.v"
        >{{ opt.label }}</button>
      </div>

      <p class="cut__carrier">
        <span class="cut__dot" :style="{ background: signalColor }" />
        <strong>{{ copy.carrier }}</strong>
        <span>{{ spec.signal.label }}</span>
      </p>
    </div>

    <p class="cut__blurb">{{ copy.blurb }}</p>

    <ul v-if="spec.chips.length" class="cut__chips">
      <li v-for="(chip, i) in spec.chips" :key="'ch' + i">
        <v-icon icon="mdi-chip" size="17" />
        <span><strong>{{ chip.label }}</strong> — {{ chip.note }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { MATERIALS, SIGNAL_COPY, type CableSpec } from '@/cables'
import CableConnector from './CableConnector.vue'

const props = defineProps<{ spec: CableSpec; title?: string }>()

const W = 920
const H = 340
const CY = 168
const X0 = 96
const X1 = W - 96
const STEP = 46
const HMAX = 74

const SPEEDS = [
  { label: '0.25×', v: 0.25 },
  { label: '1×', v: 1 },
  { label: '3×', v: 3 }
]

const playing = ref(false)
const rate = ref(1)

const layersOuterFirst = computed(() => props.spec.layers ?? [])
const connKind = computed(() => props.spec.connectors?.[0]?.kind ?? 'coax-fitting')
const copy = computed(() => SIGNAL_COPY[props.spec.signal.kind] ?? SIGNAL_COPY.current)
const signalColor = computed(() => copy.value.color)

const innerLayer = computed(() => layersOuterFirst.value[layersOuterFirst.value.length - 1])
const coreH = computed(() => Math.max(7, HMAX * (innerLayer.value?.r ?? 0.2)))
const shieldY = computed(() => {
  const shield = layersOuterFirst.value.find(l => l.pattern === 'braid' || l.pattern === 'foil')
  return HMAX * (shield?.r ?? 0.8) * 0.9
})
const pairGap = computed(() => Math.min(coreH.value * 0.55, 16))

function mat(id: string) {
  return MATERIALS[id] ?? MATERIALS.copper
}

/** Outermost layer is stripped back furthest right. */
function layerX(i: number) {
  const n = layersOuterFirst.value.length
  return X0 + (n - 1 - i) * STEP
}
function layerH(ly: { r: number }) {
  return Math.max(7, HMAX * ly.r)
}
function calloutY(i: number) {
  const ly = layersOuterFirst.value[i]
  // alternate above/below so labels never collide
  return i % 2 === 0 ? CY - layerH(ly) - 12 - (i % 4) * 13 : CY + layerH(ly) + 20 + (i % 4) * 13
}

function armourCount(i: number) {
  return Math.max(3, Math.floor((X1 - layerX(i)) / 54))
}
function armourPath(i: number, k: number) {
  const ly = layersOuterFirst.value[i]
  const h = layerH(ly)
  const x = layerX(i) + 16 + k * 54
  return `M${x} ${CY - h} Q${x + 27} ${CY} ${x} ${CY + h}`
}
function braidPath(i: number, dir: number) {
  const ly = layersOuterFirst.value[i]
  const h = layerH(ly) * 0.82
  const x0 = layerX(i)
  let d = `M${x0} ${CY + dir * h}`
  for (let x = x0; x < X1; x += 34) {
    d += ` Q${x + 17} ${CY - dir * h} ${x + 34} ${CY + dir * h}`
  }
  return d
}
function chipX(i: number) {
  const span = X1 - 120 - (X0 + 180)
  const n = props.spec.chips.length
  return X0 + 180 + (n === 1 ? span * 0.62 : (span * (i + 0.5)) / n)
}

// ── particle system ────────────────────────────────────────────
interface P { id: number; t: number; x: number; y: number; r: number; a: number }
const particles = ref<P[]>([])
const bursts = ref<{ id: number; t: number }[]>([])
const chipHot = reactive<boolean[]>([])
const frontX = ref(X0)
const phase = ref(0)
let raf = 0
let seq = 0
let last = 0

const COUNT = 22

function seed() {
  // Position from t immediately, so the very first painted frame already
  // shows the signal spread along the cable rather than stacked at the end.
  particles.value = Array.from({ length: COUNT }, (_, i) => {
    const t = i / COUNT
    return {
      id: seq++,
      t,
      x: X0 + (X1 - X0) * t,
      y: yFor(t),
      r: 3.6,
      a: Math.min(1, Math.min(t, 1 - t) * 8) * 0.95
    }
  })
}

const bouncePath = computed(() => {
  // the zig-zag of total internal reflection
  const h = coreH.value * 0.78
  let d = `M${X0} ${CY}`
  let up = true
  for (let x = X0; x < X1; x += 58) {
    d += ` L${x + 29} ${CY + (up ? -h : h)} L${x + 58} ${CY}`
    up = !up
  }
  return d
})

const wavePath = computed(() => {
  const h = coreH.value * 0.8
  const k = phase.value
  let d = `M${X0} ${CY}`
  for (let x = X0; x <= X1; x += 6) {
    d += ` L${x} ${(CY + Math.sin((x - X0) / 26 - k) * h).toFixed(1)}`
  }
  return d
})

const returnFlow = computed(() =>
  Array.from({ length: 9 }, (_, i) => ({
    x: X0 + (((X1 - X0) * ((i / 9 + 1 - (phase.value % (Math.PI * 2)) / (Math.PI * 2)) % 1))),
  }))
)

const leftLive = computed(() => playing.value)
const rightLive = computed(() => bursts.value.length > 0)

function yFor(t: number) {
  const kind = props.spec.signal.kind
  if (kind === 'light') {
    // triangle wave = the bounce
    const h = coreH.value * 0.78
    const u = ((t * (X1 - X0)) / 58) % 2
    return CY + (u < 1 ? -h + u * 2 * h : h - (u - 1) * 2 * h) * 0.9
  }
  return CY
}

function frame(now: number) {
  if (!last) last = now
  const dt = Math.min(0.05, (now - last) / 1000)
  last = now

  const v = 0.26 * props.spec.signal.speed * rate.value
  phase.value += dt * 7 * rate.value

  for (const p of particles.value) {
    p.t += dt * v
    if (p.t >= 1) {
      p.t -= 1
      bursts.value.push({ id: seq++, t: 0 })
    }
    p.x = X0 + (X1 - X0) * p.t
    p.y = yFor(p.t)
    // fade in/out at the ends so nothing pops
    p.a = Math.min(1, Math.min(p.t, 1 - p.t) * 8) * 0.95
    p.r = 3.4 + Math.sin(p.t * 22 + phase.value) * 0.5
  }

  frontX.value = X0 + (X1 - X0) * (((now / 1000) * v * 1.6) % 1)

  // chips light up as signal passes through them
  props.spec.chips.forEach((_, i) => {
    const cx = chipX(i)
    chipHot[i] = particles.value.some(p => Math.abs(p.x - cx) < 34)
  })

  for (const b of bursts.value) b.t += dt * 1.8
  bursts.value = bursts.value.filter(b => b.t < 1)

  raf = requestAnimationFrame(frame)
}

function start() {
  if (raf) return
  last = 0
  raf = requestAnimationFrame(frame)
}
function stop() {
  cancelAnimationFrame(raf)
  raf = 0
}
function toggle() {
  playing.value = !playing.value
}

watch(playing, on => {
  if (on) { seed(); start() } else { stop(); bursts.value = []; particles.value = [] }
})

watch(() => props.spec, () => {
  if (playing.value) seed()
})

onMounted(seed)
onBeforeUnmount(stop)
</script>

<style scoped>
.cut { display: flex; flex-direction: column; gap: 14px; }

.cut__stage {
  background: var(--abyss-deep);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  padding: 8px;
  overflow: hidden;
}

.cut__svg { width: 100%; height: auto; display: block; }

.cut__label {
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.cut__mini {
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 10.5px;
  font-weight: 600;
}

.cut__chiptext {
  font-family: ui-sans-serif, system-ui, sans-serif;
  font-size: 10px;
  font-weight: 800;
  fill: #1a1005;
}

.cut__chip circle { transition: opacity 160ms ease; }
.cut__chip.is-hot { filter: drop-shadow(0 0 8px rgba(245, 208, 111, 0.55)); }

.cut__bar {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.cut__play {
  appearance: none;
  border: 1px solid var(--line-copper);
  background: var(--copper-tint);
  color: var(--copper-bright);
  font: inherit;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.02em;
  padding: 9px 16px;
  border-radius: var(--r-pill);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background-color var(--t-fast) var(--ease), color var(--t-fast) var(--ease);
}

.cut__play:hover { background: var(--copper); color: var(--text-on-accent); }
.cut__play.is-on { background: var(--copper); color: var(--text-on-accent); }

.cut__carrier {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 0.82rem;
  color: var(--text-muted);
}

.cut__carrier strong { color: var(--text); }

.cut__dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.cut__blurb {
  margin: 0;
  color: var(--text-muted);
  font-size: 0.9rem;
  line-height: 1.6;
  max-width: 78ch;
}

.cut__chips {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.cut__chips li {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 10px 12px;
  border-radius: var(--r-md);
  background: var(--brass-tint);
  border: 1px solid rgba(245, 208, 111, 0.28);
  font-size: 0.86rem;
  line-height: 1.55;
  color: var(--text-muted);
}

.cut__chips strong { color: var(--brass); }
.cut__chips .v-icon { color: var(--brass); margin-top: 2px; flex: none; }
</style>
