"""TP2 — Lit les mesures du laser sur le port série, les trace et les enregistre.

Usage : python plot_serial.py COM3        (Linux : /dev/ttyUSB0)

Le croquis tp2_laser.ino envoie une ligne CSV par mesure :
    temps_ms,brut_mm,filtre_mm,valide

Ce que le script doit faire :
  1. ouvrir le port série à 115200 bauds (pyserial), attendre 2 s (l'ESP32
     redémarre à l'ouverture du port) puis vider le tampon d'entrée ;
  2. lire N = 400 lignes valides : découper sur les virgules, ignorer les lignes
     qui n'ont pas 4 champs ou qui ne se convertissent pas en entiers ;
  3. enregistrer t, brut, filtré dans mesures/tp2_laser.csv (avec un en-tête) ;
  4. afficher la moyenne et l'écart-type des mesures brutes et filtrées : le
     filtre doit réduire l'écart-type sans déplacer la moyenne ;
  5. tracer les deux courbes en fonction du temps en secondes (matplotlib),
     enregistrer la figure dans mesures/tp2_laser.png et l'afficher.
"""
import csv, sys, time
import numpy as np
import matplotlib.pyplot as plt
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "COM3"   # Linux : /dev/ttyUSB0
N = 400                                                # nombre de mesures


def lire_mesures(ser, n):
    """Renvoie trois listes (t_ms, brut_mm, filtre_mm) de n mesures valides."""
    raise NotImplementedError("À compléter : étape 2")


def main():
    """Étapes 1 à 5 décrites en tête de fichier."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main()
