"""TP7 — Enregistre les lignes CSV du port série pendant N secondes.

Usage : python log_serial.py COM3 mesures/echelon.csv 4 "p 150"
        (port, fichier de sortie, durée en secondes, commande facultative)

Sert à enregistrer la réponse indicielle du moteur : on envoie « p 150 » au
croquis tp7_banc_moteur.ino et on garde ses lignes
    temps_ms,consigne,vG,vD,pwmG,pwmD

Ce que le script doit faire :
  1. ouvrir le port (115200 bauds), attendre 2 s (redémarrage de l'ESP32 à
     l'ouverture du port), vider le tampon d'entrée ;
  2. si une commande est donnée, l'envoyer suivie de « \\n » ;
  3. pendant la durée demandée : lire les lignes et n'écrire dans le fichier que
     celles qui commencent par un chiffre (les autres sont des messages) ;
  4. envoyer « s » pour arrêter les moteurs et afficher le nombre de lignes.
"""
import sys, time
import serial


def main(port, fichier, duree, commande=None):
    """Étapes 1 à 4 décrites en tête de fichier."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else None)
