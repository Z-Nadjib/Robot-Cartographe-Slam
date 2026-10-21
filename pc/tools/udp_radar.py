# TP4 — Reçoit les balayages en UDP, affiche le radar, compte les pertes, mesure la latence
import socket, sys, time
import numpy as np
import matplotlib.pyplot as plt

ROBOT_IP = sys.argv[1]                         # IP affichée par l'ESP32 sur le moniteur série
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5005))
sock.setblocking(False)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(projection="polar")
ax.set_thetamin(0); ax.set_thetamax(180)
pts, = ax.plot([], [], "o", ms=4)
dernier, perdus, recus, rtts, t_ping = None, 0, 0, [], 0.0

while plt.fignum_exists(fig.number):
    if time.time() - t_ping > 1:               # un ping par seconde
        t_ping = time.time()
        sock.sendto(f"P,{time.perf_counter()}".encode(), (ROBOT_IP, 5006))
    try:
        data, _ = sock.recvfrom(2048)
    except (BlockingIOError, ConnectionResetError):
        plt.pause(0.02); continue
    f = data.decode(errors="ignore").strip().split(",")
    if f[0] == "P":
        rtts.append((time.perf_counter() - float(f[1])) * 1000)
        print(f"aller-retour : {rtts[-1]:.1f} ms (moyenne {np.mean(rtts):.1f} ms)")
    elif f[0] == "S":
        seq, a0, pas = int(f[1]), int(f[2]), int(f[3])
        d = np.array(f[4:], float); d[d == 0] = np.nan
        if dernier is not None and seq > dernier + 1:
            perdus += seq - dernier - 1
        dernier, recus = seq, recus + 1
        pts.set_data(np.radians(a0 + pas * np.arange(len(d))), d)
        ax.set_rmax(np.nanmax(d) * 1.1 if np.any(d > 0) else 2000)
        ax.set_title(f"balayage n°{seq} · perdus : {perdus}/{recus + perdus}")
        plt.pause(0.01)
