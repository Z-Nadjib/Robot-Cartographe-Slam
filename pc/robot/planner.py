"""planner.py — gonflement des obstacles + recherche de chemin A* (TP12).

inflate(prob, rayon_m, res, seuil)
    Cases interdites au CENTRE du robot : une case est un obstacle si sa
    probabilité dépasse « seuil » ; on élargit ensuite chaque obstacle du rayon
    du robot (plus une marge) avec une dilatation morphologique
    (cv2.getStructuringElement en ellipse de rayon k cases, puis cv2.dilate).
    Ainsi on peut planifier comme si le robot était un point.
    Renvoie un tableau de booléens indexé [j, i].

astar(bloque, depart, but)
    Plus court chemin sur la grille, 8 voisins (coût 1 en ligne droite, √2 en
    diagonale), heuristique = distance en ligne droite jusqu'au but (elle ne
    surestime jamais : le chemin trouvé est optimal).
    - file de priorité (heapq) triée par f = g + h ;
    - g[c] = meilleur coût connu depuis le départ, parent[c] = case précédente ;
    - sortir une case : si c'est le but, terminer ; si elle a déjà été atteinte
      avec un meilleur coût, l'ignorer ; sinon examiner ses voisins (dans la
      grille et non bloqués) et les ajouter quand leur coût s'améliore ;
    - reconstruire le chemin en remontant les parents depuis le but.
    depart et but sont des cases (i, j). Renvoie la liste des cases du départ au
    but, ou None si le but est inaccessible.
"""
import heapq, math
import cv2
import numpy as np


def inflate(prob, rayon_m, res, seuil=0.65):
    """Cases interdites : obstacles élargis du rayon du robot (+ marge)."""
    raise NotImplementedError("À compléter")


def astar(bloque, depart, but):
    """bloque[j, i] ; depart et but en cases (i, j). Renvoie la liste des cases ou None."""
    raise NotImplementedError("À compléter")
