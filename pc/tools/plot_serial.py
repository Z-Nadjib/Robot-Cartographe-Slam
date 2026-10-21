# Lit le port série (format t_ms,brut,filtre,valide), trace et enregistre un CSV
import csv, sys, time
import numpy as np
import matplotlib.pyplot as plt
import serial

PORT = sys.argv[1] if len(sys.argv) > 1 else "COM3"   # Linux : /dev/ttyUSB0
N = 400                                                # nombre de mesures
ser = serial.Serial(PORT, 115200, timeout=1)
time.sleep(2)
ser.reset_input_buffer()

t, brut, filt = [], [], []
while len(t) < N:
    champs = ser.readline().decode(errors="ignore").strip().split(",")
    if len(champs) != 4:
        continue
    try:
        t.append(int(champs[0])); brut.append(int(champs[1])); filt.append(int(champs[2]))
    except ValueError:
        continue
ser.close()

with open("mesures/tp2_laser.csv", "w", newline="") as f:
    csv.writer(f).writerows([("t_ms", "brut_mm", "filtre_mm"), *zip(t, brut, filt)])

b, m = np.array(brut), np.array(filt)
print(f"brut   : moyenne {b.mean():.1f} mm, écart-type {b.std():.1f} mm")
print(f"filtré : moyenne {m.mean():.1f} mm, écart-type {m.std():.1f} mm")
plt.plot((np.array(t) - t[0]) / 1000, b, color="0.6", lw=1, label="brut")
plt.plot((np.array(t) - t[0]) / 1000, m, lw=2, label="médiane sur 5")
plt.xlabel("temps (s)"); plt.ylabel("distance (mm)"); plt.legend(); plt.grid(alpha=0.3)
plt.savefig("mesures/tp2_laser.png", dpi=150)
plt.show()
