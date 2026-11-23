#!/usr/bin/env python3
"""THE WORLD TODAY - Monday 23 November 2026.

Renders one front-page image summing up the world's news of
23 November 2026: masthead, dotted world map with numbered pins,
and 36 numbered stories in three columns. No network access.
Writes /output/entry.png (1024x1024, under 1 MiB).
"""

import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
PAPER = (247, 243, 234)
INK = (18, 16, 14)
RED = (178, 34, 28)
GREY = (96, 90, 82)
LIGHT = (226, 219, 205)
DOT = (58, 72, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def env_int(key, default):
    try:
        return int(os.environ.get(key, default))
    except ValueError:
        return default


# Tunables (env overrides used only while choosing the final look).
# Chosen after judging 8 candidates: map 195 px, type 13/9 pt.
MAP_H = env_int("MAP_H", 195)

# ---------------------------------------------------------------- stories
# head: short headline, kept near 30 characters so it fits one line.
# body: short summary, kept near 105 characters so it fits two lines.
# lat/lon: pin position. tag: section label (kept for the record).
STORIES = [
    ("COP31 COLLAPSES IN ANTALYA",
     "UN climate talks end with no deal and no fossil-fuel mention - the longest COP ever, first failure since 2009.",
     36.90, 30.70, "CLIMATE"),
    ("IRAN HITS US BASE IN BAHRAIN",
     "Tehran says its missiles destroyed Patriot radars at a US base in Bahrain and downed a US drone over Qeshm.",
     26.20, 50.60, "WAR"),
    ("HOUTHI MISSILE AT SAUDI ARABIA",
     "The Saudi-led coalition says it intercepted a Houthi ballistic missile fired at western Saudi Arabia.",
     21.50, 39.20, "WAR"),
    ("UN TALKS ON KILLER ROBOTS GO ON",
     "Nations agree to keep negotiating curbs on lethal autonomous weapons at the UN conference in Geneva.",
     46.20, 6.10, "UN"),
    ("RUSSIAN SHIP BURNS OFF FINLAND",
     "A Russian cargo ship is still on fire in the Baltic after a drone attack, as the Ukraine war spills over.",
     60.00, 24.00, "UKRAINE"),
    ("14 MISSING AFTER KYIV STRIKE",
     "At least 14 people are missing after a Russian drone hit a residential building in the Kyiv region.",
     50.45, 30.52, "UKRAINE"),
    ("INDONESIA FACTORY FIRE HORROR",
     "Three dead and dozens missing after a blaze at a candy factory; rescuers have recovered 24 body bags.",
     -6.20, 106.80, "ASIA"),
    ("MYANMAR SLAMS ASEAN DECISION",
     "Myanmar's army-backed government calls the ASEAN decision on its status 'unfair and imbalanced'.",
     19.75, 96.10, "ASIA"),
    ("THOUSANDS MARCH IN LISBON",
     "Protesters fill Lisbon's streets as soaring living costs fuel anger across Portugal.",
     38.70, -9.10, "EUROPE"),
    ("NEPAL PM MEETS MODI IN DELHI",
     "Nepal's PM Balendra Shah meets Narendra Modi in New Delhi on a two-day state visit to review ties.",
     28.60, 77.20, "ASIA"),
    ("SEOUL MINISTER QUITS OVER AI",
     "South Korea's education minister resigns after AI-assisted cheating marred the college entrance exam.",
     37.57, 126.98, "ASIA"),
    ("INDIA SMASH 720 IN WELLINGTON",
     "India declare on 720 for 9 - a record Test total in New Zealand - at the Basin Reserve in Wellington.",
     -41.29, 174.78, "SPORT"),
    ("MEXICO NABS MOST-WANTED KINGPIN",
     "'El Chapo Isidro' is captured after shoot-outs in Sinaloa leave 11 dead, Mexican authorities say.",
     24.80, -107.40, "AMERICAS"),
    ("LIVERPOOL ROUT 10-MAN UNITED",
     "Liverpool thrash Manchester United in Mauricio Pochettino's first match in charge at Old Trafford.",
     53.40, -3.00, "SPORT"),
    ("DEMOCRATS SEAL HISTORIC WIN",
     "Democrats clinch at least 258 House seats - their largest majority since 1992 - in a midterm result.",
     38.90, -77.00, "AMERICAS"),
    ("US PRESSES NVIDIA ON CHINA",
     "Washington seeks answers on Nvidia's sale of advanced chips to China, Treasury chief Bessent says.",
     37.35, -121.95, "TECH"),
    ("TANKER DRAMA IN GULF OF OMAN",
     "UKMTO reports an incident involving a tanker and military forces in the Gulf of Oman amid the war.",
     25.00, 58.00, "WAR"),
    ("SUDAN SHOOTS DOWN DRONES",
     "Sudan says it shot down drones launched from Ethiopian territory and aimed at the capital, Khartoum.",
     15.60, 32.50, "AFRICA"),
    ("JORDAN STANDS WITH BAHRAIN",
     "Jordan reaffirms solidarity with Bahrain after Iranian missile strikes hit the Gulf island state.",
     31.95, 35.93, "MIDDLE EAST"),
    ("CALL TO END ICE AFTER ARRESTS",
     "A US official calls for ICE to be abolished after masked agents detained two people at Seattle airport.",
     47.60, -122.30, "AMERICAS"),
    ("GEORGIA MAN FUNDED ISIS",
     "A Georgia man is charged with sending more than $26,000 to ISIS and obstructing justice.",
     32.08, -81.09, "AMERICAS"),
    ("ZELENSKIY: 165 MISSILES IN WEEK",
     "Russia fired 165 missiles in a single week, Zelenskiy says, pressing allies over Patriot delays.",
     50.85, 4.35, "UKRAINE"),
    ("EISENKOT SLAMS SETTLER ATTACKS",
     "Israel's defence minister denounces settler violence in the West Bank as 'an act of Jewish terrorism'.",
     31.90, 35.20, "MIDDLE EAST"),
    ("GERMANY TESTS SUICIDE DRONES",
     "Germany's army begins testing suicide drones and an AI targeting tool, its commanders confirm.",
     52.52, 13.40, "EUROPE"),
    ("UK UNVEILS NEW RUSSIA SANCTIONS",
     "London announces fresh sanctions on Moscow, insisting Ukraine 'has not been abandoned' at the table.",
     51.50, -0.13, "EUROPE"),
    ("DELTA GROUNDS THOUSANDS",
     "Delta Air Lines grounds thousands of US flights after a system malfunction ripples through its network.",
     33.75, -84.39, "AMERICAS"),
    ("24 KILLED IN SOUTH SUDAN ATTACK",
     "SPLA-IO forces kill 24 civilians in an attack in South Sudan, officials report.",
     4.85, 31.60, "AFRICA"),
    ("FIGHTING HITS CONGO EBOLA FIGHT",
     "The WHO warns that fighting near the Ebola outbreak area in Congo is disrupting the response effort.",
     -4.30, 15.30, "AFRICA"),
    ("POLAND: RUSSIA TARGETED RAPPER",
     "Warsaw says Russia allegedly tried twice to kill a Ukrainian-American rapper on Polish soil.",
     52.23, 21.01, "EUROPE"),
    ("PAKISTAN HOPES FOR US-IRAN DEAL",
     "Pakistan's foreign minister says he hopes for a US-Iran deal but warns against a prolonged war.",
     33.68, 73.05, "ASIA"),
    ("SHAH'S RS 4,000-CRORE PUSH",
     "Amit Shah launches roads and power projects worth Rs 4,000 crore in Arunachal Pradesh.",
     28.20, 94.70, "INDIA"),
    ("IFFI HOSTS BRICS ROUNDTABLE",
     "The film festival in Goa hosts a BRICS roundtable to strengthen industry partnerships.",
     15.30, 74.10, "CULTURE"),
    ("BJP MP WADKUTE DIES IN DELHI",
     "Rajya Sabha MP Ramrao Wadkute dies of a cardiac arrest in the capital, colleagues confirm.",
     28.60, 77.20, "INDIA"),
    ("INDIA, BULGARIA TALK IMEC",
     "New Delhi and Sofia discuss bilateral ties, the IMEC corridor and the Black Sea situation.",
     42.70, 23.30, "EUROPE"),
    ("PAOLO BULGARI DIES, AGED 89",
     "The Italian jeweller and businessman Paolo Bulgari has died in Rome, his family says.",
     41.90, 12.50, "EUROPE"),
    ("FERRARI FURY AT VEGAS CRASH",
     "Ferrari call the Hamilton-Leclerc collision in Las Vegas 'completely unacceptable', the boss says.",
     36.17, -115.14, "SPORT"),
]

# ------------------------------------------------------- coarse world land
# Each entry: (row, col_start, col_end) on a 96 x 44 grid.
# lon = col * 3.75 - 180 ; lat = 83 - row * 3.25.
LAND = [
    (0, 20, 26), (0, 78, 82),
    (1, 18, 27), (1, 34, 40), (1, 58, 66), (1, 80, 86),
    (2, 16, 28), (2, 35, 41), (2, 50, 54), (2, 56, 88),
    (3, 14, 30), (3, 36, 41), (3, 49, 56), (3, 56, 90),
    (4, 4, 10), (4, 12, 31), (4, 37, 41), (4, 49, 56), (4, 56, 91),
    (5, 3, 10), (5, 12, 31), (5, 38, 41), (5, 41, 43), (5, 49, 56), (5, 56, 91),
    (6, 3, 10), (6, 12, 31), (6, 38, 40), (6, 49, 55), (6, 56, 90),
    (7, 4, 9), (7, 13, 31), (7, 46, 48), (7, 49, 55), (7, 56, 89),
    (8, 6, 8), (8, 14, 30), (8, 46, 48), (8, 48, 57), (8, 57, 88),
    (9, 14, 30), (9, 46, 48), (9, 47, 58), (9, 58, 87),
    (10, 14, 30), (10, 45, 47), (10, 47, 58), (10, 68, 84),
    (11, 14, 29), (11, 45, 47), (11, 47, 58), (11, 57, 63), (11, 68, 85), (11, 82, 86),
    (12, 15, 29), (12, 44, 46), (12, 48, 58), (12, 57, 63), (12, 68, 85), (12, 83, 86),
    (13, 15, 28), (13, 44, 46), (13, 50, 55), (13, 57, 63), (13, 66, 70), (13, 68, 84),
    (14, 16, 27), (14, 44, 60), (14, 57, 63), (14, 66, 70), (14, 68, 83),
    (15, 16, 26), (15, 44, 60), (15, 58, 63), (15, 66, 69), (15, 68, 82),
    (16, 17, 25), (16, 44, 60), (16, 58, 63), (16, 66, 69), (16, 73, 77), (16, 68, 82),
    (17, 17, 25), (17, 44, 60), (17, 59, 63), (17, 66, 69), (17, 73, 77), (17, 68, 81),
    (18, 18, 24), (18, 45, 59), (18, 59, 62), (18, 66, 68), (18, 73, 76), (18, 68, 80),
    (19, 20, 24), (19, 45, 59), (19, 59, 62), (19, 66, 68), (19, 73, 76), (19, 74, 78),
    (20, 23, 27), (20, 27, 38), (20, 46, 58), (20, 60, 62), (20, 66, 67), (20, 73, 76), (20, 74, 84),
    (21, 24, 27), (21, 27, 38), (21, 46, 58), (21, 60, 61), (21, 73, 75), (21, 74, 82),
    (22, 25, 27), (22, 27, 38), (22, 46, 58), (22, 74, 80),
    (23, 26, 27), (23, 28, 38), (23, 46, 58), (23, 75, 79),
    (24, 28, 37), (24, 47, 58),
    (25, 28, 36), (25, 47, 57),
    (26, 28, 35), (26, 48, 57), (26, 78, 86),
    (27, 29, 35), (27, 48, 56), (27, 78, 87),
    (28, 29, 34), (28, 50, 56), (28, 59, 61), (28, 78, 87),
    (29, 29, 34), (29, 50, 56), (29, 59, 61), (29, 78, 87),
    (30, 30, 34), (30, 50, 55), (30, 59, 60), (30, 78, 87),
    (31, 30, 33), (31, 51, 55), (31, 59, 60), (31, 79, 86),
    (32, 30, 33), (32, 51, 54), (32, 79, 86), (32, 92, 94),
    (33, 30, 32), (33, 51, 54), (33, 79, 85), (33, 92, 94),
    (34, 30, 32), (34, 52, 54), (34, 80, 84), (34, 92, 93),
    (35, 31, 32), (35, 80, 83), (35, 92, 93),
    (36, 31, 32), (37, 31, 32), (38, 31, 32), (39, 31, 32),
]


def land_cells():
    cells = set()
    for row, c0, c1 in LAND:
        for c in range(c0, c1 + 1):
            cells.add((row, c))
    return cells


def wrap(text, fnt, width, draw):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_map(draw, x0, y0, w, h, pin_xy):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 235, 226),
                   outline=GREY, width=1)
    cells = land_cells()
    step = 7
    for gy in range(y0 + 4, y0 + h - 2, step):
        for gx in range(x0 + 4, x0 + w - 2, step):
            col = int((gx - x0) / w * 96)
            row = int((gy - y0) / h * 44)
            if (row, col) in cells:
                draw.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=DOT)
    for (px, py, num) in pin_xy:
        r = 7
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        f = font("DejaVuSans-Bold.ttf", 8)
        t = str(num)
        tw = draw.textlength(t, font=f)
        draw.text((px - tw / 2, py - 5), t, font=f, fill=(255, 255, 255))


def place_pins(x0, y0, w, h):
    pts = []
    rng = random.Random(20261123)
    for i, story in enumerate(STORIES):
        _, _, lat, lon, _ = story
        px = x0 + (lon + 180.0) / 360.0 * w
        py = y0 + (83.0 - lat) / 143.0 * h
        px += rng.uniform(-4, 4)
        py += rng.uniform(-4, 4)
        pts.append([px, py, i + 1])
    for _ in range(60):
        moved = False
        for a in range(len(pts)):
            for b in range(a + 1, len(pts)):
                dx = pts[b][0] - pts[a][0]
                dy = pts[b][1] - pts[a][1]
                d = math.hypot(dx, dy)
                if d < 19 and d > 0.01:
                    push = (19 - d) / 2.0
                    ux, uy = dx / d, dy / d
                    pts[a][0] -= ux * push
                    pts[a][1] -= uy * push
                    pts[b][0] += ux * push
                    pts[b][1] += uy * push
                    moved = True
        if not moved:
            break
    out = []
    for px, py, num in pts:
        px = max(x0 + 9, min(x0 + w - 9, px))
        py = max(y0 + 9, min(y0 + h - 9, py))
        out.append((px, py, num))
    return out


def story_lines(draw, story, col_w, head_pt, body_pt):
    head_f = font("DejaVuSerif-Bold.ttf", head_pt)
    body_f = font("DejaVuSans.ttf", body_pt)
    head = wrap(story[0], head_f, col_w - 30, draw)[:2]
    body = wrap(story[1], body_f, col_w - 30, draw)[:2]
    return head, body


def story_height(draw, story, col_w, head_pt, body_pt):
    head, body = story_lines(draw, story, col_w, head_pt, body_pt)
    return len(head) * (head_pt + 3) + len(body) * (body_pt + 3) + 8


def draw_story(draw, story, num, x, y, col_w, head_pt, body_pt):
    head_f = font("DejaVuSerif-Bold.ttf", head_pt)
    body_f = font("DejaVuSans.ttf", body_pt)
    # red number badge
    draw.ellipse([x, y + 1, x + 17, y + 18], fill=RED)
    tf = font("DejaVuSans-Bold.ttf", 9)
    t = str(num)
    tw = draw.textlength(t, font=tf)
    draw.text((x + 8.5 - tw / 2, y + 4), t, font=tf, fill=(255, 255, 255))
    tx = x + 24
    hy = y
    head, body = story_lines(draw, story, col_w, head_pt, body_pt)
    for line in head:
        draw.text((tx, hy), line, font=head_f, fill=INK)
        hy += head_pt + 3
    for line in body:
        draw.text((tx, hy), line, font=body_f, fill=(38, 34, 30))
        hy += body_pt + 3
    draw.line([x, hy + 2, x + col_w - 6, hy + 2], fill=LIGHT, width=1)
    return hy + 8


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # ---- masthead
    title_f = font("DejaVuSerif-Bold.ttf", 64)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=title_f)
    draw.text(((W - tw) / 2, 18), title, font=title_f, fill=INK)
    draw.line([MARGIN, 96, W - MARGIN, 96], fill=INK, width=2)
    draw.line([MARGIN, 100, W - MARGIN, 100], fill=INK, width=1)
    # ---- red date banner
    banner = "MONDAY 23 NOVEMBER 2026  •  36 STORIES FROM AROUND THE WORLD  •  MORNING EDITION"
    bf = font("DejaVuSans-Bold.ttf", 15)
    bw = draw.textlength(banner, font=bf)
    draw.rectangle([MARGIN, 108, W - MARGIN, 136], fill=RED)
    draw.text(((W - bw) / 2, 114), banner, font=bf, fill=(255, 255, 255))
    sub = "The day's news in one picture  —  COP31 collapses  •  Iran strikes a US base  •  Lisbon marches"
    sf = font("DejaVuSerif.ttf", 13)
    sw = draw.textlength(sub, font=sf)
    draw.text(((W - sw) / 2, 142), sub, font=sf, fill=GREY)
    # ---- map + columns: pick the largest (map height, type sizes) that fits
    map_x, map_y = MARGIN, 168
    map_w = W - 2 * MARGIN
    gap = 18
    col_w = (W - 2 * MARGIN - 2 * gap) // 3
    xs = [MARGIN + i * (col_w + gap) for i in range(3)]
    chosen = None
    for mh in (MAP_H, 205, 185):
        for hp, bp in [(13, 10), (13, 9), (12, 10), (12, 9)]:
            cols_top = map_y + mh + 26
            ok = True
            for ci in range(3):
                total = 0
                for si in range(ci * 12, min(ci * 12 + 12, 36)):
                    total += story_height(draw, STORIES[si], col_w, hp, bp)
                if total > 992 - cols_top:
                    ok = False
                    break
            if ok:
                chosen = (mh, hp, bp)
                break
        if chosen:
            break
    if chosen is None:
        chosen = (185, 12, 9)
    map_h, hp, bp = chosen
    pins = place_pins(map_x, map_y, map_w, map_h)
    draw_map(draw, map_x, map_y, map_w, map_h, pins)
    cap_f = font("DejaVuSans.ttf", 10)
    cap = "Each numbered pin marks where a story below took place."
    draw.text((map_x, map_y + map_h + 4), cap, font=cap_f, fill=GREY)
    # ---- columns
    cols_top = map_y + map_h + 26
    for ci in range(3):
        y = cols_top
        for si in range(ci * 12, min(ci * 12 + 12, 36)):
            y = draw_story(draw, STORIES[si], si + 1, xs[ci], y, col_w,
                           hp, bp)
    # ---- footer
    draw.line([MARGIN, 1000, W - MARGIN, 1000], fill=INK, width=1)
    ff = font("DejaVuSans.ttf", 9)
    foot = "Sources: Reuters  •  BBC  •  CNN  •  AP  •  AFP     |     Compiled Monday 23 November 2026, 00:00–01:00 UTC"
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, 1006), foot, font=ff, fill=GREY)
    return img


def main():
    out = os.environ.get("ENTRY_OUT", "/output/entry.png")
    img = render()
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
