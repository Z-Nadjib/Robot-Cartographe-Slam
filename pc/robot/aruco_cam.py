# Détection des marqueurs ArUco et estimation de la distance et de l'angle
import math, sys, urllib.request
import cv2
import numpy as np

TAILLE = 0.10                                   # côté du carré noir imprimé (m)
calib = np.load("calib.npz")
K, DIST = calib["K"], calib["dist"]
# Coins du marqueur dans son propre repère, dans l'ordre renvoyé par OpenCV
OBJ = np.array([[-TAILLE / 2,  TAILLE / 2, 0], [TAILLE / 2,  TAILLE / 2, 0],
                [ TAILLE / 2, -TAILLE / 2, 0], [-TAILLE / 2, -TAILLE / 2, 0]], np.float32)
DETECTEUR = cv2.aruco.ArucoDetector(cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50),
                                    cv2.aruco.DetectorParameters())

def detecter(img):
    """Renvoie [(id, distance_m, angle_rad)] ; angle > 0 = marqueur à gauche de l'axe optique."""
    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coins, ids, _ = DETECTEUR.detectMarkers(gris)
    res = []
    if ids is None:
        return res
    for c, i in zip(coins, ids.flatten()):
        ok, rvec, tvec = cv2.solvePnP(OBJ, c[0], K, DIST, flags=cv2.SOLVEPNP_IPPE_SQUARE)
        if not ok:
            continue
        tx, ty, tz = tvec.flatten()             # repère caméra : x à droite, y en bas, z devant
        res.append((int(i), math.hypot(tx, tz), -math.atan2(tx, tz)))
        cv2.drawFrameAxes(img, K, DIST, rvec, tvec, TAILLE / 2)
    cv2.aruco.drawDetectedMarkers(img, coins, ids)
    return res

def lire_image(src, cap=None):
    """src = URL /capture de l'ESP32-CAM (image la plus récente) ou numéro de webcam."""
    if src.startswith("http"):
        data = urllib.request.urlopen(src, timeout=3).read()
        return cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    ok, img = cap.read()
    return img if ok else None

if __name__ == "__main__":
    SRC = sys.argv[1] if len(sys.argv) > 1 else "0"
    cap = None if SRC.startswith("http") else cv2.VideoCapture(int(SRC))
    while True:
        img = lire_image(SRC, cap)
        if img is None:
            continue
        for i, r, a in detecter(img):
            print(f"marqueur {i} : {r * 100:.1f} cm, {math.degrees(a):+.1f}°")
        cv2.imshow("ArUco", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
