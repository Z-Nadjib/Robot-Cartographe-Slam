"""link.py — communication UDP avec le robot (TP9).

Rôle : envoyer des commandes au robot et récupérer, sans jamais bloquer, tous les
messages qu'il a envoyés depuis le dernier appel.

Ports : le PC écoute sur 5005 (messages O et S du robot) et envoie vers le port
5006 du robot (commandes V, C, X, M, P). Un message = une ligne de texte dont les
champs sont séparés par des virgules.

Link(robot_ip)
    Créer une socket UDP, la lier à ("0.0.0.0", port_rx), la rendre non
    bloquante, retenir l'adresse (robot_ip, port_tx).
send(msg)
    Encoder la chaîne et l'envoyer au robot.
poll()
    Lire tous les datagrammes en attente et renvoyer une liste de messages,
    chacun déjà découpé en liste de champs (ex. ["O", "12", "3400", ...]).
    BlockingIOError signifie qu'il n'y a plus rien à lire. Sous Windows,
    ConnectionResetError peut apparaître tant que le robot n'écoute pas : l'ignorer.
"""
import socket


class Link:
    def __init__(self, robot_ip, port_rx=5005, port_tx=5006):
        raise NotImplementedError("À compléter")

    def send(self, msg):
        raise NotImplementedError("À compléter")

    def poll(self):
        """Renvoie la liste des messages reçus depuis le dernier appel (listes de champs)."""
        raise NotImplementedError("À compléter")
