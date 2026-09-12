<template>
  <v-app>
    <!-- Mobile navigation drawer -->
    <v-navigation-drawer v-model="drawer" temporary location="left" class="nav-drawer">
      <div class="drawer-brand">
        <span class="brand-mark" aria-hidden="true"></span>
        <span class="brand-word">Cable Museum</span>
      </div>
      <hr class="rule-fade" />
      <nav class="drawer-nav" aria-label="Main">
        <button
          v-for="nav in navigationItems"
          :key="nav.value"
          type="button"
          class="drawer-link"
          :class="{ 'is-active': store.currentView === nav.value }"
          :aria-current="store.currentView === nav.value ? 'page' : undefined"
          @click="handleNavClick(nav.value)"
        >
          <v-icon :icon="nav.icon" size="20" />
          <span>{{ nav.title }}</span>
        </button>
      </nav>
    </v-navigation-drawer>

    <!-- ── Top navigation ──────────────────────────────────────
         A flat, blurred bar in the same family as the page — not a
         slab of saturated colour. Active state is a copper rule
         under the word, not a box around it. -->
    <v-app-bar flat color="transparent" height="64" class="topbar">
      <v-app-bar-nav-icon
        v-if="$vuetify.display.mobile"
        class="d-md-none topbar__burger"
        aria-label="Open navigation"
        @click="drawer = !drawer"
      />

      <a class="brand" href="#" @click.prevent="store.setView('museum')">
        <span class="brand-mark" aria-hidden="true"></span>
        <span class="brand-word">Cable<span class="brand-word--thin">Museum</span></span>
      </a>

      <v-spacer />

      <nav v-if="!$vuetify.display.mobile" class="topnav" aria-label="Main">
        <button
          v-for="nav in navigationItems"
          :key="nav.value"
          type="button"
          class="topnav__link"
          :class="{ 'is-active': store.currentView === nav.value }"
          :aria-current="store.currentView === nav.value ? 'page' : undefined"
          @click="store.setView(nav.value)"
        >
          <v-icon :icon="nav.icon" size="17" class="topnav__icon" />
          <span>{{ nav.title }}</span>
        </button>
      </nav>

      <a
        class="topbar__github"
        href="https://github.com/"
        target="_blank"
        rel="noopener"
        aria-label="View source on GitHub"
      >
        <v-icon icon="mdi-github" size="21" />
      </a>
    </v-app-bar>

    <v-main>
      <transition name="museum-transition" mode="out-in">
        <div v-if="store.currentView === 'museum'" class="layout" key="museum">
          <aside class="timeline-pane">
            <Timeline />
          </aside>
          <section class="hero-pane">
            <div class="hero">
              <p class="eyebrow hero__eyebrow">175 years of signal</p>
              <h1 class="hero__title">
                Time-travel through
                <span class="gradient-text">Cable History</span>
              </h1>
              <p class="hero__lede">
                Step through 175 years of cable innovation — from Morse code to multi-gigabit fiber.
                Each stop on the timeline reveals the sparks, signals, and stories behind our connected planet.
              </p>
              <div class="hero__hint">
                <v-icon icon="mdi-arrow-left" size="16" />
                <span>Pick an era to open the exhibit</span>
              </div>
              <div class="sparkles" ref="sparkles" aria-hidden="true"></div>
            </div>
            <div class="hero-ladder">
              <SpeedLadder />
            </div>
          </section>
        </div>
        <div v-else-if="store.currentView === 'passport'" class="passport-layout" key="passport">
          <Passport />
        </div>
        <div v-else-if="store.currentView === 'builder'" class="builder-layout" key="builder">
          <CableBuilder />
        </div>
        <div v-else class="legends-layout" key="legends">
          <LegendsPage />
        </div>
      </transition>
    </v-main>

    <EraDialog />
  </v-app>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { gsap } from 'gsap'
import { useMuseumStore } from './stores/museum'
import Timeline from './components/Timeline.vue'
import CableBuilder from './components/CableBuilder.vue'
import Passport from './components/Passport.vue'
import LegendsPage from './components/LegendsPage.vue'
import EraDialog from './components/EraDialog.vue'
import SpeedLadder from './components/SpeedLadder.vue'

type ViewName = 'museum' | 'builder' | 'passport' | 'legends'

const store = useMuseumStore()
const sparkles = ref<HTMLDivElement | null>(null)
const drawer = ref(false)

const navigationItems: { title: string; value: ViewName; icon: string }[] = [
  { title: 'Museum', value: 'museum', icon: 'mdi-timeline' },
  { title: 'Cable Builder', value: 'builder', icon: 'mdi-wrench' },
  { title: 'Passport', value: 'passport', icon: 'mdi-passport' },
  { title: 'Legends', value: 'legends', icon: 'mdi-crown' }
]

// Handle navigation clicks and close drawer
function handleNavClick(view: ViewName) {
  store.setView(view)
  drawer.value = false
}

onMounted(async () => {
  await store.loadContent()
  if (sparkles.value) {
    gsap.to(sparkles.value, { backgroundPositionX: '200%', repeat: -1, duration: 12, ease: 'none' })
  }
})
</script>

<style scoped>
/* ── Top bar ───────────────────────────────────────────────── */
.topbar {
  background: rgba(7, 11, 20, 0.72) !important;
  backdrop-filter: blur(16px) saturate(160%);
  -webkit-backdrop-filter: blur(16px) saturate(160%);
  border-bottom: 1px solid var(--line);
}

.topbar :deep(.v-toolbar__content) {
  padding-inline: clamp(12px, 3vw, 28px);
  gap: 8px;
}

.topbar__burger { color: var(--text-muted); }

/* ── Brand ─────────────────────────────────────────────────── */
.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text);
  padding: 4px 2px;
  border-radius: var(--r-sm);
}

/* A copper conductor seen end-on: bright core, insulation, jacket. */
.brand-mark {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  flex: none;
  background: radial-gradient(circle at 50% 50%,
      var(--brass) 0 22%,
      var(--copper) 22% 42%,
      var(--abyss-deep) 42% 62%,
      var(--copper-deep) 62% 100%);
  box-shadow: 0 0 0 1px var(--line-copper), 0 0 14px var(--copper-glow);
}

.brand-word {
  font-weight: 800;
  font-size: 1.02rem;
  letter-spacing: var(--tracking-tight);
}

.brand-word--thin {
  font-weight: 400;
  color: var(--text-muted);
  margin-left: 0.28em;
}

/* ── Nav links: text + copper underline, no boxes ──────────── */
.topnav {
  display: flex;
  align-items: center;
  gap: clamp(2px, 1vw, 10px);
  height: 100%;
}

.topnav__link {
  position: relative;
  appearance: none;
  background: none;
  border: 0;
  cursor: pointer;
  font: inherit;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: var(--tracking-caps);
  color: var(--text-muted);
  padding: 8px 12px 9px;
  border-radius: var(--r-sm);
  display: inline-flex;
  align-items: center;
  gap: 7px;
  white-space: nowrap;
  transition: color var(--t-fast) var(--ease);
}

.topnav__icon {
  opacity: 0.65;
  transition: opacity var(--t-fast) var(--ease), color var(--t-fast) var(--ease);
}

/* The indicator. Scales from the centre so it reads like a signal
   arriving, and it is the ONLY thing marking the active tab. */
.topnav__link::after {
  content: '';
  position: absolute;
  left: 12px;
  right: 12px;
  bottom: 0;
  height: 2px;
  border-radius: var(--r-pill);
  background: var(--copper);
  box-shadow: 0 0 12px var(--copper-glow);
  transform: scaleX(0);
  transition: transform var(--t-med) var(--ease-out);
}

.topnav__link:hover {
  color: var(--text);
}

.topnav__link:hover .topnav__icon { opacity: 1; }

.topnav__link:hover::after {
  transform: scaleX(0.45);
  background: var(--text-dim);
  box-shadow: none;
}

.topnav__link.is-active {
  color: var(--copper-bright);
}

.topnav__link.is-active .topnav__icon {
  opacity: 1;
  color: var(--copper);
}

.topnav__link.is-active::after,
.topnav__link.is-active:hover::after {
  transform: scaleX(1);
  background: var(--copper);
  box-shadow: 0 0 12px var(--copper-glow);
}

.topbar__github {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  margin-left: 6px;
  border-radius: var(--r-sm);
  color: var(--text-muted);
  border: 1px solid transparent;
  transition: color var(--t-fast) var(--ease), border-color var(--t-fast) var(--ease), background-color var(--t-fast) var(--ease);
}

.topbar__github:hover {
  color: var(--text);
  background: var(--surface-2);
  border-color: var(--line);
}

/* ── Layout ────────────────────────────────────────────────── */
.layout {
  display: grid;
  grid-template-columns: minmax(280px, 420px) 1fr;
  min-height: calc(100dvh - 64px);
}

.timeline-pane {
  border-right: 1px solid var(--line);
  overflow: auto;
}

.hero-pane {
  position: relative;
  overflow: auto;
  max-height: calc(100dvh - 64px);
}

.hero-ladder {
  padding: 0 clamp(24px, 6vw, 80px) clamp(28px, 4vw, 48px);
  position: relative;
  z-index: 1;
}

.hero {
  padding: clamp(32px, 6vw, 72px) clamp(24px, 6vw, 80px) clamp(20px, 3vw, 32px);
  max-width: 780px;
  position: relative;
  z-index: 1;
}

.hero__eyebrow {
  color: var(--copper);
  margin: 0 0 14px;
}

.hero__title {
  font-size: clamp(2.1rem, 4.6vw, 3.4rem);
  font-weight: 800;
  margin: 0 0 18px;
  line-height: 1.06;
}

.hero__lede {
  color: var(--text-muted);
  font-size: clamp(0.98rem, 1.2vw, 1.1rem);
  line-height: 1.65;
  max-width: 62ch;
  margin: 0;
}

.hero__hint {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 28px;
  padding: 8px 14px;
  border-radius: var(--r-pill);
  background: var(--surface);
  border: 1px solid var(--line);
  color: var(--text-muted);
  font-size: 0.82rem;
  font-weight: 600;
}

.hero__hint .v-icon { color: var(--copper); }

.builder-layout,
.passport-layout,
.legends-layout {
  padding: clamp(16px, 3vw, 32px);
}

/* ── Drawer ────────────────────────────────────────────────── */
.nav-drawer {
  background: var(--surface) !important;
  border-right: 1px solid var(--line) !important;
  width: 280px;
}

.drawer-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 18px 18px 14px;
}

.drawer-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 12px 10px;
}

.drawer-link {
  appearance: none;
  border: 0;
  background: transparent;
  cursor: pointer;
  font: inherit;
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.03em;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 12px;
  border-radius: var(--r-md);
  text-align: left;
  position: relative;
  transition: color var(--t-fast) var(--ease), background-color var(--t-fast) var(--ease);
}

.drawer-link:hover {
  color: var(--text);
  background: var(--surface-2);
}

.drawer-link.is-active {
  color: var(--copper-bright);
  background: var(--copper-tint);
}

/* Copper spine on the active row — vertical echo of the top-bar rule. */
.drawer-link.is-active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 3px;
  border-radius: var(--r-pill);
  background: var(--copper);
  box-shadow: 0 0 10px var(--copper-glow);
}

/* ── View transitions ──────────────────────────────────────── */
.museum-transition-enter-active,
.museum-transition-leave-active {
  transition: opacity var(--t-med) var(--ease), transform var(--t-med) var(--ease-out);
}

.museum-transition-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.museum-transition-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* ── Sparkle field ─────────────────────────────────────────── */
.sparkles {
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(2px 2px at 20% 30%, var(--copper-glow), transparent 40%),
    radial-gradient(2px 2px at 60% 70%, var(--teal-glow), transparent 40%),
    radial-gradient(1.5px 1.5px at 80% 20%, var(--brass-tint), transparent 40%);
  background-size: 200% 100%;
  pointer-events: none;
  z-index: 0;
}

@media (max-width: 900px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .timeline-pane {
    order: 2;
    border-right: 0;
    border-top: 1px solid var(--line);
  }

  .hero-pane {
    order: 1;
  }

  .nav-drawer :deep(.v-navigation-drawer__content) {
    padding-top: 8px;
  }
}
</style>
