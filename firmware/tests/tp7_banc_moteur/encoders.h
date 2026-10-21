/*
 * encoders.h — comptage des encodeurs en quadrature (x4) par interruptions
 *
 * Rôle : compter les ticks de chaque roue, avec leur signe, en décodant les
 * deux signaux A et B décalés de 90°.
 *
 * Principe du décodage x4 : à chaque front (montant ou descendant) de A OU de B,
 * on lit l'état AB (2 bits). L'index = (ancien état << 2) | nouvel état (4 bits)
 * donne, dans une table de 16 cases, +1, -1 ou 0 (transition impossible ou
 * parasite). Construire la table QDEC à partir de la séquence 00 -> 01 -> 11 -> 10
 * (un sens) et de la séquence inverse (l'autre sens).
 *
 * À implémenter :
 *   isrL() / isrR()   IRAM_ATTR : mettre à jour l'état (garder 4 bits) et ajouter
 *                     QDEC[état] au compteur de la roue.
 *   encodersBegin()   les 4 broches en INPUT (GPIO 34 à 39 n'ont PAS de pull-up
 *                     interne : résistance de 10 kΩ vers 3,3 V obligatoire) et une
 *                     interruption CHANGE sur chacune des 4 broches.
 *   getTicksL/R()     compteur multiplié par ENC_L_SIGN / ENC_R_SIGN (config.h).
 */
#pragma once
#include "config.h"

// Table de décodage : index = (ancien état AB << 2) | nouvel état AB
static const int8_t QDEC[16] = { 0 };   // À compléter : 16 valeurs parmi +1, -1, 0
volatile int32_t ticksL = 0, ticksR = 0;
volatile uint8_t stL = 0, stR = 0;

void IRAM_ATTR isrL() {
  // À compléter.
}
void IRAM_ATTR isrR() {
  // À compléter.
}

void encodersBegin() {
  // À compléter.
}

int32_t getTicksL() { return 0; }   // À compléter (lecture 32 bits : atomique sur ESP32)
int32_t getTicksR() { return 0; }   // À compléter
