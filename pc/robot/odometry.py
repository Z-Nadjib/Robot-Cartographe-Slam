# odometry.py — pose (x, y, θ) en mètres et radians à partir des ticks et du cap
import math

def wrap(a):
    """Ramène un angle dans ]-pi, pi]."""
    return (a + math.pi) % (2 * math.pi) - math.pi

class Odometry:
    def __init__(self, mm_per_tick, track_mm, use_gyro=True):
        self.k = mm_per_tick / 1000
        self.L = track_mm / 1000
        self.use_gyro = use_gyro
        self.x = self.y = self.th = 0.0
        self.prev = None

    def update(self, tl, tr, heading_mdeg):
        """Renvoie (d, dθ) : distance parcourue et rotation depuis le message précédent."""
        h = math.radians(heading_mdeg / 1000)
        if self.prev is None:
            self.prev = (tl, tr, h)
            return 0.0, 0.0
        dl = (tl - self.prev[0]) * self.k
        dr = (tr - self.prev[1]) * self.k
        d = (dl + dr) / 2
        dth = wrap(h - self.prev[2]) if self.use_gyro else (dr - dl) / self.L
        self.prev = (tl, tr, h)
        a = self.th + dth / 2                      # angle moyen pendant le pas
        self.x += d * math.cos(a)
        self.y += d * math.sin(a)
        self.th = wrap(self.th + dth)
        return d, dth
