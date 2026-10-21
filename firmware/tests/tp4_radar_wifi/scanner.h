// scanner.h — balayage servo + laser, NON bloquant (réutilisé jusqu'au TP12)
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
int scIndex = 0;
uint32_t scT0 = 0;

void servoWriteDeg(float deg) {         // PWM 50 Hz, 14 bits : 20 ms = 16384 pas
  deg = constrain(deg, 0, 180);
  float us = SERVO_US_MIN + (SERVO_US_MAX - SERVO_US_MIN) * deg / 180.0f;
  ledcWrite(PIN_SERVO, (uint32_t)(us * 16383.0f / 20000.0f));
}

bool scannerBegin() {
  ledcAttachChannel(PIN_SERVO, 50, 14, SERVO_CH);
  servoWriteDeg(90);
  tof.setTimeout(500);
  if (!tof.init()) return false;
  tof.setDistanceMode(VL53L1X::Long);
  tof.setMeasurementTimingBudget(33000);   // 33 ms : compromis vitesse / bruit
  tof.startContinuous(33);
  return true;
}

void scanStart() {
  scanReady = false;
  scIndex = 0;
  servoWriteDeg(SCAN_MIN);
  scT0 = millis();
  scState = SC_SETTLE;
}

bool scanBusy() { return scState != SC_IDLE; }

void scanUpdate() {                     // à appeler à chaque tour de loop()
  switch (scState) {
    case SC_IDLE:                       // servo au centre : on surveille l'avant
      if (tof.dataReady()) {
        uint16_t d = tof.read(false);
        frontMm = (tof.ranging_data.range_status == VL53L1X::RangeValid) ? d : 0;
      }
      break;
    case SC_SETTLE:                     // attendre que le servo soit arrivé
      if (millis() - scT0 >= (scIndex == 0 ? 400 : SETTLE_MS)) scState = SC_FLUSH;
      break;
    case SC_FLUSH:                      // jeter la mesure commencée pendant le mouvement
      if (tof.dataReady()) { tof.read(false); scState = SC_MEASURE; }
      break;
    case SC_MEASURE:
      if (tof.dataReady()) {
        uint16_t d = tof.read(false);
        scanDist[scIndex] = (tof.ranging_data.range_status == VL53L1X::RangeValid) ? d : 0;
        if (++scIndex >= SCAN_N) {      // fin du balayage
          servoWriteDeg(90);
          scState = SC_IDLE;
          scanReady = true;
        } else {
          servoWriteDeg(SCAN_MIN + scIndex * SCAN_STEP);
          scT0 = millis();
          scState = SC_SETTLE;
        }
      }
      break;
  }
}
