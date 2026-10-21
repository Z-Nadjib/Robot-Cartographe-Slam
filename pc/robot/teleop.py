"""teleop.py — TP9 : pilotage au clavier (Z Q S D, espace = stop, Échap = quitter).

Usage : python teleop.py IP_ROBOT

Rôle : conduire le robot à la main et vérifier l'odométrie en traçant la
trajectoire calculée.

Ce que le script doit faire, en boucle (environ 20 fois par seconde) :
  1. lire tous les messages du robot (Link.poll) ; pour chaque message O
     (8 champs) : mettre à jour l'odométrie avec ticksG, ticksD, cap_mdeg,
     retenir la tension batterie, ajouter (x, y) à la trace ;
  2. dessiner une image blanche 500 x 500 (1 pixel = 1 cm, départ au centre,
     y vers le haut) avec la trace et un texte : x, y, cap en degrés, batterie ;
  3. cv2.waitKey(50) : Z avance (v = 150 mm/s), S recule, Q tourne à gauche
     (w = 1500 mrad/s), D à droite, espace arrête, Échap quitte ;
  4. envoyer « V,v,w » À CHAQUE tour : le robot s'arrête de lui-même s'il ne
     reçoit rien pendant 500 ms (chien de garde).
En quittant, envoyer « X ».

Validation : un carré de 1 m parcouru au clavier se referme à moins de 5 cm.
"""
import math, sys
import cv2
import numpy as np
from link import Link
from odometry import Odometry

MM_PER_TICK, TRACK_MM = 0.1418, 130.0          # recopier les valeurs de config.h


def main(robot_ip):
    """Boucle de pilotage décrite en tête de fichier."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main(sys.argv[1])
