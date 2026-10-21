"""fusion_test.py — TP11 : compare odométrie seule et EKF pendant un trajet téléopéré.

Usage : python fusion_test.py IP_ROBOT http://IP_CAMERA/capture

Rôle : conduire le robot au clavier devant les marqueurs ArUco, faire tourner en
parallèle l'odométrie seule et le filtre de Kalman, et enregistrer les deux
trajectoires pour le rapport.

Ce que le script doit faire, en boucle :
  1. messages O : odométrie (renvoie d, dθ), puis ekf.predict(d, dθ) ; ajouter
     (odo.x, odo.y, ekf.mu) au journal ;
  2. deux fois par seconde seulement (la caméra est lente) : lire une image,
     détecter les marqueurs ; pour chaque marqueur connu de markers.json,
     convertir la mesure (mesure_vers_robot) et appeler ekf.update_landmark ;
     afficher « accepté » ou « rejeté » (test du χ²) ; montrer l'image ;
     une erreur de la caméra ne doit pas arrêter le programme (try/except) ;
  3. clavier comme teleop.py, « V,v,w » envoyé à chaque tour, « X » en quittant ;
  4. à la fin : enregistrer le journal dans mesures/tp11_trajets.csv
     (colonnes odo_x, odo_y, ekf_x, ekf_y, ekf_th).

Validation : après un tour de la pièce, l'EKF revient à moins de 10 cm du point
de départ alors que l'odométrie seule dérive bien plus.
"""
import json, sys, time
import cv2
import numpy as np
from link import Link
from odometry import Odometry
from ekf import EKF, mesure_vers_robot
import aruco_cam

MM_PER_TICK, TRACK_MM = 0.1418, 130.0


def charger_marqueurs(fichier="markers.json"):
    """Renvoie {id: (x, y)} : position des marqueurs dans le repère de la carte, en mètres."""
    raise NotImplementedError("À compléter")


def main(robot_ip, cam_url):
    """Boucle décrite en tête de fichier."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
