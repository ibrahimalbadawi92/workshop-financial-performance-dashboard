# -*- coding: utf-8 -*-
"""
Single source of truth for every color used in the app -- UI chrome and
chart marks alike. This is the neutral Portfolio-demo palette: navy/slate
chrome with a teal accent (no gold/yellow accent, and not the exact
navy+gold pairing of any particular brand). The categorical chart-mark set
was validated with the dataviz skill's CVD/contrast checker (all checks
pass: lightness band, chroma floor, CVD separation, normal-vision floor,
contrast vs. surface).
"""

# --- Brand chrome (UI surfaces, never chart data marks) --------------------
BRAND_NAVY = "#153F5C"
BRAND_NAVY_DEEP = "#0E2C41"
BRAND_NAVY_TINT = "#E8EEF2"
BRAND_TEAL = "#0E8C72"
BRAND_TEAL_DEEP = "#0B6D5A"
WHITE = "#FFFFFF"
PAGE_BG = "#F6F8F9"

INK_PRIMARY = "#161B22"
INK_SECONDARY = "#52514E"
INK_MUTED = "#898781"
BORDER = "rgba(21,63,92,0.12)"
GRIDLINE = "#E6E8EC"

# --- Chart data marks (validated categorical set, <=3 series) --------------
CHART_NAVY = "#1B5C8C"        # slot 1: primary / actual / base / revenue
CHART_TEAL = "#0E8C72"        # slot 2: secondary / scenario / comparison / expenses
CHART_TERRACOTTA = "#C4622A"  # slot 3: tertiary (e.g. a secondary revenue category) -- always direct-labeled

# --- Sequential ramp (magnitude bars, heatmap) -- one hue, light->dark -----
SEQUENTIAL_BLUE = {
    100: "#cde2fb", 150: "#b7d3f6", 200: "#9ec5f4", 250: "#86b6ef",
    300: "#6da7ec", 350: "#5598e7", 400: "#3987e5", 450: "#2a78d6",
    500: "#256abf", 550: "#1c5cab", 600: "#184f95", 650: "#104281",
    700: "#0d366b",
}
SEQUENTIAL_DEFAULT_MARK = SEQUENTIAL_BLUE[600]

# --- Status (reserved -- profit/loss movement only, never generic series) --
STATUS_GOOD = "#0ca30c"      # improvement / narrowing gap / positive movement
STATUS_CRITICAL = "#d03b3b"  # deterioration / widening gap / negative movement
STATUS_WARNING = "#fab219"

# --- Neutral delta ink (revenue/expense change -- factual, not judged) -----
NEUTRAL_DELTA = INK_SECONDARY

# Reserved, fixed status color for a data-quality uncertainty state: an
# apparent expense decrease that is actually an account missing from the
# comparison year's dataset. Deliberately a cool slate gray -- distinct from
# both the warm INK_MUTED text color and from STATUS_GOOD green -- so it
# never reads as "confirmed improvement". ~4.6:1 contrast on white; always
# paired with a label/tooltip, never color alone.
STATUS_NOT_PRESENT = "#6B7280"
