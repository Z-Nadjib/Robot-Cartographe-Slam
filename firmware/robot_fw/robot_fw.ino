/*
 * robot_fw.ino — firmware complet du robot (TP9 -> TP13)
 *
 * Rôle : assembler toutes les briques des TPs précédents. L'ESP32 ne fait que le
 * temps réel ; tout le reste (carte, vision, Kalman, A*) tourne sur le PC.
 *
 * Protocole (une ligne de texte par datagramme UDP) :
 *   PC -> robot  V,v_mm_s,w_mrad_s   consigne de vitesse d'avance et de rotation
 *                M,pwmG,pwmD         commande directe des moteurs (tests)
 *                C                   lancer un balayage (ignoré s'il y en a déjà un)
 *                X                   arrêt : consignes à zéro, moteurs coupés
 *                P,...               ping : renvoyer la ligne telle quelle
 *   robot -> PC  O,seq,t_ms,ticksG,ticksD,cap_mdeg,avant_mm,vbat_mV   à 20 Hz
 *                S,seq,angle0,pas,d0,...,d60                         après un balayage
 *
 * À implémenter :
 *   handleCommand(c)  décoder la commande (sscanf convient) et mettre à jour
 *                     vRef (mm/s), wRef (rad/s : reçu en mrad/s), direct, pwmDir*.
 *   controlStep(dt)   appelée toutes les CTRL_MS :
 *       1. vitesses mesurées des roues (ticks -> mm/s, comme au TP7) ;
 *       2. intégrer le cap : headingDeg += gyroZ() * dt ;
 *       3. chien de garde : plus de commande depuis 500 ms -> consignes à zéro ;
 *       4. en mode direct, appliquer pwmDirL/R et s'arrêter là ;
 *       5. sécurité : ne pas avancer si 0 < frontMm < STOP_MM ;
 *       6. consignes nulles -> remettre les PI à zéro et couper les moteurs ;
 *       7. cinématique différentielle :
 *            refL = v - w * TRACK_MM / 2      refR = v + w * TRACK_MM / 2
 *          puis setMotors(piL.update(refL, vL, dt), piR.update(refR, vR, dt)).
 *   sendOdom(now)     construire et envoyer le message O (snprintf) : cap en
 *                     millidegrés, tension batterie en mV.
 *   sendScan()        construire et envoyer le message S (comme au TP4).
 *   setup()           série, LED, I2C 400 kHz, moteurs, encodeurs, IMU, scanner
 *                     (messages d'erreur si un capteur manque), calibration du
 *                     gyroscope ROBOT IMMOBILE, Wi-Fi, LED allumée = prêt.
 *   loop()            traiter toutes les commandes reçues ; controlStep toutes
 *                     les CTRL_MS ; sendOdom toutes les 50 ms ; scanUpdate() ;
 *                     envoyer le balayage quand scanReady.
 */
#include "config.h"
#include "motors.h"
#include "encoders.h"
#include "speed_pi.h"
#include "imu.h"
#include "scanner.h"
#include "comms.h"
#include "battery.h"

SpeedPI piL, piR;
float vRef = 0, wRef = 0;          // consignes reçues : mm/s et rad/s
int   pwmDirL = 0, pwmDirR = 0;    // commande directe (tests)
bool  direct = false;
float headingDeg = 0;              // cap intégré à 50 Hz à partir du gyroscope

void handleCommand(char* c) {
  // À compléter.
}

void controlStep(float dt) {
  // À compléter.
}

void sendOdom(uint32_t now) {
  // À compléter.
}

void sendScan() {
  // À compléter.
}

void setup() {
  // À compléter.
}

void loop() {
  // À compléter.
}
