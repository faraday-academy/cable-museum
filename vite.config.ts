import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  // MUST include trailing slash for GitHub Pages project sites
  base: '/cable-museum/',

  plugins: [
    vue(),
    vuetify({ autoImport: true }),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icons/icon.svg'],
      manifest: {
        name: 'Cable Museum',
        short_name: 'CableMuseum',
        description: 'A fun, animated digital museum of cables through time.',
        theme_color: '#111827',
        background_color: '#0b1020',
        display: 'standalone',
        // PWA paths should match the base, *with* trailing slash
        start_url: '/cable-museum/',
        scope: '/cable-museum/',
        icons: [
          { src: 'icons/icon.svg', sizes: '512x512', type: 'image/svg+xml', purpose: 'any maskable' }
        ]
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,json,woff2}']
      }
    })
  ],

  resolve: {
    alias: { '@': '/src' }
  },

  server: { port: 5173 }
})
