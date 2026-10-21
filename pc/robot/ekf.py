# ekf.py — filtre de Kalman étendu : odométrie (prédiction) + marqueurs ArUco (correction)
import math
import numpy as np
from odometry import wrap

CAM_X = 0.08                       # caméra 8 cm devant le centre des roues (à mesurer)

def mesure_vers_robot(r, a):
    """Distance / angle vus par la caméra → par rapport au centre des roues."""
    px, py = CAM_X + r * math.cos(a), r * math.sin(a)
    return math.hypot(px, py), math.atan2(py, px)

class EKF:
    def __init__(self, x0=(0.0, 0.0, 0.0)):
        self.mu = np.array(x0, float)                  # état estimé [x, y, θ]
        self.S = np.diag([1e-4, 1e-4, 1e-4])           # covariance (incertitude)

    def predict(self, d, dth, k_d=0.03, k_th=0.05):
        x, y, th = self.mu
        a = th + dth / 2
        self.mu = np.array([x + d * math.cos(a), y + d * math.sin(a), wrap(th + dth)])
        G = np.array([[1, 0, -d * math.sin(a)],        # jacobienne du modèle de mouvement
                      [0, 1,  d * math.cos(a)],
                      [0, 0,  1]])
        q_xy = (k_d * abs(d)) ** 2 + 1e-7              # le bruit grandit avec le déplacement
        q_th = (k_th * abs(dth)) ** 2 + (0.01 * abs(d)) ** 2 + 1e-7
        self.S = G @ self.S @ G.T + np.diag([q_xy, q_xy, q_th])

    def update_landmark(self, r, phi, mx, my, s_phi=math.radians(3)):
        """Correction avec un marqueur de position connue (mx, my) vu à (r, phi)."""
        x, y, th = self.mu
        dx, dy = mx - x, my - y
        q = dx * dx + dy * dy
        sq = math.sqrt(q)
        z_pred = np.array([sq, wrap(math.atan2(dy, dx) - th)])
        H = np.array([[-dx / sq, -dy / sq,  0],
                      [ dy / q,  -dx / q,  -1]])
        R = np.diag([(0.03 + 0.05 * r) ** 2, s_phi ** 2])
        nu = np.array([r - z_pred[0], wrap(phi - z_pred[1])])   # innovation
        Sz = H @ self.S @ H.T + R
        if nu @ np.linalg.solve(Sz, nu) > 9.21:        # test du chi² (99 %) : mesure aberrante
            return False
        Kg = self.S @ H.T @ np.linalg.inv(Sz)          # gain de Kalman
        self.mu = self.mu + Kg @ nu
        self.mu[2] = wrap(self.mu[2])
        self.S = (np.eye(3) - Kg @ H) @ self.S
        return True
