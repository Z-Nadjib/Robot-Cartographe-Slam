/*
 * TP4 — Radar sans fil : balayages envoyés au PC en UDP + écho pour la latence
 *
 * But : remplacer le câble USB par le Wi-Fi. Même balayage qu'au TP3, mais
 * chaque balayage part en UDP vers le PC (port 5005) et l'ESP32 répond aux
 * pings du PC pour mesurer l'aller-retour.
 *
 * Ce que le programme doit faire :
 *   - sendScan() : construire la ligne
 *        S,seq,angle0,pas,d0,...,d60
 *     avec seq = txSeq++ (numéro qui permet au PC de compter les pertes),
 *     angle0 = SCAN_MIN, pas = SCAN_STEP, puis les SCAN_N distances ;
 *     l'envoyer avec sendLine().
 *   - setup : port série, I2C (21/22, 400 kHz), wifiBegin(), scannerBegin(),
 *     premier scanStart().
 *   - loop :
 *       1. lire toutes les commandes arrivées (while readCommand(...)) ; si une
 *          commande commence par 'P', la renvoyer telle quelle (écho) ;
 *       2. scanUpdate() ;
 *       3. si scanReady : le remettre à faux, sendScan(), scanStart().
 *
 * Côté PC : pc/tools/udp_radar.py affiche le radar, les pertes et la latence.
 */
#include "scanner.h"
#include "comms.h"

void sendScan() {
  // À compléter.
}

void setup() {
  // À compléter.
}

void loop() {
  // À compléter.
}
