#!/usr/bin/env python3
"""Render a professional BayAreaLa8s course marketing PNG (BayServe style)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "course-production-grade-microservices-marketing.png"
OUT_SQUARE = ROOT / "docs" / "course-production-grade-microservices-marketing-square.png"

# BayAreaLa8s brand (aligned with BayServe enterprise creatives)
NAVY = (10, 31, 51)
NAVY_2 = (14, 48, 74)
TEAL = (13, 143, 173)
TEAL_DK = (8, 110, 135)
GOLD = (201, 162, 39)
GOLD_LT = (232, 201, 98)
WHITE = (248, 251, 253)
MUTED = (186, 204, 214)
CARD = (18, 52, 78)
CARD_EDGE = (36, 92, 118)

W, H = 1920, 1080

CAPABILITIES = [
    ("Enterprise Architecture", "Bounded contexts, C4, API contracts"),
    ("Production Deployment", "ECS Fargate · ALB · VPC · Terraform"),
    ("Event-Driven Systems", "EventBridge async flows & sagas"),
    ("Security by Design", "IAM least privilege · JWT · network controls"),
    ("CI/CD & Delivery", "GitHub Actions → ECR → rolling deploys"),
    ("Observability", "CloudWatch · tracing · operational runbooks"),
    ("Resilience & DR", "Retries, ownership, failure modes in production"),
    ("FinOps & Cost Control", "Idle detection · start/stop lab hygiene"),
    ("Hands-On Capstones", "E-commerce · Banking · SaaS · Idle Cost Advisor"),
    ("Multi-Stack Ready", "FastAPI · Spring Boot · NestJS patterns"),
    ("Student → Professional", "Portfolio demos employers recognize"),
    ("Enterprise Upskilling", "Team-ready platform engineering outcomes"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Neue.ttc",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def draw_chevron_shield(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
    s = scale
    draw.polygon(
        [
            (x + 8 * s, y + 2 * s),
            (x + 56 * s, y + 2 * s),
            (x + 64 * s, y + 28 * s),
            (x + 0 * s, y + 28 * s),
        ],
        fill=GOLD,
    )
    draw.polygon(
        [
            (x + 4 * s, y + 30 * s),
            (x + 60 * s, y + 30 * s),
            (x + 68 * s, y + 56 * s),
            (x - 4 * s, y + 56 * s),
        ],
        fill=TEAL,
    )
    draw.polygon(
        [
            (x + 0 * s, y + 58 * s),
            (x + 64 * s, y + 58 * s),
            (x + 70 * s, y + 80 * s),
            (x + 32 * s, y + 88 * s),
            (x - 6 * s, y + 80 * s),
        ],
        fill=(6, 28, 46),
    )


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill,
    outline=None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def paint_backdrop(w: int, h: int) -> Image.Image:
    img = Image.new("RGB", (w, h), NAVY)
    draw = ImageDraw.Draw(img)

    for y in range(h):
        t = y / h
        r = int(NAVY[0] * (1 - t) + NAVY_2[0] * t)
        g = int(NAVY[1] * (1 - t) + (NAVY_2[1] + 20) * t)
        b = int(NAVY[2] * (1 - t) + TEAL_DK[2] * t * 0.55)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((w * 0.55, -120, w * 1.15, h * 0.72), fill=(13, 143, 173, 55))
    gdraw.ellipse((-200, h * 0.55, w * 0.4, h * 1.2), fill=(201, 162, 39, 28))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Microservice mesh (right side)
    cx, cy = int(w * 0.78), int(h * 0.36)
    for i in range(18):
        ang = i * (math.pi * 2 / 18)
        rr = 190 + (i % 4) * 26
        x = int(cx + math.cos(ang) * rr)
        y = int(cy + math.sin(ang) * rr)
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=TEAL)
    for i in range(0, 18, 2):
        ang1 = i * (math.pi * 2 / 18)
        ang2 = (i + 3) * (math.pi * 2 / 18)
        rr = 230
        p1 = (int(cx + math.cos(ang1) * rr), int(cy + math.sin(ang1) * rr))
        p2 = (int(cx + math.cos(ang2) * rr), int(cy + math.sin(ang2) * rr))
        draw.line([p1, p2], fill=(36, 110, 130), width=1)

    # Central hub
    draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=GOLD, outline=GOLD_LT, width=2)
    return img


def render_wide() -> Image.Image:
    img = paint_backdrop(W, H)
    draw = ImageDraw.Draw(img)

    title = font(58, bold=True)
    subtitle = font(26, bold=False)
    body = font(22, bold=False)
    small = font(18, bold=False)
    card_title = font(21, bold=True)
    card_body = font(15, bold=False)
    ribbon = font(20, bold=True)
    eyebrow = font(20, bold=True)

    draw_chevron_shield(draw, 72, 64, scale=1.05)

    draw.text((168, 68), "BayAreaLa8s", font=eyebrow, fill=GOLD_LT)
    draw.text((168, 100), "Production-Grade Microservices", font=title, fill=WHITE)
    draw.text((168, 168), "on AWS", font=title, fill=WHITE)
    draw.rectangle((168, 248, 520, 256), fill=GOLD)
    draw.text(
        (168, 278),
        "Design · Build · Deploy · Secure · Scale · Operate",
        font=subtitle,
        fill=GOLD_LT,
    )
    draw.text(
        (168, 322),
        "The enterprise course that goes beyond “hello Docker” —\n"
        "real platform engineering for students and engineering teams.",
        font=body,
        fill=MUTED,
        spacing=8,
    )

    metrics = [
        ("Duration", "10 weeks · 72 hours\nInstructor-led / Hybrid / Self-paced"),
        ("Audience", "Engineers · Architects\nStudents · Enterprise teams"),
        ("Outcome", "Ship production platforms\nCapstone demos + AWS ops"),
    ]
    mx, my = 168, 410
    for i, (label, value) in enumerate(metrics):
        x0 = mx + i * 340
        rounded_rect(draw, (x0, my, x0 + 320, my + 118), 14, CARD, CARD_EDGE, 2)
        draw.rectangle((x0, my, x0 + 8, my + 118), fill=GOLD)
        draw.text((x0 + 22, my + 16), label, font=small, fill=GOLD_LT)
        draw.text((x0 + 22, my + 46), value, font=card_body, fill=WHITE, spacing=4)

    journey = ["Design", "Build", "Deploy", "Secure", "Observe", "CI/CD", "Capstone", "Operate"]
    jy = 550
    draw.text((168, jy), "Learning journey (lab-first)", font=small, fill=MUTED)
    jx = 168
    step_w = 168
    for i, step in enumerate(journey):
        box = (jx, jy + 28, jx + step_w, jy + 66)
        rounded_rect(draw, box, 10, (12, 60, 82), TEAL, 1)
        tw = draw.textlength(step, font=small)
        draw.text((jx + max(10, (step_w - tw) / 2), jy + 40), step, font=small, fill=WHITE)
        if i < len(journey) - 1:
            draw.text((jx + step_w + 4, jy + 38), "→", font=small, fill=GOLD)
        jx += step_w + 20

    draw.text((168, 640), "Why students and enterprises enroll", font=subtitle, fill=WHITE)
    cols = 3
    card_w, card_h = 540, 68
    gx, gy = 168, 688
    gap_x, gap_y = 20, 10
    for i, (name, desc) in enumerate(CAPABILITIES):
        col = i % cols
        row = i // cols
        x0 = gx + col * (card_w + gap_x)
        y0 = gy + row * (card_h + gap_y)
        rounded_rect(draw, (x0, y0, x0 + card_w, y0 + card_h), 12, CARD, CARD_EDGE, 1)
        draw.ellipse((x0 + 16, y0 + 26, x0 + 28, y0 + 38), fill=GOLD)
        draw.text((x0 + 44, y0 + 10), name, font=card_title, fill=WHITE)
        draw.text((x0 + 44, y0 + 38), desc, font=card_body, fill=MUTED)

    draw.rectangle((0, H - 64, W, H), fill=(6, 22, 36))
    draw.rectangle((0, H - 68, W, H - 64), fill=GOLD)
    draw.text(
        (72, H - 44),
        "BayAreaLa8s  ·  bayareala8s.com  ·  FastAPI · ECS · EventBridge · Terraform · Observability · Capstone",
        font=ribbon,
        fill=WHITE,
    )
    return img


def render_square() -> Image.Image:
    """LinkedIn / social square crop of the same brand story."""
    sw, sh = 1080, 1080
    img = paint_backdrop(sw, sh)
    draw = ImageDraw.Draw(img)

    title = font(44, bold=True)
    subtitle = font(22, bold=False)
    body = font(20, bold=False)
    small = font(17, bold=False)
    card_title = font(20, bold=True)
    card_body = font(15, bold=False)
    ribbon = font(16, bold=True)
    eyebrow = font(18, bold=True)

    draw_chevron_shield(draw, 56, 48, scale=0.95)
    draw.text((148, 52), "BayAreaLa8s", font=eyebrow, fill=GOLD_LT)
    draw.text((148, 84), "Production-Grade", font=title, fill=WHITE)
    draw.text((148, 136), "Microservices on AWS", font=title, fill=WHITE)
    draw.rectangle((148, 200, 420, 206), fill=GOLD)
    draw.text(
        (56, 230),
        "Design · Build · Deploy · Secure · Scale · Operate",
        font=subtitle,
        fill=GOLD_LT,
    )
    draw.text(
        (56, 272),
        "Enterprise platform engineering for students\nand engineering teams — not toy demos.",
        font=body,
        fill=MUTED,
        spacing=6,
    )

    pills = [
        ("10 weeks", "72 hours"),
        ("Labs-first", "AWS + Compose"),
        ("4 Capstones", "Hire-ready demos"),
    ]
    for i, (a, b) in enumerate(pills):
        x0 = 56 + i * 330
        rounded_rect(draw, (x0, 360, x0 + 310, 360 + 92), 14, CARD, CARD_EDGE, 2)
        draw.rectangle((x0, 360, x0 + 8, 452), fill=GOLD)
        draw.text((x0 + 22, 376), a, font=card_title, fill=WHITE)
        draw.text((x0 + 22, 410), b, font=small, fill=MUTED)

    highlights = CAPABILITIES[:6]
    for i, (name, desc) in enumerate(highlights):
        row = i // 2
        col = i % 2
        x0 = 56 + col * 500
        y0 = 480 + row * 110
        rounded_rect(draw, (x0, y0, x0 + 480, y0 + 96), 12, CARD, CARD_EDGE, 1)
        draw.ellipse((x0 + 18, y0 + 40, x0 + 32, y0 + 54), fill=GOLD)
        draw.text((x0 + 48, y0 + 22), name, font=card_title, fill=WHITE)
        draw.text((x0 + 48, y0 + 54), desc, font=card_body, fill=MUTED)

    draw.rectangle((0, sh - 56, sw, sh), fill=(6, 22, 36))
    draw.rectangle((0, sh - 60, sw, sh - 56), fill=GOLD)
    draw.text(
        (40, sh - 38),
        "BayAreaLa8s  ·  Students & Enterprise  ·  bayareala8s.com",
        font=ribbon,
        fill=WHITE,
    )
    return img


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wide = render_wide()
    wide.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT}")

    square = render_square()
    square.save(OUT_SQUARE, "PNG", optimize=True)
    print(f"Wrote {OUT_SQUARE}")


if __name__ == "__main__":
    main()
