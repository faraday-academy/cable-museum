#!/usr/bin/env python3
"""
Build public/content/cable_eras_v2.json.

  * adds the 23 cables that were missing from the timeline
  * attaches a `history` block to every exhibit:
        beats      — problem / breakthrough / legacy  (the default view)
        milestones — the cable's whole life, not just its debut
        stats      — comparable figures across all exhibits
  * attaches `bitrate` (bits per second) so the museum-wide speed
    ladder can place every cable on one log scale

Existing exhibits keep their own summary/facts/links/trivia; this only
adds fields. Run:  python3 scripts/build_content.py
"""

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERA_PATH = os.path.join(ROOT, "public/content/cable_eras_v2.json")


def H(problem, breakthrough, legacy, milestones, stats):
    return {
        "beats": {"problem": problem, "breakthrough": breakthrough, "legacy": legacy},
        "milestones": [{"year": y, "label": l} for y, l in milestones],
        "stats": [{"label": k, "value": v} for k, v in stats],
    }


def wiki(slug, label):
    return {"label": label, "href": f"https://en.wikipedia.org/wiki/{slug}"}


# ═══════════════════════════════════════════════════════════════
#  NEW EXHIBITS — the 23 gaps
# ═══════════════════════════════════════════════════════════════
NEW_ERAS = [
    {
        "id": "1878-phone-jack",
        "title": "The ¼-inch Phone Jack",
        "years": "1878",
        "sortYear": 1878,
        "summary": "A plug designed for telephone switchboards that is still in every guitar amp today.",
        "keyAdvancement": "Fast, reusable audio connection",
        "bitrate": 3000,
        "facts": [
            "Named 'phone jack' because it was literally for telephones.",
            "The tip/ring/sleeve layout still names the contacts today."
        ],
        "links": [wiki("Phone_connector_(audio)", "Phone connector (audio)")],
        "history": H(
            "Switchboard operators had to connect any caller to any other caller in seconds, thousands of times a day.",
            "A metal plug that could be jammed into a socket and yanked out one-handed, making and breaking a circuit instantly.",
            "It outlived the switchboard by a century. Guitars, headphones and studio gear all still use the same shape.",
            [("1878", "Appears in the first commercial telephone exchanges"),
             ("1920s", "Adopted by radio studios for patch bays"),
             ("1950s", "Becomes the standard guitar and amplifier connector"),
             ("1964", "The 3.5 mm miniature version ships with pocket radios"),
             ("today", "Still the default on stage and in the studio")],
            [("Signal", "Analogue audio"), ("Contacts", "2–3 (TS / TRS)"),
             ("Diameter", "6.35 mm"), ("Still used", "Yes — everywhere")],
        ),
    },
    {
        "id": "1950s-xlr",
        "title": "XLR: The Balanced Audio Cable",
        "years": "1950s",
        "sortYear": 1955,
        "summary": "Three pins that let a microphone run 100 metres without picking up a radio station.",
        "keyAdvancement": "Balanced, shielded, latching audio",
        "bitrate": 4000,
        "facts": [
            "Pin 1 is ground, pins 2 and 3 carry the same signal in opposite polarity.",
            "The latch exists because a mic cable falling out mid-concert is unacceptable."
        ],
        "links": [wiki("XLR_connector", "XLR connector")],
        "history": H(
            "Long microphone runs acted like antennas, so live sound picked up hum, buzz and the occasional radio broadcast.",
            "Send the audio twice down a twisted pair — once inverted. The mixer subtracts the two, and noise picked up by both wires cancels out.",
            "Balanced audio became non-negotiable in professional sound. Every stage and studio on earth runs on it.",
            [("1950s", "Cannon introduces the X series connector"),
             ("1950s", "A latch is added — the 'L' in XLR"),
             ("1960s", "Rubber compound around the contacts completes the name"),
             ("1980s", "Becomes the universal professional audio standard"),
             ("today", "Also carries DMX lighting control on the same connector")],
            [("Signal", "Balanced analogue"), ("Pins", "3"),
             ("Usable length", "100 m+"), ("Still used", "Yes — industry standard")],
        ),
    },
    {
        "id": "1954-gotland-hvdc",
        "title": "Gotland: The First HVDC Submarine Power Cable",
        "years": "1954",
        "sortYear": 1954,
        "summary": "Not data — raw electrical power, 98 km under the Baltic Sea.",
        "keyAdvancement": "High-voltage DC power under the sea",
        "bitrate": None,
        "facts": [
            "Carried 20 MW at 100 kV DC to the island of Gotland.",
            "AC cannot cross long undersea distances; the sea itself soaks up the energy."
        ],
        "links": [wiki("HVDC_Gotland", "HVDC Gotland")],
        "history": H(
            "An island needed mainland electricity, but alternating current wastes almost all its energy in a long undersea cable.",
            "Convert to direct current at one end, send it through oil-soaked paper insulation, and convert back at the other.",
            "Every offshore wind farm and cross-border power link since is a descendant of this cable.",
            [("1954", "Gotland link enters service — 98 km, 100 kV DC"),
             ("1954", "Mercury-arc valves do the AC/DC conversion"),
             ("1970", "Upgraded with solid-state thyristor valves"),
             ("1990s", "HVDC becomes standard for offshore wind"),
             ("today", "Multi-gigawatt links span the North Sea")],
            [("Carries", "Power, not data"), ("Voltage", "100 kV DC"),
             ("Length", "98 km"), ("Still used", "Superseded, principle universal")],
        ),
    },
    {
        "id": "1962-rs232",
        "title": "RS-232: The Serial Cable",
        "years": "1962",
        "sortYear": 1962,
        "summary": "One bit at a time, at ±12 volts — and it still runs factory floors sixty years on.",
        "keyAdvancement": "A standard pinout for serial data",
        "bitrate": 20000,
        "facts": [
            "A '1' is −12 V and a '0' is +12 V — the logic is upside down.",
            "The RS-232-C revision of 1969 is the one almost everyone actually used."
        ],
        "links": [wiki("RS-232", "RS-232")],
        "history": H(
            "Every terminal and modem maker wired their plugs differently. Connecting two machines meant hand-building a cable and hoping.",
            "The EIA published one agreed pinout with defined voltages and a handshake, so any terminal could talk to any modem.",
            "USB buried it for consumers, but it never died: industrial machines, network switches and lab gear still expose a serial port.",
            [("1962", "EIA publishes the RS-232 standard"),
             ("1969", "RS-232-C — the revision that stuck"),
             ("1981", "The IBM PC ships with a serial port"),
             ("1998", "USB begins replacing it on consumer machines"),
             ("today", "Still standard for industrial and network console access")],
            [("Speed", "20 kb/s typical"), ("Max length", "15 m"),
             ("Pins", "25 (or 9)"), ("Still used", "Yes — industrial")],
        ),
    },
    {
        "id": "1970-centronics",
        "title": "The Centronics Parallel Printer Cable",
        "years": "1970",
        "sortYear": 1970,
        "summary": "Eight bits side by side — fast, until the wires started interfering with each other.",
        "keyAdvancement": "Parallel data transfer to peripherals",
        "bitrate": 1000000,
        "facts": [
            "36 pins, and a connector held on with two springy wire clips.",
            "Sending 8 bits at once is only faster if all 8 arrive at the same moment."
        ],
        "links": [wiki("Parallel_port", "Parallel port")],
        "history": H(
            "Serial cables sent one bit at a time, which made printing a page painfully slow.",
            "Run eight wires in parallel and move a whole byte per clock tick, with extra wires for 'ready' and 'busy' handshaking.",
            "Parallel hit a wall: at higher speeds the eight bits drift out of step. Every modern interface went back to serial.",
            [("1970", "Centronics ships it with its dot-matrix printers"),
             ("1981", "IBM PC adopts it as the printer port"),
             ("1994", "IEEE 1284 standardises bidirectional modes"),
             ("2000s", "USB replaces it completely"),
             ("today", "Gone from consumer machines")],
            [("Speed", "~1 Mb/s"), ("Max length", "5 m"),
             ("Pins", "36"), ("Still used", "No — obsolete")],
        ),
    },
    {
        "id": "1980-10base5",
        "title": "10BASE5: The Thick Yellow Ethernet",
        "years": "1980",
        "sortYear": 1980,
        "summary": "A rigid yellow hosepipe you drilled into with a spike called a vampire tap.",
        "keyAdvancement": "The first commercial Ethernet cable",
        "bitrate": 10000000,
        "facts": [
            "Black bands every 2.5 m marked the only legal places to tap in.",
            "One cable could run 500 m and serve 100 machines — all sharing it."
        ],
        "links": [wiki("10BASE5", "10BASE5")],
        "history": H(
            "Offices had computers that could not talk to each other, and no agreed way to wire a building for data.",
            "One thick shared coaxial backbone that every machine clamped onto, with a protocol for detecting when two machines talked at once.",
            "The shared-wire model was doomed — but Ethernet the protocol won everything, and still runs the internet's plumbing.",
            [("1980", "DEC, Intel and Xerox publish the DIX standard"),
             ("1983", "Ratified as IEEE 802.3"),
             ("1985", "Thinner, cheaper 10BASE2 arrives"),
             ("1990", "10BASE-T over twisted pair kills it"),
             ("today", "Extinct, but 802.3 is everywhere")],
            [("Speed", "10 Mb/s"), ("Max length", "500 m"),
             ("Topology", "Shared bus"), ("Still used", "No — obsolete")],
        ),
    },
    {
        "id": "1983-midi",
        "title": "MIDI: The Cable That Made Synths Talk",
        "years": "1983",
        "sortYear": 1983,
        "summary": "A slow current loop that let any synthesiser control any other — and still does.",
        "keyAdvancement": "Universal instrument control protocol",
        "bitrate": 31250,
        "facts": [
            "MIDI sends instructions, not sound: 'note 60, velocity 90, on'.",
            "Rival manufacturers agreed on it — and never charged a licence fee."
        ],
        "links": [wiki("MIDI", "MIDI")],
        "history": H(
            "Every synthesiser maker used its own control voltages, so two keyboards from different brands could not be played together.",
            "A shared serial protocol over a 5-pin DIN cable, with an opto-isolator at each input so no two amplifiers ever share a ground.",
            "Forty years unchanged and still universal — one of the most successful standards in music, precisely because nobody owned it.",
            [("1981", "Dave Smith proposes a universal synth interface"),
             ("1983", "MIDI 1.0 published; first cross-brand demo"),
             ("1980s", "Becomes the backbone of studio sequencing"),
             ("2020", "MIDI 2.0 adds higher resolution — backwards compatible"),
             ("today", "Still standard on nearly every instrument")],
            [("Speed", "31.25 kb/s"), ("Max length", "15 m"),
             ("Pins", "5 (3 used)"), ("Still used", "Yes — universal")],
        ),
    },
    {
        "id": "1985-10base2",
        "title": "10BASE2 'Cheapernet'",
        "years": "1985",
        "sortYear": 1985,
        "summary": "Thin coax and BNC twists — cheap, flexible, and one loose end killed the whole office.",
        "keyAdvancement": "Affordable coaxial Ethernet",
        "bitrate": 10000000,
        "facts": [
            "Every machine sat on one shared wire via a T-connector.",
            "Both ends needed a 50 Ω terminator or the whole segment failed."
        ],
        "links": [wiki("10BASE2", "10BASE2")],
        "history": H(
            "10BASE5 was expensive, rigid, and needed a specialist with a drill to add a machine to the network.",
            "Thinner 50 Ω coax with twist-lock BNC connectors, so anyone could add a machine by unplugging a T and clicking it in.",
            "It taught the industry why shared buses are fragile: any single break or missing terminator took down everybody.",
            [("1985", "Standardised as IEEE 802.3a"),
             ("late 1980s", "Becomes the default small-office network"),
             ("1990", "10BASE-T offers per-machine wiring instead"),
             ("mid 1990s", "Structured cabling wins; thinnet fades"),
             ("today", "Obsolete")],
            [("Speed", "10 Mb/s"), ("Max length", "185 m"),
             ("Topology", "Shared bus"), ("Still used", "No — obsolete")],
        ),
    },
    {
        "id": "1985-token-ring",
        "title": "Token Ring",
        "years": "1985",
        "sortYear": 1986,
        "summary": "IBM's orderly answer to Ethernet: you may only transmit while holding the token.",
        "keyAdvancement": "Deterministic, collision-free networking",
        "bitrate": 16000000,
        "facts": [
            "No collisions were possible — a machine waited its turn, always.",
            "The IBM Data Connector mates with itself: there is no male or female."
        ],
        "links": [wiki("Token_Ring", "Token Ring")],
        "history": H(
            "Early Ethernet let any machine talk whenever it liked, so busy networks wasted time on collisions and slowed unpredictably.",
            "Pass a special 'token' frame around a ring. Only the holder may transmit, so the network never collides and timing is guaranteed.",
            "Technically superior and genuinely deterministic — but it was proprietary and dearer, and cheap Ethernet simply outsold it.",
            [("1985", "IBM launches Token Ring at 4 Mb/s"),
             ("1989", "16 Mb/s version arrives"),
             ("1990s", "Loses ground to cheap switched Ethernet"),
             ("2000s", "Effectively discontinued"),
             ("today", "A cautionary tale about better-but-pricier")],
            [("Speed", "4–16 Mb/s"), ("Topology", "Ring"),
             ("Collisions", "None by design"), ("Still used", "No — obsolete")],
        ),
    },
    {
        "id": "1986-scsi",
        "title": "SCSI: The Small Computer System Interface",
        "years": "1986",
        "sortYear": 1987,
        "summary": "Fast and capable, and cursed with termination problems and ID conflicts.",
        "keyAdvancement": "A standard parallel bus for peripherals",
        "bitrate": 40000000,
        "facts": [
            "Up to eight devices shared one chain, each needing a unique ID.",
            "Getting termination wrong produced faults that looked like random hardware failure."
        ],
        "links": [wiki("SCSI", "SCSI")],
        "history": H(
            "Every hard disk, scanner and tape drive shipped with its own incompatible controller card.",
            "One standard parallel bus that any peripheral could join, addressed by ID, with a defined command set that survives to this day.",
            "The cable is long gone, but SCSI's command language still runs inside USB storage, SAS drives and cloud storage arrays.",
            [("1986", "Ratified as ANSI X3.131"),
             ("1986", "Macintosh Plus ships with a SCSI port"),
             ("1990s", "Fast/Wide/Ultra variants push the bus harder"),
             ("2003", "Serial Attached SCSI replaces the parallel cable"),
             ("today", "SCSI commands live on inside USB and SAS")],
            [("Speed", "5–40 MB/s"), ("Devices", "8 per chain"),
             ("Pins", "50"), ("Still used", "Command set only")],
        ),
    },
    {
        "id": "1986-ide-ata",
        "title": "The IDE Ribbon Cable",
        "years": "1986",
        "sortYear": 1988,
        "summary": "The grey ribbon inside every beige PC — 40 wires and one red stripe.",
        "keyAdvancement": "Drive controller moved onto the drive",
        "bitrate": 1064000000,
        "facts": [
            "The red stripe marks pin 1. Getting it backwards was a rite of passage.",
            "Faster versions needed 80 wires — 40 of them grounds, just to stop crosstalk."
        ],
        "links": [wiki("Parallel_ATA", "Parallel ATA")],
        "history": H(
            "Hard drives needed an expensive dedicated controller card, and every drive maker did it differently.",
            "Put the controller on the drive itself — Integrated Drive Electronics — so the cable only had to carry a simple 16-bit bus.",
            "Parallel ATA ran out of headroom exactly like every parallel bus before it, and SATA replaced it with two serial pairs.",
            [("1986", "Compaq and Western Digital create IDE"),
             ("1994", "Standardised as ATA-1"),
             ("1998", "80-wire cable added for faster UDMA modes"),
             ("2003", "SATA begins replacing it"),
             ("today", "Obsolete in new machines")],
            [("Speed", "up to 133 MB/s"), ("Max length", "46 cm"),
             ("Wires", "40 or 80"), ("Still used", "No — legacy only")],
        ),
    },
    {
        "id": "1987-vga",
        "title": "VGA: Analogue Video",
        "years": "1987",
        "sortYear": 1989,
        "summary": "Three analogue colour signals, each in its own miniature coaxial cable.",
        "keyAdvancement": "A universal monitor connection",
        "bitrate": 1000000000,
        "facts": [
            "VGA is analogue: the monitor never knew what a pixel was.",
            "Its 15-pin plug survived on projectors for over thirty years."
        ],
        "links": [wiki("VGA_connector", "VGA connector")],
        "history": H(
            "Every graphics card used a different digital monitor connector, each locked to a fixed set of resolutions.",
            "Go analogue: send red, green and blue as smooth voltages, and the same cable can carry any resolution the monitor can handle.",
            "That flexibility kept it alive for decades, but analogue meant fuzziness at high resolution — and digital eventually won.",
            [("1987", "IBM introduces VGA with the PS/2 line"),
             ("1990s", "Becomes the universal PC monitor connector"),
             ("1999", "DVI starts the move to digital"),
             ("2010", "Major vendors announce end of support"),
             ("today", "Lingers on projectors and older AV kit")],
            [("Signal", "Analogue RGB"), ("Pins", "15"),
             ("Max length", "~10 m usable"), ("Still used", "Rarely — legacy AV")],
        ),
    },
    {
        "id": "1987-ps2",
        "title": "The PS/2 Keyboard & Mouse Cable",
        "years": "1987",
        "sortYear": 1990,
        "summary": "Purple for keyboard, green for mouse — and never, ever hot-pluggable.",
        "keyAdvancement": "A compact dedicated input port",
        "bitrate": 12000,
        "facts": [
            "Plugging one in while the PC was on could kill the port.",
            "Colour coding was added because the two plugs are physically identical."
        ],
        "links": [wiki("PS/2_port", "PS/2 port")],
        "history": H(
            "Keyboards used a large 5-pin DIN plug, and mice took up a whole serial port that something else needed.",
            "A compact 6-pin mini-DIN for each, keyed so it only fits one way, freeing the serial port entirely.",
            "USB made it redundant, though gamers clung on: PS/2 keyboards interrupt the CPU directly rather than being polled.",
            [("1987", "Introduced with the IBM PS/2"),
             ("1990s", "Becomes standard on virtually every PC"),
             ("2000s", "USB peripherals take over"),
             ("2010s", "Disappears from most motherboards"),
             ("today", "Occasionally kept for BIOS access and gaming")],
            [("Speed", "~12 kb/s"), ("Pins", "6"),
             ("Hot-plug", "No"), ("Still used", "Rarely")],
        ),
    },
    {
        "id": "1995-firewire",
        "title": "FireWire (IEEE 1394)",
        "years": "1995",
        "sortYear": 1995.5,
        "summary": "Faster than early USB, and devices could talk to each other without a computer.",
        "keyAdvancement": "Peer-to-peer high-speed peripheral bus",
        "bitrate": 400000000,
        "facts": [
            "Two camcorders could copy to each other with no PC involved.",
            "It could deliver up to 45 W down the cable, long before USB could."
        ],
        "links": [wiki("IEEE_1394", "IEEE 1394")],
        "history": H(
            "Digital video needed guaranteed, uninterrupted bandwidth, and USB 1.0 was far too slow to carry it.",
            "A peer-to-peer bus with guaranteed isochronous timeslots, bus power, and no need for a host computer to mediate.",
            "Technically ahead of USB for years, but Apple's licence fees and USB's ubiquity decided it. USB-C finally absorbed the ideas.",
            [("1995", "Standardised as IEEE 1394"),
             ("1999", "Apple ships FireWire 400 across the Mac line"),
             ("2002", "FireWire 800 doubles the speed"),
             ("2008", "USB 3.0 removes the speed advantage"),
             ("2011", "Thunderbolt inherits the concept")],
            [("Speed", "400–800 Mb/s"), ("Max length", "4.5 m"),
             ("Power", "up to 45 W"), ("Still used", "No — superseded")],
        ),
    },
    {
        "id": "1999-dvi",
        "title": "DVI: The Bridge to Digital",
        "years": "1999",
        "sortYear": 1999,
        "summary": "One shell carrying both digital and analogue pins, so it could talk to either world.",
        "keyAdvancement": "Digital video with analogue fallback",
        "bitrate": 9900000000,
        "facts": [
            "DVI-I carries digital and analogue at once; DVI-D drops the analogue pins.",
            "Its TMDS signalling is the same one HDMI adopted three years later."
        ],
        "links": [wiki("Digital_Visual_Interface", "Digital Visual Interface")],
        "history": H(
            "Flat panels are digital, but PCs output analogue VGA — so the signal was converted to analogue and back, losing quality twice.",
            "Send the pixels digitally with TMDS signalling, and include analogue pins in the same connector so old monitors still work.",
            "The transitional design did its job and was retired: HDMI took its signalling to televisions, DisplayPort took it to computers.",
            [("1999", "Digital Display Working Group publishes DVI"),
             ("2000s", "Becomes the standard PC flat-panel connector"),
             ("2002", "HDMI adopts DVI's TMDS signalling"),
             ("2008", "DisplayPort begins displacing it"),
             ("today", "Largely retired")],
            [("Signal", "Digital + analogue"), ("Bandwidth", "9.9 Gb/s dual link"),
             ("Pins", "24 + 4"), ("Still used", "Rarely — legacy")],
        ),
    },
    {
        "id": "2002-cat6",
        "title": "Category 6 Cable",
        "years": "2002",
        "sortYear": 2002.5,
        "summary": "A plastic spine down the middle, holding the four pairs apart at gigabit speeds.",
        "keyAdvancement": "Gigabit Ethernet over copper",
        "bitrate": 1000000000,
        "facts": [
            "The X-shaped spline inside is the visual signature of Cat6.",
            "Gigabit uses all four pairs at once, in both directions simultaneously."
        ],
        "links": [wiki("Category_6_cable", "Category 6 cable")],
        "history": H(
            "At gigabit speeds the four pairs inside a Cat5 cable started leaking signal into each other.",
            "A rigid plastic cross running the length of the cable, keeping each pair in its own quadrant, plus tighter twist rates.",
            "Cat6 is still the default for new building wiring twenty years on — the format proved remarkably durable.",
            [("2002", "TIA/EIA ratifies the Category 6 standard"),
             ("2000s", "Becomes standard for new office installs"),
             ("2008", "Cat6a adds shielding for 10 Gb/s"),
             ("2016", "Cat8 pushes to 40 Gb/s over short runs"),
             ("today", "Still the workhorse of building cabling")],
            [("Speed", "1 Gb/s (10 Gb/s short)"), ("Max length", "100 m"),
             ("Pairs", "4"), ("Still used", "Yes — standard")],
        ),
    },
    {
        "id": "2003-sata",
        "title": "SATA: Serial ATA",
        "years": "2003",
        "sortYear": 2003,
        "summary": "Seven wires beat forty — serial won because parallel had run out of road.",
        "keyAdvancement": "Serial replacement for the drive ribbon",
        "bitrate": 6000000000,
        "facts": [
            "The L-shaped connector physically cannot go in backwards.",
            "A thin round cable improved airflow inside the case dramatically."
        ],
        "links": [wiki("SATA", "SATA")],
        "history": H(
            "The 80-wire IDE ribbon blocked airflow, and its parallel bits could no longer be kept in step at higher speeds.",
            "Two differential pairs running at gigahertz rates — fewer wires, far faster, and hot-pluggable.",
            "SATA is still how most desktop drives connect, though NVMe over PCIe now carries the fastest storage.",
            [("2003", "SATA 1.5 Gb/s ships"),
             ("2004", "SATA II doubles it to 3 Gb/s"),
             ("2009", "SATA III reaches 6 Gb/s"),
             ("2013", "NVMe begins taking the high end"),
             ("today", "Still standard for hard disks and budget SSDs")],
            [("Speed", "1.5–6 Gb/s"), ("Max length", "1 m"),
             ("Wires", "7"), ("Still used", "Yes — standard")],
        ),
    },
    {
        "id": "2003-poe",
        "title": "Power over Ethernet",
        "years": "2003",
        "sortYear": 2003.5,
        "summary": "One cable that carries the network and runs the device off it.",
        "keyAdvancement": "Data and power down one cable",
        "bitrate": 1000000000,
        "facts": [
            "The switch tests for a known resistance before it dares send 48 V.",
            "Modern PoE++ can deliver up to 90 W — enough for a laptop."
        ],
        "links": [wiki("Power_over_Ethernet", "Power over Ethernet")],
        "history": H(
            "Ceiling-mounted phones, cameras and access points each needed a network cable and a mains socket next to them.",
            "Put DC power on the same twisted pairs as the data, with a negotiation step so the switch never energises a device that cannot take it.",
            "It quietly rewired buildings: security cameras, phones, wireless access points and even LED lighting now run on Ethernet.",
            [("2003", "IEEE 802.3af — up to 15 W"),
             ("2009", "802.3at (PoE+) raises it to 30 W"),
             ("2018", "802.3bt (PoE++) reaches 90 W"),
             ("2020s", "Used for lighting and building automation"),
             ("today", "Standard on business network switches")],
            [("Power", "15–90 W"), ("Voltage", "48 V DC"),
             ("Max length", "100 m"), ("Still used", "Yes — growing")],
        ),
    },
    {
        "id": "2006-displayport",
        "title": "DisplayPort",
        "years": "2006",
        "sortYear": 2006,
        "summary": "Video sent as data packets rather than as a scanning beam.",
        "keyAdvancement": "Packetised, extensible video transport",
        "bitrate": 80000000000,
        "facts": [
            "Because it is packet-based, one port can drive several daisy-chained monitors.",
            "It is royalty-free, which is why computers favour it over HDMI."
        ],
        "links": [wiki("DisplayPort", "DisplayPort")],
        "history": H(
            "HDMI and DVI still imitated the scanning pattern of a cathode-ray tube, which limited how the link could be shared or extended.",
            "Treat video as micro-packets on a generic high-speed link, so bandwidth can be divided between multiple displays and other data.",
            "DisplayPort became the computer industry's display standard, and its protocol is what runs inside USB-C's video mode.",
            [("2006", "VESA publishes DisplayPort 1.0"),
             ("2009", "Multi-Stream Transport enables monitor daisy-chaining"),
             ("2014", "DisplayPort Alt Mode brings it to USB-C"),
             ("2019", "DP 2.0 reaches 80 Gb/s"),
             ("today", "Standard on computers and GPUs")],
            [("Bandwidth", "up to 80 Gb/s"), ("Max length", "3 m passive"),
             ("Lanes", "4"), ("Still used", "Yes — standard")],
        ),
    },
    {
        "id": "2006-10gbase-t",
        "title": "10GBASE-T over Cat6a",
        "years": "2006",
        "sortYear": 2006.5,
        "summary": "Ten gigabits over twisted copper — an idea most engineers called impossible.",
        "keyAdvancement": "10 Gb/s on ordinary building cabling",
        "bitrate": 10000000000,
        "facts": [
            "It fights 'alien crosstalk' — interference from the cable lying next to it.",
            "The signal processing burns several watts per port just to keep the link up."
        ],
        "links": [wiki("10GBASE-T", "10GBASE-T")],
        "history": H(
            "Data centres needed ten gigabits, and everyone assumed that meant ripping out copper and installing fibre everywhere.",
            "Throw enormous digital signal processing at the problem: cancel the echo, cancel the crosstalk, and correct the errors that remain.",
            "It bought copper another decade in the data centre, at the cost of power draw that fibre never had.",
            [("2006", "Ratified as IEEE 802.3an"),
             ("2008", "Cat6a cabling standard finalised"),
             ("2010s", "Becomes common in data centres and servers"),
             ("2016", "2.5G and 5G variants reuse older cable"),
             ("today", "Standard on servers and high-end desktops")],
            [("Speed", "10 Gb/s"), ("Max length", "100 m"),
             ("Power", "~3 W per port"), ("Still used", "Yes")],
        ),
    },
    {
        "id": "2011-thunderbolt",
        "title": "Thunderbolt",
        "years": "2011",
        "sortYear": 2011,
        "summary": "PCI Express stretched down a cable — your graphics card on the end of a wire.",
        "keyAdvancement": "External PCIe over a cable",
        "bitrate": 40000000000,
        "facts": [
            "Active cables contain retimer chips; without them the cable could only be centimetres long.",
            "It exposes PCIe directly, which is powerful — and a genuine security consideration."
        ],
        "links": [wiki("Thunderbolt_(interface)", "Thunderbolt (interface)")],
        "history": H(
            "External devices were always slower than internal ones, because nothing could carry the PC's internal PCIe bus outside the case.",
            "Tunnel PCIe and DisplayPort down one cable at 10 Gb/s, using active chips in the plugs to keep the signal intact.",
            "It made external GPUs and single-cable docking real, and merged into USB4 — which is Thunderbolt 3 donated to the USB standard.",
            [("2011", "Thunderbolt 1 ships on the MacBook Pro, 10 Gb/s"),
             ("2013", "Thunderbolt 2 reaches 20 Gb/s"),
             ("2015", "Thunderbolt 3 adopts the USB-C connector, 40 Gb/s"),
             ("2019", "Intel donates the spec; it becomes USB4"),
             ("2023", "Thunderbolt 5 reaches 80–120 Gb/s")],
            [("Speed", "10–120 Gb/s"), ("Max passive length", "0.8 m"),
             ("Power", "up to 100 W"), ("Still used", "Yes — current")],
        ),
    },
    {
        "id": "2012-lightning",
        "title": "Lightning",
        "years": "2012",
        "sortYear": 2012,
        "summary": "The first reversible phone plug — with a chip deciding what each pin does.",
        "keyAdvancement": "Reversible connector with active pin assignment",
        "bitrate": 480000000,
        "facts": [
            "It is reversible because a chip re-assigns the pins based on orientation.",
            "The authentication chip is why some third-party cables stopped working after updates."
        ],
        "links": [wiki("Lightning_(connector)", "Lightning (connector)")],
        "history": H(
            "Apple's 30-pin dock connector was bulky, only went in one way, and wasted space inside increasingly thin phones.",
            "A small 8-pin plug with a controller chip inside, so the pins can be re-assigned depending on which way round it is inserted.",
            "It beat USB-C to reversibility by two years, then was retired when EU law required USB-C on phones.",
            [("2012", "Introduced with the iPhone 5"),
             ("2014", "USB-C arrives with the same reversible idea"),
             ("2022", "EU adopts the common charger directive"),
             ("2023", "iPhone 15 switches to USB-C"),
             ("today", "Being phased out")],
            [("Speed", "480 Mb/s"), ("Pins", "8"),
             ("Reversible", "Yes"), ("Still used", "Phasing out")],
        ),
    },
    {
        "id": "2019-usb4",
        "title": "USB4",
        "years": "2019",
        "sortYear": 2019,
        "summary": "One cable carrying USB, DisplayPort and PCIe at once — in negotiated shares.",
        "keyAdvancement": "Protocol tunnelling over one link",
        "bitrate": 40000000000,
        "facts": [
            "Bandwidth is allocated dynamically: give the monitor more, the SSD gets less.",
            "It is built on Thunderbolt 3, which Intel donated to the USB standard."
        ],
        "links": [wiki("USB4", "USB4")],
        "history": H(
            "USB-C had one shape but a bewildering range of capabilities, and no way for a user to tell what a given cable could actually do.",
            "One tunnelling architecture carrying USB, DisplayPort and PCIe together, with the cable's e-marker chip declaring its own abilities.",
            "It unified the connector at last — though the naming remains famously confusing, and cables still vary enormously in capability.",
            [("2019", "USB4 specification published"),
             ("2020", "First USB4 devices ship"),
             ("2022", "USB4 v2 targets 80 Gb/s"),
             ("2024", "Becomes common on laptops and phones"),
             ("today", "The converged standard")],
            [("Speed", "20–80 Gb/s"), ("Max passive length", "0.8 m"),
             ("Power", "up to 240 W"), ("Still used", "Yes — current")],
        ),
    },
]

# ═══════════════════════════════════════════════════════════════
#  HISTORY for the 23 exhibits that already existed
# ═══════════════════════════════════════════════════════════════
HISTORY = {
    "1850-dover-calais": (1850, 8, H(
        "England and France were minutes apart by signal fire and days apart by messenger. Nobody had ever run a working wire under the sea.",
        "Wrap a copper wire in gutta-percha — a tree latex that stays watertight in cold seawater — and armour it against the seabed.",
        "It proved undersea telegraphy was possible at all. Within twenty years the idea had wired the planet.",
        [("1850", "First cable laid across the Channel — it failed within hours"),
         ("1851", "An armoured second attempt works and stays working"),
         ("1850s", "Gutta-percha becomes the standard undersea insulator"),
         ("1860s", "Channel model scaled up for the Atlantic"),
         ("today", "Fibre follows almost the same route")],
        [("Speed", "~8 bit/s"), ("Length", "40 km"),
         ("Conductor", "Single copper wire"), ("Still used", "No — historic")])),
    "1858-transatlantic": (1858, 8, H(
        "A message to America took ten days by ship. Business, diplomacy and news all moved at the speed of the Atlantic crossing.",
        "2 500 miles of armoured cable dragged across the ocean floor by two warships meeting in mid-Atlantic.",
        "It worked for three weeks, then died — but Queen Victoria had messaged President Buchanan, and the world had seen it was possible.",
        [("1857", "First laying attempt fails when the cable snaps"),
         ("1858", "Cable completed; Victoria messages Buchanan"),
         ("1858", "Excessive voltage destroys the insulation in weeks"),
         ("1865", "Brunel's Great Eastern attempts a heavier design"),
         ("1866", "A durable cable finally succeeds")],
        [("Speed", "~0.1 words/min"), ("Length", "3 200 km"),
         ("Lifespan", "3 weeks"), ("Still used", "No — historic")])),
    "1866-transatlantic": (1866, 12, H(
        "The 1858 cable had failed publicly and expensively, and investors were sceptical that a permanent Atlantic link could exist.",
        "Heavier copper, four alternating layers of insulation, galvanised armour — and one ship, the Great Eastern, big enough to carry it all.",
        "It lasted decades. News that took ten days now took minutes, and the modern financial market became possible.",
        [("1865", "Attempt fails; cable lost in deep water"),
         ("1866", "Great Eastern completes the crossing"),
         ("1866", "The lost 1865 cable is recovered and completed too"),
         ("1870s", "Cable networks reach India and Australia"),
         ("today", "The template for all submarine cable design")],
        [("Speed", "~8 words/min"), ("Length", "3 200 km"),
         ("Lifespan", "Decades"), ("Still used", "No — historic")])),
    "1876-first-telephone": (1876, 3000, H(
        "The telegraph could send letters, but only trained operators could use it, and it could never carry a human voice.",
        "A varying current that copies the shape of a sound wave, so the wire carries speech itself rather than coded symbols.",
        "It turned the wire from a professional instrument into a household object, and built the largest machine humans had ever made.",
        [("1876", "Bell patents the telephone"),
         ("1876", "First outdoor two-way call over a real line"),
         ("1877", "First commercial telephone line installed"),
         ("1880s", "Exchanges and switchboards spread through cities"),
         ("today", "The copper local loop still reaches many homes")],
        [("Signal", "Analogue voice"), ("Conductor", "Iron line wire"),
         ("Range", "A few km"), ("Still used", "Principle, yes")])),
    "1881-twisted-pair": (1881, 3000, H(
        "Telephone lines strung beside electric power and telegraph wires picked up so much hum and crosstalk they became unusable.",
        "Twist the two wires of the pair around each other. Interference then hits both wires equally and cancels out at the receiver.",
        "One of the most quietly important ideas in all of electronics — every Ethernet cable in the world still uses it.",
        [("1881", "Bell patents the twisting technique"),
         ("1900s", "Becomes standard for all telephone cabling"),
         ("1980s", "Adopted for computer networking"),
         ("1990", "10BASE-T runs Ethernet over it"),
         ("today", "Inside every Cat5/6/6a cable")],
        [("Signal", "Balanced pair"), ("Benefit", "Noise cancellation"),
         ("Twists", "Varies per pair"), ("Still used", "Yes — universal")])),
    "1931-coax-patent": (1931, 1000000, H(
        "Ordinary parallel wires radiate their signal into the air at high frequencies, losing energy and interfering with everything nearby.",
        "Wrap the return conductor completely around the signal conductor. The fields cancel outside the cable, so it neither leaks nor picks up.",
        "Coaxial geometry made broadband possible — television, cable internet and radio all depend on it.",
        [("1929", "Espenschied and Affel file the patent"),
         ("1931", "Patent granted to Bell Labs"),
         ("1936", "First long-haul field trials"),
         ("1950s", "Carries television across continents"),
         ("today", "Still delivers cable internet to homes")],
        [("Signal", "RF carrier"), ("Impedance", "50 or 75 Ω"),
         ("Bandwidth", "Very wide"), ("Still used", "Yes")])),
    "1936-coax-trials": (1936, 2000000, H(
        "Long-distance telephony needed many calls on one route, but existing cables could carry only a handful at a time.",
        "A coaxial tube, mostly air, carrying a broad band of frequencies with each call stacked on its own carrier frequency.",
        "Frequency-division multiplexing turned one cable into hundreds of channels, and set the pattern for all broadband transmission.",
        [("1936", "First long-haul coax trials between US cities"),
         ("1930s", "240 simultaneous calls demonstrated"),
         ("1940s", "Coax routes span the United States"),
         ("1950s", "Extended to television distribution"),
         ("today", "Superseded by fibre for long haul")],
        [("Capacity", "~240 calls"), ("Dielectric", "Mostly air"),
         ("Technique", "Frequency multiplexing"), ("Still used", "No")])),
    "1956-tat1": (1956, 2000000, H(
        "You could telegraph across the Atlantic since 1866, but a voice call still had to go by unreliable shortwave radio.",
        "A coaxial submarine cable with vacuum-tube amplifiers spliced into it every 70 km, built to run unattended on the seabed for 20 years.",
        "It began the era of intercontinental telephony, and proved that active electronics could survive decades under the ocean.",
        [("1956", "TAT-1 enters service — 36 simultaneous calls"),
         ("1956", "Demand immediately exceeds capacity"),
         ("1960s", "Successive TAT cables add capacity"),
         ("1978", "TAT-1 retired after 22 years"),
         ("1988", "TAT-8 makes the route optical")],
        [("Capacity", "36 calls"), ("Length", "3 600 km"),
         ("Repeaters", "Every ~70 km"), ("Still used", "No — retired")])),
    "1966-fiber-theory": (1966, 1000000000, H(
        "Glass fibre could carry light, but so badly that the signal died within metres. Everyone assumed glass was simply too lossy.",
        "Charles Kao showed the loss was not the glass itself but the impurities in it — make the silica pure enough and light could travel kilometres.",
        "It won him a Nobel Prize and created the entire optical industry. Essentially all internet traffic now travels this way.",
        [("1966", "Kao and Hockham publish the low-loss fibre paper"),
         ("1970", "Corning produces fibre meeting Kao's target"),
         ("1977", "First live telephone traffic over fibre"),
         ("2009", "Kao awarded the Nobel Prize in Physics"),
         ("today", "The backbone of the global internet")],
        [("Signal", "Guided light"), ("Core", "Ultra-pure silica"),
         ("Loss target", "20 dB/km"), ("Still used", "Yes — foundational")])),
    "1977-first-fiber": (1977, 45000000, H(
        "Kao's theory was proven in the lab, but no telephone company had risked real customer traffic on strands of glass.",
        "A working fibre link carrying live telephone calls under the streets of Chicago, with lasers at one end and photodiodes at the other.",
        "Once it worked in the field, copper's days as a long-distance medium were numbered.",
        [("1975", "First trials of fibre in telephone networks"),
         ("1977", "Live traffic carried commercially in Chicago"),
         ("1980s", "Fibre replaces copper trunk routes"),
         ("1988", "First transatlantic fibre cable"),
         ("today", "Fibre reaches individual homes")],
        [("Speed", "45 Mb/s"), ("Fibre type", "Multimode"),
         ("Source", "LED / laser"), ("Still used", "Superseded")])),
    "1988-tat8": (1988, 280000000, H(
        "Transatlantic copper cables were saturated, and each new one added only a few thousand calls at enormous cost.",
        "Three pairs of single-mode fibre on the ocean floor, with optical repeaters powered by a copper conductor in the same cable.",
        "Capacity jumped from thousands of calls to tens of thousands overnight, and the modern internet became economically possible.",
        [("1988", "TAT-8 enters service — 40 000 calls"),
         ("1988", "First transatlantic fibre-optic cable"),
         ("1990s", "Optical amplifiers remove the need for regeneration"),
         ("2002", "TAT-8 retired"),
         ("today", "Hundreds of fibre cables cross the oceans")],
        [("Capacity", "40 000 calls"), ("Speed", "280 Mb/s"),
         ("Fibre pairs", "3"), ("Still used", "No — retired")])),
    "1990-10baset": (1990, 10000000, H(
        "Coaxial Ethernet put every machine on one shared wire, so a single break or loose connector took down the entire office.",
        "Give every machine its own twisted-pair cable back to a central hub, using the cheap wiring the building already had for telephones.",
        "This is the moment Ethernet took its modern shape. The RJ45 socket on your wall descends directly from it.",
        [("1990", "Ratified as IEEE 802.3i"),
         ("1990s", "Hubs give way to switches"),
         ("1995", "Fast Ethernet raises it to 100 Mb/s"),
         ("1999", "Gigabit Ethernet over copper arrives"),
         ("today", "The universal wired network")],
        [("Speed", "10 Mb/s"), ("Max length", "100 m"),
         ("Topology", "Star"), ("Still used", "Evolved")])),
    "1991-568-cat5": (1991, 100000000, H(
        "Every vendor wired buildings differently, so moving a desk could mean rewiring, and nothing was guaranteed to interoperate.",
        "A single structured cabling standard defining categories, pinouts and test limits, so any compliant cable works with any compliant device.",
        "It made building wiring a commodity. The reason a network cable from any shop simply works is this standard.",
        [("1991", "TIA/EIA-568 published"),
         ("1995", "Category 5 formally specified"),
         ("2001", "Cat5e improves crosstalk performance"),
         ("2002", "Cat6 supersedes it"),
         ("today", "The framework all building cabling follows")],
        [("Speed", "100 Mb/s"), ("Max length", "100 m"),
         ("Pairs", "4"), ("Still used", "Superseded by Cat6")])),
    "1995-fast-ethernet": (1995, 100000000, H(
        "Ten megabits stopped being enough as networks filled with graphics, shared files and early multimedia.",
        "Tighter twist rates and smarter encoding pushed the same four-pair cable ten times faster without rewiring the building.",
        "It established the pattern Ethernet has followed ever since: keep the cable and the socket, change the silicon.",
        [("1995", "100BASE-TX standardised as IEEE 802.3u"),
         ("late 1990s", "Becomes the default desktop speed"),
         ("1999", "Gigabit Ethernet standardised"),
         ("2006", "10 Gb/s over copper arrives"),
         ("today", "Superseded but still widely present")],
        [("Speed", "100 Mb/s"), ("Max length", "100 m"),
         ("Pairs used", "2 of 4"), ("Still used", "Legacy")])),
    "1996-usb1": (1996, 12000000, H(
        "The back of a PC held a serial port, a parallel port, PS/2 sockets and a game port — each incompatible, most needing a reboot to use.",
        "One connector for everything, with power in the cable, automatic detection of what you plugged in, and no reboot required.",
        "It became the most widely deployed connector in history, and quietly killed every port it replaced.",
        [("1996", "USB 1.0 released"),
         ("1998", "The iMac ships USB-only and forces adoption"),
         ("2000", "USB 2.0 reaches 480 Mb/s"),
         ("2008", "USB 3.0 adds SuperSpeed lanes"),
         ("today", "Billions of ports in use")],
        [("Speed", "12 Mb/s"), ("Max length", "5 m"),
         ("Power", "2.5 W"), ("Still used", "Evolved")])),
    "1997-docsis1": (1997, 40000000, H(
        "Cable TV reached most homes but only sent signal one way, while internet access meant tying up a phone line at 56 kb/s.",
        "A standard for two-way IP data over the existing television coax, using spare frequency channels above and below the TV bands.",
        "It brought always-on broadband to millions of homes without laying a single new cable.",
        [("1997", "DOCSIS 1.0 published"),
         ("2001", "DOCSIS 2.0 improves upstream capacity"),
         ("2006", "DOCSIS 3.0 bonds channels for 100 Mb/s+"),
         ("2017", "DOCSIS 3.1 reaches gigabit speeds"),
         ("today", "Still serves a large share of home broadband")],
        [("Speed", "40 Mb/s down"), ("Medium", "TV coax"),
         ("Connector", "F-type"), ("Still used", "Yes — evolved")])),
    "2002-hdmi1": (2002, 4900000000, H(
        "A home cinema needed separate cables for video and audio, and the move to digital screens had produced a mess of incompatible connectors.",
        "One connector carrying digital video, multichannel audio and device control together, with content protection built in.",
        "It became the single connector on the back of every television, and made the AV receiver's cable spaghetti largely disappear.",
        [("2002", "HDMI 1.0 released"),
         ("2006", "Adopted across televisions and consoles"),
         ("2009", "HDMI 1.4 adds ethernet and audio return"),
         ("2017", "HDMI 2.1 supports 8K and 120 Hz"),
         ("today", "Universal on televisions")],
        [("Bandwidth", "4.9 Gb/s (v1.0)"), ("Pins", "19"),
         ("Carries", "Video + audio + control"), ("Still used", "Yes")])),
    "2008-usb3": (2008, 5000000000, H(
        "USB 2.0 at 480 Mb/s had become the bottleneck for external hard drives, which could read far faster than the cable could carry.",
        "Add two extra shielded pairs — one for each direction — so data flows both ways at once at 5 Gb/s, while staying backwards compatible.",
        "It kept USB competitive against FireWire and eSATA, and set up the lane architecture that USB-C and USB4 would inherit.",
        [("2008", "USB 3.0 specification released"),
         ("2010", "First consumer devices ship"),
         ("2013", "USB 3.1 doubles it to 10 Gb/s"),
         ("2017", "USB 3.2 reaches 20 Gb/s over USB-C"),
         ("today", "Folded into the USB4 family")],
        [("Speed", "5 Gb/s"), ("Max length", "3 m"),
         ("Pairs", "2 SuperSpeed + 1 USB 2.0"), ("Still used", "Yes")])),
    "2014-usbc": (2014, 40000000000, H(
        "USB plugs only went in one way, came in five incompatible shapes, and could not carry enough power to charge a laptop.",
        "A small reversible connector with 24 mirrored contacts, up to 100 W of power, and a chip in the cable declaring its own capabilities.",
        "It is becoming the single connector for nearly everything — and it introduced most people to the idea that a cable can contain a computer.",
        [("2014", "USB Type-C specification published"),
         ("2015", "First laptops and phones adopt it"),
         ("2016", "Thunderbolt 3 adopts the same connector"),
         ("2021", "USB PD reaches 240 W"),
         ("today", "Converging on one universal port")],
        [("Speed", "up to 40 Gb/s"), ("Power", "up to 240 W"),
         ("Contacts", "24"), ("Still used", "Yes — current")])),
    "2017-8023bs": (2017, 400000000000, H(
        "Data centres and cloud providers were exhausting 100 Gb/s links faster than anyone had forecast.",
        "Run eight parallel optical lanes at 50 Gb/s each, using multi-level signalling to squeeze more bits into every pulse of light.",
        "It set the speed of the modern cloud: the traffic between data centres largely rides on links like these.",
        [("2017", "IEEE 802.3bs ratified for 200G and 400G"),
         ("2018", "First 400G equipment ships"),
         ("2020s", "400G becomes standard between data centres"),
         ("2022", "800G products arrive"),
         ("today", "1.6T under development")],
        [("Speed", "400 Gb/s"), ("Lanes", "8 × 50 Gb/s"),
         ("Connector", "MPO/MTP"), ("Still used", "Yes — current")])),
    "2020-800g": (2020, 800000000000, H(
        "Fibre routes were full, and digging new ones across oceans and continents costs a fortune.",
        "Encode data in the light's phase and polarisation as well as its brightness, then use a DSP to undo the distortion of 1 000 km of glass.",
        "Coherent optics multiplied the capacity of cables already in the ground — the cheapest possible way to add bandwidth.",
        [("2020", "800G coherent systems begin deployment"),
         ("2020s", "Coherent DSPs move to 3 nm silicon"),
         ("2022", "800G becomes commercially widespread"),
         ("2024", "1.6T coherent demonstrated"),
         ("today", "Standard for long-haul and subsea")],
        [("Speed", "800 Gb/s per wavelength"), ("Technique", "Coherent DWDM"),
         ("Reach", "1 000 km+"), ("Still used", "Yes — current")])),
    "2024-eu-usbc": (2024, 40000000000, H(
        "Every phone brand used a different charger, generating an estimated 11 000 tonnes of discarded cables and chargers a year in the EU.",
        "Legislation: from the end of 2024, most portable electronics sold in the EU must charge over USB-C.",
        "A rare case of regulation settling a standards war outright. Apple moved the iPhone to USB-C the year before it took effect.",
        [("2022", "EU adopts the common charger directive"),
         ("2023", "iPhone 15 switches to USB-C ahead of the deadline"),
         ("2024", "Rules apply to phones, tablets and cameras"),
         ("2026", "Extends to laptops"),
         ("today", "One charger for nearly everything")],
        [("Mandate", "USB-C on most devices"), ("Region", "European Union"),
         ("Waste saved", "~11 000 t/year"), ("Still used", "Yes — in force")])),
    "2020s-self-healing": (2026, 1000000000, H(
        "A cable's insulation is its weakest point: one nick from a chair leg or a door hinge and the cable is scrap.",
        "Insulation containing microcapsules of healing agent, or polymers whose bonds re-form when cut faces touch — so damage repairs itself.",
        "Still largely in the laboratory, but it points at cables that report their own health and outlive the devices they connect.",
        [("2010s", "Self-healing polymers demonstrated in labs"),
         ("2018", "Liquid-metal conductors that reflow after cutting"),
         ("2020s", "Microcapsule insulation reaches prototypes"),
         ("2020s", "Health-monitoring ICs added to cable assemblies"),
         ("future", "Aiming at aerospace and undersea use")],
        [("Status", "Emerging"), ("Mechanism", "Microcapsules / reversible bonds"),
         ("Target", "Aerospace, subsea"), ("Still used", "Not yet mainstream")])),
}


def main():
    eras = json.load(open(ERA_PATH))
    by_id = {e["id"]: e for e in eras}

    # attach history + bitrate + sortYear to the existing exhibits
    for eid, (sort_year, bitrate, hist) in HISTORY.items():
        if eid not in by_id:
            print(f"  !! existing era not found: {eid}")
            continue
        by_id[eid]["history"] = hist
        by_id[eid]["bitrate"] = bitrate
        by_id[eid]["sortYear"] = sort_year

    # add the new exhibits
    added = []
    for era in NEW_ERAS:
        if era["id"] in by_id:
            by_id[era["id"]].update(era)
        else:
            era.setdefault("image", f"images/eras/{era['id']}.svg")
            era.setdefault("gallery", [])
            eras.append(era)
            added.append(era["id"])

    eras.sort(key=lambda e: e.get("sortYear", 9999))

    missing = [e["id"] for e in eras if "history" not in e]
    with open(ERA_PATH, "w") as f:
        json.dump(eras, f, indent=1, ensure_ascii=False)

    print(f"total exhibits : {len(eras)}")
    print(f"newly added    : {len(added)}")
    print(f"with history   : {sum(1 for e in eras if 'history' in e)}")
    if missing:
        print(f"  !! no history: {missing}")


if __name__ == "__main__":
    main()
