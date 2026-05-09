import math

import pygame

from . import settings as S


class Tiger:
    def __init__(self, ground_y, gap=S.TIGER_BASE_GAP):
        self.ground_y = ground_y
        self.gap = gap
        self.base_gap = gap
        self.run_time = 0.0
        self.w = 96
        self.h = 56

    def reset(self):
        self.gap = self.base_gap
        self.run_time = 0.0

    def hit_player(self):
        """Tiger surges forward when the player is hit."""
        self.gap = max(S.TIGER_CATCH_GAP, self.gap - S.HIT_TIGER_PUSH)

    def update(self, dt, player_x):
        self.run_time += dt
        # tiger drifts back when player is doing well
        self.gap = min(self.base_gap, self.gap + S.TIGER_RECOVERY * dt)

    @property
    def caught_player(self):
        return self.gap <= S.TIGER_CATCH_GAP + 0.5

    def get_x(self, player_x):
        return player_x - self.gap

    def draw(self, surface, player_x):
        x = int(self.get_x(player_x))
        y = int(self.ground_y - self.h)
        phase = math.sin(self.run_time * 16)

        # legs
        leg_top = y + self.h - 14
        pygame.draw.rect(surface, S.TIGER_DARK, (x + 14, leg_top, 8, 14 + int(phase * 2)))
        pygame.draw.rect(surface, S.TIGER_DARK, (x + 30, leg_top, 8, 14 - int(phase * 2)))
        pygame.draw.rect(surface, S.TIGER_DARK, (x + 60, leg_top, 8, 14 + int(phase * 2)))
        pygame.draw.rect(surface, S.TIGER_DARK, (x + 76, leg_top, 8, 14 - int(phase * 2)))

        # body
        body_rect = pygame.Rect(x + 8, y + 18, self.w - 12, self.h - 28)
        pygame.draw.ellipse(surface, S.TIGER_ORANGE, body_rect)

        # belly
        belly_rect = pygame.Rect(x + 14, y + 30, self.w - 22, self.h - 38)
        pygame.draw.ellipse(surface, S.TIGER_BELLY, belly_rect)

        # stripes
        for i in range(5):
            sx = x + 14 + i * 14
            pygame.draw.rect(surface, S.TIGER_DARK, (sx, y + 20, 4, self.h - 32))

        # head + jaw
        head_rect = pygame.Rect(x + self.w - 30, y + 8, 30, 28)
        pygame.draw.ellipse(surface, S.TIGER_ORANGE, head_rect)
        pygame.draw.ellipse(surface, S.TIGER_BELLY, (x + self.w - 22, y + 22, 18, 12))
        # ears
        pygame.draw.polygon(
            surface, S.TIGER_DARK,
            [(x + self.w - 26, y + 8), (x + self.w - 22, y), (x + self.w - 18, y + 8)],
        )
        pygame.draw.polygon(
            surface, S.TIGER_DARK,
            [(x + self.w - 14, y + 8), (x + self.w - 10, y), (x + self.w - 6, y + 8)],
        )
        # eye + fang
        pygame.draw.rect(surface, (255, 235, 130), (x + self.w - 14, y + 16, 4, 4))
        pygame.draw.rect(surface, (20, 8, 4), (x + self.w - 13, y + 17, 2, 2))
        pygame.draw.polygon(
            surface, (250, 245, 230),
            [(x + self.w - 6, y + 28), (x + self.w - 3, y + 28), (x + self.w - 4, y + 33)],
        )
        # tail (whips)
        tail_y = y + 22 + int(phase * 3)
        pygame.draw.rect(surface, S.TIGER_ORANGE, (x - 14, tail_y, 18, 6))
        pygame.draw.rect(surface, S.TIGER_DARK, (x - 14, tail_y, 4, 6))

    def draw_warning(self, surface, player_x, font):
        if self.gap > self.base_gap * 0.55:
            return
        intensity = 1.0 - (self.gap / (self.base_gap * 0.55))
        alpha = int(120 + intensity * 120)
        x = int(self.get_x(player_x)) + self.w // 2
        text = font.render("!", True, S.DANGER)
        text.set_alpha(alpha)
        surface.blit(text, (x - text.get_width() // 2, int(self.ground_y - self.h - 26)))
