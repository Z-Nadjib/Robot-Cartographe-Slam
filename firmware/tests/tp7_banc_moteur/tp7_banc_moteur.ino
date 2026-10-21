/*
 * TP7 — Banc moteur (roues en l'air) : boucle ouverte, réponse indicielle, PI
 *
 * But : piloter les moteurs depuis le moniteur série, mesurer la vitesse des
 * roues avec les encodeurs, enregistrer une réponse indicielle puis tester le
 * régulateur PI.
 *
 * Commandes reçues sur le port série (une par ligne) :
 *   p <pwm>   boucle OUVERTE : même PWM sur les deux roues (ex. « p 150 »)
 *   v <mm/s>  boucle FERMÉE  : consigne de vitesse pour les deux PI (remis à zéro)
 *   t         afficher les ticks cumulés des deux encodeurs
 *   autre     arrêt (mode STOP)
 *
 * lireCommande() : si une ligne est disponible, la lire jusqu'à '\n', la nettoyer
 * (trim) puis mettre à jour « mode » et « consigne » selon la première lettre.
 *
 * loop() : appeler lireCommande(), puis toutes les CTRL_MS millisecondes :
 *   1. dt en secondes depuis le dernier calcul ;
 *   2. vitesses vL, vR en mm/s = (ticks actuels - ticks précédents) * MM_PER_TICK / dt ;
 *   3. commande : OUVERT -> uL = uR = consigne ; FERME -> piL.update / piR.update ;
 *      STOP -> motorsOff(), sinon setMotors(uL, uR) ;
 *   4. hors STOP, envoyer une ligne CSV  temps_ms,consigne,vG,vD,pwmG,pwmD
 *      (lue par pc/tools/log_serial.py puis pc/tools/analyse_echelon.py).
 */
#include "config.h"
#include "motors.h"
#include "encoders.h"
#include "speed_pi.h"

SpeedPI piL, piR;
enum { STOP, OUVERT, FERME } mode = STOP;
float consigne = 0;                 // PWM (mode OUVERT) ou mm/s (mode FERME)

void lireCommande() {
  // À compléter.
}

void setup() {
  Serial.begin(115200);
  motorsBegin();
  encodersBegin();
  Serial.println("Commandes : p <pwm> | v <mm/s> | t (ticks) | s (stop)");
}

void loop() {
  lireCommande();
  // À compléter : calcul périodique (CTRL_MS), vitesses, commande, ligne CSV.
}
