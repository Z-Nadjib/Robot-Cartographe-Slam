# Réponse indicielle en boucle ouverte → modèle du 1er ordre (K, tau) → réglage du PI
import sys
import numpy as np
import matplotlib.pyplot as plt

d = np.loadtxt(sys.argv[1], delimiter=",")       # t_ms,consigne,vG,vD,pwmG,pwmD
t = (d[:, 0] - d[0, 0]) / 1000
v = (d[:, 2] + d[:, 3]) / 2
pwm = d[:, 4].max()

v_inf = v[t > 0.6 * t[-1]].mean()                # vitesse finale
tau = t[np.argmax(v >= 0.63 * v_inf)]            # temps pour atteindre 63 %
K = v_inf / pwm
print(f"K = {K:.2f} (mm/s) par unité de PWM, tau = {tau * 1000:.0f} ms")

tau_bf = tau / 2                                 # boucle fermée 2 fois plus rapide
Kp = tau / (K * tau_bf)
Ki = Kp / tau                                    # le zéro du PI compense le pôle du moteur
print(f"Proposition : KP = {Kp:.2f}, KI = {Ki:.1f}  (à recopier dans config.h)")

plt.plot(t, v, label="mesure")
plt.plot(t, v_inf * (1 - np.exp(-t / tau)), "--", label="modèle 1er ordre")
plt.xlabel("t (s)"); plt.ylabel("vitesse (mm/s)"); plt.legend(); plt.grid(alpha=0.3)
plt.show()
