"""TP5 — Génère 8 marqueurs ArUco (dictionnaire 4x4_50) à imprimer.

Ce que le script doit faire, pour chaque identifiant de 0 à 7 :
  - générer l'image du marqueur avec cv2.aruco.generateImageMarker
    (dictionnaire cv2.aruco.DICT_4X4_50, carré de 600 px) ;
  - ajouter une marge blanche d'environ 120 px tout autour (cv2.copyMakeBorder) :
    le détecteur a besoin d'un bord blanc pour trouver le carré noir ;
  - écrire « ID i » dans la marge, pour ne pas confondre les marqueurs collés au mur ;
  - enregistrer marker_i.png.
Terminer en rappelant d'imprimer à 100 % et de vérifier au réglet que le carré
noir mesure exactement 10 cm (c'est la taille TAILLE utilisée dans aruco_cam.py).
"""
import cv2

DICTIONNAIRE = cv2.aruco.DICT_4X4_50
NB_MARQUEURS = 8


def main():
    """Génère et enregistre les marqueurs (voir la description ci-dessus)."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main()
