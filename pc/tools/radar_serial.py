# Affiche en direct le radar reçu sur le port série (lignes "S,d0,d1,...")
import sys
import numpy as np
import matplotlib.pyplot as plt
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "COM3"
ANGLES = np.radians(np.arange(0, 181, 3))       # 61 angles : 0°, 3°, …, 180°

def mediane_angulaire(d, k=3):
    """Filtre médian le long de l'angle : supprime les points isolés aberrants."""
    p = np.pad(d, k // 2, mode="edge")
    return np.array([np.nanmedian(p[i:i + k]) for i in range(len(d))])

ser = serial.Serial(PORT, 115200, timeout=1)
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(projection="polar")
ax.set_thetamin(0); ax.set_thetamax(180)
brut, = ax.plot([], [], "o", ms=3, color="0.6", label="brut")
filtre, = ax.plot([], [], "-", lw=2, label="médiane")
ax.legend(loc="lower left")

while plt.fignum_exists(fig.number):
    ligne = ser.readline().decode(errors="ignore").strip()
    if not ligne.startswith("S,"):
        plt.pause(0.01); continue
    d = np.array(ligne.split(",")[1:], float)
    if len(d) != len(ANGLES):
        continue
    d[d == 0] = np.nan                            # 0 = mesure invalide
    brut.set_data(ANGLES, d)
    filtre.set_data(ANGLES, mediane_angulaire(d))
    ax.set_rmax(np.nanmax(d) * 1.1 if np.any(d > 0) else 2000)
    plt.pause(0.01)
