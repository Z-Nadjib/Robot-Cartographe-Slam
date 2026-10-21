"""TP5 — Calibration de la caméra avec un damier de 9 x 6 coins intérieurs.

Usage : python calibrate.py 0                        (webcam du PC)
        python calibrate.py http://IP_CAM/capture    (ESP32-CAM)

But : obtenir la matrice K (focales, centre optique) et les coefficients de
distorsion de la caméra, indispensables pour mesurer une distance avec ArUco.
Le résultat est enregistré dans calib.npz (K, dist), lu par aruco_cam.py.

Ce que le script doit faire :
  1. lire_image() : depuis l'URL (urllib, puis cv2.imdecode) ou depuis la
     webcam (cv2.VideoCapture) ;
  2. préparer les points 3D du damier : une grille 9 x 6 dont le pas vaut la
     taille réelle d'une case EN MÈTRES (à mesurer sur l'impression), z = 0 ;
  3. en boucle : chercher les coins (cv2.findChessboardCorners), les dessiner,
     afficher le nombre d'images retenues ;
       ESPACE -> si le damier est vu, affiner les coins (cv2.cornerSubPix) et
                 garder le couple (points 3D, points image) ;
       Q      -> terminer s'il y a au moins 10 images ;
  4. cv2.calibrateCamera, puis enregistrer calib.npz et afficher l'erreur de
     reprojection (bonne si < 0,5 px, acceptable si < 1 px).

Conseil : 15 à 25 images, damier incliné, près, loin, dans les coins de l'image.
"""
import sys, urllib.request
import cv2
import numpy as np

SRC = sys.argv[1] if len(sys.argv) > 1 else "0"   # "0" = webcam, ou http://IP_CAM/capture
COINS, CARRE = (9, 6), 0.025                       # côté d'une case en mètres : MESUREZ-LE


def lire_image(cap):
    """Renvoie une image BGR (ou None) depuis l'URL SRC ou la webcam cap."""
    raise NotImplementedError("À compléter")


def points_damier():
    """Renvoie le tableau (54, 3) float32 des coins du damier dans son repère, en mètres."""
    raise NotImplementedError("À compléter")


def main():
    """Boucle de capture puis calibration (étapes 3 et 4)."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main()
