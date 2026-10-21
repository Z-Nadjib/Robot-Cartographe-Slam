"""app.py — application finale : carte en direct, recalage ArUco, navigation multi-points (TP12).

Usage : python app.py IP_ROBOT http://IP_CAMERA/capture

Rôle : réunir tous les modules. Le robot s'arrête, balaye, la carte se met à
jour, la caméra recale la position, puis le robot rejoint un par un les buts
cliqués sur la carte.

Ce que le programme doit faire, en boucle (≈ 20 fois par seconde) :
  1. Messages du robot :
       O -> odometry.update, puis ekf.predict(d, dθ) ;
       S -> carte.add_scan(pose estimée par l'EKF, angles, distances) ; le
            balayage est fini : revenir à l'état ATTENTE.
  2. Recalage, deux fois par seconde : détecter les marqueurs, et pour chaque
     marqueur connu (markers.json) appeler ekf.update_landmark ; une erreur de
     la caméra est affichée sans arrêter le programme.
  3. Navigation, s'il reste des buts et qu'aucun balayage n'est en cours :
       - pas de chemin courant -> inflate(carte.prob(), 0,12 m, res), puis A*
         de la case du robot à la case du premier but ; but inaccessible ->
         le signaler et le retirer de la liste ;
       - garder un point de passage sur 4 (chemin plus fluide), plus le but ;
       - suivre(pose, premier point) -> (v, w) ; point atteint à moins de 5 cm
         -> passer au suivant ; but atteint -> le retirer, envoyer « C » et
         passer à l'état SCAN (on balaye avant de repartir).
     Envoyer « V,v,w » à chaque tour (en mm/s et mrad/s), même à l'arrêt.
  4. Affichage : carte agrandie, buts numérotés, points du chemin, robot (cercle
     + direction), état courant (ATTENTE, ROULE, SCAN).
     Clic gauche = ajouter un but (convertir pixels -> case -> mètres) ;
     C = balayage manuel ; E = enregistrer mesures/carte_finale.png ; Échap = quitter.
  En quittant, envoyer « X ».
"""
import json, math, sys, time
import cv2
from link import Link
from odometry import Odometry
from grid_map import GridMap
from ekf import EKF, mesure_vers_robot
from planner import inflate, astar
from controller import suivre
import aruco_cam

MM_PER_TICK, TRACK_MM, ECH = 0.1418, 130.0, 4


def main(robot_ip, cam_url):
    """Boucle principale décrite en tête de fichier."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
