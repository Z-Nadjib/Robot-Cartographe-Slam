// battery.h — mesure de la tension batterie (2S : 6,0 V vide → 8,4 V pleine)
#pragma once
#include "config.h"

const float VBAT_RATIO = (100.0f + 33.0f) / 33.0f;   // pont 100 kΩ / 33 kΩ : 8,4 V → 2,08 V
float vbatCorr = 1.00f;                               // à ajuster avec le multimètre (TP8)

float readVbat() {                                    // en volts, moyenne de 16 lectures
  uint32_t mv = 0;
  for (int i = 0; i < 16; i++) mv += analogReadMilliVolts(PIN_VBAT);
  return (mv / 16.0f) / 1000.0f * VBAT_RATIO * vbatCorr;
}
