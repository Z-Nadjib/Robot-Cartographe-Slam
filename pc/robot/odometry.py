"""odometry.py — pose (x, y, θ) en mètres et radians à partir des ticks et du cap (TP9).

Rôle : à chaque message O du robot, calculer de combien le robot a avancé et
tourné depuis le message précédent, et cumuler la pose.

Modèle de la voiture (deux roues motrices, entraxe L) :
    dl, dr = déplacement de chaque roue = (ticks - ticks précédents) · mètres par tick
    d      = (dl + dr) / 2                       distance parcourue par le centre
    dθ     = (dr - dl) / L                       rotation, d'après les roues
          ou différence de deux caps du gyroscope (plus fiable : les roues glissent)
    x += d · cos(θ + dθ/2)   y += d · sin(θ + dθ/2)   θ += dθ
L'angle moyen θ + dθ/2 donne un meilleur résultat qu'utiliser θ seul.
Penser à ramener les angles dans ]-π, π] (fonction wrap) : sinon la différence de
deux caps proches de ±180° donne un saut de 360°.

update(tl, tr, heading_mdeg)
    Au premier appel : mémoriser les valeurs et renvoyer (0, 0).
    Ensuite : calculer d et dθ, mettre à jour la pose, mémoriser les valeurs et
    renvoyer (d, dθ) ; ce couple sert aussi à la prédiction du filtre de Kalman.
"""
import math


def wrap(a):
    """Ramène un angle dans ]-pi, pi]."""
    raise NotImplementedError("À compléter")


class Odometry:
    def __init__(self, mm_per_tick, track_mm, use_gyro=True):
        self.k = mm_per_tick / 1000          # mètres par tick
        self.L = track_mm / 1000             # entraxe en mètres
        self.use_gyro = use_gyro
        self.x = self.y = self.th = 0.0
        self.prev = None                     # (ticks gauche, ticks droite, cap en rad) précédents

    def update(self, tl, tr, heading_mdeg):
        """Renvoie (d, dθ) : distance parcourue et rotation depuis le message précédent."""
        raise NotImplementedError("À compléter")
