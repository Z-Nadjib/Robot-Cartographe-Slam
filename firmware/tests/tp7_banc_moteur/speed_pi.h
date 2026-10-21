// speed_pi.h — régulateur PI de vitesse (mm/s → commande PWM)
#pragma once
#include "config.h"

struct SpeedPI {
  float integ = 0;
  float update(float consigne, float mesure, float dt) {
    float e = consigne - mesure;
    float u = KP * e + integ + KI * e * dt;
    if (u > -255 && u < 255) integ += KI * e * dt;   // anti-emballement : pas d'intégration en saturation
    return constrain(u, -255, 255);
  }
  void reset() { integ = 0; }
};
