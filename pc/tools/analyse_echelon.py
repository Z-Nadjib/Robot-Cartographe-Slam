"""TP7 — Réponse indicielle en boucle ouverte -> modèle du 1er ordre (K, tau) -> réglage du PI.

Usage : python analyse_echelon.py mesures/echelon.csv
        (fichier produit par log_serial.py : t_ms,consigne,vG,vD,pwmG,pwmD)

Modèle du moteur : v(t) = K · u · (1 - exp(-t / tau)) pour un échelon de PWM u.

Ce que le script doit faire :
  1. charger le CSV (np.loadtxt), temps en secondes depuis le début, vitesse =
     moyenne des deux roues, u = PWM appliquée ;
  2. vitesse finale v_inf = moyenne de la fin de l'enregistrement (régime établi) ;
  3. tau = instant où la vitesse atteint 63 % de v_inf ; K = v_inf / u ;
  4. réglage par compensation du pôle : on choisit une boucle fermée deux fois
     plus rapide (tau_bf = tau / 2), d'où
        Kp = tau / (K · tau_bf)      Ki = Kp / tau
     (le zéro du PI compense le pôle du moteur) ; afficher les valeurs à
     recopier dans config.h ;
  5. tracer la mesure et le modèle pour vérifier qu'ils se superposent.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt


def identifier(t, v, u):
    """Renvoie (K, tau, v_inf) à partir de la réponse indicielle (étapes 2 et 3)."""
    raise NotImplementedError("À compléter")


def reglage_pi(K, tau):
    """Renvoie (Kp, Ki) par compensation du pôle (étape 4)."""
    raise NotImplementedError("À compléter")


def main(fichier):
    """Charge le fichier, identifie le modèle, propose KP/KI et trace (étapes 1 à 5)."""
    raise NotImplementedError("À compléter")


if __name__ == "__main__":
    main(sys.argv[1])
