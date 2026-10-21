"""ekf.py — filtre de Kalman étendu : odométrie (prédiction) + marqueurs ArUco (correction) (TP11).

État estimé : mu = [x, y, θ] et sa covariance S (3 x 3), qui mesure l'incertitude.

Prédiction — predict(d, dθ), à chaque message O :
    même modèle que l'odométrie : a = θ + dθ/2, x += d cos a, y += d sin a, θ += dθ ;
    G = jacobienne du modèle par rapport à l'état :
        [[1, 0, -d sin a],
         [0, 1,  d cos a],
         [0, 0,  1      ]]
    S = G S Gᵀ + Q, avec un bruit Q qui grandit avec le déplacement :
        q_xy = (k_d · |d|)² + petit terme
        q_θ  = (k_th · |dθ|)² + (0,01 · |d|)² + petit terme

Correction — update_landmark(r, φ, mx, my), quand un marqueur de position connue
(mx, my) est vu à la distance r et à l'angle φ (dans le repère du robot) :
    dx = mx - x, dy = my - y, q = dx² + dy² ;
    mesure prédite  ẑ = [√q, wrap(atan2(dy, dx) - θ)] ;
    H = [[-dx/√q, -dy/√q,  0],
         [ dy/q,  -dx/q,  -1]] ;
    R = bruit de mesure : écart-type de distance 3 cm + 5 % de r, d'angle s_phi ;
    innovation ν = [r - ẑ₀, wrap(φ - ẑ₁)] ; Sz = H S Hᵀ + R ;
    test du χ² : si νᵀ Sz⁻¹ ν > 9,21 (99 % pour 2 degrés de liberté), la mesure
    est aberrante : la rejeter et renvoyer False ;
    sinon gain K = S Hᵀ Sz⁻¹ ; mu += K ν (θ ramené par wrap) ; S = (I - K H) S ;
    renvoyer True.

mesure_vers_robot(r, a) : la caméra est CAM_X mètres devant le centre des roues ;
convertir la mesure (distance, angle) vue de la caméra en mesure vue du centre
des roues (passer par les coordonnées cartésiennes).
"""
import math
import numpy as np
from odometry import wrap

CAM_X = 0.08                       # caméra 8 cm devant le centre des roues (à mesurer)


def mesure_vers_robot(r, a):
    """Distance / angle vus par la caméra → par rapport au centre des roues."""
    raise NotImplementedError("À compléter")


class EKF:
    def __init__(self, x0=(0.0, 0.0, 0.0)):
        self.mu = np.array(x0, float)                  # état estimé [x, y, θ]
        self.S = np.diag([1e-4, 1e-4, 1e-4])           # covariance (incertitude)

    def predict(self, d, dth, k_d=0.03, k_th=0.05):
        raise NotImplementedError("À compléter")

    def update_landmark(self, r, phi, mx, my, s_phi=math.radians(3)):
        """Correction avec un marqueur de position connue (mx, my) vu à (r, phi)."""
        raise NotImplementedError("À compléter")
