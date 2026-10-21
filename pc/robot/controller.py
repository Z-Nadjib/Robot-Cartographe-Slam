"""controller.py — suivi d'un point : tourner vers lui, puis avancer en corrigeant le cap (TP12).

suivre(pose, cible, v_max, k_w, w_max) renvoie (v en m/s, w en rad/s, distance restante en m) :
    - distance et direction de la cible depuis la pose (x, y, θ) ;
    - erreur de cap = direction de la cible - θ, ramenée dans ]-π, π] ;
    - rotation proportionnelle à l'erreur : w = k_w · erreur, bornée à ±w_max ;
    - si l'erreur dépasse environ 25°, tourner sur place (v = 0) ; sinon avancer
      à min(v_max, 0,8 · distance) pour ralentir en approchant.
"""
import math
from odometry import wrap


def suivre(pose, cible, v_max=0.15, k_w=2.0, w_max=1.5):
    """Renvoie (v en m/s, w en rad/s, distance restante en m)."""
    raise NotImplementedError("À compléter")
