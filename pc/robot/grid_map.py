# grid_map.py — carte en grille d'occupation (log-odds)
import math
import numpy as np

SERVO_SENS = +1        # -1 si le radar apparaît en miroir (voir TP3)
SENSOR_X = 0.06        # position du laser devant le centre des roues (m)

def bresenham(c0, c1):
    """Cases traversées par le segment c0 → c1 (algorithme de Bresenham)."""
    (x0, y0), (x1, y1) = c0, c1
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err, cells = dx + dy, []
    while True:
        cells.append((x0, y0))
        if (x0, y0) == (x1, y1):
            return cells
        e2 = 2 * err
        if e2 >= dy: err += dy; x0 += sx
        if e2 <= dx: err += dx; y0 += sy

class GridMap:
    def __init__(self, size_m=6.0, res=0.05, origin=(1.0, 1.0)):
        self.res = res
        self.n = int(size_m / res)                 # 120 x 120 cases de 5 cm
        self.L = np.zeros((self.n, self.n), np.float32)
        self.ox, self.oy = origin                  # le départ du robot est à (1 m, 1 m) du coin

    def to_cell(self, x, y):
        return int((x + self.ox) / self.res), int((y + self.oy) / self.res)

    def to_world(self, i, j):
        return (i + 0.5) * self.res - self.ox, (j + 0.5) * self.res - self.oy

    def _add(self, i, j, v):
        if 0 <= i < self.n and 0 <= j < self.n:
            self.L[j, i] += v

    def add_scan(self, pose, angles_deg, dists_mm, max_r=3.5):
        x, y, th = pose
        sx, sy = x + SENSOR_X * math.cos(th), y + SENSOR_X * math.sin(th)
        c0 = self.to_cell(sx, sy)
        for a, d in zip(angles_deg, dists_mm):
            if d <= 0:
                continue                           # mesure invalide
            r = min(d / 1000, max_r)
            b = th + SERVO_SENS * math.radians(a - 90)
            c1 = self.to_cell(sx + r * math.cos(b), sy + r * math.sin(b))
            cells = bresenham(c0, c1)
            for i, j in cells[:-1]:
                self._add(i, j, -0.4)              # le faisceau a traversé : libre
            if d / 1000 < max_r:
                self._add(*c1, +0.85)              # il s'est arrêté : obstacle
        np.clip(self.L, -5, 5, out=self.L)

    def prob(self):
        return 1 - 1 / (1 + np.exp(self.L))       # probabilité d'occupation

    def image(self):
        """Image en niveaux de gris : blanc = libre, noir = mur, gris = inconnu."""
        return np.flipud((255 * (1 - self.prob())).astype(np.uint8))
