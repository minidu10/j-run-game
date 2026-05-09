import sys

import pygame

from . import settings as S
from .audio import Audio
from .background import Background
from .input_handler import InputHandler
from .obstacle import Spawner
from .player import Player
from .tiger import Tiger
from .utils import aabb, clamp


class GameState:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("J-Run — Forest Chase")
        self.screen = pygame.display.set_mode((S.SCREEN_W, S.SCREEN_H))
        self.clock = pygame.time.Clock()

        self.font_big   = pygame.font.SysFont("arial", 56, bold=True)
        self.font_mid   = pygame.font.SysFont("arial", 22, bold=True)
        self.font_small = pygame.font.SysFont("arial", 16)
        self.font_warn  = pygame.font.SysFont("arial", 28, bold=True)

        self.audio = Audio()
        self.input = InputHandler()
        self.background = Background(S.SCREEN_W, S.SCREEN_H, S.GROUND_Y)

        self.state = GameState.MENU
        self.best_score = 0
        self._reset_run()

    def _reset_run(self):
        self.player = Player(S.GROUND_Y)
        self.tiger = Tiger(S.GROUND_Y)
        self.spawner = Spawner(S.SCREEN_W, S.GROUND_Y)
        self.obstacles = []
        self.speed = S.START_SPEED
        self.elapsed = 0.0
        self.score = 0.0
        self.input.reset()

    def run(self):
        while True:
            dt = self.clock.tick(S.FPS) / 1000.0
            dt = min(dt, 1 / 30)
            self._handle_events()
            self._update(dt)
            self._draw()
            self.input.end_frame()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit()
            self.input.feed(event)

        if self.input.was_pressed("quit"):
            self._quit()

        if self.state == GameState.MENU:
            if self.input.was_pressed("jump") or self.input.was_pressed("dash"):
                self._start()
        elif self.state == GameState.PLAYING:
            if self.input.was_pressed("pause"):
                self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED:
            if self.input.was_pressed("pause"):
                self.state = GameState.PLAYING
            elif self.input.was_pressed("restart"):
                self._start()
        elif self.state == GameState.GAME_OVER:
            if self.input.was_pressed("restart") or self.input.was_pressed("jump"):
                self._start()

    def _start(self):
        self._reset_run()
        self.state = GameState.PLAYING

    def _quit(self):
        pygame.quit()
        sys.exit(0)

    def _update(self, dt):
        if self.state == GameState.MENU:
            self.background.update(dt, S.START_SPEED * 0.5)
            return

        if self.state == GameState.PAUSED:
            return

        if self.state == GameState.GAME_OVER:
            self.background.update(dt, max(0, self.speed - 200))
            self.speed = max(0, self.speed - 600 * dt)
            for obs in self.obstacles:
                obs.update(dt, self.speed)
            return

        # playing
        self.elapsed += dt
        self.speed = clamp(
            S.START_SPEED + self.elapsed * S.SPEED_RAMP, S.START_SPEED, S.MAX_SPEED
        )
        difficulty = (self.speed - S.START_SPEED) / 40.0

        self.background.update(dt, self.speed)
        self.player.update(dt, self.input, self.audio)
        self.tiger.update(dt, self.player.x)
        self.spawner.update(dt, self.obstacles, difficulty)

        # obstacles
        for obs in self.obstacles:
            obs.update(dt, self.speed)
            if not obs.passed and obs.x + obs.w < self.player.x:
                obs.passed = True
                self.score += S.SCORE_PER_OBSTACLE
                self.audio.score()
            if not self.player.is_invulnerable and aabb(self.player.bbox, obs.bbox):
                if self.player.take_hit():
                    self.tiger.hit_player()
                    self.audio.hit()

        self.obstacles = [o for o in self.obstacles if o.x + o.w > -20]

        # passive score
        self.score += S.SCORE_PER_SECOND * dt

        if self.player.lives <= 0 or self.tiger.caught_player:
            self._end_run()

    def _end_run(self):
        self.state = GameState.GAME_OVER
        self.audio.over()
        self.best_score = max(self.best_score, int(self.score))

    def _draw(self):
        self.background.draw(self.screen)

        # gameplay actors are drawn during PLAYING / PAUSED / GAME_OVER
        if self.state != GameState.MENU:
            for obs in self.obstacles:
                obs.draw(self.screen)
            self.tiger.draw(self.screen, self.player.x)
            self.tiger.draw_warning(self.screen, self.player.x, self.font_warn)
            self.player.draw(self.screen)
            self._draw_hud()

        if self.state == GameState.MENU:
            self._draw_menu()
        elif self.state == GameState.PAUSED:
            self._draw_centered_panel("PAUSED", "Press P to resume  ·  R to restart")
        elif self.state == GameState.GAME_OVER:
            sub = f"Score {int(self.score)}   ·   Best {self.best_score}   ·   Press R to retry"
            self._draw_centered_panel("THE TIGER GOT YOU", sub, color=S.DANGER)

        pygame.display.flip()

    def _draw_hud(self):
        # left: score + best
        pad = 18
        score_text = self.font_mid.render(f"SCORE  {int(self.score):05d}", True, S.ACCENT)
        best_text = self.font_small.render(f"BEST {self.best_score:05d}", True, S.INK_DIM)
        self.screen.blit(score_text, (pad, pad))
        self.screen.blit(best_text, (pad, pad + 28))

        # right: lives
        for i in range(S.PLAYER_LIVES):
            cx = S.SCREEN_W - pad - i * 22
            color = S.DANGER if i < self.player.lives else (60, 30, 30)
            pygame.draw.polygon(
                self.screen,
                color,
                [
                    (cx, pad + 14),
                    (cx - 10, pad + 4),
                    (cx - 7, pad),
                    (cx, pad + 4),
                    (cx + 7, pad),
                    (cx + 10, pad + 4),
                ],
            )

        # speed bar
        bar_w = 160
        bar_x = S.SCREEN_W - pad - bar_w
        bar_y = pad + 26
        pygame.draw.rect(self.screen, (40, 40, 40), (bar_x, bar_y, bar_w, 6), border_radius=3)
        ratio = (self.speed - S.START_SPEED) / (S.MAX_SPEED - S.START_SPEED)
        ratio = clamp(ratio, 0.0, 1.0)
        pygame.draw.rect(self.screen, S.GOOD, (bar_x, bar_y, int(bar_w * ratio), 6), border_radius=3)

    def _draw_menu(self):
        overlay = pygame.Surface((S.SCREEN_W, S.SCREEN_H), pygame.SRCALPHA)
        overlay.fill((8, 14, 11, 170))
        self.screen.blit(overlay, (0, 0))

        title = self.font_big.render("J-RUN", True, S.ACCENT)
        sub = self.font_mid.render("A man, a forest, and a very hungry tiger.", True, S.INK)
        line1 = self.font_small.render("[Space / W / Up]  Jump          [Down / S]  Slide", True, S.INK_DIM)
        line2 = self.font_small.render("[Shift / D]  Dash               [P]  Pause   [Esc]  Quit", True, S.INK_DIM)
        prompt = self.font_mid.render("Press SPACE to start", True, S.GOOD)

        cx = S.SCREEN_W // 2
        self.screen.blit(title, (cx - title.get_width() // 2, 130))
        self.screen.blit(sub, (cx - sub.get_width() // 2, 210))
        self.screen.blit(line1, (cx - line1.get_width() // 2, 290))
        self.screen.blit(line2, (cx - line2.get_width() // 2, 314))
        self.screen.blit(prompt, (cx - prompt.get_width() // 2, 380))

    def _draw_centered_panel(self, headline, sub, color=S.ACCENT):
        overlay = pygame.Surface((S.SCREEN_W, S.SCREEN_H), pygame.SRCALPHA)
        overlay.fill((8, 14, 11, 150))
        self.screen.blit(overlay, (0, 0))

        title = self.font_big.render(headline, True, color)
        subtitle = self.font_mid.render(sub, True, S.INK)
        cx = S.SCREEN_W // 2
        self.screen.blit(title, (cx - title.get_width() // 2, 200))
        self.screen.blit(subtitle, (cx - subtitle.get_width() // 2, 280))
