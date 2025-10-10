import { defineStore } from 'pinia'

export type Era = {
  id: string
  title: string
  years: string
  summary: string
  image: string
  video?: string
  gallery?: string[]
  facts?: string[]
  links?: { label: string; href: string }[]
  crossSection?: {
    svg: string
    parts: { name: string; path: string; color: string }[]
  }
  keyAdvancement?: string
  trivia?: {
    question: string
    options: string[]
    correct: number
    fact: string
  }[]
}

export type CablePart = {
  id: string
  name: string
  type: 'wire' | 'insulation' | 'connector'
  specs: { [key: string]: string | number }
  color?: string
}

export const useMuseumStore = defineStore('museum', {
  state: () => ({
    eras: [] as Era[],
    selectedEraId: null as string | null,
    dialogOpen: false,
    currentView: 'museum' as 'museum' | 'builder' | 'passport' | 'legends',
    cableParts: [
      // Wires
      { id: 'copper-22awg', name: 'Copper 22AWG', type: 'wire', specs: { gauge: 22, material: 'Copper', resistance: '16.5 Ω/km' }, color: '#b87333' },
      { id: 'aluminum-18awg', name: 'Aluminum 18AWG', type: 'wire', specs: { gauge: 18, material: 'Aluminum', resistance: '21.4 Ω/km' }, color: '#c0c0c0' },
      { id: 'fiber-optic', name: 'Fiber Optic Strand', type: 'wire', specs: { type: 'Single-mode', bandwidth: '10Gbps', distance: '10km' }, color: '#ffffff' },
      // Insulation
      { id: 'pvc-insul', name: 'PVC Insulation', type: 'insulation', specs: { material: 'PVC', tempRating: '80°C', dielectric: '4' }, color: '#ffa500' },
      { id: 'teflon-insul', name: 'Teflon Insulation', type: 'insulation', specs: { material: 'PTFE', tempRating: '200°C', dielectric: '2.1' }, color: '#ffffff' },
      { id: 'rubber-insul', name: 'Rubber Insulation', type: 'insulation', specs: { material: 'EPDM', tempRating: '90°C', dielectric: '3' }, color: '#000000' },
      // Connectors
      { id: 'rj45-male', name: 'RJ45 Male', type: 'connector', specs: { type: 'Ethernet', pins: 8, standard: 'T568A' }, color: '#c0c0c0' },
      { id: 'usb-c-male', name: 'USB-C Male', type: 'connector', specs: { type: 'USB', version: '3.1', power: '100W' }, color: '#000000' },
      { id: 'hdmi-male', name: 'HDMI Male', type: 'connector', specs: { type: 'Video', version: '2.1', resolution: '8K' }, color: '#000000' },
      { id: 'banana-plug', name: 'Banana Plug', type: 'connector', specs: { type: 'Audio', gauge: '4mm', material: 'Brass' }, color: '#ffd700' }
    ] as CablePart[],
    selectedCable: {
      wire: null as CablePart | null,
      insulation: null as CablePart | null,
      connector: null as CablePart | null
    },
    answeredTrivia: {} as Record<string, number[]>, // eraId -> array of answered question indices
    savedCables: [] as Array<{ name: string; cable: { wire: CablePart | null; insulation: CablePart | null; connector: CablePart | null } }>,
    visitedEras: [] as string[]
  }),
  getters: {
    selectedEra(state) {
      return state.eras.find(e => e.id === state.selectedEraId) || null
    },
    assembledCable(state) {
      const { wire, insulation, connector } = state.selectedCable
      if (!wire || !insulation || !connector) return null
      return {
        parts: [wire, insulation, connector],
        totalSpecs: {
          ...wire.specs,
          insulation: insulation.name,
          connector: connector.name
        }
      }
    }
  },
  actions: {
    async loadContent() {
      const base = import.meta.env.BASE_URL || '/'
      const res = await fetch(`${base}content/cable_eras_v2.json`)
      this.eras = await res.json()
    },
    openEra(id: string) {
      this.selectedEraId = id
      this.dialogOpen = true
    },
    closeDialog() {
      this.dialogOpen = false
    },
    setView(view: 'museum' | 'builder' | 'passport' | 'legends') {
      this.currentView = view
    },
    selectPart(type: 'wire' | 'insulation' | 'connector', part: CablePart | null) {
      this.selectedCable[type] = part
    },
    markTriviaAnswered(eraId: string, questionIndex: number) {
      if (!this.answeredTrivia[eraId]) {
        this.answeredTrivia[eraId] = []
      }
      if (!this.answeredTrivia[eraId].includes(questionIndex)) {
        this.answeredTrivia[eraId].push(questionIndex)
      }
    },
    isTriviaAnswered(eraId: string, questionIndex: number): boolean {
      return this.answeredTrivia[eraId]?.includes(questionIndex) || false
    },
    saveCable(name: string) {
      const cable = { ...this.selectedCable }
      this.savedCables.push({ name, cable })
    },
    markEraVisited(eraId: string) {
      if (!this.visitedEras.includes(eraId)) {
        this.visitedEras.push(eraId)
      }
    }
  },
  persist: {
    key: 'cable-museum',
    paths: ['selectedEraId', 'currentView', 'selectedCable', 'answeredTrivia', 'savedCables', 'visitedEras']
  }
})
