"""TP4 — Reçoit les balayages en UDP, affiche le radar, compte les pertes, mesure la latence.

Usage : python udp_radar.py IP_ROBOT     (IP affichée par l'ESP32 sur le moniteur série)

Réseau : le robot envoie vers le port 5005 du PC ; le PC envoie vers le port 5006
du robot. Messages reçus :
    S,seq,angle0,pas,d0,...,d60     un balayage
    P,<horodatage>                  écho d'un ping envoyé par ce script

Ce que le script doit faire :
  1. socket UDP liée à ("0.0.0.0", 5005), non bloquante ;
  2. figure polaire 0°..180° (comme radar_serial.py) ;
  3. en boucle, tant que la fenêtre est ouverte :
     - une fois par seconde, envoyer « P,<time.perf_counter()> » au robot ;
     - lire un datagramme s'il y en a un (BlockingIOError : rien à lire ; sous
       Windows, ConnectionResetError peut aussi arriver tant que le robot
       n'écoute pas) ;
     - écho P : latence aller-retour = maintenant - horodatage, en ms ; afficher
       la dernière et la moyenne ;
     - balayage S : les angles valent angle0 + pas * k ; compter les pertes avec
       le numéro seq (un saut de seq = des paquets perdus) ; mettre à jour le
       tracé et un titre « balayage n°… · perdus : …/… ».

Valeurs typiques sur un partage de connexion : 5 à 30 ms d'aller-retour, moins
de 1 % de pertes à 2 m du téléphone.
"""
import socket, sys, time
import numpy as np
import matplotlib.pyplot as plt

PORT_PC, PORT_ROBOT = 5005, 5006


def main(robot_ip):
    """Étapes 1 à 3 décrites en tête de fichier."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main(sys.argv[1])
