# Calibration de la caméra avec un damier de 9 x 6 coins intérieurs
import sys, urllib.request
import cv2
import numpy as np

SRC = sys.argv[1] if len(sys.argv) > 1 else "0"   # "0" = webcam, ou http://IP_CAM/capture
COINS, CARRE = (9, 6), 0.025                       # côté d'une case en mètres : MESUREZ-LE

def lire_image(cap):
    if SRC.startswith("http"):
        data = urllib.request.urlopen(SRC, timeout=3).read()
        return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    ok, img = cap.read()
    return img if ok else None

cap = None if SRC.startswith("http") else cv2.VideoCapture(int(SRC))
objp = np.zeros((COINS[0] * COINS[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:COINS[0], 0:COINS[1]].T.reshape(-1, 2) * CARRE
obj_pts, img_pts, gris = [], [], None
print("ESPACE = garder l'image, Q = calculer (15 à 25 images, angles et distances variés)")

while True:
    img = lire_image(cap)
    if img is None:
        continue
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ok, coins = cv2.findChessboardCorners(gris, COINS)
    vue = img.copy()
    if ok:
        cv2.drawChessboardCorners(vue, COINS, coins, ok)
    cv2.putText(vue, f"images : {len(obj_pts)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("calibration", vue)
    k = cv2.waitKey(30) & 0xFF
    if k == ord(" ") and ok:
        coins = cv2.cornerSubPix(gris, coins, (11, 11), (-1, -1),
                                 (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001))
        obj_pts.append(objp); img_pts.append(coins)
    elif k == ord("q") and len(obj_pts) >= 10:
        break

err, K, dist, _, _ = cv2.calibrateCamera(obj_pts, img_pts, gris.shape[::-1], None, None)
np.savez("calib.npz", K=K, dist=dist)
print(f"Erreur de reprojection : {err:.3f} px (bon si < 0,5 ; acceptable si < 1)")
print("Matrice K :\n", K)
