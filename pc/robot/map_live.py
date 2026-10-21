# map_live.py — TP10 : téléopération + construction de la carte (stop and scan)
import math, sys
import cv2
from link import Link
from odometry import Odometry
from grid_map import GridMap

MM_PER_TICK, TRACK_MM, ECH = 0.1418, 130.0, 4     # ECH : pixels par case à l'écran
link, odo, carte = Link(sys.argv[1]), Odometry(MM_PER_TICK, TRACK_MM), GridMap()
v = w = 0

while True:
    for m in link.poll():
        if m[0] == "O" and len(m) >= 8:
            odo.update(int(m[3]), int(m[4]), int(m[5]))
        elif m[0] == "S":                           # balayage reçu : on l'ajoute à la carte
            a0, pas, d = int(m[2]), int(m[3]), [int(x) for x in m[4:]]
            carte.add_scan((odo.x, odo.y, odo.th), [a0 + pas * k for k in range(len(d))], d)
    img = cv2.cvtColor(cv2.resize(carte.image(), None, fx=ECH, fy=ECH,
                                  interpolation=cv2.INTER_NEAREST), cv2.COLOR_GRAY2BGR)
    i, j = carte.to_cell(odo.x, odo.y)
    p = (i * ECH, (carte.n - 1 - j) * ECH)
    cv2.circle(img, p, 6, (0, 150, 0), 2)
    cv2.line(img, p, (int(p[0] + 20 * math.cos(odo.th)), int(p[1] - 20 * math.sin(odo.th))), (0, 150, 0), 2)
    cv2.imshow("carte", img)
    k = cv2.waitKey(50) & 0xFF
    if k == ord("c"): v, w = 0, 0; link.send("C")  # s'arrêter et balayer
    elif k == ord("z"): v, w = 150, 0
    elif k == ord("s"): v, w = -150, 0
    elif k == ord("q"): v, w = 0, 1500
    elif k == ord("d"): v, w = 0, -1500
    elif k == ord(" "): v, w = 0, 0
    elif k == ord("e"): cv2.imwrite("mesures/carte.png", img)
    elif k == 27: break
    link.send(f"V,{v},{w}")
link.send("X")
