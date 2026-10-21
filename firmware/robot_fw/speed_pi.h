/*
 * speed_pi.h — régulateur PI de vitesse (mm/s -> commande PWM)
 *
 * Rôle : calculer la commande PWM d'une roue pour que sa vitesse mesurée suive
 * la consigne. Un objet SpeedPI par roue.
 *
 * update(consigne, mesure, dt) :
 *   e = consigne - mesure
 *   u = KP * e + intégrale + KI * e * dt
 *   anti-emballement : n'ajouter KI * e * dt à l'intégrale QUE si u n'est pas
 *   saturée (-255 < u < 255), sinon l'intégrale grossit sans effet et provoque
 *   un gros dépassement quand la saturation cesse ;
 *   renvoyer u bornée à ±255.
 * reset() : remettre l'intégrale à zéro (changement de consigne, arrêt).
 *
 * KP et KI sont dans config.h ; pc/tools/analyse_echelon.py propose des valeurs
 * à partir de la réponse indicielle du moteur (TP7).
 */
#pragma once
#include "config.h"

struct SpeedPI {
  float integ = 0;
  float update(float consigne, float mesure, float dt) {
    // À compléter.
    return 0;
  }
  void reset() { integ = 0; }
};
