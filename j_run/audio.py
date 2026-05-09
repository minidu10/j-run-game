import math

import pygame

try:
    import numpy as np
    HAVE_NUMPY = True
except Exception:
    HAVE_NUMPY = False


class Audio:
    """Procedural SFX. Falls back to silence when sound is unavailable."""

    def __init__(self):
        self.enabled = False
        self.sounds = {}
        self.channels = 1
        try:
            pygame.mixer.pre_init(44100, -16, 1, 512)
            pygame.mixer.init()
            self.enabled = True
        except pygame.error:
            self.enabled = False
            return

        init = pygame.mixer.get_init()
        if init:
            self.channels = init[2]

        if not HAVE_NUMPY:
            # mixer is up but we can't synthesize without numpy
            self.enabled = False
            return

        self.sounds["jump"]  = self._tone(540, 0.12, "square",   0.5)
        self.sounds["slide"] = self._tone(220, 0.14, "sawtooth", 0.4)
        self.sounds["dash"]  = self._tone(720, 0.10, "triangle", 0.6, sweep=900)
        self.sounds["hit"]   = self._tone(120, 0.22, "sawtooth", 0.7)
        self.sounds["score"] = self._tone(880, 0.06, "sine",     0.4)
        self.sounds["over"]  = self._tone(140, 0.55, "sawtooth", 0.7, sweep=70)

    def _tone(self, freq, duration, wave, gain, sweep=None):
        rate = 44100
        n = int(rate * duration)
        t = np.linspace(0, duration, n, endpoint=False)
        if sweep is None:
            phase = 2 * math.pi * freq * t
        else:
            f = np.linspace(freq, sweep, n)
            phase = 2 * math.pi * np.cumsum(f) / rate

        if wave == "sine":
            samples = np.sin(phase)
        elif wave == "square":
            samples = np.sign(np.sin(phase))
        elif wave == "triangle":
            samples = 2 * np.abs(2 * ((phase / (2 * math.pi)) % 1) - 1) - 1
        else:  # sawtooth
            samples = 2 * ((phase / (2 * math.pi)) % 1) - 1

        # quick attack/decay envelope
        env = np.ones(n)
        attack = max(1, int(rate * 0.005))
        release = max(1, int(rate * min(0.08, duration * 0.6)))
        env[:attack] = np.linspace(0, 1, attack)
        env[-release:] = np.linspace(1, 0, release)

        samples = (samples * env * gain * 32767).astype(np.int16)
        if self.channels == 2:
            samples = np.column_stack((samples, samples))
        return pygame.sndarray.make_sound(samples)

    def _play(self, key):
        if not self.enabled:
            return
        snd = self.sounds.get(key)
        if snd is not None:
            snd.play()

    def jump(self):  self._play("jump")
    def slide(self): self._play("slide")
    def dash(self):  self._play("dash")
    def hit(self):   self._play("hit")
    def score(self): self._play("score")
    def over(self):  self._play("over")
