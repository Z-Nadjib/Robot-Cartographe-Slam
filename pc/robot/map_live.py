"""map_live.py — TP10 : téléopération + construction de la carte (« s'arrêter pour balayer »).

Usage : python map_live.py IP_ROBOT

Rôle : conduire le robot au clavier comme dans teleop.py, et ajouter chaque
balayage reçu à la grille d'occupation affichée en direct.

Ce que le script doit faire, en boucle :
  1. messages O -> odométrie ; messages S -> angles = angle0 + pas · k et
     distances, puis carte.add_scan((x, y, θ), angles, distances) ;
  2. afficher carte.image() agrandie ECH fois (cv2.resize, INTER_NEAREST),
     avec le robot (cercle + trait dans la direction du cap) ;
  3. clavier : mêmes touches que teleop.py, plus
       C  s'arrêter et lancer un balayage (envoyer « C ») ;
       E  enregistrer l'image dans mesures/carte.png ;
  4. envoyer « V,v,w » à chaque tour (chien de garde) ; « X » en quittant.

Stratégie conseillée : s'arrêter, balayer (≈ 5 s), demi-tour sur place, balayer,
avancer d'environ 50 cm. Une mesure prise en roulant serait mal placée.
"""
import math, sys
import cv2
from link import Link
from odometry import Odometry
from grid_map import GridMap

MM_PER_TICK, TRACK_MM, ECH = 0.1418, 130.0, 4     # ECH : pixels par case à l'écran


def main(robot_ip):
    """Boucle décrite en tête de fichier."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main(sys.argv[1])
