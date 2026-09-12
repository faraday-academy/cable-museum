import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

// Keep these in sync with src/styles/_tokens.scss — that file is the
// source of truth for CSS; this mirrors it for Vuetify's `color` props.
export const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi }
  },
  defaults: {
    VCard: { flat: true },
    VBtn: { variant: 'flat' },
    VChip: { variant: 'flat' }
  },
  theme: {
    defaultTheme: 'abyssCopper',
    themes: {
      abyssCopper: {
        dark: true,
        colors: {
          background: '#070b14',
          surface: '#0f1724',
          'surface-bright': '#16202f',
          'surface-variant': '#1e2a3c',
          'on-surface-variant': '#e8edf5',

          primary: '#e8913a',   // copper — the hero accent
          secondary: '#3fbfd4', // teal — signal
          accent: '#f5d06f',    // brass — rewards & highlights

          success: '#46c98b',
          info: '#3fbfd4',
          warning: '#f5b547',
          error: '#ef5f5f',

          'on-primary': '#1a1005',
          'on-accent': '#1a1005',
          'on-background': '#e8edf5',
          'on-surface': '#e8edf5'
        },
        variables: {
          'border-color': '#94b4d6',
          'border-opacity': 0.12,
          'high-emphasis-opacity': 1,
          'medium-emphasis-opacity': 0.72,
          'disabled-opacity': 0.38,
          'theme-overlay-multiplier': 1.4
        }
      }
    }
  }
})
