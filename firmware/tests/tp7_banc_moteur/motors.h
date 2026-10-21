/*
 * motors.h — pont en H TB6612FNG : commande signée de -255 à +255 par roue
 *
 * Rôle : traduire une commande signée par roue en signaux pour le TB6612.
 *
 * Table de vérité d'une voie du TB6612 :
 *   IN1 = 1, IN2 = 0 : un sens      IN1 = 0, IN2 = 1 : l'autre sens
 *   IN1 = 0, IN2 = 0 : roue libre   PWM : rapport cyclique = vitesse
 *   STBY = 0 : tout le pont est coupé (état sûr au démarrage)
 *
 * À implémenter :
 *   motorsBegin()       broches IN1/IN2/STBY en sortie et à 0 ; PWMA sur le canal
 *                       LEDC 0 et PWMB sur le canal 1 (même timer), à PWM_FREQ
 *                       et PWM_BITS (ledcAttachChannel).
 *   driveOne(...)       borner la commande à ±255, fixer IN1/IN2 selon le signe,
 *                       écrire |commande| sur la PWM.
 *   setMotors(g, d)     sortir du mode veille (STBY à 1) et piloter les deux voies
 *                       en appliquant MOTOR_L_SIGN / MOTOR_R_SIGN (config.h) pour
 *                       qu'une commande positive fasse toujours avancer la roue.
 *   motorsOff()         commandes à zéro puis STBY à 0.
 */
#pragma once
#include "config.h"

const uint32_t PWM_FREQ = 20000;   // 20 kHz : au-dessus de l'audible
const uint8_t  PWM_BITS = 8;       // rapport cyclique de 0 à 255

void motorsBegin() {
  // À compléter.
}

static void driveOne(int in1, int in2, int pwmPin, int cmd) {
  // À compléter.
}

void setMotors(int left, int right) {
  // À compléter.
}

void motorsOff() {
  // À compléter.
}
