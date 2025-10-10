# Cable Museum (Vue 3 + Pinia + Vuetify + Vite PWA)

- **Stack**: Vue 3, Vite, Pinia, Vuetify 3, GSAP, VueUse, vite-plugin-pwa
- **Features**: Vertical timeline museum with key advancements, cable builder with preview, cross-section views, interactive explorer mode with zoom/animations, quiz trivia dialogs, user passport for progress tracking, dialogs with video/gallery, animated theme, PWA-ready, GitHub Pages friendly

## Sections

- **Museum**: Explore cable history through an interactive vertical timeline. Click eras for stories, videos, and facts.
- **Cable Builder**: Design custom cables by selecting wires, insulation, and connectors. See live SVG preview and specs.
- **Passport**: Track your exploration progress, view visited eras, and manage saved cables.

## Local dev

```bash
pnpm i # or npm i / yarn
pnpm dev
```

Open http://localhost:5173/cable-museum/ if base is applied, or http://localhost:5173 depending on your setup.

## Build

```bash
pnpm build
pnpm preview
```

## Content

- JSON at `public/content/cable_eras.json`
- Images in `public/images/` and icons in `public/icons/`

## Deploy to GitHub Pages

The app is pre-configured for automatic deployment to GitHub Pages:

### Automatic Deployment (Recommended)
1. Push your code to the `main` branch
2. GitHub Actions will automatically build and deploy to Pages
3. Your site will be available at `https://[username].github.io/cable-museum/`

### Manual Deployment
```bash
npm run deploy  # Builds and deploys to gh-pages branch
```

### Configuration
- Base path: `/cable-museum/` (configured in `vite.config.ts`)
- PWA-ready with service worker caching
- `.nojekyll` file prevents Jekyll processing
- SPA routing compatible with GitHub Pages

### Repository Settings
1. Go to Settings → Pages
2. Set source to "GitHub Actions" (recommended) or "Deploy from a branch" → `gh-pages`
3. The site will be live at your GitHub Pages URL

## PWA

- vite-plugin-pwa is configured for `autoUpdate` and caches built assets.
- Manifest at `public/manifest.webmanifest` and icon at `public/icons/icon.svg`.

## Accessibility & Responsiveness

- Works on mobile/desktop, keyboard activations on timeline cards, proper color contrast in dark theme.
