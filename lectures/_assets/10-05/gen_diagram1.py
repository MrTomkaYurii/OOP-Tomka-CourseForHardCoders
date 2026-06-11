# -*- coding: utf-8 -*-
# Diagram 1: Hash table internal structure
from PIL import Image, ImageDraw, ImageFont

BG     = "#111413"
ACCENT = "#76c7ad"
TEXT   = "#e5e9e7"
MUTED  = "#a1aaa6"
LINE   = "#2c3531"
PANEL  = "#191e1c"
ORANGE = "#c7a276"
DARK   = "#161c1a"

W, H = 920, 420
img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)

def load(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

fb  = load("C:/Windows/Fonts/arialbd.ttf", 14)
fr  = load("C:/Windows/Fonts/arial.ttf",   13)
fs  = load("C:/Windows/Fonts/arial.ttf",   11)
ft  = load("C:/Windows/Fonts/arialbd.ttf", 16)
fh  = load("C:/Windows/Fonts/arialbd.ttf", 13)

d.text((W//2, 24), "Dictionary<K,V> — внутрішня структура (хеш-таблиця)", font=ft, fill=ACCENT, anchor="mm")

# === LEFT: Keys column ===
keys = ["P001", "P002", "P003", "P004"]
key_x, key_y0 = 60, 80
key_w, key_h = 100, 42
key_gap = 10

d.text((key_x + key_w//2, key_y0 - 14), "Ключ (K)", font=fh, fill=ACCENT, anchor="mm")

key_centers = []
for i, k in enumerate(keys):
    ky = key_y0 + i * (key_h + key_gap)
    key_centers.append(ky + key_h//2)
    d.rounded_rectangle([key_x, ky, key_x+key_w, ky+key_h], radius=5, fill=PANEL, outline=ACCENT, width=1)
    d.text((key_x + key_w//2, ky + key_h//2), f'"{k}"', font=fb, fill=ACCENT, anchor="mm")

# === MIDDLE: Hash function box ===
hash_x = 230
hash_y = key_y0 + (len(keys)*(key_h+key_gap))//2 - 35
hash_w, hash_h = 140, 70
d.rounded_rectangle([hash_x, hash_y, hash_x+hash_w, hash_y+hash_h], radius=8, fill=DARK, outline=ORANGE, width=2)
d.text((hash_x+hash_w//2, hash_y+22), "GetHashCode()", font=fb, fill=ORANGE, anchor="mm")
d.text((hash_x+hash_w//2, hash_y+40), "→ index", font=fs, fill=MUTED, anchor="mm")
d.text((hash_x+hash_w//2, hash_y+54), "% buckets", font=fs, fill=MUTED, anchor="mm")

# Arrows: keys → hash function
for ky_c in key_centers:
    d.line([(key_x + key_w, ky_c), (hash_x, hash_y + hash_h//2)], fill=LINE, width=1)
    d.polygon([(hash_x, hash_y+hash_h//2),
               (hash_x-8, hash_y+hash_h//2-4),
               (hash_x-8, hash_y+hash_h//2+4)], fill=LINE)

# === RIGHT: Buckets array ===
bucket_x = 440
bucket_y0 = 68
bucket_w, bucket_h = 160, 42
bucket_gap = 10
n_buckets = 6

d.text((bucket_x + bucket_w//2, bucket_y0 - 14), "Масив бакетів", font=fh, fill=TEXT, anchor="mm")

# index labels
idx_x = bucket_x - 28
for i in range(n_buckets):
    by = bucket_y0 + i*(bucket_h+bucket_gap)
    d.text((idx_x, by + bucket_h//2), f"[{i}]", font=fs, fill=MUTED, anchor="mm")
    shade = PANEL if i % 2 == 0 else DARK
    d.rounded_rectangle([bucket_x, by, bucket_x+bucket_w, by+bucket_h],
                         radius=4, fill=shade, outline=LINE, width=1)

# Fill some buckets with entries
occupied = {1: "P001", 3: "P002", 4: "P003", 5: "P004"}
for idx, key_val in occupied.items():
    by = bucket_y0 + idx*(bucket_h+bucket_gap)
    d.rounded_rectangle([bucket_x+2, by+2, bucket_x+bucket_w-2, by+bucket_h-2],
                         radius=3, fill="#1e2a27", outline=ACCENT, width=1)
    d.text((bucket_x+bucket_w//2, by+bucket_h//2), key_val, font=fb, fill=ACCENT, anchor="mm")

# Arrow: hash → buckets
arr_start_x = hash_x + hash_w
arr_end_x   = bucket_x - 2
arr_y       = hash_y + hash_h//2
d.line([(arr_start_x, arr_y), (arr_end_x, arr_y)], fill=ORANGE, width=2)
d.polygon([(arr_end_x, arr_y),
           (arr_end_x-8, arr_y-5),
           (arr_end_x-8, arr_y+5)], fill=ORANGE)

# === FAR RIGHT: Values ===
val_x = 680
val_y0 = bucket_y0
val_w  = 180
val_h  = bucket_h

d.text((val_x + val_w//2, val_y0 - 14), "Значення (V)", font=fh, fill=ORANGE, anchor="mm")

values_map = {
    1: ("Петренко Іван",   "кардіолог"),
    3: ("Коваль Марія",    "невролог"),
    4: ("Сидоренко Олег",  "хірург"),
    5: ("Мельник Ганна",   "терапевт"),
}

for idx, (name, spec) in values_map.items():
    by = val_y0 + idx*(bucket_h+bucket_gap)
    d.rounded_rectangle([val_x, by, val_x+val_w, by+val_h],
                         radius=4, fill=PANEL, outline=ORANGE, width=1)
    d.text((val_x + 8, by + 14), name, font=fb, fill=TEXT, anchor="lm")
    d.text((val_x + 8, by + 28), spec, font=fs, fill=MUTED, anchor="lm")

    # Arrow bucket → value
    bx_end   = bucket_x + bucket_w + 2
    val_start = val_x - 2
    arrow_y  = by + val_h//2
    d.line([(bx_end, arrow_y), (val_start, arrow_y)], fill=ORANGE, width=1)
    d.polygon([(val_start, arrow_y),
               (val_start-6, arrow_y-3),
               (val_start-6, arrow_y+3)], fill=ORANGE)

# Bottom legend
ly = H - 55
d.line([(30, ly - 10), (W-30, ly - 10)], fill=LINE, width=1)
d.text((30, ly),    "Пошук за ключем — O(1) в середньому:", font=fh, fill=ACCENT)
d.text((30, ly+18), "  1. Обчислити хеш ключа (GetHashCode)", font=fs, fill=TEXT)
d.text((30, ly+32), "  2. Знайти бакет: index = hash % bucketCount", font=fs, fill=TEXT)
d.text((420, ly+18), "  3. Повернути значення з бакету", font=fs, fill=TEXT)
d.text((420, ly+32), "  Колізії (кілька ключів в одному бакеті) — рідкісні, але існують", font=fs, fill=MUTED)

out = "C:/Users/Yurii/source/repos/OOP-Tomka-CourseForHardCoders/.claude/worktrees/ecstatic-merkle-5676fd/lectures/_assets/10-05/dictionary-hash-structure.png"
img.save(out)
print("OK:", out)
