import math

import pygame

from . import settings as S
from .utils import pick, rand, randint


NEEDS = {
    "log": "jump",
    "rock": "jump",
    "branch": "slide",
    "vine": "slide",
    "wide": "dash",
}


class Obstacle:
    def __init__(self, type_, x, ground_y):
        self.type = type_
        self.x = float(x)
        self.ground_y = ground_y
        self.passed = False

        if type_ == "log":
            self.w, self.h = 60, 26
            self.y = ground_y - self.h
        elif type_ == "rock":
            self.w, self.h = 38, 36
            self.y = ground_y - self.h
        elif type_ == "branch":
            self.w, self.h = 80, 22
            self.y = ground_y - 64
        elif type_ == "vine":
            self.w, self.h = 36, 70
            self.y = ground_y - 96
        elif type_ == "wide":
            self.w, self.h = 110, 30
            self.y = ground_y - self.h

    @property
    def bbox(self):
        return (self.x + 3, self.y + 3, self.w - 6, self.h - 6)

    def needs(self):
        return NEEDS[self.type]

    def update(self, dt, speed):
        self.x -= speed * dt

    def draw(self, surface):
        if self.type == "log":
            self._draw_log(surface)
        elif self.type == "rock":
            self._draw_rock(surface)
        elif self.type == "branch":
            self._draw_branch(surface)
        elif self.type == "vine":
            self._draw_vine(surface)
        elif self.type == "wide":
            self._draw_wide(surface)

    def _draw_log(self, surface):
        x, y, w, h = int(self.x), int(self.y), self.w, self.h
        pygame.draw.rect(surface, S.WOOD, (x, y, w, h))
        pygame.draw.rect(surface, S.WOOD_HIGH, (x, y, w, 6))
        pygame.draw.rect(surface, (58, 36, 16), (x + 6, y + 10, 4, 4))
        pygame.draw.rect(surface, (58, 36, 16), (x + w - 12, y + 14, 4, 4))

    def _draw_rock(self, surface):
        x, y, w, h = int(self.x), int(self.y), self.w, self.h
        points = [
            (x, y + h),
            (x + 8, y + 8),
            (x + int(w * 0.55), y),
            (x + w - 6, y + 12),
            (x + w, y + h),
        ]
        pygame.draw.polygon(surface, S.ROCK, points)
        pygame.draw.rect(surface, S.ROCK_HIGH, (x + 12, y + 10, 8, 4))

    def _draw_branch(self, surface):
        x, y, w, h = int(self.x), int(self.y), self.w, self.h
        pygame.draw.rect(surface, (61, 42, 24), (x, y + 6, w, 8))
        for i in range(5):
            pygame.draw.ellipse(surface, S.LEAF, (x + 4 + i * 15, y - 2, 18, 14))
        for i in range(3):
            pygame.draw.ellipse(surface, S.LEAF_HIGH, (x + 12 + i * 22, y + 12, 14, 8))

    def _draw_vine(self, surface):
        x, y, w, h = int(self.x), int(self.y), self.w, self.h
        pygame.draw.rect(surface, S.LEAF, (x + w // 2 - 3, y, 6, h))
        for i in range(4):
            yy = y + 10 + i * 16
            pygame.draw.ellipse(surface, S.LEAF_HIGH, (x - 2, yy - 5, 16, 10))
            pygame.draw.ellipse(surface, S.LEAF_HIGH, (x + w - 14, yy + 1, 16, 10))

    def _draw_wide(self, surface):
        x, y, w, h = int(self.x), int(self.y), self.w, self.h
        pygame.draw.rect(surface, (58, 42, 24), (x, y, w, h))
        pygame.draw.rect(surface, (90, 58, 34), (x, y, w, 5))
        for i in range(4):
            pygame.draw.rect(surface, (26, 17, 8), (x + 8 + i * 26, y + 12, 14, 4))
        warning = [
            (x + w // 2 - 8, y),
            (x + w // 2, y - 12),
            (x + w // 2 + 8, y),
        ]
        pygame.draw.polygon(surface, S.DANGER, warning)


class Spawner:
    def __init__(self, width, ground_y):
        self.width = width
        self.ground_y = ground_y
        self.cooldown = 1.4
        self.elapsed = 0.0

    def reset(self):
        self.cooldown = 1.4
        self.elapsed = 0.0

    def update(self, dt, obstacles, difficulty):
        self.elapsed += dt
        if self.elapsed < self.cooldown:
            return

        if obstacles:
            min_gap = 220 - difficulty * 8
            if obstacles[-1].x > self.width - min_gap:
                return

        roll = rand(0.0, 1.0)
        if roll < 0.42:
            type_ = pick(["log", "rock"])
        elif roll < 0.78:
            type_ = pick(["branch", "vine"])
        else:
            type_ = "wide"

        spawn_x = self.width + 40
        obstacles.append(Obstacle(type_, spawn_x, self.ground_y))

        # occasional pair to force a fast slide-then-jump or a dash
        pair_chance = min(0.35, 0.08 + difficulty * 0.025)
        if rand(0.0, 1.0) < pair_chance:
            partner = pick(["branch", "vine"]) if type_ in ("log", "rock") else "log"
            obstacles.append(Obstacle(partner, spawn_x + randint(40, 70), self.ground_y))

        self.cooldown = rand(0.85, 1.45) - min(0.55, difficulty * 0.05)
        self.elapsed = 0.0
