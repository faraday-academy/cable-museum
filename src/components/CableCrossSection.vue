<template>
  <div class="xsec">
    <div class="xsec__figure">
      <svg :viewBox="`0 0 ${SIZE} ${SIZE}`" class="xsec__svg" role="img" :aria-label="`Cross-section of ${title}`">
        <defs>
          <radialGradient id="xsec-depth" cx="38%" cy="32%" r="78%">
            <stop offset="0%" stop-color="#fff" stop-opacity="0.20" />
            <stop offset="55%" stop-color="#fff" stop-opacity="0.02" />
            <stop offset="100%" stop-color="#000" stop-opacity="0.40" />
          </radialGradient>
        </defs>

        <!-- concentric layers, outermost first -->
        <g>
          <g
            v-for="(ly, i) in layers"
            :key="ly.label + i"
            class="xsec__layer"
            :class="{ 'is-dim': active !== null && active !== i }"
            @mouseenter="active = i"
            @mouseleave="active = null"
            @focus="active = i"
            @blur="active = null"
            tabindex="0"
            role="button"
            :aria-label="ly.label"
          >
            <circle
              :cx="C" :cy="C" :r="ly.r * R"
              :fill="mat(ly.material).fill"
              :stroke="active === i ? 'var(--copper-bright)' : mat(ly.material).edge"
              :stroke-width="active === i ? 3 : 1.4"
            />
            <!-- construction texture -->
            <template v-if="ly.pattern === 'armour'">
              <circle
                v-for="(p, k) in ringPoints(16, ly.r * R * 0.9)" :key="'a' + k"
                :cx="p.x" :cy="p.y" :r="R * 0.062"
                :fill="mat(ly.material).hi" :stroke="mat(ly.material).edge" stroke-width="1"
              />
            </template>
            <template v-else-if="ly.pattern === 'braid'">
              <circle
                v-for="(p, k) in ringPoints(26, ly.r * R * 0.93)" :key="'b' + k"
                :cx="p.x" :cy="p.y" :r="R * 0.03" :fill="mat(ly.material).hi" opacity="0.9"
              />
            </template>
            <template v-else-if="ly.pattern === 'weave'">
              <circle
                v-for="(p, k) in ringPoints(22, ly.r * R * 0.92)" :key="'w' + k"
                :cx="p.x" :cy="p.y" :r="R * 0.026" :fill="mat(ly.material).hi" opacity="0.55"
              />
            </template>
            <template v-else-if="ly.pattern === 'foil'">
              <circle :cx="C" :cy="C" :r="ly.r * R * 0.97" fill="none" :stroke="mat(ly.material).hi" :stroke-width="R * 0.02" opacity="0.9" />
            </template>
            <template v-else-if="ly.pattern === 'foam'">
              <circle
                v-for="(p, k) in ringPoints(9, ly.r * R * 0.66, 0.3)" :key="'f' + k"
                :cx="p.x" :cy="p.y" :r="R * 0.035" :fill="mat(ly.material).hi" opacity="0.4"
              />
            </template>
          </g>
        </g>

        <!-- stranded / ribbon cores -->
        <g v-if="spec.cores" class="xsec__cores">
          <template v-if="spec.cores.row">
            <circle
              v-for="(p, k) in rowPoints(spec.cores)" :key="'r' + k"
              :cx="p.x" :cy="p.y" :r="spec.cores.r * R"
              :fill="mat(spec.cores.material).fill" :stroke="mat(spec.cores.material).edge" stroke-width="1"
            />
          </template>
          <template v-else-if="spec.cores.count === 2 || spec.cores.twist">
            <g v-for="(sx, k) in [-1, 1]" :key="'t' + k">
              <circle
                :cx="C + sx * spec.cores.ring * R" :cy="C" :r="spec.cores.r * R"
                :fill="k === 0 ? mat(spec.cores.material).fill : mat('tinned').fill"
                :stroke="mat(spec.cores.material).edge" stroke-width="1.2"
              />
              <circle :cx="C + sx * spec.cores.ring * R" :cy="C" :r="spec.cores.r * R * 0.45" :fill="mat('copper').fill" />
            </g>
          </template>
          <template v-else>
            <circle :cx="C" :cy="C" :r="spec.cores.r * R" :fill="mat(spec.cores.material).fill" :stroke="mat(spec.cores.material).edge" stroke-width="1" />
            <circle
              v-for="(p, k) in ringPoints(spec.cores.count - 1, spec.cores.ring * R)" :key="'s' + k"
              :cx="p.x" :cy="p.y" :r="spec.cores.r * R"
              :fill="mat(spec.cores.material).fill" :stroke="mat(spec.cores.material).edge" stroke-width="1"
            />
          </template>
        </g>

        <!-- twisted pairs -->
        <g v-if="spec.pairs" class="xsec__pairs">
          <g v-for="(p, k) in ringPoints(spec.pairs.count, spec.pairs.ring * R, -Math.PI / 4)" :key="'p' + k">
            <circle :cx="p.x - spec.pairs.r * R * 0.5" :cy="p.y" :r="spec.pairs.r * R * 0.52" :fill="spec.pairs.colors[k % spec.pairs.colors.length]" stroke="#0e1620" stroke-width="1.2" />
            <circle :cx="p.x + spec.pairs.r * R * 0.5" :cy="p.y" :r="spec.pairs.r * R * 0.52" fill="#e8eef5" stroke="#0e1620" stroke-width="1.2" />
            <circle :cx="p.x - spec.pairs.r * R * 0.5" :cy="p.y" :r="spec.pairs.r * R * 0.24" :fill="mat('copper').fill" />
            <circle :cx="p.x + spec.pairs.r * R * 0.5" :cy="p.y" :r="spec.pairs.r * R * 0.24" :fill="mat('copper').fill" />
          </g>
        </g>

        <!-- loose bundle -->
        <g v-if="spec.bundle" class="xsec__bundle">
          <g v-for="(w, k) in spec.bundle" :key="'u' + k">
            <circle v-if="w.shielded" :cx="C + w.cx * R" :cy="C + w.cy * R" :r="w.r * R * 1.16" fill="none" :stroke="mat('foil').fill" :stroke-width="R * 0.022" opacity="0.9" />
            <circle :cx="C + w.cx * R" :cy="C + w.cy * R" :r="w.r * R" :fill="mat('teflon').fill" :stroke="mat('teflon').edge" stroke-width="1" />
            <template v-if="w.pair">
              <circle :cx="C + w.cx * R - w.r * R * 0.42" :cy="C + w.cy * R" :r="w.r * R * 0.34" :fill="mat(w.material).fill" :stroke="mat(w.material).edge" stroke-width="0.8" />
              <circle :cx="C + w.cx * R + w.r * R * 0.42" :cy="C + w.cy * R" :r="w.r * R * 0.34" :fill="mat(w.material).fill" :stroke="mat(w.material).edge" stroke-width="0.8" />
            </template>
            <circle v-else :cx="C + w.cx * R" :cy="C + w.cy * R" :r="w.r * R * 0.52" :fill="mat(w.material).fill" :stroke="mat(w.material).edge" stroke-width="0.8" />
          </g>
        </g>

        <!-- depth shading, drawn last so it sits over everything -->
        <circle :cx="C" :cy="C" :r="R" fill="url(#xsec-depth)" pointer-events="none" />
      </svg>
    </div>

    <!-- ── Legend: the labels live here, not as leader lines, so
             they stay readable at any size ── -->
    <ul class="xsec__legend">
      <li
        v-for="(ly, i) in layers"
        :key="ly.label + i"
        class="xsec__item"
        :class="{ 'is-active': active === i }"
        @mouseenter="active = i"
        @mouseleave="active = null"
      >
        <span class="xsec__swatch" :style="{ background: mat(ly.material).fill, borderColor: mat(ly.material).edge }" />
        <span class="xsec__text">
          <span class="xsec__label">{{ ly.label }}</span>
          <span v-if="ly.note" class="xsec__note">{{ ly.note }}</span>
        </span>
      </li>
      <li v-if="extraLabel" class="xsec__item is-extra">
        <span class="xsec__swatch xsec__swatch--multi" />
        <span class="xsec__text"><span class="xsec__label">{{ extraLabel }}</span></span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { MATERIALS, type CableSpec } from '@/cables'

const props = defineProps<{ spec: CableSpec; title?: string }>()

const SIZE = 320
const C = SIZE / 2
const R = SIZE / 2 - 14

const active = ref<number | null>(null)
const layers = computed(() => props.spec.layers ?? [])

function mat(id: string) {
  return MATERIALS[id] ?? MATERIALS.copper
}

function ringPoints(n: number, radius: number, phase = -Math.PI / 2) {
  return Array.from({ length: Math.max(0, n) }, (_, i) => ({
    x: C + radius * Math.cos(phase + (i * 2 * Math.PI) / n),
    y: C + radius * Math.sin(phase + (i * 2 * Math.PI) / n)
  }))
}

function rowPoints(cores: NonNullable<CableSpec['cores']>) {
  const span = cores.ring * R * 2
  const n = cores.count
  return Array.from({ length: n }, (_, i) => ({
    x: C - span / 2 + span * (i / Math.max(1, n - 1)),
    y: C
  }))
}

const extraLabel = computed(() => {
  if (props.spec.pairs) return `${props.spec.pairs.count} twisted pairs`
  if (props.spec.bundle) return `${props.spec.bundle.length} conductors in the bundle`
  if (props.spec.cores) return `${props.spec.cores.count} × ${mat(props.spec.cores.material).name.toLowerCase()}`
  return ''
})
</script>

<style scoped>
.xsec {
  display: grid;
  grid-template-columns: minmax(220px, 320px) 1fr;
  gap: clamp(16px, 3vw, 32px);
  align-items: start;
}

.xsec__figure {
  background: var(--abyss-deep);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  padding: 12px;
}

.xsec__svg { width: 100%; height: auto; display: block; }

.xsec__layer { cursor: pointer; transition: opacity var(--t-fast) var(--ease); }
.xsec__layer.is-dim { opacity: 0.35; }
.xsec__layer:focus-visible { outline: none; }

.xsec__legend {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.xsec__item {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 9px 10px;
  border-radius: var(--r-md);
  border: 1px solid transparent;
  cursor: default;
  transition: background-color var(--t-fast) var(--ease), border-color var(--t-fast) var(--ease);
}

.xsec__item.is-active {
  background: var(--copper-tint);
  border-color: var(--line-copper);
}

.xsec__swatch {
  width: 14px;
  height: 14px;
  border-radius: 4px;
  border: 1px solid;
  flex: none;
  margin-top: 2px;
}

.xsec__swatch--multi {
  background: linear-gradient(135deg, var(--teal) 0 25%, var(--copper) 25% 50%, var(--success) 50% 75%, var(--error) 75% 100%);
  border-color: var(--line-strong);
}

.xsec__text { display: flex; flex-direction: column; gap: 2px; }

.xsec__label {
  font-weight: 700;
  font-size: 0.88rem;
  color: var(--text);
}

.xsec__note {
  font-size: 0.8rem;
  color: var(--text-muted);
  line-height: 1.5;
}

.xsec__item.is-extra .xsec__label { color: var(--teal); }

@media (max-width: 760px) {
  .xsec { grid-template-columns: 1fr; }
}
</style>
