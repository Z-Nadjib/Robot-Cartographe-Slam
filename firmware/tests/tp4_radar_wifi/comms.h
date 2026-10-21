// comms.h — Wi-Fi + UDP en texte (robot → PC : port 5005, PC → robot : port 5006)
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
  WiFi.mode(WIFI_STA);
  WiFi.setSleep(false);                      // pas d'économie d'énergie : latence plus faible
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connexion Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) { delay(300); Serial.print('.'); }
  Serial.printf("\nConnecte. IP du robot : %s\n", WiFi.localIP().toString().c_str());
  udp.begin(PORT_RX);
}

void sendLine(const String& s) {
  udp.beginPacket(pcIP, PORT_TX);
  udp.print(s);
  udp.endPacket();
}

// Renvoie true et remplit buf si une commande est arrivée
bool readCommand(char* buf, size_t len) {
  int n = udp.parsePacket();
  if (n <= 0) return false;
  pcIP = udp.remoteIP();                     // on répond à l'ordinateur qui nous parle
  int r = udp.read(buf, len - 1);
  buf[r > 0 ? r : 0] = '\0';
  lastCmdMs = millis();
  return true;
}
