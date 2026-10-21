/*
 * TP3 — Radar 2D sur table : un balayage de 180° envoyé sur le port série
 *
 * But : utiliser scanner.h (machine d'états non bloquante) pour obtenir des
 * balayages complets et les envoyer au PC.
 *
 * Ce que le programme doit faire :
 *   - setup : port série 115200, bus I2C (21/22, 400 kHz), scannerBegin()
 *     (s'arrêter avec un message s'il échoue), puis lancer un premier balayage
 *     avec scanStart().
 *   - loop : appeler scanUpdate() à CHAQUE tour (elle ne bloque jamais). Quand
 *     scanReady passe à vrai : le remettre à faux, envoyer une ligne
 *        S,d0,d1,...,d60
 *     (les SCAN_N distances de scanDist[], en mm) puis relancer scanStart().
 *
 * Le format est celui que lit pc/tools/radar_serial.py.
 * Preuve que rien ne bloque : ajouter un clignotement de LED toutes les 100 ms
 * dans loop() ; il doit rester régulier pendant le balayage.
 */
#include "scanner.h"

void setup() {
  // À compléter.
}

void loop() {
  // À compléter.
}
