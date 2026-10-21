/*
 * comms.h — Wi-Fi + UDP en texte (robot -> PC : port 5005, PC -> robot : port 5006)
 *
 * Rôle : connecter l'ESP32 au réseau Wi-Fi (partage de connexion d'un téléphone
 * en 2,4 GHz) et échanger des lignes de texte avec le PC, une ligne par datagramme.
 *
 * À implémenter :
 *   wifiBegin()   mode station, économie d'énergie DÉSACTIVÉE (latence plus
 *                 faible), connexion avec WIFI_SSID / WIFI_PASS, attente de la
 *                 connexion en affichant des points, affichage de l'IP obtenue
 *                 (le PC en a besoin), puis écoute UDP sur PORT_RX.
 *   sendLine(s)   envoyer la chaîne s dans un datagramme vers pcIP:PORT_TX.
 *   readCommand() si un datagramme est arrivé : retenir l'adresse de l'expéditeur
 *                 dans pcIP (on répond à l'ordinateur qui nous parle), copier le
 *                 texte dans buf en le terminant par '\0', noter l'instant dans
 *                 lastCmdMs (chien de garde) et renvoyer true ; sinon false.
 *
 * Classes utiles : WiFi (mode, setSleep, begin, status, localIP) et WiFiUDP
 * (begin, beginPacket, print, endPacket, parsePacket, read, remoteIP).
 */
#pragma once
#include <WiFi.h>
#include <WiFiUdp.h>

const char* WIFI_SSID = "MonPartage";        // partage de connexion du téléphone, en 2,4 GHz
const char* WIFI_PASS = "motdepasse";
IPAddress   pcIP(192, 168, 43, 100);         // IP du PC (remplacée dès qu'une commande arrive)
const uint16_t PORT_TX = 5005, PORT_RX = 5006;

WiFiUDP  udp;
uint32_t txSeq = 0;                          // numéro de message : détecte les pertes
uint32_t lastCmdMs = 0;                      // instant de la dernière commande reçue

void wifiBegin() {
  // À compléter.
}

void sendLine(const String& s) {
  // À compléter.
}

// Renvoie true et remplit buf si une commande est arrivée
bool readCommand(char* buf, size_t len) {
  // À compléter.
  return false;
}
