import math
import random
import pygame

pygame.init()
W, H = 900, 860
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("LOVE YOU")
clock = pygame.time.Clock()

TEXT = "LOVE YOU"
S = 21.5                   
OX = W // 2
OY = H // 2 - 2.5 * S       
FONT_NAMES = "helveticaneue,arial,dejavusans"

# (مقیاس لایه، اندازه فونت، تعداد نقطه)
LAYERS = [
    (1.00, 15, 300),
    (0.88, 14, 270),
    (0.76, 13, 240),
    (0.64, 12, 200),
    (0.52, 11, 160),
    (0.40, 10, 120),
    (0.28, 9, 80),
]
ALPHA_LEVELS = 8

fonts, cache = {}, {}


def heart_xy(t):
    x = 16 * math.sin(t) ** 3
    y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
    return x, y


def layer_color(i):
    k = i / (len(LAYERS) - 1)
    return (255, int(95 + 85 * k), int(165 + 50 * k))


def get_text(size, level, color_idx):
    key = (size, level, color_idx)
    if key not in cache:
        if size not in fonts:
            fonts[size] = pygame.font.SysFont(FONT_NAMES, size, bold=True)
        surf = fonts[size].render(TEXT, True, layer_color(color_idx)).convert_alpha()
        surf.set_alpha(int(60 + 195 * level / (ALPHA_LEVELS - 1)))
        cache[key] = surf
    return cache[key]


def build_points():
    pts = []
    for li, (k, size, count) in enumerate(LAYERS):
        for i in range(count):
            t = i / count * 2 * math.pi + random.uniform(-0.01, 0.01)
            x, y = heart_xy(t)
            pts.append({
                "x": x * k, "y": y * k, "size": size, "layer": li,
                "base": random.uniform(0.35, 1.0),
                "phase": random.uniform(0, 6.28),
                "sx": random.uniform(0, W), "sy": random.uniform(0, H),
                "delay": random.uniform(0, 2.2),
                "jx": random.uniform(-1.5, 1.5), "jy": random.uniform(-1.5, 1.5),
            })
    return pts


def bloom(surface):
    small = pygame.transform.smoothscale(surface, (W // 5, H // 5))
    return pygame.transform.smoothscale(small, (W, H))


points = build_points()
scene = pygame.Surface((W, H))
start = pygame.time.get_ticks() / 1000

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_r: 
            points = build_points()
            start = pygame.time.get_ticks() / 1000

    now = pygame.time.get_ticks() / 1000
    t = now - start
    beat = 1 + 0.035 * max(0, math.sin(now * 3.0)) ** 4

    scene.fill((5, 4, 16))

    for p in points:
        prog = max(0.0, min(1.0, (t - p["delay"]) / 1.6))
        ease = 1 - (1 - prog) ** 3
        if ease <= 0.01:
            continue
        tx = OX + p["x"] * S * beat + p["jx"]
        ty = OY - p["y"] * S * beat + p["jy"]
        x = p["sx"] + (tx - p["sx"]) * ease
        y = p["sy"] + (ty - p["sy"]) * ease

        shimmer = 0.5 + 0.5 * math.sin(now * 2.2 + p["phase"])
        a = (0.65 * p["base"] + 0.35 * shimmer) * ease
        level = max(0, min(ALPHA_LEVELS - 1, int(a * (ALPHA_LEVELS - 1))))
        img = get_text(p["size"], level, p["layer"])
        scene.blit(img, img.get_rect(center=(x, y)))

    screen.blit(scene, (0, 0))
    screen.blit(bloom(scene), (0, 0), special_flags=pygame.BLEND_ADD)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
