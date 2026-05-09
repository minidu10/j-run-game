import pygame

KEY_MAP = {
    pygame.K_SPACE: "jump",
    pygame.K_UP: "jump",
    pygame.K_w: "jump",
    pygame.K_DOWN: "slide",
    pygame.K_s: "slide",
    pygame.K_LSHIFT: "dash",
    pygame.K_RSHIFT: "dash",
    pygame.K_d: "dash",
    pygame.K_p: "pause",
    pygame.K_r: "restart",
    pygame.K_ESCAPE: "quit",
}


class InputHandler:
    def __init__(self):
        self._held = set()
        self._pressed = set()

    def feed(self, event):
        if event.type == pygame.KEYDOWN:
            action = KEY_MAP.get(event.key)
            if action and action not in self._held:
                self._pressed.add(action)
            if action:
                self._held.add(action)
        elif event.type == pygame.KEYUP:
            action = KEY_MAP.get(event.key)
            if action:
                self._held.discard(action)

    def is_down(self, action):
        return action in self._held

    def was_pressed(self, action):
        return action in self._pressed

    def end_frame(self):
        self._pressed.clear()

    def reset(self):
        self._held.clear()
        self._pressed.clear()
