# teleop.py — pilotage au clavier (Z Q S D, espace = stop, Échap = quitter)
import math, sys
import cv2
import numpy as np
from link import Link
from odometry import Odometry

MM_PER_TICK, TRACK_MM = 0.1418, 130.0          # recopier les valeurs de config.h
link = Link(sys.argv[1])
odo = Odometry(MM_PER_TICK, TRACK_MM)
v = w = 0
trace, vbat = [], 0.0

while True:
    for m in link.poll():
        if m[0] == "O" and len(m) >= 8:
            odo.update(int(m[3]), int(m[4]), int(m[5]))
            vbat = int(m[7]) / 1000
            trace.append((odo.x, odo.y))
    img = np.full((500, 500, 3), 255, np.uint8)
    for x, y in trace[-3000:]:                  # 1 pixel = 1 cm, départ au centre
        cv2.circle(img, (int(250 + x * 100), int(250 - y * 100)), 1, (200, 80, 0), -1)
    txt = f"x={odo.x:.2f} m  y={odo.y:.2f} m  cap={math.degrees(odo.th):.0f} deg  batt={vbat:.2f} V"
    cv2.putText(img, txt, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.imshow("teleop", img)
    k = cv2.waitKey(50) & 0xFF
    if k == ord("z"):   v, w = 150, 0           # mm/s, mrad/s
    elif k == ord("s"): v, w = -150, 0
    elif k == ord("q"): v, w = 0, 1500
    elif k == ord("d"): v, w = 0, -1500
    elif k == ord(" "): v, w = 0, 0
    elif k == 27: break
    link.send(f"V,{v},{w}")                     # répété à 20 Hz, sinon le robot s'arrête
link.send("X")
