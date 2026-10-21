"""grid_map.py — carte en grille d'occupation (log-odds) (TP10).

Rôle : transformer les balayages et la pose du robot en une carte de la pièce.

La pièce est découpée en cases de res mètres (5 cm). Chaque case garde un score
L (log-odds) : négatif = probablement libre, positif = probablement un mur,
0 = inconnu. Probabilité correspondante : p = 1 - 1 / (1 + exp(L)).
Additionner des scores revient à combiner des observations indépendantes.

Repères : le monde est en mètres, le départ du robot est à « origin » du coin
de la carte. La case (i, j) contient le point
    x = (i + 0,5) · res - ox      y = (j + 0,5) · res - oy
et le tableau est indexé L[j, i] (ligne = y, colonne = x).

À implémenter :
  bresenham(c0, c1)
      Liste des cases traversées par le segment entre deux cases (algorithme de
      Bresenham, entiers seulement), c0 et c1 comprises.
  to_cell / to_world
      Conversions mètres <-> indices de case (formules ci-dessus).
  add_scan(pose, angles_deg, dists_mm)
      Pour chaque mesure valide (d > 0) :
        - position du capteur : SENSOR_X mètres devant le centre des roues ;
        - direction du faisceau : θ + SERVO_SENS · (angle - 90°) (90° = devant) ;
        - distance bornée à max_r ; case d'arrivée ;
        - cases traversées (sauf la dernière) : score - 0,4 (libre) ;
        - case d'arrivée, seulement si la mesure est < max_r : score + 0,85 (mur).
      Enfin borner les scores à ±5 pour que la carte puisse encore changer.
  prob()   probabilité d'occupation de chaque case.
  image()  image en niveaux de gris : blanc = libre, noir = mur, gris = inconnu,
           retournée verticalement (np.flipud) pour avoir y vers le haut à l'écran.
"""
import math
import numpy as np

SERVO_SENS = +1        # -1 si le radar apparaît en miroir (voir TP3)
SENSOR_X = 0.06        # position du laser devant le centre des roues (m)


def bresenham(c0, c1):
    """Cases traversées par le segment c0 → c1 (algorithme de Bresenham)."""
    raise NotImplementedError("À compléter")


class GridMap:
    def __init__(self, size_m=6.0, res=0.05, origin=(1.0, 1.0)):
        self.res = res
        self.n = int(size_m / res)                 # 120 x 120 cases de 5 cm
        self.L = np.zeros((self.n, self.n), np.float32)
        self.ox, self.oy = origin                  # le départ du robot est à (1 m, 1 m) du coin

    def to_cell(self, x, y):
        raise NotImplementedError("À compléter")

    def to_world(self, i, j):
        raise NotImplementedError("À compléter")

    def add_scan(self, pose, angles_deg, dists_mm, max_r=3.5):
        raise NotImplementedError("À compléter")

    def prob(self):
        """Probabilité d'occupation de chaque case."""
        raise NotImplementedError("À compléter")

    def image(self):
        """Image en niveaux de gris : blanc = libre, noir = mur, gris = inconnu."""
        raise NotImplementedError("À compléter")
