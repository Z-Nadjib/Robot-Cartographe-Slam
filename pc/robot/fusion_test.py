# fusion_test.py — TP11 : compare odométrie seule et EKF pendant un trajet téléopéré
import json, math, sys, time
import cv2
import numpy as np
from link import Link
from odometry import Odometry
from ekf import EKF, mesure_vers_robot
import aruco_cam

ROBOT_IP, CAM_URL = sys.argv[1], sys.argv[2]   # ex. 192.168.43.50  http://192.168.43.51/capture
MARQUEURS = {int(k): v for k, v in json.load(open("markers.json")).items()}
link, odo, ekf = Link(ROBOT_IP), Odometry(0.1418, 130.0), EKF()
v = w = 0
t_cam, journal = 0.0, []

while True:
    for m in link.poll():
        if m[0] == "O" and len(m) >= 8:
            d, dth = odo.update(int(m[3]), int(m[4]), int(m[5]))
            ekf.predict(d, dth)
            journal.append((odo.x, odo.y, *ekf.mu))
    if time.time() - t_cam > 0.5:                 # 2 images par seconde suffisent
        t_cam = time.time()
        try:
            img = aruco_cam.lire_image(CAM_URL)
            for mid, r, a in aruco_cam.detecter(img):
                if mid in MARQUEURS:
                    ok = ekf.update_landmark(*mesure_vers_robot(r, a), *MARQUEURS[mid])
                    print(f"marqueur {mid} : {'accepté' if ok else 'rejeté'}")
            cv2.imshow("camera", img)
        except Exception as e:
            print("caméra :", e)
    k = cv2.waitKey(30) & 0xFF
    if k == ord("z"):   v, w = 150, 0
    elif k == ord("s"): v, w = -150, 0
    elif k == ord("q"): v, w = 0, 1500
    elif k == ord("d"): v, w = 0, -1500
    elif k == ord(" "): v, w = 0, 0
    elif k == 27: break
    link.send(f"V,{v},{w}")
link.send("X")
np.savetxt("mesures/tp11_trajets.csv", np.array(journal), delimiter=",",
           header="odo_x,odo_y,ekf_x,ekf_y,ekf_th", comments="")
