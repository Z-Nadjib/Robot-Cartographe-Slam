/*
 * TP6 — Cap du robot par intégration du gyroscope
 *
 * But : obtenir l'angle de rotation du robot (le cap, en degrés) en intégrant
 * la vitesse de rotation donnée par le gyroscope Z du MPU6050 (imu.h).
 *
 * Ce que le programme doit faire :
 *   - setup : port série, I2C (21/22, 400 kHz), imuBegin() (s'arrêter si le
 *     capteur manque), demander de ne pas bouger, imuCalibrate(), afficher le
 *     biais mesuré (gzBias), mémoriser l'instant de départ avec micros().
 *   - loop :
 *       1. dt = temps écoulé depuis le tour précédent, en secondes (micros()) ;
 *       2. gz = gyroZ() en °/s ;
 *       3. cap += gz * dt   (intégration par la méthode des rectangles) ;
 *       4. toutes les 50 ms, envoyer une ligne CSV  temps_ms,vitesse_deg_s,cap_deg
 *       5. une petite pause de quelques ms pour ne pas saturer le bus.
 *
 * Validation : immobile, le cap dérive de moins de 1° par minute ; un quart de
 * tour à la main donne 90° à ±2° près.
 */
#include "imu.h"

float cap = 0;                  // degrés
uint32_t tPrev;                 // instant du tour précédent (µs)

void setup() {
  // À compléter.
}

void loop() {
  // À compléter.
}
