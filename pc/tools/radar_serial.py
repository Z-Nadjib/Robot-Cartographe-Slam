"""TP3 — Affiche en direct le radar reçu sur le port série (lignes « S,d0,d1,... »).

Usage : python radar_serial.py COM3        (Linux : /dev/ttyUSB0)

Ce que le script doit faire :
  - ouvrir le port série (115200 bauds) ;
  - créer une figure polaire limitée au demi-cercle 0°..180° avec deux tracés :
    les points bruts (gris) et la courbe filtrée par une médiane angulaire ;
  - en boucle, tant que la fenêtre est ouverte : lire une ligne ; si elle
    commence par « S, », convertir les distances en tableau numpy, remplacer
    les 0 (mesures invalides) par NaN, vérifier qu'il y a bien 61 valeurs, puis
    mettre à jour les deux tracés et l'échelle radiale ; plt.pause(0.01) laisse
    la fenêtre se redessiner.

mediane_angulaire(d, k) : pour chaque angle, la médiane des k distances voisines
(prolonger les bords en répétant la première et la dernière valeur, np.pad
mode « edge » ; np.nanmedian ignore les NaN). Elle supprime les points isolés
aberrants (reflets, bords d'objets).
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "COM3"
ANGLES = np.radians(np.arange(0, 181, 3))       # 61 angles : 0°, 3°, …, 180°


def mediane_angulaire(d, k=3):
    """Filtre médian le long de l'angle : supprime les points isolés aberrants."""
    raise NotImplementedError("À compléter")


def main():
    """Ouvre le port, crée la figure polaire et la met à jour à chaque balayage."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main()
