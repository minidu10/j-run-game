import pygame

from . import settings as S
from .utils import rand


def _gradient_surface(width, height, top, bottom):
    surf = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (width, y))
    return surf


def _make_layer(count, width, min_h, max_h, min_w, max_w):
    return [
        {
            "x": rand(0, width),
            "h": rand(min_h, max_h),
            "w": rand(min_w, max_w),
        }
        for _ in range(count)
    ]


class Background:
    def __init__(self, width, height, ground_y):
        self.width = width
        self.height = height
        self.ground_y = ground_y

        self.scroll_far = 0.0
        self.scroll_mid = 0.0
        self.scroll_near = 0.0
        self.scroll_ground = 0.0

        span_far = width * 1.4
        span_mid = width * 1.4
        span_near = width * 1.6

        self.far_trees = _make_layer(22, span_far,  70,  130, 40, 80)
        self.mid_trees = _make_layer(16, span_mid,  110, 180, 60, 110)
        self.near_trees = _make_layer(10, span_near, 170, 260, 80, 150)
        self.tufts = [
            {"x": rand(0, span_far), "w": rand(8, 18), "h": rand(3, 7)}
            for _ in range(60)
        ]

        self.span_far = span_far
        self.span_mid = span_mid
        self.span_near = span_near

        self.sky = _gradient_surface(width, ground_y, S.SKY_TOP, S.SKY_BOT)
        self.ground_grad = _gradient_surface(width, height - ground_y, S.GROUND_TOP, S.GROUND_BOT)

    def update(self, dt, speed):
        self.scroll_far = (self.scroll_far + speed * 0.15 * dt) % self.span_far
        self.scroll_mid = (self.scroll_mid + speed * 0.35 * dt) % self.span_mid
        self.scroll_near = (self.scroll_near + speed * 0.65 * dt) % self.span_near
        self.scroll_ground = (self.scroll_ground + speed * 1.0 * dt) % self.span_far

    def draw(self, surface):
        surface.blit(self.sky, (0, 0))
        # moon
        pygame.draw.circle(surface, (245, 220, 160), (int(self.width * 0.78), int(self.ground_y * 0.32)), 22)
        pygame.draw.circle(surface, (215, 200, 150), (int(self.width * 0.78), int(self.ground_y * 0.32)), 22, 2)

        self._draw_trees(surface, self.far_trees, self.scroll_far, self.span_far, S.TREE_FAR, 0.55)
        self._draw_trees(surface, self.mid_trees, self.scroll_mid, self.span_mid, S.TREE_MID, 0.78)
        self._draw_trees(surface, self.near_trees, self.scroll_near, self.span_near, S.TREE_NEAR, 1.0)

        surface.blit(self.ground_grad, (0, self.ground_y))
        pygame.draw.line(surface, (0, 0, 0), (0, self.ground_y), (self.width, self.ground_y), 2)

        for t in self.tufts:
            x = int(t["x"] - self.scroll_ground)
            if x < -t["w"]:
                x += int(self.span_far)
            pygame.draw.rect(surface, S.GRASS, (x, self.ground_y - int(t["h"]), int(t["w"]), int(t["h"])))

    def _draw_trees(self, surface, items, scroll, span, color, scale):
        for t in items:
            x = t["x"] - scroll
            if x < -120:
                x += span
            base_y = self.ground_y
            w = t["w"] * scale
            h = t["h"] * scale
            points = [
                (x, base_y),
                (x + w / 2, base_y - h),
                (x + w, base_y),
            ]
            pygame.draw.polygon(surface, color, points)
            pygame.draw.rect(
                surface,
                (40, 26, 14),
                (x + w / 2 - 3, base_y - h * 0.15, 6, h * 0.15),
            )
