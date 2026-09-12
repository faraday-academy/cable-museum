"""
Construction specs for the 23 cables added to fill gaps in the timeline.

Same schema as SPECS in generate_cable_art.py:
  layers  — OUTERMOST first, radius normalised to 1.0
  pattern — solid | armour | braid | foil | weave | foam
  cores / pairs / bundle — sub-conductors inside the innermost layer
"""


def L(label, material, r, pattern="solid", note=""):
    return {"label": label, "material": material, "r": r, "pattern": pattern, "note": note}


def C(kind, label, note=""):
    return {"kind": kind, "label": label, "note": note}


def CHIP(label, role, note=""):
    return {"label": label, "role": role, "note": note}


NEW_SPECS = {
    # ── Pre-computer ────────────────────────────────────────────
    "1878-phone-jack": {
        "family": "audio",
        "signal": {"kind": "audio", "label": "Switchboard voice", "speed": 0.6},
        "tagline": "The plug a telephone operator jammed into a board — still in your guitar amp.",
        "layers": [
            L("Cotton braid", "cotton", 1.00, "braid", "Cloth-covered flex, the standard finish before plastics."),
            L("Rubber insulation", "rubber", 0.74, "solid", "Separates the two conductors of the speech circuit."),
        ],
        "cores": {"count": 2, "material": "copper", "r": 0.30, "ring": 0.32, "twist": True},
        "connectors": [C("binding-post", "¼-inch tip-sleeve plug", "Tip carries the signal, sleeve is the return. The shape has not changed in 145 years.")],
        "chips": [],
    },
    "1950s-xlr": {
        "family": "audio",
        "signal": {"kind": "differential", "label": "Balanced audio", "speed": 0.7},
        "tagline": "Three pins that let a microphone run 100 m without picking up a radio station.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.86, "braid", "The shield is the third pin — it drains interference to ground."),
        ],
        "cores": {"count": 2, "material": "copper", "r": 0.26, "ring": 0.30, "twist": True},
        "connectors": [C("terminal", "XLR 3-pin", "Pin 1 ground, pins 2 and 3 the balanced pair. Latching, so it cannot fall out mid-show.")],
        "chips": [],
    },
    "1954-gotland-hvdc": {
        "family": "power",
        "signal": {"kind": "current", "label": "100 kV DC", "speed": 0.5},
        "tagline": "Not data — raw power, 98 km under the Baltic.",
        "layers": [
            L("Steel wire armour", "steel", 1.00, "armour", "Double armour against anchors and ice scour."),
            L("Jute bedding", "jute", 0.82, "weave", ""),
            L("Lead sheath", "tinned", 0.70, "solid", "A seamless lead tube — the only thing that reliably keeps seawater out of paper."),
            L("Oil-impregnated paper", "paper", 0.58, "solid", "Hundreds of paper tapes soaked in insulating oil. Cheap, and it survives 100 kV."),
            L("Stranded copper conductor", "copper", 0.28, "solid", "Carries 20 MW of direct current to the island of Gotland."),
        ],
        "cores": {"count": 7, "material": "copper", "r": 0.09, "ring": 0.165},
        "connectors": [C("terminal", "Shore termination", "A porcelain bushing the size of a person, transferring the core to the overhead grid.")],
        "chips": [],
    },
    # ── Early computing ─────────────────────────────────────────
    "1962-rs232": {
        "family": "serial",
        "signal": {"kind": "current", "label": "±12 V serial", "speed": 0.35},
        "tagline": "One bit at a time, at ±12 volts, and it still runs factory floors.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Foil shield", "foil", 0.88, "foil", "Needed because the big voltage swings radiate badly."),
        ],
        "bundle": [
            {"label": "TxD transmit", "material": "copper", "cx": -0.30, "cy": -0.28, "r": 0.17},
            {"label": "RxD receive", "material": "copper-lit", "cx": 0.30, "cy": -0.28, "r": 0.17},
            {"label": "RTS / CTS handshake", "material": "tinned", "cx": -0.30, "cy": 0.28, "r": 0.17},
            {"label": "Signal ground", "material": "tinned", "cx": 0.30, "cy": 0.28, "r": 0.17},
        ],
        "connectors": [C("terminal", "DB-25 / DE-9 D-sub", "Screw locks on either side, because nobody trusted friction to hold it.")],
        "chips": [CHIP("Line driver / UART", "phy", "Converts the computer's 5 V logic into the ±12 V swing the standard demands.")],
    },
    "1970-centronics": {
        "family": "parallel",
        "signal": {"kind": "differential", "label": "8-bit parallel", "speed": 0.5},
        "tagline": "Eight bits side by side — fast, until the wires started talking to each other.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.88, "braid", "36 wires in a bundle radiate a lot; the braid contained it."),
        ],
        "bundle": [
            {"label": "Data bits 0–3", "material": "copper", "cx": -0.30, "cy": -0.26, "r": 0.18},
            {"label": "Data bits 4–7", "material": "copper", "cx": 0.30, "cy": -0.26, "r": 0.18},
            {"label": "STROBE / ACK / BUSY", "material": "copper-lit", "cx": -0.30, "cy": 0.28, "r": 0.17},
            {"label": "Ground returns", "material": "tinned", "cx": 0.30, "cy": 0.28, "r": 0.17},
        ],
        "connectors": [C("rj45", "36-pin Centronics", "A wide ribbon connector held on by two spring clips.")],
        "chips": [],
    },
    "1980-10base5": {
        "family": "coax",
        "signal": {"kind": "rf", "label": "10 Mb/s baseband", "speed": 0.77},
        "tagline": "The thick yellow hosepipe you drilled into with a 'vampire tap'.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", "Bright yellow by convention, with a black band every 2.5 m marking where you may tap."),
            L("Braided shield", "braid", 0.82, "braid", ""),
            L("Foil shield", "foil", 0.72, "foil", "Double shielding — this cable ran through ceilings full of fluorescent lights."),
            L("Polyethylene dielectric", "pe", 0.62, "solid", ""),
            L("Solid copper core", "copper", 0.22, "solid", "The vampire tap's spike bit through everything to reach this."),
        ],
        "connectors": [C("coax-fitting", "N-type / vampire tap", "A clamp that drove a spike into the core without cutting the cable.")],
        "chips": [CHIP("Ethernet transceiver (MAU)", "phy", "Bolted onto the tap, it listened for collisions on the shared wire.")],
    },
    "1983-midi": {
        "family": "serial",
        "signal": {"kind": "current", "label": "31.25 kb/s current loop", "speed": 0.4},
        "tagline": "A current loop that let any synth talk to any other — and still does.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.86, "braid", "Connected at one end only, to stop ground loops humming through the PA."),
        ],
        "cores": {"count": 2, "material": "copper", "r": 0.28, "ring": 0.30, "twist": True},
        "connectors": [C("terminal", "5-pin DIN", "Only three pins are used. The other two were left for a future that never came.")],
        "chips": [CHIP("Opto-isolator", "isolator", "Light, not wire, carries the signal across the gap — so two amps never share a ground.")],
    },
    "1985-10base2": {
        "family": "coax",
        "signal": {"kind": "rf", "label": "10 Mb/s baseband", "speed": 0.8},
        "tagline": "Cheapernet: thin coax, BNC twists, and one loose end killing the whole office.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.84, "braid", ""),
            L("Polyethylene dielectric", "pe", 0.68, "solid", "50 Ω — thinner and far more flexible than 10BASE5."),
            L("Stranded copper core", "copper", 0.24, "solid", ""),
        ],
        "connectors": [C("coax-fitting", "BNC T-connector", "A quarter turn to lock. Every machine sat on the same wire, so one bad terminator downed the segment.")],
        "chips": [CHIP("Ethernet transceiver", "phy", "")],
    },
    "1985-token-ring": {
        "family": "twisted",
        "signal": {"kind": "differential", "label": "4/16 Mb/s ring", "speed": 0.72},
        "tagline": "IBM's orderly answer to Ethernet: you may only speak while holding the token.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Overall braid", "braid", 0.88, "braid", "IBM Type 1 was fully shielded — heavy, expensive, and very quiet electrically."),
        ],
        "pairs": {"count": 2, "colors": ["#e8913a", "#3fbfd4"], "ring": 0.42, "r": 0.26, "twist": True},
        "connectors": [C("rj45", "IBM Data Connector", "A hermaphroditic connector — any plug mates with any other, no male or female.")],
        "chips": [CHIP("Ring interface chip", "phy", "Repeats every frame around the ring and strips its own messages back off.")],
    },
    "1986-scsi": {
        "family": "parallel",
        "signal": {"kind": "differential", "label": "8-bit parallel bus", "speed": 0.62},
        "tagline": "Fast, capable, and cursed with termination problems and ID conflicts.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.90, "braid", ""),
            L("Foil shield", "foil", 0.82, "foil", ""),
        ],
        "bundle": [
            {"label": "Data bus 0–7", "material": "copper", "cx": -0.30, "cy": -0.26, "r": 0.18, "pair": True},
            {"label": "Parity + control", "material": "copper-lit", "cx": 0.30, "cy": -0.26, "r": 0.18, "pair": True},
            {"label": "REQ / ACK handshake", "material": "copper", "cx": -0.30, "cy": 0.28, "r": 0.17, "pair": True},
            {"label": "Ground returns", "material": "tinned", "cx": 0.30, "cy": 0.28, "r": 0.17},
        ],
        "connectors": [C("rj45", "Centronics-50 / DB-25", "Every device needed a unique ID, and the last one on the chain needed a terminator.")],
        "chips": [CHIP("SCSI controller", "controller", "Arbitrates which of up to eight devices may drive the shared bus.")],
    },
    "1986-ide-ata": {
        "family": "parallel",
        "signal": {"kind": "differential", "label": "16-bit parallel", "speed": 0.6},
        "tagline": "The grey ribbon inside every beige PC — 40 wires, one red stripe.",
        "layers": [
            L("PVC ribbon", "pvc", 1.00, "solid", "Flat, unshielded, and colour-coded by a single red stripe marking pin 1."),
        ],
        "bundle": [
            {"label": "Data bits 0–7", "material": "copper", "cx": -0.34, "cy": 0.0, "r": 0.17},
            {"label": "Data bits 8–15", "material": "copper", "cx": 0.0, "cy": 0.0, "r": 0.17},
            {"label": "Control + ground", "material": "tinned", "cx": 0.34, "cy": 0.0, "r": 0.17},
        ],
        "connectors": [C("rj45", "40-pin IDC header", "Insulation-displacement: the connector's blades slice straight through the ribbon.")],
        "chips": [CHIP("Drive controller", "controller", "IDE's trick was moving the controller onto the drive itself — Integrated Drive Electronics.")],
    },
    # ── PC peripheral era ───────────────────────────────────────
    "1987-vga": {
        "family": "av",
        "signal": {"kind": "rf", "label": "Analogue RGB", "speed": 0.82},
        "tagline": "Three analogue colour signals, each in its own miniature coax.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Overall braid", "braid", 0.90, "braid", ""),
        ],
        "bundle": [
            {"label": "Red channel (coax)", "material": "copper", "cx": -0.32, "cy": -0.26, "r": 0.17, "shielded": True},
            {"label": "Green channel (coax)", "material": "copper", "cx": 0.32, "cy": -0.26, "r": 0.17, "shielded": True},
            {"label": "Blue channel (coax)", "material": "copper", "cx": -0.32, "cy": 0.26, "r": 0.17, "shielded": True},
            {"label": "H/V sync + DDC", "material": "tinned", "cx": 0.32, "cy": 0.26, "r": 0.16},
        ],
        "connectors": [C("terminal", "DE-15 (VGA)", "15 pins in three rows, with thumbscrews. Purely analogue — the monitor never knew what pixels were.")],
        "chips": [CHIP("RAMDAC", "dac", "Converts the digital framebuffer into three smooth analogue voltages, millions of times a second.")],
    },
    "1987-ps2": {
        "family": "serial",
        "signal": {"kind": "current", "label": "Clocked serial", "speed": 0.3},
        "tagline": "Purple for keyboard, green for mouse — and never hot-pluggable.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Foil shield", "foil", 0.86, "foil", ""),
        ],
        "bundle": [
            {"label": "Data", "material": "copper", "cx": -0.28, "cy": -0.24, "r": 0.18},
            {"label": "Clock", "material": "copper-lit", "cx": 0.28, "cy": -0.24, "r": 0.18},
            {"label": "+5 V", "material": "copper-lit", "cx": -0.28, "cy": 0.28, "r": 0.17},
            {"label": "Ground", "material": "tinned", "cx": 0.28, "cy": 0.28, "r": 0.17},
        ],
        "connectors": [C("terminal", "6-pin mini-DIN", "Keyed so it only goes in one way — which you discovered by feel, under a desk.")],
        "chips": [CHIP("Keyboard controller", "controller", "Scans the key matrix and clocks each keypress out one bit at a time.")],
    },
    "1995-firewire": {
        "family": "usb",
        "signal": {"kind": "differential", "label": "400 Mb/s peer-to-peer", "speed": 0.9},
        "tagline": "Faster than USB, and devices could talk to each other without a PC.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Overall braid", "braid", 0.90, "braid", ""),
        ],
        "bundle": [
            {"label": "TPA signal pair", "material": "copper", "cx": -0.30, "cy": -0.26, "r": 0.18, "pair": True, "shielded": True},
            {"label": "TPB signal pair", "material": "copper", "cx": 0.30, "cy": -0.26, "r": 0.18, "pair": True, "shielded": True},
            {"label": "Power (up to 30 V)", "material": "copper-lit", "cx": -0.28, "cy": 0.28, "r": 0.17},
            {"label": "Ground", "material": "tinned", "cx": 0.28, "cy": 0.28, "r": 0.17},
        ],
        "connectors": [C("usb-a", "IEEE 1394 6-pin", "Carried bus power, so a camcorder could run off the cable.")],
        "chips": [CHIP("1394 link/PHY", "phy", "Every device is a peer with its own bus arbitration — no host computer required.")],
    },
    "1999-dvi": {
        "family": "av",
        "signal": {"kind": "differential", "label": "Digital TMDS", "speed": 0.88},
        "tagline": "The bridge cable: digital pins and analogue pins in one shell.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Overall braid", "braid", 0.90, "braid", ""),
        ],
        "bundle": [
            {"label": "TMDS pair 0", "material": "copper", "cx": -0.30, "cy": -0.26, "r": 0.17, "pair": True, "shielded": True},
            {"label": "TMDS pair 1", "material": "copper", "cx": 0.30, "cy": -0.26, "r": 0.17, "pair": True, "shielded": True},
            {"label": "TMDS pair 2", "material": "copper", "cx": -0.30, "cy": 0.26, "r": 0.17, "pair": True, "shielded": True},
            {"label": "Analogue RGB (DVI-I)", "material": "tinned", "cx": 0.30, "cy": 0.26, "r": 0.17},
        ],
        "connectors": [C("hdmi", "DVI-I dual link", "24 digital pins plus 4 analogue ones, so it could drive a VGA monitor through an adapter.")],
        "chips": [CHIP("TMDS transmitter", "phy", "The same signalling HDMI would adopt three years later.")],
    },
    "2002-cat6": {
        "family": "twisted",
        "signal": {"kind": "differential", "label": "1 Gb/s", "speed": 0.9},
        "tagline": "A plastic spine down the middle to keep the four pairs apart.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Cross-filler spine", "teflon", 0.88, "solid", "An X-shaped plastic spline holding each pair in its own quadrant — the visual signature of Cat6."),
        ],
        "pairs": {"count": 4, "colors": ["#3fbfd4", "#e8913a", "#46c98b", "#ef5f5f"], "ring": 0.52, "r": 0.19, "twist": True},
        "connectors": [C("rj45", "RJ45 (8P8C)", "")],
        "chips": [CHIP("Gigabit PHY", "phy", "Runs all four pairs at once, in both directions simultaneously, and cancels its own echo.")],
    },
    # ── Modern ──────────────────────────────────────────────────
    "2003-sata": {
        "family": "serial",
        "signal": {"kind": "differential", "label": "1.5–6 Gb/s serial", "speed": 0.95},
        "tagline": "Seven wires beat forty: serial won because parallel ran out of road.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Foil + drain", "foil", 0.86, "foil", "Each pair individually wrapped — at 6 GHz the pairs must not hear each other."),
        ],
        "bundle": [
            {"label": "Transmit pair (A+/A−)", "material": "copper", "cx": -0.32, "cy": 0.0, "r": 0.22, "pair": True, "shielded": True},
            {"label": "Receive pair (B+/B−)", "material": "copper", "cx": 0.32, "cy": 0.0, "r": 0.22, "pair": True, "shielded": True},
        ],
        "connectors": [C("usb-a", "SATA 7-pin", "L-shaped so it only fits one way. Three grounds separate the two pairs.")],
        "chips": [CHIP("SATA PHY", "phy", "Serialises at 6 GHz — far past the point where 40 parallel wires could stay in step.")],
    },
    "2003-poe": {
        "family": "twisted",
        "signal": {"kind": "differential", "label": "Data + 48 V DC", "speed": 0.88},
        "tagline": "One cable that carries the network *and* runs the device off it.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Pair separator", "teflon", 0.88, "solid", ""),
        ],
        "pairs": {"count": 4, "colors": ["#3fbfd4", "#e8913a", "#46c98b", "#ef5f5f"], "ring": 0.52, "r": 0.19, "twist": True},
        "connectors": [C("rj45", "RJ45 (8P8C)", "Identical plug to plain Ethernet — the power is negotiated, not wired in.")],
        "chips": [
            CHIP("PoE controller (PSE/PD)", "controller", "The switch probes for a known resistance before it dares apply 48 V, so it never fries a laptop."),
        ],
    },
    "2006-displayport": {
        "family": "av",
        "signal": {"kind": "differential", "label": "Packetised video", "speed": 0.97},
        "tagline": "Video as data packets, not as a scanning beam.",
        "layers": [
            L("PVC jacket", "pvc", 1.00, "solid", ""),
            L("Overall braid", "braid", 0.91, "braid", ""),
            L("Foil shield", "foil", 0.84, "foil", ""),
        ],
        "bundle": [
            {"label": "Main lane 0", "material": "copper", "cx": -0.32, "cy": -0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "Main lane 1", "material": "copper", "cx": 0.32, "cy": -0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "Main lane 2", "material": "copper", "cx": -0.32, "cy": 0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "Main lane 3", "material": "copper", "cx": 0.32, "cy": 0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "AUX channel + power", "material": "tinned", "cx": 0.0, "cy": 0.0, "r": 0.14},
        ],
        "connectors": [C("hdmi", "DisplayPort", "A latching plug — squeeze the release or you will pull your monitor off the desk.")],
        "chips": [CHIP("DisplayPort transmitter", "phy", "Chops the image into micro-packets, so one cable can drive several monitors in a chain.")],
    },
    "2006-10gbase-t": {
        "family": "twisted",
        "signal": {"kind": "differential", "label": "10 Gb/s", "speed": 0.96},
        "tagline": "Ten gigabits over twisted copper — an idea most engineers called impossible.",
        "layers": [
            L("LSZH jacket", "lszh", 1.00, "solid", ""),
            L("Overall braid", "braid", 0.90, "braid", "Cat6a adds shielding to fight alien crosstalk — interference from the cable lying next to it."),
            L("Cross-filler spine", "teflon", 0.80, "solid", ""),
        ],
        "pairs": {"count": 4, "colors": ["#3fbfd4", "#e8913a", "#46c98b", "#ef5f5f"], "ring": 0.50, "r": 0.18, "twist": True},
        "connectors": [C("rj45", "Shielded RJ45", "")],
        "chips": [CHIP("10GBASE-T DSP", "dsp", "Burns several watts running error correction and echo cancellation just to keep the link alive.")],
    },
    "2011-thunderbolt": {
        "family": "usb",
        "signal": {"kind": "differential", "label": "10–40 Gb/s", "speed": 1.0},
        "tagline": "PCI Express, stretched down a cable — your GPU on the end of a wire.",
        "layers": [
            L("TPE jacket", "lszh", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.91, "braid", ""),
            L("Foil shield", "foil", 0.84, "foil", ""),
        ],
        "bundle": [
            {"label": "Lane 1 TX/RX", "material": "copper", "cx": -0.32, "cy": -0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "Lane 2 TX/RX", "material": "copper", "cx": 0.32, "cy": -0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "Lane 3 TX/RX", "material": "copper", "cx": -0.32, "cy": 0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "Bus power", "material": "copper-lit", "cx": 0.32, "cy": 0.26, "r": 0.16},
        ],
        "connectors": [C("usb-c", "Thunderbolt (USB-C shell)", "Same plug as USB-C, but only certified cables carry the full 40 Gb/s.")],
        "chips": [
            CHIP("Thunderbolt retimer", "retimer", "An active chip in each plug that receives the signal, cleans it, and re-sends it — without it the cable could only be a few centimetres long."),
            CHIP("E-marker IC", "emarker", "Tells the host this is a 40 Gb/s cable and not a charging lead."),
        ],
    },
    "2012-lightning": {
        "family": "usb",
        "signal": {"kind": "differential", "label": "USB 2.0 · 480 Mb/s", "speed": 0.7},
        "tagline": "The first reversible phone plug — with a chip that decides what each pin does.",
        "layers": [
            L("TPE jacket", "lszh", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.88, "braid", ""),
        ],
        "bundle": [
            {"label": "USB D+/D− pair", "material": "copper", "cx": -0.28, "cy": -0.22, "r": 0.20, "pair": True},
            {"label": "Power", "material": "copper-lit", "cx": 0.30, "cy": -0.22, "r": 0.17},
            {"label": "Accessory ID", "material": "tinned", "cx": -0.28, "cy": 0.28, "r": 0.16},
            {"label": "Ground", "material": "tinned", "cx": 0.30, "cy": 0.28, "r": 0.16},
        ],
        "connectors": [C("usb-c", "Lightning 8-pin", "Reversible because the plug's chip re-assigns the pins depending on which way up it went in.")],
        "chips": [CHIP("Authentication IC", "emarker", "Apple's MFi chip. If it is missing or cloned, the phone refuses the cable — the reason third-party leads suddenly stopped working after updates.")],
    },
    "2019-usb4": {
        "family": "usb",
        "signal": {"kind": "differential", "label": "40 Gb/s tunnelled", "speed": 1.0},
        "tagline": "One cable that carries USB, DisplayPort and PCIe at the same time, in shares.",
        "layers": [
            L("TPE jacket", "lszh", 1.00, "solid", ""),
            L("Braided shield", "braid", 0.91, "braid", ""),
            L("Foil shield", "foil", 0.84, "foil", ""),
        ],
        "bundle": [
            {"label": "TX/RX lane pair 1", "material": "copper", "cx": -0.32, "cy": -0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "TX/RX lane pair 2", "material": "copper", "cx": 0.32, "cy": -0.26, "r": 0.16, "pair": True, "shielded": True},
            {"label": "USB 2.0 fallback pair", "material": "copper", "cx": -0.32, "cy": 0.26, "r": 0.15, "pair": True},
            {"label": "VBUS + CC", "material": "copper-lit", "cx": 0.32, "cy": 0.26, "r": 0.16},
        ],
        "connectors": [C("usb-c", "USB Type-C", "")],
        "chips": [
            CHIP("USB4 router", "controller", "Splits the cable's bandwidth on the fly — give the monitor more, the SSD gets less."),
            CHIP("E-marker IC", "emarker", "Declares speed and wattage so the host knows what the cable can actually do."),
        ],
    },
}
