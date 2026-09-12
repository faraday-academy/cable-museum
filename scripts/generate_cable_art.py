#!/usr/bin/env python3
"""
Generate the Cable Museum's cable artwork + spec data from ONE source.

Outputs
  public/content/cable_specs.json   — layer/connector/chip spec per era
  public/images/eras/<id>.svg       — thumbnail: real cross-section + connector

The Vue components (CableCrossSection / CableCutaway) read the same JSON,
so the thumbnail and the interactive diagram can never drift apart.

Run:  python3 scripts/generate_cable_art.py
"""

import json
import math
import os

from cable_specs_new import NEW_SPECS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Material palette ─────────────────────────────────────────────
# Kept close to the real thing: copper is copper, glass is pale blue,
# steel armour is cold grey. Matches the Abyss & Copper tokens.
M = {
    "copper":     {"fill": "#b87333", "edge": "#8a5524", "hi": "#e8913a", "name": "Copper"},
    "copper-lit": {"fill": "#e8913a", "edge": "#b86b22", "hi": "#ffc98a", "name": "Copper"},
    "tinned":     {"fill": "#c3ccd8", "edge": "#8d97a4", "hi": "#e8eef5", "name": "Tinned copper"},
    "steel":      {"fill": "#9aa7b4", "edge": "#6d7884", "hi": "#c9d4de", "name": "Steel"},
    "iron":       {"fill": "#7d8894", "edge": "#586471", "hi": "#a7b2bd", "name": "Iron"},
    "gutta":      {"fill": "#6b4f2a", "edge": "#4a3619", "hi": "#8f6d3d", "name": "Gutta-percha"},
    "hemp":       {"fill": "#8a6b45", "edge": "#5f4930", "hi": "#ab8a60", "name": "Tarred hemp"},
    "jute":       {"fill": "#7e6a48", "edge": "#584a33", "hi": "#a08a63", "name": "Jute serving"},
    "rubber":     {"fill": "#2c2c30", "edge": "#161618", "hi": "#45454b", "name": "Rubber"},
    "cotton":     {"fill": "#b9ae95", "edge": "#8b8170", "hi": "#d8cfba", "name": "Cotton braid"},
    "paper":      {"fill": "#a9a08c", "edge": "#7d7566", "hi": "#cbc3b1", "name": "Paper"},
    "pe":         {"fill": "#22303f", "edge": "#14202c", "hi": "#35485c", "name": "Polyethylene"},
    "foam-pe":    {"fill": "#2b3b4c", "edge": "#1a2735", "hi": "#3f556d", "name": "Foamed PE"},
    "pvc":        {"fill": "#1b2531", "edge": "#0e1620", "hi": "#2c3a4a", "name": "PVC jacket"},
    "lszh":       {"fill": "#1d2a2a", "edge": "#101a1a", "hi": "#2e4242", "name": "LSZH jacket"},
    "teflon":     {"fill": "#2a3646", "edge": "#18212c", "hi": "#3d4c60", "name": "FEP insulation"},
    "foil":       {"fill": "#c7d2da", "edge": "#94a1ab", "hi": "#e6eef4", "name": "Foil shield"},
    "braid":      {"fill": "#8b98a8", "edge": "#5f6b79", "hi": "#b6c2cf", "name": "Braided shield"},
    "glass":      {"fill": "#8fd8e8", "edge": "#4f9db0", "hi": "#d3f4fb", "name": "Glass core"},
    "cladding":   {"fill": "#3a6b7d", "edge": "#25495a", "hi": "#5b93a7", "name": "Cladding"},
    "coating":    {"fill": "#244553", "edge": "#152e39", "hi": "#376a7d", "name": "Acrylate coating"},
    "aramid":     {"fill": "#d9c48a", "edge": "#a89660", "hi": "#f0e0b0", "name": "Aramid yarn"},
    "gel":        {"fill": "#2f4a52", "edge": "#1c3037", "hi": "#476b76", "name": "Filling gel"},
    "gold":       {"fill": "#f5d06f", "edge": "#c0a047", "hi": "#ffeaa8", "name": "Gold contact"},
    "silicon":    {"fill": "#38455c", "edge": "#222c3d", "hi": "#54658a", "name": "Silicon die"},
    "pcb":        {"fill": "#1f4d3d", "edge": "#123024", "hi": "#2f7259", "name": "PCB"},
    "polymer":    {"fill": "#4c3a63", "edge": "#2f2340", "hi": "#6f5690", "name": "Healing polymer"},
    "capsule":    {"fill": "#7fe3c0", "edge": "#3f9e82", "hi": "#b6f5e0", "name": "Microcapsules"},
    "air":        {"fill": "#0d1420", "edge": "#060a12", "hi": "#1a2536", "name": "Air gap"},
}

# ── Cable specs ──────────────────────────────────────────────────
# layers are listed OUTERMOST → INNERMOST, radius normalised to 1.0
# pattern: solid | armour | braid | foil | weave | foam
# cores: sub-conductors drawn inside the innermost layer
#
# L(label, material, r, pattern, note)
def L(label, material, r, pattern="solid", note=""):
    return {"label": label, "material": material, "r": r, "pattern": pattern, "note": note}


def C(kind, label, note=""):
    return {"kind": kind, "label": label, "note": note}


def CHIP(label, role, note=""):
    return {"label": label, "role": role, "note": note}


SPECS = {
    # ── Telegraph era ────────────────────────────────────────────
    "1850-dover-calais": {
        "family": "telegraph",
        "signal": {"kind": "current", "label": "Morse current", "speed": 0.55},
        "tagline": "One copper wire, wrapped in tree sap, dropped in the Channel.",
        "layers": [
            L("Iron wire armour", "iron", 1.00, "armour", "Ten iron wires laid in a spiral so trawlers and rock could not cut the core."),
            L("Tarred hemp", "hemp", 0.72, "weave", "A cushion between hard armour and soft insulation."),
            L("Gutta-percha", "gutta", 0.52, "solid", "Latex from a Malayan tree — the first plastic that stayed watertight in cold seawater."),
            L("Copper conductor", "copper", 0.24, "solid", "A single solid copper wire. Every Morse dot crossed the Channel through this."),
        ],
        "connectors": [C("terminal", "Brass screw terminal", "The wire was simply clamped under a brass screw at the shore station.")],
        "chips": [],
    },
    "1858-transatlantic": {
        "family": "telegraph",
        "signal": {"kind": "current", "label": "Morse current", "speed": 0.28},
        "tagline": "Seven copper strands, 2 500 miles, and about 0.1 words per minute.",
        "layers": [
            L("Iron wire armour", "iron", 1.00, "armour", "18 iron strands — too light for the job, which is partly why it failed."),
            L("Tarred hemp", "hemp", 0.74, "weave", "Padding and corrosion protection."),
            L("Gutta-percha", "gutta", 0.54, "solid", "Three coats. Any pinhole meant seawater and a dead cable."),
            L("Stranded copper", "copper", 0.26, "solid", "Seven copper wires twisted together — stranding survives bending better than one thick wire."),
        ],
        "cores": {"count": 7, "material": "copper", "r": 0.085, "ring": 0.155},
        "connectors": [C("terminal", "Brass screw terminal", "Shore ends landed on brass terminals in a wooden testing hut.")],
        "chips": [],
    },
    "1866-transatlantic": {
        "family": "telegraph",
        "signal": {"kind": "current", "label": "Morse current", "speed": 0.42},
        "tagline": "Same idea as 1858, built properly. It lasted decades.",
        "layers": [
            L("Galvanised steel armour", "steel", 1.00, "armour", "Stronger, zinc-coated wires, each wrapped in tarred manila."),
            L("Jute serving", "jute", 0.76, "weave", "Bedding layer that let the armour flex without biting in."),
            L("Gutta-percha", "gutta", 0.56, "solid", "Four alternating layers of gutta-percha and Chatterton's compound."),
            L("Stranded copper", "copper", 0.27, "solid", "Heavier copper than 1858 — less resistance, faster signalling."),
        ],
        "cores": {"count": 7, "material": "copper", "r": 0.088, "ring": 0.16},
        "connectors": [C("terminal", "Brass screw terminal", "")],
        "chips": [],
    },
    # ── Telephone era ────────────────────────────────────────────
    "1876-first-telephone": {
        "family": "telephone",
        "signal": {"kind": "audio", "label": "Analogue voice", "speed": 0.6},
        "tagline": "Voice, as a wobbling current, on a bare iron line.",
        "layers": [
            L("Cotton braid", "cotton", 1.00, "braid", "Waxed cotton — weatherproofing, 1870s style."),
            L("Rubber insulation", "rubber", 0.72, "solid", "Natural rubber kept the line from shorting on wet poles."),
            L("Iron line wire", "iron", 0.38, "solid", "Iron, not copper — cheap and strong, but lossy and noisy."),
        ],
        "connectors": [C("binding-post", "Binding post", "A screw post on the telephone box; you wrapped the wire round it by hand.")],
        "chips": [],
    },
    "1881-twisted-pair": {
        "family": "telephone",
        "signal": {"kind": "differential", "label": "Balanced pair", "speed": 0.7},
        "tagline": "Twist the two wires together and the noise cancels itself out.",
        "layers": [
            L("Cotton braid", "cotton", 1.00, "braid", "Outer protective braid."),
            L("Paper insulation", "paper", 0.80, "solid", "Dry paper wrap — cheap, and a fine insulator until it got wet."),
        ],
        "cores": {"count": 2, "material": "copper", "r": 0.30, "ring": 0.31, "twist": True},
        "connectors": [C("binding-post", "Binding post", "")],
        "chips": [],
    },
    # ── Coax era ─────────────────────────────────────────────────
    "1931-coax-patent": {
        "family": "coax",
        "signal": {"kind": "rf", "label": "RF carrier", "speed": 0.85},
        "tagline": "Put the return path *around* the signal and the cable stops radiating.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", "Keeps water and hands off the shield."),
            L("Copper braid shield", "braid", 0.82, "braid", "The return conductor AND the shield — this is the whole trick of coax."),
            L("Polyethylene dielectric", "pe", 0.66, "solid", "Holds the centre wire exactly on the axis. Spacing sets the impedance."),
            L("Copper centre conductor", "copper", 0.20, "solid", "Signal rides here, perfectly surrounded by its own return path."),
        ],
        "connectors": [C("coax-fitting", "Coaxial fitting", "Early screw fittings kept the shield continuous through the joint.")],
        "chips": [],
    },
    "1936-coax-trials": {
        "family": "coax",
        "signal": {"kind": "rf", "label": "Broadband carrier", "speed": 0.88},
        "tagline": "240 telephone calls down one tube of copper.",
        "layers": [
            L("Steel tape armour", "steel", 1.00, "armour", "Long-haul routes were buried; the tape took the abuse."),
            L("Lead sheath", "tinned", 0.84, "solid", "A sealed metal sheath — the only reliable moisture barrier of the era."),
            L("Copper outer tube", "copper", 0.70, "solid", "A solid copper tube as the return conductor."),
            L("Disc spacers / air", "air", 0.60, "foam", "Mostly air, with insulating discs every few centimetres. Air is the best dielectric there is."),
            L("Copper centre conductor", "copper", 0.18, "solid", "Carried the multiplexed carrier signal."),
        ],
        "connectors": [C("coax-fitting", "Coaxial fitting", "")],
        "chips": [],
    },
    "1956-tat1": {
        "family": "coax",
        "signal": {"kind": "rf", "label": "Voice carrier", "speed": 0.8},
        "tagline": "The first transatlantic telephone cable — with valve amplifiers on the seabed.",
        "layers": [
            L("Steel wire armour", "steel", 1.00, "armour", "Deep-water armour rated for 4 km of ocean."),
            L("Jute bedding", "jute", 0.80, "weave", ""),
            L("Polyethylene dielectric", "pe", 0.68, "solid", "Polyethylene replaced gutta-percha — stable, low loss, mass-producible."),
            L("Copper return tube", "copper", 0.40, "solid", "Outer conductor completing the coaxial pair."),
            L("Copper centre conductor", "copper", 0.18, "solid", "36 simultaneous telephone calls."),
        ],
        "connectors": [C("repeater", "Submerged repeater", "Vacuum-tube amplifiers spliced inline every ~70 km, built to run 20 years unattended.")],
        "chips": [],
    },
    # ── Fiber era ────────────────────────────────────────────────
    "1966-fiber-theory": {
        "family": "fiber",
        "signal": {"kind": "light", "label": "Guided light", "speed": 1.0},
        "tagline": "Kao's insight: the loss wasn't the glass, it was the impurities in it.",
        "layers": [
            L("Acrylate coating", "coating", 1.00, "solid", "Protects the glass surface — a scratch is where a fibre breaks."),
            L("Cladding glass", "cladding", 0.74, "solid", "Slightly lower refractive index, so light striking the boundary reflects back inward."),
            L("Core glass", "glass", 0.34, "solid", "Ultra-pure silica. Light bounces along inside it by total internal reflection."),
        ],
        "connectors": [C("bare-fiber", "Cleaved fibre end", "A flat, polished end face — the whole signal enters through this.")],
        "chips": [],
    },
    "1977-first-fiber": {
        "family": "fiber",
        "signal": {"kind": "light", "label": "Pulsed light", "speed": 1.0},
        "tagline": "Live phone traffic on light, in Chicago.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Aramid yarn", "aramid", 0.84, "weave", "Takes the pulling load so the glass never feels the tension."),
            L("Acrylate coating", "coating", 0.62, "solid", ""),
            L("Cladding", "cladding", 0.46, "solid", ""),
            L("Multimode core", "glass", 0.26, "solid", "A wide core — easy to couple light into, but modes spread the pulse."),
        ],
        "connectors": [C("sc-fiber", "SC fibre connector", "Spring-loaded ceramic ferrule holds two fibre ends within a micron of each other.")],
        "chips": [CHIP("LED / photodiode", "transceiver", "Electricity in, light out at one end; light in, electricity out at the other.")],
    },
    "1988-tat8": {
        "family": "fiber",
        "signal": {"kind": "light", "label": "Digital optical", "speed": 1.0},
        "tagline": "The Atlantic goes optical: 40 000 calls at once.",
        "layers": [
            L("Polyethylene sheath", "pe", 1.00, "solid", ""),
            L("Steel wire strength member", "steel", 0.86, "armour", "Takes the weight of the cable hanging off the back of the ship."),
            L("Copper power conductor", "copper", 0.70, "solid", "Carries DC power to the optical repeaters on the seabed."),
            L("Filling gel", "gel", 0.54, "foam", "Blocks water from running along inside the tube if the sheath is breached."),
            L("Fibre pairs", "glass", 0.30, "solid", "Three working pairs of single-mode fibre."),
        ],
        "cores": {"count": 6, "material": "glass", "r": 0.055, "ring": 0.17},
        "connectors": [C("repeater", "Optical repeater", "Regenerated the light pulses every ~70 km along the ocean floor.")],
        "chips": [CHIP("Laser + regenerator", "transceiver", "Converted light to electrical bits and back to clean light.")],
    },
    # ── Ethernet / structured cabling ────────────────────────────
    "1990-10baset": {
        "family": "twisted",
        "signal": {"kind": "differential", "label": "10 Mb/s baseband", "speed": 0.72},
        "tagline": "Ethernet leaves the thick yellow coax and moves onto phone-style wire.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", "Four pairs in one sheath — the shape office cabling took for the next 30 years."),
        ],
        "pairs": {"count": 4, "colors": ["#3fbfd4", "#e8913a", "#46c98b", "#ef5f5f"], "ring": 0.52, "r": 0.20},
        "connectors": [C("rj45", "RJ45 (8P8C)", "Eight gold-plated contacts that pierce the wire insulation when crimped.")],
        "chips": [CHIP("Ethernet PHY", "phy", "Turns bits into the precise voltage waveform the pairs carry.")],
    },
    "1991-568-cat5": {
        "family": "twisted",
        "signal": {"kind": "differential", "label": "Structured cabling", "speed": 0.78},
        "tagline": "One standard socket for any building, any vendor.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Rip cord + separator", "aramid", 0.86, "weave", "The string you pull to split the jacket without nicking the pairs."),
        ],
        "pairs": {"count": 4, "colors": ["#3fbfd4", "#e8913a", "#46c98b", "#ef5f5f"], "ring": 0.50, "r": 0.19, "twist": True},
        "connectors": [C("rj45", "RJ45 (8P8C)", "The standard that made structured cabling interchangeable.")],
        "chips": [CHIP("Ethernet PHY", "phy", "")],
    },
    "1995-fast-ethernet": {
        "family": "twisted",
        "signal": {"kind": "differential", "label": "100 Mb/s", "speed": 0.86},
        "tagline": "Ten times faster on the same four pairs — by twisting tighter.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Pair separator", "teflon", 0.86, "solid", "Each pair gets a different twist rate so neighbours do not couple."),
        ],
        "pairs": {"count": 4, "colors": ["#3fbfd4", "#e8913a", "#46c98b", "#ef5f5f"], "ring": 0.50, "r": 0.19, "twist": True},
        "connectors": [C("rj45", "RJ45 (8P8C)", "")],
        "chips": [CHIP("100BASE-TX PHY", "phy", "Encodes data so the signal stays inside the cable's bandwidth.")],
    },
    # ── Consumer interconnect ────────────────────────────────────
    "1996-usb1": {
        "family": "usb",
        "signal": {"kind": "differential", "label": "USB 1.0 · 12 Mb/s", "speed": 0.7},
        "tagline": "One connector to replace serial, parallel, PS/2 and the rest.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.88, "braid", "Keeps USB's fast edges from radiating into your radio."),
            L("Aluminium foil", "foil", 0.78, "foil", "Foil catches the high frequencies the braid misses."),
        ],
        "bundle": [
            {"label": "D+ / D− data pair", "material": "copper", "cx": -0.22, "cy": 0.0, "r": 0.20, "pair": True},
            {"label": "VBUS +5 V", "material": "copper-lit", "cx": 0.22, "cy": -0.20, "r": 0.16},
            {"label": "Ground", "material": "tinned", "cx": 0.22, "cy": 0.20, "r": 0.16},
        ],
        "connectors": [C("usb-a", "USB Type-A", "Deliberately un-reversible — and famously hard to insert first try.")],
        "chips": [CHIP("USB controller", "controller", "Handles enumeration: the handshake where your PC asks 'what are you?'")],
    },
    "1997-docsis1": {
        "family": "coax",
        "signal": {"kind": "rf", "label": "DOCSIS RF", "speed": 0.87},
        "tagline": "The TV cable learns to talk back.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.84, "braid", "60 % coverage braid over the foil."),
            L("Aluminium foil", "foil", 0.74, "foil", "Bonded foil — the primary shield against ingress."),
            L("Foamed polyethylene", "foam-pe", 0.64, "foam", "Mostly gas bubbles: lower loss than solid plastic."),
            L("Copper-clad steel core", "copper", 0.18, "solid", "Steel for strength, copper skin because RF only travels on the surface."),
        ],
        "connectors": [C("f-type", "F-type screw connector", "The centre conductor of the cable *is* the connector pin — no separate pin needed.")],
        "chips": [CHIP("DOCSIS modem SoC", "modem", "Tunes RF channels and turns them into IP packets.")],
    },
    "2002-hdmi1": {
        "family": "av",
        "signal": {"kind": "differential", "label": "TMDS video", "speed": 0.9},
        "tagline": "Video, audio and control down one plug.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Overall braid", "braid", 0.90, "braid", "A second shield around the whole bundle."),
        ],
        "bundle": [
            {"label": "TMDS pair 0", "material": "copper", "cx": -0.30, "cy": -0.26, "r": 0.17, "pair": True, "shielded": True},
            {"label": "TMDS pair 1", "material": "copper", "cx": 0.30, "cy": -0.26, "r": 0.17, "pair": True, "shielded": True},
            {"label": "TMDS pair 2", "material": "copper", "cx": -0.30, "cy": 0.26, "r": 0.17, "pair": True, "shielded": True},
            {"label": "TMDS clock", "material": "copper", "cx": 0.30, "cy": 0.26, "r": 0.17, "pair": True, "shielded": True},
            {"label": "DDC / CEC / power", "material": "tinned", "cx": 0.0, "cy": 0.0, "r": 0.15},
        ],
        "connectors": [C("hdmi", "HDMI Type-A", "19 pins: three video pairs, a clock, and a control channel.")],
        "chips": [CHIP("TMDS transmitter", "phy", "Serialises each colour channel and scrambles it to keep the signal balanced.")],
    },
    "2008-usb3": {
        "family": "usb",
        "signal": {"kind": "differential", "label": "SuperSpeed · 5 Gb/s", "speed": 0.94},
        "tagline": "Two extra shielded pairs bolted onto USB 2.0, one each way.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.90, "braid", ""),
            L("Aluminium foil", "foil", 0.82, "foil", ""),
        ],
        "bundle": [
            {"label": "SuperSpeed TX pair", "material": "copper", "cx": -0.30, "cy": -0.24, "r": 0.18, "pair": True, "shielded": True},
            {"label": "SuperSpeed RX pair", "material": "copper", "cx": 0.30, "cy": -0.24, "r": 0.18, "pair": True, "shielded": True},
            {"label": "USB 2.0 D+/D− pair", "material": "copper", "cx": -0.28, "cy": 0.28, "r": 0.16, "pair": True},
            {"label": "VBUS + GND", "material": "copper-lit", "cx": 0.28, "cy": 0.28, "r": 0.16},
        ],
        "connectors": [C("usb-a", "USB 3.0 Type-A", "Five extra contacts set deeper in the shell — which is why the plug is blue.")],
        "chips": [CHIP("SuperSpeed PHY", "phy", "Recovers a 5 GHz clock from the data stream itself.")],
    },
    "2014-usbc": {
        "family": "usb",
        "signal": {"kind": "differential", "label": "USB-C · up to 40 Gb/s", "speed": 1.0},
        "tagline": "Reversible, 100 W capable — and the first cable with a brain inside the plug.",
        "layers": [
            L("TPE jacket", "lszh", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.91, "braid", ""),
            L("Aluminium foil", "foil", 0.84, "foil", ""),
        ],
        "bundle": [
            {"label": "TX1 pair", "material": "copper", "cx": -0.32, "cy": -0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "RX1 pair", "material": "copper", "cx": 0.32, "cy": -0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "TX2 pair", "material": "copper", "cx": -0.32, "cy": 0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "RX2 pair", "material": "copper", "cx": 0.32, "cy": 0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "VBUS (up to 5 A)", "material": "copper-lit", "cx": 0.0, "cy": -0.30, "r": 0.15},
            {"label": "CC / SBU signal wires", "material": "tinned", "cx": 0.0, "cy": 0.0, "r": 0.12},
            {"label": "Ground", "material": "tinned", "cx": 0.0, "cy": 0.30, "r": 0.15},
        ],
        "connectors": [C("usb-c", "USB Type-C", "24 contacts, mirrored top and bottom, so it works either way up.")],
        "chips": [
            CHIP("E-marker IC", "emarker", "A real chip moulded into the plug. The charger asks it how much current the cable can survive — that is why a cheap cable charges your laptop slowly."),
            CHIP("Retimer", "retimer", "In long high-speed cables, it cleans up and re-transmits the signal mid-flight."),
        ],
    },
    "2017-8023bs": {
        "family": "fiber",
        "signal": {"kind": "light", "label": "400 Gb/s optical", "speed": 1.0},
        "tagline": "Eight fibres in parallel, 50 Gb/s on each.",
        "layers": [
            L("LSZH jacket", "lszh", 1.00, "solid", "Low-smoke zero-halogen — it will not poison a data hall if it burns."),
            L("Aramid yarn", "aramid", 0.88, "weave", ""),
            L("Ribbon matrix", "coating", 0.72, "solid", "Fibres bonded side by side in a flat ribbon so all eight terminate at once."),
        ],
        "cores": {"count": 8, "material": "glass", "r": 0.05, "ring": 0.34, "row": True},
        "connectors": [C("mpo", "MPO/MTP ribbon connector", "Twelve fibres land in one push-on ferrule, aligned by two steel guide pins.")],
        "chips": [CHIP("DSP + optical engine", "dsp", "A digital signal processor drives eight lasers and un-smears what comes back.")],
    },
    "2020-800g": {
        "family": "fiber",
        "signal": {"kind": "light", "label": "Coherent DWDM", "speed": 1.0},
        "tagline": "Colour, phase and polarisation all carry data at once.",
        "layers": [
            L("LSZH jacket", "lszh", 1.00, "solid", ""),
            L("Aramid strength", "aramid", 0.88, "weave", ""),
            L("Buffer tube", "coating", 0.74, "solid", ""),
            L("Cladding", "cladding", 0.50, "solid", ""),
            L("Single-mode core", "glass", 0.22, "solid", "Only ~9 µm across — narrow enough that light travels one single path."),
        ],
        "connectors": [C("lc-fiber", "LC duplex connector", "A latching ceramic ferrule; one fibre out, one fibre back.")],
        "chips": [CHIP("Coherent DSP", "dsp", "Measures the light's phase and polarisation, then undoes the distortion of 1 000 km of glass — billions of operations per second.")],
    },
    "2024-eu-usbc": {
        "family": "usb",
        "signal": {"kind": "differential", "label": "USB-C PD", "speed": 1.0},
        "tagline": "One charger for everything, by law.",
        "layers": [
            L("TPE jacket", "lszh", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.91, "braid", ""),
            L("Aluminium foil", "foil", 0.84, "foil", ""),
        ],
        "bundle": [
            {"label": "High-speed pairs", "material": "copper", "cx": -0.30, "cy": -0.24, "r": 0.17, "pair": True, "shielded": True},
            {"label": "High-speed pairs", "material": "copper", "cx": 0.30, "cy": -0.24, "r": 0.17, "pair": True, "shielded": True},
            {"label": "VBUS (up to 240 W)", "material": "copper-lit", "cx": -0.28, "cy": 0.28, "r": 0.18},
            {"label": "CC configuration wires", "material": "tinned", "cx": 0.28, "cy": 0.28, "r": 0.15},
        ],
        "connectors": [C("usb-c", "USB Type-C", "The connector the EU made mandatory for phones, tablets and cameras.")],
        "chips": [CHIP("E-marker IC", "emarker", "Declares the cable's wattage and speed rating. Required for anything above 60 W.")],
    },
    "2020s-self-healing": {
        "family": "smart",
        "signal": {"kind": "current", "label": "Self-repairing link", "speed": 0.8},
        "tagline": "Cut it, and the insulation grows back.",
        "layers": [
            L("Elastomer jacket", "lszh", 1.00, "solid", ""),
            L("Microcapsule layer", "capsule", 0.86, "foam", "Tiny capsules of healing agent. A tear ruptures them and the liquid floods the gap and sets."),
            L("Self-healing polymer", "polymer", 0.70, "solid", "Reversible bonds re-form across a cut when the two faces touch again."),
            L("Conductive core", "copper", 0.30, "solid", "Some designs use a liquid-metal core that simply flows back together."),
        ],
        "connectors": [C("usb-c", "USB Type-C", "")],
        "chips": [CHIP("Health-monitor IC", "monitor", "Watches resistance along the cable and reports damage before the link drops.")],
    },
}


# ── SVG helpers ──────────────────────────────────────────────────
def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def ring_points(n, radius, cx, cy, phase=-math.pi / 2):
    return [
        (cx + radius * math.cos(phase + i * 2 * math.pi / n),
         cy + radius * math.sin(phase + i * 2 * math.pi / n))
        for i in range(n)
    ]


def cross_section_svg(spec, cx, cy, R, idp=""):
    """Concentric cross-section, outermost first."""
    out = []
    layers = spec.get("layers", [])
    for i, ly in enumerate(layers):
        m = M[ly["material"]]
        r = ly["r"] * R
        out.append(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{m["fill"]}" '
            f'stroke="{m["edge"]}" stroke-width="{max(0.6, R*0.018):.2f}"/>'
        )
        if ly["pattern"] == "armour":
            n = 16
            rr = r * 0.90
            for (px, py) in ring_points(n, rr, cx, cy):
                out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{R*0.062:.2f}" fill="{m["hi"]}" stroke="{m["edge"]}" stroke-width="0.5"/>')
        elif ly["pattern"] == "braid":
            n = 24
            rr = r * 0.93
            for (px, py) in ring_points(n, rr, cx, cy):
                out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{R*0.030:.2f}" fill="{m["hi"]}" opacity="0.9"/>')
        elif ly["pattern"] == "foil":
            out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r*0.97:.2f}" fill="none" stroke="{m["hi"]}" stroke-width="{R*0.02:.2f}" opacity="0.85"/>')
        elif ly["pattern"] == "weave":
            n = 20
            for (px, py) in ring_points(n, r * 0.92, cx, cy):
                out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{R*0.026:.2f}" fill="{m["hi"]}" opacity="0.55"/>')
        elif ly["pattern"] == "foam":
            for k, (px, py) in enumerate(ring_points(9, r * 0.68, cx, cy, phase=0.3)):
                out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{R*0.035:.2f}" fill="{m["hi"]}" opacity="0.4"/>')

    # stranded / multi cores
    cores = spec.get("cores")
    if cores:
        m = M[cores["material"]]
        if cores.get("row"):
            n = cores["count"]
            span = cores["ring"] * R * 2
            for i in range(n):
                px = cx - span / 2 + span * (i / max(1, n - 1))
                out.append(f'<circle cx="{px:.2f}" cy="{cy:.2f}" r="{cores["r"]*R:.2f}" fill="{m["fill"]}" stroke="{m["edge"]}" stroke-width="0.5"/>')
        elif cores["count"] == 2 or cores.get("twist"):
            # a pair sits side by side, not one inside the other
            off = cores["ring"] * R
            for sx, col in ((-1, m["fill"]), (1, M["tinned"]["fill"])):
                out.append(f'<circle cx="{cx + sx*off:.2f}" cy="{cy:.2f}" r="{cores["r"]*R:.2f}" fill="{col}" stroke="{m["edge"]}" stroke-width="0.6"/>')
                out.append(f'<circle cx="{cx + sx*off:.2f}" cy="{cy:.2f}" r="{cores["r"]*R*0.45:.2f}" fill="{M["copper"]["fill"]}"/>')
        else:
            # stranded: one in the middle, the rest in a ring around it
            pts = ring_points(cores["count"] - 1, cores["ring"] * R, cx, cy) if cores["count"] > 1 else []
            out.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{cores["r"]*R:.2f}" fill="{m["fill"]}" stroke="{m["edge"]}" stroke-width="0.5"/>')
            for (px, py) in pts:
                out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{cores["r"]*R:.2f}" fill="{m["fill"]}" stroke="{m["edge"]}" stroke-width="0.5"/>')

    # twisted pairs
    pairs = spec.get("pairs")
    if pairs:
        for i, (px, py) in enumerate(ring_points(pairs["count"], pairs["ring"] * R, cx, cy, phase=-math.pi / 4)):
            col = pairs["colors"][i % len(pairs["colors"])]
            pr = pairs["r"] * R
            out.append(f'<circle cx="{px - pr*0.5:.2f}" cy="{py:.2f}" r="{pr*0.52:.2f}" fill="{col}" stroke="#0e1620" stroke-width="0.6"/>')
            out.append(f'<circle cx="{px + pr*0.5:.2f}" cy="{py:.2f}" r="{pr*0.52:.2f}" fill="#e8eef5" stroke="#0e1620" stroke-width="0.6"/>')
            out.append(f'<circle cx="{px - pr*0.5:.2f}" cy="{py:.2f}" r="{pr*0.24:.2f}" fill="{M["copper"]["fill"]}"/>')
            out.append(f'<circle cx="{px + pr*0.5:.2f}" cy="{py:.2f}" r="{pr*0.24:.2f}" fill="{M["copper"]["fill"]}"/>')

    # loose bundle (USB / HDMI)
    bundle = spec.get("bundle")
    if bundle:
        for w in bundle:
            m = M[w["material"]]
            px, py = cx + w["cx"] * R, cy + w["cy"] * R
            wr = w["r"] * R
            if w.get("shielded"):
                out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{wr*1.16:.2f}" fill="none" stroke="{M["foil"]["fill"]}" stroke-width="{R*0.022:.2f}" opacity="0.9"/>')
            if w.get("pair"):
                out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{wr:.2f}" fill="{M["teflon"]["fill"]}" stroke="{M["teflon"]["edge"]}" stroke-width="0.5"/>')
                out.append(f'<circle cx="{px - wr*0.42:.2f}" cy="{py:.2f}" r="{wr*0.34:.2f}" fill="{m["fill"]}" stroke="{m["edge"]}" stroke-width="0.4"/>')
                out.append(f'<circle cx="{px + wr*0.42:.2f}" cy="{py:.2f}" r="{wr*0.34:.2f}" fill="{m["fill"]}" stroke="{m["edge"]}" stroke-width="0.4"/>')
            else:
                out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{wr:.2f}" fill="{M["teflon"]["fill"]}" stroke="{M["teflon"]["edge"]}" stroke-width="0.5"/>')
                out.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{wr*0.52:.2f}" fill="{m["fill"]}" stroke="{m["edge"]}" stroke-width="0.4"/>')

    return "\n    ".join(out)


# ── Connector glyphs (side view, drawn at origin, facing right) ──
def connector_svg(kind, x, y, s, flip=False):
    """s = height scale. Returns svg string for a side-view connector."""
    g = []
    t = f'translate({x:.2f},{y:.2f}){" scale(-1,1)" if flip else ""}'
    gold, shell, dark = M["gold"]["fill"], "#9aa7b4", "#141d29"

    if kind in ("usb-c",):
        g.append(f'<rect x="{-s*1.5:.2f}" y="{-s*0.42:.2f}" width="{s*1.5:.2f}" height="{s*0.84:.2f}" rx="{s*0.42:.2f}" fill="{shell}" stroke="#5f6b79" stroke-width="{s*0.05:.2f}"/>')
        g.append(f'<rect x="{-s*1.28:.2f}" y="{-s*0.22:.2f}" width="{s*1.0:.2f}" height="{s*0.44:.2f}" rx="{s*0.22:.2f}" fill="{dark}"/>')
        g.append(f'<rect x="{-s*1.18:.2f}" y="{-s*0.10:.2f}" width="{s*0.80:.2f}" height="{s*0.07:.2f}" fill="{gold}"/>')
        g.append(f'<rect x="{-s*1.18:.2f}" y="{s*0.03:.2f}" width="{s*0.80:.2f}" height="{s*0.07:.2f}" fill="{gold}"/>')
    elif kind == "usb-a":
        g.append(f'<rect x="{-s*1.5:.2f}" y="{-s*0.40:.2f}" width="{s*1.5:.2f}" height="{s*0.80:.2f}" rx="{s*0.06:.2f}" fill="{shell}" stroke="#5f6b79" stroke-width="{s*0.05:.2f}"/>')
        g.append(f'<rect x="{-s*1.30:.2f}" y="{-s*0.24:.2f}" width="{s*1.05:.2f}" height="{s*0.30:.2f}" fill="{dark}"/>')
        g.append(f'<rect x="{-s*1.22:.2f}" y="{-s*0.18:.2f}" width="{s*0.85:.2f}" height="{s*0.10:.2f}" fill="{gold}"/>')
    elif kind == "rj45":
        g.append(f'<path d="M{-s*1.5:.2f} {-s*0.46:.2f} h{s*1.5:.2f} v{s*0.92:.2f} h{-s*1.5:.2f} z" fill="#c9d4de" opacity="0.92" stroke="#7d8894" stroke-width="{s*0.05:.2f}"/>')
        g.append(f'<path d="M{-s*0.95:.2f} {s*0.46:.2f} v{s*0.34:.2f} h{s*0.42:.2f} v{-s*0.34:.2f} z" fill="#c9d4de" stroke="#7d8894" stroke-width="{s*0.05:.2f}"/>')
        for i in range(8):
            px = -s * 1.38 + i * s * 0.16
            g.append(f'<rect x="{px:.2f}" y="{-s*0.40:.2f}" width="{s*0.07:.2f}" height="{s*0.46:.2f}" fill="{gold}"/>')
    elif kind == "f-type":
        g.append(f'<rect x="{-s*1.35:.2f}" y="{-s*0.34:.2f}" width="{s*1.05:.2f}" height="{s*0.68:.2f}" fill="{shell}" stroke="#5f6b79" stroke-width="{s*0.05:.2f}"/>')
        for i in range(4):
            g.append(f'<rect x="{-s*1.32 + i*s*0.26:.2f}" y="{-s*0.34:.2f}" width="{s*0.10:.2f}" height="{s*0.68:.2f}" fill="#7d8894"/>')
        g.append(f'<rect x="{-s*0.42:.2f}" y="{-s*0.05:.2f}" width="{s*0.62:.2f}" height="{s*0.10:.2f}" fill="{M["copper"]["fill"]}"/>')
    elif kind in ("lc-fiber", "sc-fiber", "bare-fiber", "mpo"):
        g.append(f'<rect x="{-s*1.5:.2f}" y="{-s*0.40:.2f}" width="{s*1.15:.2f}" height="{s*0.80:.2f}" rx="{s*0.08:.2f}" fill="#2f3e52" stroke="#1a2432" stroke-width="{s*0.05:.2f}"/>')
        if kind == "mpo":
            for i in range(6):
                g.append(f'<circle cx="{-s*0.62 + 0:.2f}" cy="{-s*0.24 + i*s*0.10:.2f}" r="{s*0.035:.2f}" fill="{M["glass"]["fill"]}"/>')
            g.append(f'<rect x="{-s*0.40:.2f}" y="{-s*0.16:.2f}" width="{s*0.52:.2f}" height="{s*0.32:.2f}" rx="{s*0.04:.2f}" fill="#e8eef5" opacity="0.85"/>')
        else:
            g.append(f'<rect x="{-s*0.40:.2f}" y="{-s*0.13:.2f}" width="{s*0.58:.2f}" height="{s*0.26:.2f}" rx="{s*0.05:.2f}" fill="#e8eef5" opacity="0.9"/>')
            g.append(f'<circle cx="{s*0.12:.2f}" cy="0" r="{s*0.07:.2f}" fill="{M["glass"]["fill"]}"/>')
    elif kind == "hdmi":
        g.append(f'<path d="M{-s*1.5:.2f} {-s*0.34:.2f} h{s*1.5:.2f} v{s*0.68:.2f} h{-s*1.5:.2f} l{s*0.16:.2f} {-s*0.34:.2f} z" fill="{shell}" stroke="#5f6b79" stroke-width="{s*0.05:.2f}"/>')
        g.append(f'<rect x="{-s*1.30:.2f}" y="{-s*0.16:.2f}" width="{s*1.05:.2f}" height="{s*0.10:.2f}" fill="{gold}"/>')
        g.append(f'<rect x="{-s*1.30:.2f}" y="{s*0.04:.2f}" width="{s*1.05:.2f}" height="{s*0.10:.2f}" fill="{gold}"/>')
    elif kind in ("terminal", "binding-post"):
        g.append(f'<rect x="{-s*1.1:.2f}" y="{-s*0.5:.2f}" width="{s*0.75:.2f}" height="{s*1.0:.2f}" rx="{s*0.08:.2f}" fill="#3a2c1c" stroke="#241a10" stroke-width="{s*0.05:.2f}"/>')
        g.append(f'<circle cx="{-s*0.72:.2f}" cy="0" r="{s*0.28:.2f}" fill="{M["gold"]["fill"]}" stroke="{M["gold"]["edge"]}" stroke-width="{s*0.05:.2f}"/>')
        g.append(f'<rect x="{-s*0.86:.2f}" y="{-s*0.045:.2f}" width="{s*0.28:.2f}" height="{s*0.09:.2f}" fill="{M["gold"]["edge"]}"/>')
    elif kind == "repeater":
        g.append(f'<rect x="{-s*1.6:.2f}" y="{-s*0.40:.2f}" width="{s*1.35:.2f}" height="{s*0.80:.2f}" rx="{s*0.40:.2f}" fill="{shell}" stroke="#5f6b79" stroke-width="{s*0.05:.2f}"/>')
        g.append(f'<circle cx="{-s*0.92:.2f}" cy="0" r="{s*0.20:.2f}" fill="{M["copper"]["hi"]}"/>')
        g.append(f'<circle cx="{-s*0.92:.2f}" cy="0" r="{s*0.32:.2f}" fill="none" stroke="{M["copper"]["hi"]}" stroke-width="{s*0.04:.2f}" opacity="0.6"/>')
    else:  # coax-fitting + fallback
        g.append(f'<rect x="{-s*1.35:.2f}" y="{-s*0.32:.2f}" width="{s*1.0:.2f}" height="{s*0.64:.2f}" rx="{s*0.06:.2f}" fill="{shell}" stroke="#5f6b79" stroke-width="{s*0.05:.2f}"/>')
        g.append(f'<rect x="{-s*0.42:.2f}" y="{-s*0.05:.2f}" width="{s*0.60:.2f}" height="{s*0.10:.2f}" fill="{M["copper"]["fill"]}"/>')

    return f'<g transform="{t}">' + "".join(g) + "</g>"


def thumbnail(era_id, spec):
    """160x90 thumbnail: labelled cross-section + cable run into a connector."""
    W, H = 160, 90
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">')
    o.append(f'<title>{esc(spec.get("tagline",""))}</title>')
    o.append('<defs>')
    o.append('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0%" stop-color="#101b2b"/><stop offset="100%" stop-color="#070b14"/></linearGradient>')
    o.append('<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0%" stop-color="#ffffff" stop-opacity="0.16"/>'
             '<stop offset="45%" stop-color="#ffffff" stop-opacity="0.02"/>'
             '<stop offset="100%" stop-color="#000000" stop-opacity="0.22"/></linearGradient>')
    o.append('</defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

    # ── side view: cable running left→right into the connector ──
    outer = spec["layers"][0]
    mo = M[outer["material"]]
    cy = 58
    body_h = 17
    o.append(f'<rect x="0" y="{cy-body_h/2:.1f}" width="108" height="{body_h}" fill="{mo["fill"]}"/>')
    # stepped cut-away: each inner layer peeled back further right
    step_x = 26
    inner = spec["layers"][1:] if len(spec["layers"]) > 1 else []
    visible = inner[:3]
    for i, ly in enumerate(visible):
        m = M[ly["material"]]
        h = body_h * max(0.28, ly["r"])
        x0 = step_x + i * 18
        o.append(f'<rect x="{x0}" y="{cy-h/2:.1f}" width="{108-x0}" height="{h:.1f}" fill="{m["fill"]}"/>')
        o.append(f'<path d="M{x0} {cy-h/2:.1f} a 3 {h/2:.1f} 0 0 0 0 {h:.1f}" fill="{m["edge"]}" opacity="0.85"/>')
    # innermost conductor / core runs all the way in
    core_m = M[spec["layers"][-1]["material"]] if spec["layers"] else M["copper"]
    ch = max(3.0, body_h * spec["layers"][-1]["r"] * 0.8) if spec["layers"] else 4
    o.append(f'<rect x="{step_x + len(visible)*18}" y="{cy-ch/2:.1f}" width="{108-(step_x+len(visible)*18)}" height="{ch:.1f}" fill="{core_m["hi"]}"/>')
    o.append(f'<rect x="0" y="{cy-body_h/2:.1f}" width="108" height="{body_h}" fill="url(#sheen)"/>')

    # connector on the right end of the run
    conn_kind = spec["connectors"][0]["kind"] if spec.get("connectors") else "coax-fitting"
    o.append(connector_svg(conn_kind, 132, cy, 17))

    # chip package inline, if the cable has one
    if spec.get("chips"):
        o.append(f'<rect x="86" y="{cy-7:.1f}" width="16" height="14" rx="2" fill="#2f3e52" stroke="#f5d06f" stroke-width="0.9"/>')
        for i in range(3):
            o.append(f'<rect x="{84:.1f}" y="{cy-4+i*3.4:.1f}" width="2" height="1.4" fill="#f5d06f"/>')
            o.append(f'<rect x="{102:.1f}" y="{cy-4+i*3.4:.1f}" width="2" height="1.4" fill="#f5d06f"/>')
        o.append(f'<circle cx="94" cy="{cy:.1f}" r="2.6" fill="#f5d06f" opacity="0.5"/>')

    # ── cross-section disc, top-left, with a leader to the run ──
    ccx, ccy, R = 30, 26, 20
    o.append(f'<circle cx="{ccx}" cy="{ccy}" r="{R+2.5}" fill="#070b14" stroke="#1e2a3c" stroke-width="1"/>')
    o.append("    " + cross_section_svg(spec, ccx, ccy, R))
    o.append(f'<circle cx="{ccx}" cy="{ccy}" r="{R}" fill="none" stroke="#000" stroke-opacity="0.35" stroke-width="0.8"/>')
    o.append(f'<path d="M{ccx+R+3} {ccy+6} L{ccx+R+16} {ccy+20}" stroke="#3fbfd4" stroke-width="0.9" opacity="0.55"/>')

    # layer count badge
    n = len(spec["layers"]) + (1 if spec.get("pairs") or spec.get("bundle") or spec.get("cores") else 0)
    o.append(f'<text x="{W-5}" y="12" text-anchor="end" font-family="ui-sans-serif,system-ui,sans-serif" '
             f'font-size="7.5" font-weight="700" fill="#93a1b5" letter-spacing="0.6">{n} LAYERS</text>')
    o.append('</svg>')
    return "\n".join(o)


SPECS.update(NEW_SPECS)


def main():
    specs_out = {}
    era_path = os.path.join(ROOT, "public/content/cable_eras_v2.json")
    eras = json.load(open(era_path))
    made = 0
    for era in eras:
        eid = era["id"]
        spec = SPECS.get(eid)
        if not spec:
            print(f"  !! no spec for {eid}")
            continue
        specs_out[eid] = spec
        svg = thumbnail(eid, spec)
        out = os.path.join(ROOT, "public/images/eras", f"{eid}.svg")
        with open(out, "w") as f:
            f.write(svg)
        made += 1

    with open(os.path.join(ROOT, "public/content/cable_specs.json"), "w") as f:
        json.dump(specs_out, f, indent=1)

    print(f"wrote {made} era SVGs + cable_specs.json ({len(specs_out)} specs)")


if __name__ == "__main__":
    main()
