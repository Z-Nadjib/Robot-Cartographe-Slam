"""TP5 — Étapes 2 et 3 de la détection ArUco, codées à la main (à comparer avec OpenCV).

Une détection ArUco se fait en quatre étapes : (1) niveaux de gris,
(2) seuillage, (3) recherche des quadrilatères, (4) lecture des bits du code.
Ce fichier code les étapes 2 et 3 pour comprendre ce que fait OpenCV.

seuillage_adaptatif(gris, taille, c)
    Un pixel devient noir (255 dans l'image binaire) s'il est plus sombre que la
    moyenne de son voisinage taille x taille, moins c. Comparer à une moyenne
    LOCALE rend le seuil robuste aux ombres et aux éclairages inégaux.
    La moyenne locale est un filtre passe-bas 2D : cv2.blur sur l'image en float32.

quadrilateres(binaire, aire_min)
    Trouver les contours (cv2.findContours), approcher chacun par un polygone
    (cv2.approxPolyDP, tolérance ≈ 4 % du périmètre), et ne garder que ceux qui
    ont 4 sommets, sont convexes et ont une aire suffisante. Renvoyer la liste
    des quadrilatères sous forme de tableaux (4, 2).

Pour aller plus loin : remplacer cv2.blur par votre propre convolution (image
intégrale), puis redresser chaque quadrilatère (cv2.getPerspectiveTransform) et
lire la grille 4 x 4 de bits.
"""
import cv2
import numpy as np


def seuillage_adaptatif(gris, taille=23, c=7):
    """Pixel noir si plus sombre que la moyenne de son voisinage : robuste aux ombres."""
    raise NotImplementedError("À compléter")


def quadrilateres(binaire, aire_min=800):
    """Garde les contours qui ressemblent à un carré vu en perspective."""
    raise NotImplementedError("À compléter")
