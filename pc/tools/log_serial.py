# Enregistre les lignes CSV du port série pendant N secondes
# usage : python log_serial.py COM3 mesures/echelon.csv 4 "p 150"
import sys, time
import serial

port, fichier, duree = sys.argv[1], sys.argv[2], float(sys.argv[3])
ser = serial.Serial(port, 115200, timeout=0.5)
time.sleep(2)                                   # l'ESP32 redémarre à l'ouverture du port
ser.reset_input_buffer()
if len(sys.argv) > 4:
    ser.write((sys.argv[4] + "\n").encode())    # commande à envoyer au départ (ex. "p 150")

t0, n = time.time(), 0
with open(fichier, "w") as f:
    while time.time() - t0 < duree:
        l = ser.readline().decode(errors="ignore").strip()
        if l and l[0].isdigit():
            f.write(l + "\n"); n += 1
ser.write(b"s\n")                               # arrêt des moteurs
print(n, "lignes enregistrées dans", fichier)
