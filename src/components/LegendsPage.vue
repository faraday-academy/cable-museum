<template>
  <v-container class="legends-page" fluid>
    <!-- Page Header -->
    <div class="page-header">
      <h1 class="legends-title">Legends of the Wire</h1>
      <p class="legends-subtitle">
        Discover the stories, rivalries, and breakthroughs that electrified communication history — from bold inventors to high-voltage misfires.
      </p>
    </div>

    <v-divider class="section-divider" />

    <!-- Section 1: Cable Myths & Misfires -->
    <section id="misfires" class="legends-section">
      <h2 class="section-title">⚡ Cable Myths & Misfires</h2>
      <p class="section-description">
        From shark-bitten cables to wild experiments that fizzled out, these are the misfires that sparked better designs.
      </p>

      <v-row class="misfires-grid">
        <v-col v-for="misfire in misfires" :key="misfire.id" cols="12" md="6" class="misfire-col">
          <v-card class="misfire-card" hover>
            <v-img :src="withBase(misfire.image)" height="200" class="misfire-image">
              <template #placeholder>
                <div class="skeleton" />
              </template>
            </v-img>
            <v-card-title class="misfire-title">{{ misfire.title }}</v-card-title>
            <v-card-text class="misfire-fact">{{ misfire.fact }}</v-card-text>
            <v-expand-transition>
              <v-card-text v-if="expandedCard === misfire.id" class="misfire-details">
                {{ misfire.details }}
              </v-card-text>
            </v-expand-transition>
            <v-card-actions>
              <v-btn
                size="small"
                variant="text"
                @click="toggleExpand(misfire.id)"
              >
                {{ expandedCard === misfire.id ? 'Less info' : 'More info' }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </section>

    <v-divider class="section-divider" />

    <!-- Section 2: Heroes of the Wire -->
    <section id="heroes" class="legends-section">
      <h2 class="section-title">🧑‍🔬 Heroes of the Wire</h2>
      <p class="section-description">
        Meet the inventors and visionaries who bent copper, glass, and light to their will.
      </p>

      <v-slide-group v-model="activeHero" show-arrows="hover" class="heroes-carousel">
        <v-slide-group-item v-for="hero in heroes" :key="hero.id" v-slot="{ isSelected, toggle }">
          <v-card
            class="hero-card mx-2"
            :class="{ 'hero-selected': isSelected }"
            @click="toggle"
          >
            <v-img :src="withBase(hero.image)" height="200" class="hero-image">
              <template #placeholder>
                <div class="skeleton" />
              </template>
            </v-img>
            <v-card-title class="hero-name">{{ hero.name }}</v-card-title>
            <v-card-subtitle class="hero-title">{{ hero.title }}</v-card-subtitle>
            <v-card-text class="hero-bio">{{ hero.bio }}</v-card-text>
          </v-card>
        </v-slide-group-item>
      </v-slide-group>
    </section>

    <v-divider class="section-divider" />

    <!-- Section 3: War of the Wires -->
    <section id="war" class="legends-section">
      <h2 class="section-title">🕵️ War of the Wires</h2>
      <p class="section-description">
        Espionage, sabotage, and rival empires racing to control the global grid.
      </p>

      <div class="war-container">
        <div class="world-map-background">
          <!-- World map SVG would go here -->
        </div>

        <v-row class="war-stories">
          <v-col v-for="story in warStories" :key="story.id" cols="12" md="6" lg="4">
            <v-card class="war-card" hover>
              <v-card-title class="war-title">{{ story.title }}</v-card-title>
              <v-card-text class="war-description">{{ story.description }}</v-card-text>
              <v-card-actions>
                <v-btn size="small" variant="outlined" @click="showWarDetails(story)">
                  Read More
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </section>

    <v-divider class="section-divider" />

    <!-- Section 4: From Copper to Light -->
    <section id="progress" class="legends-section">
      <h2 class="section-title">💡 From Copper to Light</h2>
      <p class="section-description">
        An interactive look at how data speed exploded over 175 years.
      </p>

      <div class="progress-container">
        <v-slider
          v-model="currentSpeedIndex"
          :min="0"
          :max="speedStages.length - 1"
          step="1"
          class="speed-slider"
          color="primary"
          track-color="secondary"
        >
          <template #thumb-label="{ modelValue }">
            {{ speedStages[modelValue].speed }}
          </template>
        </v-slider>

        <div class="speed-stage-display">
          <transition name="speed-transition" mode="out-in">
            <div :key="currentSpeedIndex" class="speed-stage">
              <div class="speed-icon">
                <v-icon :icon="speedStages[currentSpeedIndex].icon" size="48" />
              </div>
              <h3 class="speed-technology">{{ speedStages[currentSpeedIndex].technology }}</h3>
              <div class="speed-value">{{ speedStages[currentSpeedIndex].speed }}</div>
              <p class="speed-description">{{ speedStages[currentSpeedIndex].description }}</p>
              <div class="speed-year">{{ speedStages[currentSpeedIndex].year }}</div>
            </div>
          </transition>
        </div>
      </div>
    </section>

    <v-divider class="section-divider" />

    <!-- Section 5: Future Tech -->
    <section id="future-tech" class="legends-section">
      <h2 class="section-title">🔮 Future Tech</h2>
      <p class="section-description">
        A glimpse into the next generation of cable technologies that are redefining what's possible.
      </p>

      <v-row class="future-tech-grid">
        <v-col cols="12" md="6" class="future-tech-col">
          <v-card class="future-tech-card" hover>
            <v-img src="images/legends/future/self-healing-wires.jpg" height="250" cover class="future-tech-image">
              <template #placeholder>
                <div class="skeleton" />
              </template>
              <div class="future-tech-overlay">
                <h3 class="future-tech-title">Self-Healing Wires</h3>
                <p class="future-tech-subtitle">Cables that repair themselves</p>
              </div>
            </v-img>
            <v-card-text class="future-tech-content">
              <p>Imagine a world where cables can fix their own cuts and nicks before they become serious problems. Self-healing cables use advanced materials that can automatically repair damage, extending their lifespan and reducing maintenance costs.</p>
              
              <v-expand-transition>
                <div v-if="expandedCard === 'self-healing'" class="future-tech-details">
                  <v-divider class="my-4" />
                  <h4>How It Works</h4>
                  <ul class="tech-features">
                    <li><v-icon small color="primary">mdi-check-circle</v-icon> <strong>Microcapsule Technology:</strong> Tiny capsules release healing agents when damaged</li>
                    <li><v-icon small color="primary">mdi-check-circle</v-icon> <strong>Dynamic Bonds:</strong> Materials that can reform broken molecular bonds</li>
                    <li><v-icon small color="primary">mdi-check-circle</v-icon> <strong>Conductive Healing:</strong> Some materials can even restore electrical conductivity</li>
                  </ul>
                  
                  <h4 class="mt-4">Potential Applications</h4>
                  <v-chip-group column>
                    <v-chip variant="outlined" color="primary" size="small">Aerospace Wiring</v-chip>
                    <v-chip variant="outlined" color="primary" size="small">Undersea Cables</v-chip>
                    <v-chip variant="outlined" color="primary" size="small">Medical Devices</v-chip>
                    <v-chip variant="outlined" color="primary" size="small">Wearable Tech</v-chip>
                  </v-chip-group>
                  
                  <p class="mt-4">While still in development, these technologies promise to revolutionize how we think about cable reliability and maintenance in critical applications.</p>
                </div>
              </v-expand-transition>
              
              <v-btn
                size="small"
                variant="text"
                color="primary"
                @click="toggleExpand('self-healing')"
                class="mt-2"
              >
                {{ expandedCard === 'self-healing' ? 'Show Less' : 'Learn More' }}
                <v-icon end>{{ expandedCard === 'self-healing' ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
        
        <!-- Placeholder for future tech cards -->
        <v-col cols="12" md="6" class="future-tech-col">
          <v-card class="future-tech-card coming-soon" height="100%">
            <v-card-text class="text-center pa-8">
              <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-lightbulb-on-outline</v-icon>
              <h3 class="text-h6 mb-2">The Future of Cables</h3>
              <p class="text-grey">What revolutionary cable technology will be next? Check back soon for more exciting developments!</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </section>

    <v-divider class="section-divider" />

    <!-- Back to Timeline Button -->
    <div class="back-button-container">
      <v-btn
        size="large"
        color="primary"
        variant="elevated"
        @click="backToTimeline"
        prepend-icon="mdi-timeline"
      >
        Back to Timeline
      </v-btn>
    </div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useMuseumStore } from '@/stores/museum'

// Store
const store = useMuseumStore()

// Reactive data
const expandedCard = ref<string | null>(null)
const activeHero = ref(0)
const currentSpeedIndex = ref(0)

// Data
const misfires = [
  {
    id: 'shark-armor',
    title: 'The Shark-Proof Cable Armor',
    image: 'images/legends/misfires/shark-armor.svg',
    fact: 'Sharks were chewing through undersea cables, so engineers added chainmail armor.',
    details: 'In the 1850s, sharks discovered that telegraph cables made perfect meals. They would bite through the insulation and feast on the gutta-percha. Engineers responded with heavy chainmail armor that made cables too rigid and expensive. Modern solutions use lighter, more flexible materials.'
  },
  {
    id: 'mercury-insulators',
    title: 'Mercury Insulators',
    image: 'images/legends/misfires/mercury-insulators.svg',
    fact: 'Liquid mercury was used as insulation in early experiments.',
    details: 'In the 1830s, scientists tried using mercury as an insulator for electrical wires. The idea was that mercury would flow and fill any gaps. Unfortunately, mercury conducts electricity and the experiments were dangerous failures that led to better insulating materials.'
  },
  {
    id: 'arctic-telegraph',
    title: 'The Arctic Telegraph That Froze',
    image: 'images/legends/misfires/arctic-telegraph.svg',
    fact: 'An attempt to lay telegraph cable across the Arctic Ocean ended in frozen disaster.',
    details: 'In 1865, the American Telegraph Company attempted to lay cable across the Arctic Ocean. The expedition reached 81°N before the cable froze solid and snapped. The failure highlighted the challenges of extreme environments and led to better cable designs.'
  },
  {
    id: 'vanishing-cable',
    title: 'The Vanishing Cable of 1858',
    image: 'images/legends/misfires/vanishing-cable.svg',
    fact: 'A perfectly functioning transatlantic cable mysteriously stopped working after 27 days.',
    details: 'The 1858 transatlantic cable worked perfectly for 27 days, transmitting 400 messages. Then it suddenly went silent. Engineers assumed it had been cut by ships\' anchors, but modern analysis suggests it may have been damaged by marine life or electrolysis.'
  }
]

const heroes = [
  {
    id: 'kao',
    name: 'Charles Kao',
    title: 'Father of Fiber Optics',
    image: 'images/legends/heroes/charles-kao.svg',
    bio: 'Pioneered low-loss optical fibers, enabling modern high-speed internet.'
  },
  {
    id: 'field',
    name: 'Cyrus Field',
    title: 'Visionary of the Atlantic Cable',
    image: 'images/legends/heroes/cyrus-field.svg',
    bio: 'Persevered through multiple failures to connect Europe and America by cable.'
  },
  {
    id: 'bell',
    name: 'Alexander Graham Bell',
    title: 'The Voice over Wire Pioneer',
    image: 'images/legends/heroes/alexander-bell.svg',
    bio: 'Invented the telephone and demonstrated voice transmission over wires.'
  },
  {
    id: 'espenschied',
    name: 'Lloyd Espenschied & Herman Affel',
    title: 'Coaxial Cable Innovators',
    image: 'images/legends/heroes/espenschied-affel.svg',
    bio: 'Developed the first practical coaxial cable for television broadcasting.'
  }
]

const warStories = [
  {
    id: 'cable-race',
    title: 'The Great Cable Race',
    description: 'Britain vs. France under the seas — empires racing to control global communication.'
  },
  {
    id: 'ivy-bells',
    title: 'Operation Ivy Bells',
    description: 'Cold War espionage tapping into Soviet undersea cables.'
  },
  {
    id: 'wwi-cutters',
    title: 'WWI Cable Cutters',
    description: 'How ships hunted telegraph cables during World War I.'
  }
]

const speedStages = [
  {
    technology: 'Telegraph',
    speed: '~10 bits/min',
    description: 'Morse code tapped by hand operators',
    year: '1830s',
    icon: 'mdi-pulse'
  },
  {
    technology: 'Telephone',
    speed: '~64 kbps',
    description: 'Analog voice transmission over copper wires',
    year: '1870s',
    icon: 'mdi-phone'
  },
  {
    technology: 'Coaxial Cable',
    speed: '~10 Mbps',
    description: 'Television broadcasting and early computer networks',
    year: '1930s',
    icon: 'mdi-access-point'
  },
  {
    technology: 'Ethernet',
    speed: '~100 Mbps',
    description: 'Local area networks and internet backbone',
    year: '1980s',
    icon: 'mdi-ethernet-cable'
  },
  {
    technology: 'Fiber Optics',
    speed: '~10 Gbps',
    description: 'Light-speed data transmission worldwide',
    year: '1980s',
    icon: 'mdi-lightbulb'
  },
  {
    technology: 'Modern Fiber',
    speed: '~100 Tbps',
    description: 'Dense wavelength division multiplexing',
    year: '2020s',
    icon: 'mdi-rocket'
  }
]

// Functions
function withBase(path: string) {
  const base = import.meta.env.BASE_URL || '/'
  return `${base}${path.replace(/^\//, '')}`
}

function toggleExpand(cardId: string) {
  expandedCard.value = expandedCard.value === cardId ? null : cardId
}

function showWarDetails(story: any) {
  // Could open a dialog with full story details
  console.log('Show war details for:', story.title)
}

function backToTimeline() {
  store.setView('museum')
}
</script>

<style scoped>
.legends-page {
  background: #0b0d17;
  color: white;
  min-height: 100vh;
  padding: 2rem 1rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.legends-title {
  background: linear-gradient(90deg, #22d3ee, #a78bfa, #f472b6, #22d3ee);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  animation: hue 16s linear infinite;
}

.legends-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.8);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.section-divider {
  margin: 4rem 0;
  border-color: rgba(255, 255, 255, 0.1);
}

.legends-section {
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #22d3ee;
}

.section-description {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 2rem;
  line-height: 1.5;
}

/* Misfires Section */
.misfires-grid {
  margin-top: 2rem;
}

.misfire-card {
  height: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.misfire-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(34, 211, 238, 0.2);
}

.misfire-image {
  border-radius: 8px 8px 0 0;
}

.misfire-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #a78bfa;
}

.misfire-fact {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.95rem;
  line-height: 1.4;
}

.misfire-details {
  background: rgba(34, 211, 238, 0.1);
  border-left: 3px solid #22d3ee;
  padding: 1rem;
  margin: 0.5rem 0;
  border-radius: 4px;
}

/* Heroes Section */
.heroes-carousel {
  margin-top: 2rem;
}

.hero-card {
  min-width: 280px;
  height: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease;
}

.hero-card:hover {
  transform: translateY(-3px);
}

.hero-selected {
  border-color: #22d3ee;
  box-shadow: 0 0 20px rgba(34, 211, 238, 0.3);
}

.hero-image {
  border-radius: 8px 8px 0 0;
}

.hero-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #f472b6;
}

.hero-title {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.hero-bio {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.85rem;
  line-height: 1.4;
}

/* War Section */
.war-container {
  position: relative;
  margin-top: 2rem;
}

.world-map-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(34, 211, 238, 0.05);
  border-radius: 12px;
  opacity: 0.3;
}

.war-stories {
  position: relative;
  z-index: 2;
}

.war-card {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease;
}

.war-card:hover {
  transform: translateY(-3px);
  background: rgba(255, 255, 255, 0.12);
}

.war-title {
  color: #a78bfa;
  font-weight: 600;
}

.war-description {
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.4;
}

/* Progress Section */
.progress-container {
  margin-top: 3rem;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.speed-slider {
  margin-bottom: 3rem;
}

.speed-stage-display {
  text-align: center;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.speed-stage {
  max-width: 400px;
}

.speed-icon {
  margin-bottom: 1rem;
  color: #22d3ee;
}

.speed-technology {
  font-size: 1.8rem;
  font-weight: 700;
  color: #f472b6;
  margin-bottom: 0.5rem;
}

.speed-value {
  font-size: 1.4rem;
  font-weight: 600;
  color: #a78bfa;
  margin-bottom: 1rem;
}

.speed-description {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
  margin-bottom: 1rem;
}

.speed-year {
  font-size: 0.9rem;
  color: #22d3ee;
  font-weight: 500;
}

.speed-transition-enter-active,
.speed-transition-leave-active {
  transition: all 0.5s ease;
}

.speed-transition-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.9);
}

.speed-transition-leave-to {
  opacity: 0;
  transform: translateY(-20px) scale(1.1);
}

/* Back Button */
.back-button-container {
  text-align: center;
  margin-top: 4rem;
  padding-bottom: 2rem;
}

/* Animations */
@keyframes hue {
  from {
    filter: hue-rotate(0deg);
  }
  to {
    filter: hue-rotate(360deg);
  }
}

.skeleton {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Future Tech Section */
.future-tech-grid {
  margin-top: 2rem;
}

.future-tech-card {
  height: 100%;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border-radius: 12px;
  overflow: hidden;
  background: #1a1e2e;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.future-tech-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
}

.future-tech-image {
  position: relative;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
}

.future-tech-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 1.5rem;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  color: white;
}

.future-tech-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
}

.future-tech-subtitle {
  margin: 0.25rem 0 0;
  opacity: 0.9;
  font-weight: 400;
}

.future-tech-content {
  padding: 1.5rem;
  background: #1a1e2e;
}

.future-tech-details {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.tech-features {
  padding-left: 1.5rem;
  margin: 1rem 0;
}

.tech-features li {
  margin-bottom: 0.75rem;
  line-height: 1.6;
  display: flex;
  align-items: flex-start;
}

.tech-features .v-icon {
  margin-right: 0.75rem;
  margin-top: 0.2rem;
  flex-shrink: 0;
}

.coming-soon {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.02) !important;
  border: 2px dashed rgba(255, 255, 255, 0.1) !important;
  transition: all 0.3s ease;
}

.coming-soon:hover {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: var(--v-primary-base) !important;
}

.coming-soon .v-icon {
  opacity: 0.7;
  transition: all 0.3s ease;
}

.coming-soon:hover .v-icon {
  color: var(--v-primary-base) !important;
  opacity: 1;
  transform: scale(1.1);
}

/* Responsive */
@media (max-width: 768px) {
  .legends-title {
    font-size: 2.5rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .hero-card {
    min-width: 250px;
  }

  .progress-container {
    padding: 1rem;
  }

  .speed-technology {
    font-size: 1.5rem;
  }
}
</style>
