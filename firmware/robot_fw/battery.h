/*
 * battery.h — mesure de la tension batterie (2S : 6,0 V vide -> 8,4 V pleine)
 *
 * Rôle : renvoyer la tension de la batterie en volts.
 *
 * Le pont diviseur 100 kΩ / 33 kΩ ramène 8,4 V à environ 2,08 V, mesurable par
 * l'ADC1 (GPIO 33 : l'ADC2 est inutilisable quand le Wi-Fi est actif).
 *
 * readVbat() : faire 16 lectures avec analogReadMilliVolts(PIN_VBAT) (valeur déjà
 * calibrée en mV par l'ESP32), en faire la moyenne, convertir en volts, multiplier
 * par le rapport du pont (VBAT_RATIO) et par vbatCorr, un facteur de correction
 * ajusté au multimètre au TP8.
 */
#pragma once
#include "config.h"

const float VBAT_RATIO = (100.0f + 33.0f) / 33.0f;   // pont 100 kΩ / 33 kΩ : 8,4 V -> 2,08 V
float vbatCorr = 1.00f;                               // à ajuster avec le multimètre (TP8)

float readVbat() {                                    // en volts, moyenne de 16 lectures
  // À compléter.
  return 0;
}
