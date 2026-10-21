# Génère 8 marqueurs ArUco (dictionnaire 4x4_50) à imprimer
import cv2

d = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
for i in range(8):
    m = cv2.aruco.generateImageMarker(d, i, 600)          # carré noir de 600 px
    m = cv2.copyMakeBorder(m, 120, 120, 120, 120, cv2.BORDER_CONSTANT, value=255)
    cv2.putText(m, f"ID {i}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, 0, 3)
    cv2.imwrite(f"marker_{i}.png", m)
print("Imprimer à 100 % puis mesurer : le carré noir doit faire exactement 10 cm.")
