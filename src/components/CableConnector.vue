<template>
  <!-- Side-view connector. Drawn facing RIGHT at the origin; the
       parent positions and mirrors it. `live` lights the contacts
       when signal is arriving. -->
  <g :transform="`translate(${x},${y}) scale(${flip ? -s : s},${s})`" class="conn" :class="{ 'is-live': live }">
    <!-- USB-C: rounded shell, contacts top and bottom -->
    <template v-if="kind === 'usb-c'">
      <rect x="-1.5" y="-0.42" width="1.5" height="0.84" rx="0.42" :fill="SHELL" :stroke="EDGE" stroke-width="0.05" />
      <rect x="-1.28" y="-0.22" width="1.0" height="0.44" rx="0.22" :fill="DARK" />
      <rect class="pin" x="-1.18" y="-0.10" width="0.8" height="0.07" :fill="GOLD" />
      <rect class="pin" x="-1.18" y="0.03" width="0.8" height="0.07" :fill="GOLD" />
    </template>

    <!-- USB-A -->
    <template v-else-if="kind === 'usb-a'">
      <rect x="-1.5" y="-0.4" width="1.5" height="0.8" rx="0.06" :fill="SHELL" :stroke="EDGE" stroke-width="0.05" />
      <rect x="-1.3" y="-0.24" width="1.05" height="0.3" :fill="DARK" />
      <rect class="pin" x="-1.22" y="-0.18" width="0.85" height="0.1" :fill="GOLD" />
    </template>

    <!-- RJ45 with its latch -->
    <template v-else-if="kind === 'rj45'">
      <path d="M-1.5 -0.46 h1.5 v0.92 h-1.5 z" fill="#c9d4de" opacity="0.92" stroke="#7d8894" stroke-width="0.05" />
      <path d="M-0.95 0.46 v0.34 h0.42 v-0.34 z" fill="#c9d4de" stroke="#7d8894" stroke-width="0.05" />
      <rect v-for="i in 8" :key="i" class="pin" :x="-1.38 + (i - 1) * 0.16" y="-0.4" width="0.07" height="0.46" :fill="GOLD" />
    </template>

    <!-- F-type screw -->
    <template v-else-if="kind === 'f-type'">
      <rect x="-1.35" y="-0.34" width="1.05" height="0.68" :fill="SHELL" :stroke="EDGE" stroke-width="0.05" />
      <rect v-for="i in 4" :key="i" :x="-1.32 + (i - 1) * 0.26" y="-0.34" width="0.1" height="0.68" fill="#7d8894" />
      <rect class="pin" x="-0.42" y="-0.05" width="0.62" height="0.1" fill="#b87333" />
    </template>

    <!-- Fiber ferrules -->
    <template v-else-if="['lc-fiber', 'sc-fiber', 'bare-fiber', 'mpo'].includes(kind)">
      <rect x="-1.5" y="-0.4" width="1.15" height="0.8" rx="0.08" fill="#2f3e52" stroke="#1a2432" stroke-width="0.05" />
      <template v-if="kind === 'mpo'">
        <rect x="-0.4" y="-0.16" width="0.52" height="0.32" rx="0.04" fill="#e8eef5" opacity="0.85" />
        <circle v-for="i in 6" :key="i" class="pin" cx="-0.62" :cy="-0.24 + (i - 1) * 0.1" r="0.035" fill="#8fd8e8" />
      </template>
      <template v-else>
        <rect x="-0.4" y="-0.13" width="0.58" height="0.26" rx="0.05" fill="#e8eef5" opacity="0.9" />
        <circle class="pin" cx="0.12" cy="0" r="0.07" fill="#8fd8e8" />
      </template>
    </template>

    <!-- HDMI: the chamfered shell -->
    <template v-else-if="kind === 'hdmi'">
      <path d="M-1.5 -0.34 h1.5 v0.68 h-1.5 l0.16 -0.34 z" :fill="SHELL" :stroke="EDGE" stroke-width="0.05" />
      <rect class="pin" x="-1.3" y="-0.16" width="1.05" height="0.1" :fill="GOLD" />
      <rect class="pin" x="-1.3" y="0.04" width="1.05" height="0.1" :fill="GOLD" />
    </template>

    <!-- Screw terminal / binding post -->
    <template v-else-if="['terminal', 'binding-post'].includes(kind)">
      <rect x="-1.1" y="-0.5" width="0.75" height="1" rx="0.08" fill="#3a2c1c" stroke="#241a10" stroke-width="0.05" />
      <circle class="pin" cx="-0.72" cy="0" r="0.28" :fill="GOLD" stroke="#c0a047" stroke-width="0.05" />
      <rect x="-0.86" y="-0.045" width="0.28" height="0.09" fill="#c0a047" />
    </template>

    <!-- Submerged repeater -->
    <template v-else-if="kind === 'repeater'">
      <rect x="-1.6" y="-0.4" width="1.35" height="0.8" rx="0.4" :fill="SHELL" :stroke="EDGE" stroke-width="0.05" />
      <circle class="pin" cx="-0.92" cy="0" r="0.2" fill="#e8913a" />
      <circle cx="-0.92" cy="0" r="0.32" fill="none" stroke="#e8913a" stroke-width="0.04" opacity="0.6" />
    </template>

    <!-- Generic coax fitting -->
    <template v-else>
      <rect x="-1.35" y="-0.32" width="1" height="0.64" rx="0.06" :fill="SHELL" :stroke="EDGE" stroke-width="0.05" />
      <rect class="pin" x="-0.42" y="-0.05" width="0.6" height="0.1" fill="#b87333" />
    </template>
  </g>
</template>

<script setup lang="ts">
defineProps<{
  kind: string
  x: number
  y: number
  s: number
  flip?: boolean
  live?: boolean
}>()

const SHELL = '#9aa7b4'
const EDGE = '#5f6b79'
const DARK = '#141d29'
const GOLD = '#f5d06f'
</script>

<style scoped>
.pin { transition: filter 180ms ease; }
.conn.is-live .pin {
  filter: drop-shadow(0 0 3px #ffd98a) brightness(1.35);
}
</style>
