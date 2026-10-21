# planner.py — gonflement des obstacles + recherche de chemin A*
import heapq, math
import cv2
import numpy as np

def inflate(prob, rayon_m, res, seuil=0.65):
    """Cases interdites : obstacles élargis du rayon du robot (+ marge)."""
    occ = (prob > seuil).astype(np.uint8)
    k = int(math.ceil(rayon_m / res))
    noyau = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * k + 1, 2 * k + 1))
    return cv2.dilate(occ, noyau) > 0

def astar(bloque, depart, but):
    """bloque[j, i] ; depart et but en cases (i, j). Renvoie la liste des cases ou None."""
    nl, nc = bloque.shape
    voisins = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1),
               (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)]
    h = lambda c: math.hypot(c[0] - but[0], c[1] - but[1])   # heuristique : ligne droite
    ouverts = [(h(depart), 0.0, depart)]
    parent, g = {depart: None}, {depart: 0.0}
    while ouverts:
        _, gc, c = heapq.heappop(ouverts)
        if c == but:
            break
        if gc > g[c]:
            continue
        for di, dj, cout in voisins:
            nb = (c[0] + di, c[1] + dj)
            if not (0 <= nb[0] < nc and 0 <= nb[1] < nl) or bloque[nb[1], nb[0]]:
                continue
            ng = gc + cout
            if ng < g.get(nb, math.inf):
                g[nb], parent[nb] = ng, c
                heapq.heappush(ouverts, (ng + h(nb), ng, nb))
    if but not in parent:
        return None
    chemin, c = [], but
    while c is not None:
        chemin.append(c)
        c = parent[c]
    return chemin[::-1]
