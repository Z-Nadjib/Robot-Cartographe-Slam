# Étapes 2 et 3 de la détection, codées à la main (à comparer avec OpenCV)
import cv2
import numpy as np

def seuillage_adaptatif(gris, taille=23, c=7):
    """Pixel noir si plus sombre que la moyenne de son voisinage : robuste aux ombres."""
    moyenne = cv2.blur(gris.astype(np.float32), (taille, taille))   # filtre passe-bas 2D
    return ((gris < moyenne - c) * 255).astype(np.uint8)

def quadrilateres(binaire, aire_min=800):
    """Garde les contours qui ressemblent à un carré vu en perspective."""
    contours, _ = cv2.findContours(binaire, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    quads = []
    for c in contours:
        a = cv2.approxPolyDP(c, 0.04 * cv2.arcLength(c, True), True)
        if len(a) == 4 and cv2.isContourConvex(a) and cv2.contourArea(a) > aire_min:
            quads.append(a.reshape(4, 2))
    return quads

# Pour aller plus loin : remplacer cv2.blur par votre propre convolution (image intégrale),
# puis redresser chaque quadrilatère (cv2.getPerspectiveTransform) et lire la grille 4 x 4 de bits.
