# controller.py — suivi d'un point : tourner vers lui, puis avancer en corrigeant le cap
import math
from odometry import wrap

def suivre(pose, cible, v_max=0.15, k_w=2.0, w_max=1.5):
    """Renvoie (v en m/s, w en rad/s, distance restante en m)."""
    x, y, th = pose
    dx, dy = cible[0] - x, cible[1] - y
    dist = math.hypot(dx, dy)
    err = wrap(math.atan2(dy, dx) - th)              # erreur de cap
    w = max(-w_max, min(w_max, k_w * err))
    v = 0.0 if abs(err) > math.radians(25) else min(v_max, 0.8 * dist)
    return v, w, dist
