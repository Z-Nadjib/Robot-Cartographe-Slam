"""aruco_cam.py — détection des marqueurs ArUco et estimation de la distance et de l'angle (TP5).

Usage autonome : python aruco_cam.py 0                         (webcam)
                 python aruco_cam.py http://IP_CAM/capture     (ESP32-CAM)

Rôle : pour chaque marqueur visible, donner son identifiant, sa distance (m) et
son angle (rad, positif = à gauche de l'axe optique). Utilisé par fusion_test.py
et app.py pour corriger la position du robot.

À implémenter :
  charger_calibration()
      Lire calib.npz (produit par pc/tools/calibrate.py) : matrice K et
      coefficients de distorsion.
  detecter(img)
      - niveaux de gris, puis cv2.aruco.ArucoDetector (dictionnaire DICT_4X4_50)
        .detectMarkers ;
      - pour chaque marqueur : cv2.solvePnP entre les 4 coins du marqueur dans son
        propre repère (carré de côté TAILLE centré en 0, z = 0, dans l'ordre
        renvoyé par OpenCV : haut-gauche, haut-droit, bas-droit, bas-gauche) et
        les 4 coins détectés dans l'image ; le drapeau SOLVEPNP_IPPE_SQUARE est
        fait pour ce cas ;
      - tvec = position du marqueur dans le repère caméra (x à droite, y en bas,
        z devant) : distance horizontale = √(x² + z²), angle = -atan2(x, z) ;
      - dessiner les axes et les contours sur l'image (aide au réglage).
  lire_image(src, cap)
      Depuis l'URL /capture de l'ESP32-CAM (urllib + cv2.imdecode) ou depuis la
      webcam cap.

Validation : marqueur à 1 m en face -> 1,00 m ± 3 cm et 0° ± 2°.
"""
import math, sys, urllib.request
import cv2
import numpy as np

TAILLE = 0.10                                   # côté du carré noir imprimé (m)


def charger_calibration(fichier="calib.npz"):
    """Renvoie (K, dist) lus dans le fichier de calibration."""
    raise NotImplementedError("À compléter")


def detecter(img):
    """Renvoie [(id, distance_m, angle_rad)] ; angle > 0 = marqueur à gauche de l'axe optique."""
    raise NotImplementedError("À compléter")


def lire_image(src, cap=None):
    """src = URL /capture de l'ESP32-CAM (image la plus récente) ou numéro de webcam."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    # À compléter : ouvrir la source donnée en argument, puis en boucle lire une
    # image, détecter, afficher « marqueur i : x cm, y° » et l'image ; Q pour quitter.
    raise NotImplementedError("À compléter")
