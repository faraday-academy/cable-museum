import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

export const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi }
  },
  theme: {
    defaultTheme: 'cableDark',
    themes: {
      cableDark: {
        dark: true,
        colors: {
          background: '#0b1020',
          surface: '#111827',
          primary: '#22d3ee',
          secondary: '#a78bfa',
          accent: '#f472b6',
          success: '#34d399',
          info: '#60a5fa',
          warning: '#f59e0b',
          error: '#ef4444'
        }
      }
    }
  }
})
