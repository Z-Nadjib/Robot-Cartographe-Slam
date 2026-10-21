/*
 * scanner.h — balayage servo + laser, NON bloquant (réutilisé jusqu'au TP12)
 *
 * Rôle : faire tourner le servo de SCAN_MIN à SCAN_MAX par pas de SCAN_STEP et
 * prendre une distance à chaque angle, sans jamais bloquer loop(). Hors
 * balayage, le servo reste à 90° et frontMm donne la distance devant le robot
 * (utilisée pour l'arrêt d'urgence).
 *
 * Servo : PWM 50 Hz (période 20 ms) en 14 bits, donc 20 ms = 16384 pas.
 * La largeur d'impulsion va de SERVO_US_MIN (0°) à SERVO_US_MAX (180°) :
 *   us    = SERVO_US_MIN + (SERVO_US_MAX - SERVO_US_MIN) * deg / 180
 *   duty  = us * 16383 / 20000
 *
 * Machine d'états (une vérification rapide par appel de scanUpdate) :
 *   SC_IDLE    servo au centre : si une mesure est prête, la lire dans frontMm
 *              (0 si la mesure n'est pas valide) ;
 *   SC_SETTLE  attendre que le servo soit arrivé : SETTLE_MS (400 ms pour le
 *              premier angle, qui part de 90°) -> SC_FLUSH ;
 *   SC_FLUSH   jeter la mesure commencée pendant le mouvement -> SC_MEASURE ;
 *   SC_MEASURE lire la mesure (0 si invalide) dans scanDist[scIndex] ; si c'était
 *              le dernier angle : servo à 90°, SC_IDLE, scanReady = true ;
 *              sinon : angle suivant, noter l'instant, SC_SETTLE.
 * Pour savoir si une mesure est prête sans attendre : tof.dataReady(), puis
 * tof.read(false) ; validité : tof.ranging_data.range_status == VL53L1X::RangeValid.
 */
#pragma once
#include <Wire.h>
#include <VL53L1X.h>

#ifndef PIN_SERVO
#define PIN_SERVO 13
#endif
const uint8_t  SERVO_CH     = 2;        // canal LEDC n°2 (timer 1, différent des moteurs)
const float    SERVO_US_MIN = 500;      // largeur d'impulsion à 0°   (à calibrer)
const float    SERVO_US_MAX = 2400;     // largeur d'impulsion à 180° (à calibrer)
const int      SCAN_MIN = 0, SCAN_MAX = 180, SCAN_STEP = 3;
const uint32_t SETTLE_MS = 25;          // temps d'arrivée du servo pour 3°
const int      SCAN_N = (SCAN_MAX - SCAN_MIN) / SCAN_STEP + 1;   // 61 points

VL53L1X  tof;
uint16_t scanDist[SCAN_N];              // résultat en mm (0 = mesure invalide)
bool     scanReady = false;             // vrai quand un balayage complet est disponible
uint16_t frontMm = 0;                   // hors balayage : distance devant le robot (servo à 90°)

enum { SC_IDLE, SC_SETTLE, SC_FLUSH, SC_MEASURE } scState = SC_IDLE;
int scIndex = 0;                        // indice de l'angle en cours
uint32_t scT0 = 0;                      // instant de la dernière commande du servo

// Place le servo à « deg » degrés (borné entre 0 et 180).
void servoWriteDeg(float deg) {
  // À compléter : formule de la largeur d'impulsion, puis ledcWrite.
}

// Configure la PWM du servo (ledcAttachChannel, 50 Hz, 14 bits, SERVO_CH), le
// met au centre, puis initialise le capteur : timeout 500 ms, mode Long,
// budget 33 ms, mesures continues toutes les 33 ms. Renvoie false si le
// capteur ne répond pas.
bool scannerBegin() {
  // À compléter.
  return false;
}

// Démarre un balayage : remet scanReady à faux et l'indice à 0, envoie le servo
// au premier angle, note l'instant et passe en SC_SETTLE.
void scanStart() {
  // À compléter.
}

bool scanBusy() { return scState != SC_IDLE; }

// À appeler à chaque tour de loop() : fait avancer la machine d'états.
void scanUpdate() {
  // À compléter : un « case » par état, comme décrit en tête de fichier.
}
