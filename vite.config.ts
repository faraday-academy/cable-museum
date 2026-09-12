import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'
import { VitePWA } from 'vite-plugin-pwa'

// The @mdi/font stylesheet lists eot, woff2, woff and ttf. Vite emits
// every file it sees referenced, so all four shipped (~3.5 MB) even
// though any browser we support takes the woff2. Rewriting the src to
// woff2 only means the other three are never referenced, so they are
// never emitted.
function mdiWoff2Only() {
  return {
    name: 'mdi-woff2-only',
    enforce: 'pre' as const,
    transform(code: string, id: string) {
      if (!id.includes('materialdesignicons') || !id.includes('.css')) return null
      const out = code.replace(
        /@font-face\{([^}]*)\}/g,
        (block: string, body: string) => {
          if (!body.includes('materialdesignicons-webfont')) return block
          const woff2 = body.match(/url\((["']?)([^)"']*materialdesignicons-webfont\.woff2[^)"']*)\1\)/)
          if (!woff2) return block
          const src = `src:url("${woff2[2]}") format("woff2")`
          // drop every existing src: declaration, then add the woff2 one
          const rest = body
            .split(';')
            .filter(d => d.trim() && !/^\s*src\s*:/.test(d))
            .join(';')
          return `@font-face{${rest};${src}}`
        }
      )
      return out === code ? null : { code: out, map: null }
    }
  }
}

export default defineConfig({
  // MUST include trailing slash for GitHub Pages project sites
  base: '/cable-museum/',

  plugins: [
    mdiWoff2Only(),
    vue(),
    vuetify({ autoImport: true }),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['icons/icon.svg'],
      manifest: {
        name: 'Cable Museum',
        short_name: 'CableMuseum',
        description: 'A fun, animated digital museum of cables through time.',
        theme_color: '#070b14',
        background_color: '#070b14',
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
