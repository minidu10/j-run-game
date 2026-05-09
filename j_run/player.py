import math

import pygame

from . import settings as S


class State:
    RUN = "run"
    JUMP = "jump"
    SLIDE = "slide"
    HURT = "hurt"


class Player:
    def __init__(self, ground_y):
        self.ground_y = ground_y
        self.x = 140.0
        self.w = 34
        self.h_run = 64
        self.h_slide = 30
        self.h = self.h_run
        self.y = ground_y - self.h
        self.vy = 0.0

        self.state = State.RUN
        self.run_time = 0.0

        self.coyote = 0.0
        self.jump_buffer = 0.0
        self.slide_timer = 0.0
        self.dash_timer = 0.0
        self.dash_cd = 0.0

        self.invuln = 0.0
        self.hurt_timer = 0.0

        self.lives = S.PLAYER_LIVES

    @property
    def bbox(self):
        pad = 4
        return (self.x + pad, self.y + pad, self.w - pad * 2, self.h - pad * 2)

    @property
    def grounded(self):
        return self.y + self.h >= self.ground_y - 0.5

    @property
    def is_invulnerable(self):
        return self.invuln > 0

    @property
    def is_dashing(self):
        return self.dash_timer > 0

    def take_hit(self):
        if self.invuln > 0:
            return False
        self.lives -= 1
        self.state = State.HURT
        self.hurt_timer = 0.35
        self.invuln = 1.1
        return True

    def update(self, dt, inputs, audio):
        self.run_time += dt
        self.coyote = max(0.0, self.coyote - dt)
        self.jump_buffer = max(0.0, self.jump_buffer - dt)
        self.invuln = max(0.0, self.invuln - dt)
        self.dash_timer = max(0.0, self.dash_timer - dt)
        self.dash_cd = max(0.0, self.dash_cd - dt)
        self.hurt_timer = max(0.0, self.hurt_timer - dt)

        if inputs.was_pressed("jump"):
            self.jump_buffer = 0.12

        if self.grounded:
            self.coyote = 0.1

        if self.jump_buffer > 0 and self.coyote > 0 and self.state != State.SLIDE:
            self.vy = S.JUMP_VELOCITY
            self.coyote = 0.0
            self.jump_buffer = 0.0
            self.state = State.JUMP
            audio.jump()

        if inputs.is_down("slide") and self.grounded and self.state != State.SLIDE:
            self._enter_slide(audio)
        if self.state == State.SLIDE:
            self.slide_timer -= dt
            if self.slide_timer <= 0 or not inputs.is_down("slide"):
                self._exit_slide()

        if inputs.was_pressed("dash") and self.dash_cd <= 0:
            self.dash_timer = S.DASH_DURATION
            self.dash_cd = S.DASH_COOLDOWN
            self.invuln = max(self.invuln, S.DASH_DURATION * 0.85)
            audio.dash()

        self.vy += S.GRAVITY * dt
        self.y += self.vy * dt
        if self.y + self.h >= self.ground_y:
            self.y = self.ground_y - self.h
            self.vy = 0.0
            if self.state == State.JUMP:
                self.state = State.RUN

        if self.hurt_timer <= 0 and self.state == State.HURT:
            self.state = State.RUN if self.grounded else State.JUMP

    def _enter_slide(self, audio):
        self.state = State.SLIDE
        self.slide_timer = S.SLIDE_DURATION
        bottom = self.y + self.h
        self.h = self.h_slide
        self.y = bottom - self.h
        audio.slide()

    def _exit_slide(self):
        self.state = State.RUN
        bottom = self.y + self.h
        self.h = self.h_run
        self.y = bottom - self.h

    def draw(self, surface):
        flicker = self.invuln > 0 and int(self.invuln * 18) % 2 == 0
        if self.dash_timer > 0:
            self._draw_dash_trail(surface)
        if self.state == State.SLIDE:
            self._draw_sliding(surface, flicker)
        else:
            self._draw_standing(surface, flicker)

    def _draw_dash_trail(self, surface):
        for i in range(1, 4):
            alpha = max(0, 120 - i * 30)
            ghost = pygame.Surface((self.w, self.h - 8), pygame.SRCALPHA)
            ghost.fill((245, 220, 160, alpha))
            surface.blit(ghost, (int(self.x) - i * 10, int(self.y) + 6))

    def _draw_standing(self, surface, flicker):
        x, y, w, h = int(self.x), int(self.y), self.w, self.h
        phase = math.sin(self.run_time * 14)
        grounded = self.grounded

        leg_color = S.PANTS
        body_color = S.SHIRT
        skin = S.SKIN
        hair = S.HAIR

        if flicker:
            leg_color = self._fade(leg_color)
            body_color = self._fade(body_color)
            skin = self._fade(skin)
            hair = self._fade(hair)

        leg_y = y + h - 16
        if grounded:
            pygame.draw.rect(surface, leg_color, (x + 6, leg_y, 8, 16 + int(phase * 2)))
            pygame.draw.rect(surface, leg_color, (x + w - 14, leg_y, 8, 16 - int(phase * 2)))
        else:
            pygame.draw.rect(surface, leg_color, (x + 4, leg_y - 4, 8, 14))
            pygame.draw.rect(surface, leg_color, (x + w - 12, leg_y + 2, 8, 14))

        pygame.draw.rect(surface, body_color, (x + 4, y + 18, w - 8, h - 36))
        pygame.draw.rect(surface, (42, 26, 16), (x + 4, y + h - 22, w - 8, 4))

        if grounded:
            pygame.draw.rect(surface, body_color, (x - 2, y + 22 - int(phase * 4), 7, 16))
            pygame.draw.rect(surface, body_color, (x + w - 5, y + 22 + int(phase * 4), 7, 16))
        else:
            pygame.draw.rect(surface, body_color, (x - 4, y + 16, 7, 16))
            pygame.draw.rect(surface, body_color, (x + w - 3, y + 16, 7, 16))
        pygame.draw.rect(surface, skin, (x - 2, y + 36, 5, 6))
        pygame.draw.rect(surface, skin, (x + w - 3, y + 36, 5, 6))

        pygame.draw.rect(surface, skin, (x + 6, y, w - 12, 18))
        pygame.draw.rect(surface, hair, (x + 6, y, w - 12, 5))
        pygame.draw.rect(surface, hair, (x + 4, y + 2, 4, 6))
        pygame.draw.rect(surface, hair, (x + w - 12, y + 8, 3, 3))

    def _draw_sliding(self, surface, flicker):
        x, y, w, h = int(self.x), int(self.y), self.w, self.h
        body = self._fade(S.SHIRT) if flicker else S.SHIRT
        skin = self._fade(S.SKIN) if flicker else S.SKIN
        hair = self._fade(S.HAIR) if flicker else S.HAIR

        pygame.draw.rect(surface, body, (x, y + 6, w, h - 6))
        pygame.draw.rect(surface, S.PANTS, (x + w - 12, y + h - 8, 14, 8))
        pygame.draw.rect(surface, skin, (x + 2, y, 18, 12))
        pygame.draw.rect(surface, hair, (x + 2, y, 18, 4))
        pygame.draw.rect(surface, hair, (x + 14, y + 6, 3, 3))

        for i in range(4):
            dx = x - 6 - i * 8
            pygame.draw.rect(surface, (220, 200, 160), (dx, y + h - 4 - (i % 2) * 2, 5, 2))

    @staticmethod
    def _fade(color):
        r, g, b = color
        return (min(255, r + 60), min(255, g + 60), min(255, b + 60))
