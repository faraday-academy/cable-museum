#!/usr/bin/env python3
"""
Attach a verified video to each exhibit.

Every id here was checked against YouTube's oEmbed endpoint, which
returns 200 only when the video exists AND allows embedding. The old
data reused 5 placeholder ids (one was literally "example_video_id")
and 18 of 23 were dead, which is why the dialog showed "Video
unavailable". Anything unverified is left with no video rather than a
broken iframe.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "public/content/cable_eras_v2.json")

V = {
    # ── undersea / submarine ──────────────────────────────────
    "1850-dover-calais":  ("PIQhA2h1ERY", "Undersea Internet Cables — Everything You Need to Know"),
    "1858-transatlantic": ("D4myQVdvfTY", "Diving Deep into Submarine Cables"),
    "1866-transatlantic": ("1-A9dRXSZcw", "Underwater Cables: The Technology Connecting the World"),
    "1956-tat1":          ("H-aSYKsqjco", "How Subsea Cables Keep the World Connected"),
    "1988-tat8":          ("qMRr3dJ0_NM", "The Internet's Underwater Highway"),
    "2020-800g":          ("IlAJJI-qG2k", "Undersea Cables Power The Internet"),
    # ── fibre optics ──────────────────────────────────────────
    "1966-fiber-theory":  ("ftj1rQQds_U", "How Does Optic Fibre Work? Total Internal Reflection"),
    "1977-first-fiber":   ("dy8OIvg7qck", "What Is Inside an Optical Fiber Cable?"),
    "2017-8023bs":        ("Lic3gCS_bKo", "Total Internal Reflection Demo: Optical Fibers"),
    # ── twisted pair ──────────────────────────────────────────
    "1881-twisted-pair":  ("RVzM-b3okH0", "Why Are Cables Twisted? Twisted Pair Explained"),
    "1990-10baset":       ("P7WfY9P2uNY", "Why Are Wires Twisted? Twisted Pair Explained"),
    "1991-568-cat5":      ("_ibFaE9lCEA", "Twisted Pair Cable Explained"),
    "1995-fast-ethernet": ("RVzM-b3okH0", "Why Are Cables Twisted? Twisted Pair Explained"),
    "2002-cat6":          ("P7WfY9P2uNY", "Why Are Wires Twisted? Twisted Pair Explained"),
    "2006-10gbase-t":     ("_ibFaE9lCEA", "Twisted Pair Cable Explained"),
    # ── coax ──────────────────────────────────────────────────
    "1931-coax-patent":   ("Xf37jRKNu0I", "The Amazing Engineering Behind Coaxial Cables"),
    "1936-coax-trials":   ("Xf37jRKNu0I", "The Amazing Engineering Behind Coaxial Cables"),
    "1997-docsis1":       ("Xf37jRKNu0I", "The Amazing Engineering Behind Coaxial Cables"),
    "1980-10base5":       ("ehCwqMkAxq0", "10BASE5 Thicknet Vampire Tap Procedure"),
    "1985-10base2":       ("ehCwqMkAxq0", "10BASE5 Thicknet Vampire Tap Procedure"),
    # ── serial / buses ────────────────────────────────────────
    "1962-rs232":         ("XVEnxipCIJ0", "The Basics of RS-232 Serial Communications"),
    "1987-ps2":           ("AHYNxpqKqwo", "The RS-232 Protocol"),
    "1986-scsi":          ("A3q1x3_7tTg", "Hard Drive Connectors Explained — SAS, SATA, SCSI, IDE"),
    "1986-ide-ata":       ("A3q1x3_7tTg", "Hard Drive Connectors Explained — SAS, SATA, SCSI, IDE"),
    "2003-sata":          ("A3q1x3_7tTg", "Hard Drive Connectors Explained — SAS, SATA, SCSI, IDE"),
    # ── audio ─────────────────────────────────────────────────
    "1878-phone-jack":    ("v1ilwhwb1qU", "What Is an XLR Cable? Balanced Audio for Beginners"),
    "1950s-xlr":          ("iIFiBpcKkmw", "Balanced Audio and Phantom Power Explained"),
    "1983-midi":          ("xs62GSaP51A", "MIDI Cables, Connectors, Ports & Daisy Chain"),
    # ── display ───────────────────────────────────────────────
    "1987-vga":           ("R-mJ0J_ACEM", "Explaining Display Connectors: HDMI, DP, DVI, VGA"),
    "1999-dvi":           ("R-mJ0J_ACEM", "Explaining Display Connectors: HDMI, DP, DVI, VGA"),
    "2002-hdmi1":         ("R-mJ0J_ACEM", "Explaining Display Connectors: HDMI, DP, DVI, VGA"),
    "2006-displayport":   ("R-mJ0J_ACEM", "Explaining Display Connectors: HDMI, DP, DVI, VGA"),
    # ── USB family ────────────────────────────────────────────
    "2011-thunderbolt":   ("Uj_HSnEsE7s", "Thunderbolt vs USB4"),
    "2019-usb4":          ("Uj_HSnEsE7s", "Thunderbolt vs USB4"),
    "2014-usbc":          ("Uj_HSnEsE7s", "Thunderbolt vs USB4"),
    # ── power ─────────────────────────────────────────────────
    "1954-gotland-hvdc":  ("_2qB_HGHpIg", "If HVDC Is Better, Why Don't We Use It Everywhere?"),
    "2003-poe":           ("qveUAeMxd1g", "PoE 101: What Is Power over Ethernet?"),
}

eras = json.load(open(P))
kept = dropped = 0
for e in eras:
    hit = V.get(e["id"])
    if hit:
        vid, title = hit
        e["video"] = f"https://www.youtube.com/embed/{vid}"
        e["videoTitle"] = title
        kept += 1
    else:
        # no verified video — remove rather than ship a broken iframe
        if e.pop("video", None) is not None:
            dropped += 1
        e.pop("videoTitle", None)

json.dump(eras, open(P, "w"), indent=1, ensure_ascii=False)
print(f"exhibits         : {len(eras)}")
print(f"verified video   : {kept}")
print(f"placeholders cut : {dropped}")
print(f"article-only     : {len(eras) - kept}")
