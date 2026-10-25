// config.h — toutes les constantes du robot au même endroit
#pragma once

// ---------- Broches ESP32-DevKitC V4, module WROOM-32E (voir la page Architecture) ----------
#define PIN_SDA    21
#define PIN_SCL    22
#define PIN_SERVO  13
#define PIN_PWMA   25   // moteur gauche
#define PIN_AIN1   26
#define PIN_AIN2   27
#define PIN_PWMB   18   // moteur droit
#define PIN_BIN1   16
#define PIN_BIN2   17
#define PIN_STBY   23
#define PIN_ENC_LA 34   // GPIO 34 à 39 : entrées seules, SANS pull-up interne
#define PIN_ENC_LB 35   //   → résistance de 10 kΩ vers 3,3 V sur chaque signal
#define PIN_ENC_RA 36
#define PIN_ENC_RB 39
#define PIN_VBAT   33   // pont diviseur 100 kΩ / 33 kΩ (ADC1 : compatible Wi-Fi)
#define PIN_LED     2   // LED externe + 220 Ω vers GND (la DevKitC V4 n'a pas de LED utilisateur)

// ---------- Sens (mettre -1 si une roue tourne ou compte à l'envers) ----------
const int MOTOR_L_SIGN = +1, MOTOR_R_SIGN = +1;
const int ENC_L_SIGN   = +1, ENC_R_SIGN   = +1;

// ---------- Géométrie (à mesurer : TP7 et TP8) ----------
const float WHEEL_D_MM    = 65.0;     // diamètre des roues
const float TRACK_MM      = 130.0;    // entraxe : distance entre les deux roues
const float TICKS_PER_REV = 1440.0;   // ticks par tour de roue (mesuré au TP7)
const float MM_PER_TICK   = PI * WHEEL_D_MM / TICKS_PER_REV;

// ---------- Régulation de vitesse ----------
const float    KP = 1.0, KI = 10.0;   // valeurs de départ, calculées au TP7
const uint32_t CTRL_MS = 20;          // période de la boucle de vitesse (50 Hz)
const uint16_t STOP_MM = 150;         // arrêt d'urgence si obstacle plus proche
