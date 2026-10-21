# app.py — application finale : carte en direct, recalage ArUco, navigation multi-points
# usage : python app.py IP_ROBOT http://IP_CAMERA/capture
import json, math, sys, time
import cv2
from link import Link
from odometry import Odometry
from grid_map import GridMap
from ekf import EKF, mesure_vers_robot
from planner import inflate, astar
from controller import suivre
import aruco_cam

ROBOT_IP, CAM_URL = sys.argv[1], sys.argv[2]
MM_PER_TICK, TRACK_MM, ECH = 0.1418, 130.0, 4
MARQUEURS = {int(k): v for k, v in json.load(open("markers.json")).items()}

link, odo, ekf, carte = Link(ROBOT_IP), Odometry(MM_PER_TICK, TRACK_MM), EKF(), GridMap()
buts, chemin, etat, t_cam = [], [], "ATTENTE", 0.0      # etat : ATTENTE, ROULE, SCAN

def ecran(x, y):                                        # mètres → pixels
    i, j = carte.to_cell(x, y)
    return i * ECH, (carte.n - 1 - j) * ECH

def clic(evt, u, v, flags, param):                      # clic gauche = nouveau but
    if evt == cv2.EVENT_LBUTTONDOWN:
        buts.append(carte.to_world(u // ECH, carte.n - 1 - v // ECH))

cv2.namedWindow("robot")
cv2.setMouseCallback("robot", clic)

while True:
    # 1. Messages du robot
    for m in link.poll():
        if m[0] == "O" and len(m) >= 8:
            ekf.predict(*odo.update(int(m[3]), int(m[4]), int(m[5])))
        elif m[0] == "S":
            a0, pas, d = int(m[2]), int(m[3]), [int(x) for x in m[4:]]
            carte.add_scan(tuple(ekf.mu), [a0 + pas * k for k in range(len(d))], d)
            etat = "ATTENTE"

    # 2. Recalage par la caméra, deux fois par seconde
    if time.time() - t_cam > 0.5:
        t_cam = time.time()
        try:
            for mid, r, a in aruco_cam.detecter(aruco_cam.lire_image(CAM_URL)):
                if mid in MARQUEURS:
                    ekf.update_landmark(*mesure_vers_robot(r, a), *MARQUEURS[mid])
        except Exception as e:
            print("caméra :", e)

    # 3. Navigation vers le premier but de la liste
    v = w = 0.0
    if buts and etat != "SCAN":
        etat = "ROULE"
        if not chemin:
            bloque = inflate(carte.prob(), 0.12, carte.res)
            cases = astar(bloque, carte.to_cell(*ekf.mu[:2]), carte.to_cell(*buts[0]))
            if cases is None:
                print("but inaccessible, ignoré"); buts.pop(0); continue
            chemin = [carte.to_world(i, j) for i, j in cases[::4]] + [buts[0]]
        v, w, dist = suivre(ekf.mu, chemin[0])
        if dist < 0.05:
            chemin.pop(0)
            if not chemin:                              # but atteint : on balaye avant le suivant
                buts.pop(0); link.send("C"); etat = "SCAN"
    link.send(f"V,{v * 1000:.0f},{w * 1000:.0f}")

    # 4. Affichage
    img = cv2.cvtColor(cv2.resize(carte.image(), None, fx=ECH, fy=ECH,
                                  interpolation=cv2.INTER_NEAREST), cv2.COLOR_GRAY2BGR)
    for k, b in enumerate(buts):
        cv2.drawMarker(img, ecran(*b), (0, 0, 255), cv2.MARKER_CROSS, 14, 2)
        cv2.putText(img, str(k + 1), ecran(*b), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    for p in chemin:
        cv2.circle(img, ecran(*p), 2, (255, 120, 0), -1)
    x, y, th = ekf.mu
    cv2.circle(img, ecran(x, y), 7, (0, 150, 0), 2)
    cv2.line(img, ecran(x, y), ecran(x + 0.15 * math.cos(th), y + 0.15 * math.sin(th)), (0, 150, 0), 2)
    cv2.putText(img, etat, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 200), 2)
    cv2.imshow("robot", img)
    k = cv2.waitKey(50) & 0xFF
    if k == ord("c"):
        link.send("C"); etat = "SCAN"                   # balayage manuel
    elif k == ord("e"):
        cv2.imwrite("mesures/carte_finale.png", img)
    elif k == 27:
        break
link.send("X")
