import random


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def lerp(a, b, t):
    return a + (b - a) * t


def rand(lo, hi):
    return random.uniform(lo, hi)


def randint(lo, hi):
    return random.randint(lo, hi)


def pick(seq):
    return random.choice(seq)


def aabb(a, b):
    """Axis-aligned bounding box overlap test. a and b are (x, y, w, h)."""
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by
