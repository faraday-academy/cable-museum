<template>
  <v-app>
    <!-- Navigation Drawer for Mobile -->
    <v-navigation-drawer
      v-model="drawer"
      temporary
      location="left"
      class="nav-drawer"
    >
      <v-list density="comfortable" class="pa-2">
        <v-list-item
          v-for="nav in navigationItems"
          :key="nav.value"
          :value="nav.value"
          :active="store.currentView === nav.value"
          @click="handleNavClick(nav.value)"
          class="nav-item"
        >
          <template #prepend>
            <v-icon :icon="nav.icon" />
          </template>
          <v-list-item-title>{{ nav.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar elevation="4" color="primary" density="comfortable">
      <v-app-bar-nav-icon
        v-if="$vuetify.display.mobile"
        @click="drawer = !drawer"
        class="d-md-none"
      />

      <v-app-bar-title class="d-flex align-center gap-2">
        <v-icon icon="mdi-cable-data" class="me-2" />
        <span class="logo-text">Cable Museum</span>
      </v-app-bar-title>
      <v-spacer />

      <!-- Desktop Navigation -->
      <v-btn-toggle
        v-if="!$vuetify.display.mobile"
        v-model="store.currentView"
        mandatory
        group
        color="primary"
        variant="outlined"
      >
        <v-btn value="museum" @click="store.setView('museum')"
          :class="{ 'active-nav': store.currentView === 'museum' }">
          <v-icon icon="mdi-timeline" class="me-1" />
          Museum
        </v-btn>
        <v-btn value="builder" @click="store.setView('builder')"
          :class="{ 'active-nav': store.currentView === 'builder' }">
          <v-icon icon="mdi-wrench" class="me-1" />
          Cable Builder
        </v-btn>
        <v-btn value="passport" @click="store.setView('passport')" :class="{ 'active-nav': store.currentView === 'passport' }">
          <v-icon icon="mdi-passport" class="me-1" />
          Passport
        </v-btn>
        <v-btn value="legends" @click="store.setView('legends')" :class="{ 'active-nav': store.currentView === 'legends' }">
          <v-icon icon="mdi-crown" class="me-1" />
          Legends
        </v-btn>
      </v-btn-toggle>

      <v-btn icon href="https://github.com/" target="_blank" rel="noopener">
        <v-icon icon="mdi-github" />
      </v-btn>
    </v-app-bar>

    <v-main>
      <transition name="museum-transition" mode="out-in">
        <div v-if="store.currentView === 'museum'" class="layout" key="museum">
          <aside class="timeline-pane">
            <Timeline />
          </aside>
          <section class="hero-pane">
            <div class="hero">
              <h1 class="gradient">Time-travel through Cable History</h1>
              <p>
                Step through 175 years of cable innovation — from Morse code to multi-gigabit fiber.
                Each stop on the timeline reveals the sparks, signals, and stories behind our connected planet.
              </p>
              <div class="sparkles" ref="sparkles" aria-hidden="true"></div>
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
import { useMuseumStore } from './stores/museum'
import Timeline from './components/Timeline.vue'
import CableBuilder from './components/CableBuilder.vue'
import Passport from './components/Passport.vue'
import LegendsPage from './components/LegendsPage.vue'
import EraDialog from './components/EraDialog.vue'

const store = useMuseumStore()
const sparkles = ref<HTMLDivElement | null>(null)
const drawer = ref(false)

// Navigation items for the mobile drawer
const navigationItems = [
  { title: 'Museum', value: 'museum', icon: 'mdi-timeline' },
  { title: 'Cable Builder', value: 'builder', icon: 'mdi-wrench' },
  { title: 'Passport', value: 'passport', icon: 'mdi-passport' },
  { title: 'Legends', value: 'legends', icon: 'mdi-crown' }
]

// Handle navigation clicks and close drawer
function handleNavClick(view: 'museum' | 'builder' | 'passport' | 'legends') {
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
.layout {
  display: grid;
  grid-template-columns: minmax(280px, 420px) 1fr;
  min-height: calc(100dvh - 64px);
}

.timeline-pane {
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  overflow: auto;
}

.hero-pane {
  position: relative;
  overflow: hidden;
}

.hero {
  padding: 40px 6vw;
}

.builder-layout {
  padding: 20px;
}

.passport-layout {
  padding: 20px;
}

.legends-layout {
  padding: 20px;
}

.nav-drawer {
  background: linear-gradient(180deg, #1a1a2e, #16213e);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  width: 280px;
}

.nav-item {
  margin-bottom: 4px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.nav-item:hover {
  background-color: rgba(34, 211, 238, 0.1);
}

.nav-item :deep(.v-list-item__overlay) {
  background: linear-gradient(135deg, #22d3ee, #a78bfa);
  opacity: 0.2;
}

.active-nav {
  background: linear-gradient(135deg, #22d3ee, #a78bfa) !important;
  color: white !important;
  box-shadow: 0 2px 8px rgba(34, 211, 238, 0.3) !important;
}

.museum-transition-enter-active,
.museum-transition-leave-active {
  transition: all 0.5s ease;
}

.museum-transition-enter-from {
  opacity: 0;
  transform: translateX(30px) scale(0.95);
}

.museum-transition-leave-to {
  opacity: 0;
  transform: translateX(-30px) scale(1.05);
}

.museum-transition-enter-active .layout {
  animation: slideInLeft 0.6s ease-out;
}

.museum-transition-enter-active .builder-layout {
  animation: slideInUp 0.6s ease-out;
}

.museum-transition-enter-active .passport-layout {
  animation: slideInRight 0.6s ease-out;
}

@keyframes slideInLeft {
  from {
    transform: translateX(-50px);
    opacity: 0;
  }

  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideInUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideInRight {
  from {
    transform: translateX(50px);
    opacity: 0;
  }

  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.gradient {
  background: linear-gradient(90deg, #22d3ee, #a78bfa, #f472b6, #22d3ee);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: hue 16s linear infinite;
}

.sparkles {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(2px 2px at 20% 30%, rgba(34, 211, 238, .35), transparent 40%), radial-gradient(2px 2px at 60% 70%, rgba(167, 139, 250, .35), transparent 40%), radial-gradient(1.5px 1.5px at 80% 20%, rgba(244, 114, 182, .35), transparent 40%);
  background-size: 200% 100%;
  pointer-events: none;
}

@keyframes hue {
  from {
    filter: hue-rotate(0deg);
  }

  to {
    filter: hue-rotate(360deg);
  }
}

.logo-text {
  font-weight: 800;
  letter-spacing: .5px;
}

@media (max-width: 900px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .timeline-pane {
    order: 2;
  }

  .hero-pane {
    order: 1;
  }

  .nav-drawer :deep(.v-navigation-drawer__content) {
    padding-top: 64px; /* Account for app bar height */
  }
}
</style>
