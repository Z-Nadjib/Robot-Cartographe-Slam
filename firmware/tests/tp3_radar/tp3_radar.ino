// TP3 — Radar 2D sur table : un balayage de 180° envoyé sur le port série
#include "scanner.h"

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  Wire.setClock(400000);
  if (!scannerBegin()) { Serial.println("VL53L1X introuvable"); while (true) delay(100); }
  scanStart();
}

void loop() {
  scanUpdate();                       // ne bloque jamais : la loop reste libre
  if (scanReady) {
    scanReady = false;
    Serial.print("S");                // une ligne par balayage : S,d0,d1,...,d60
    for (int i = 0; i < SCAN_N; i++) { Serial.print(','); Serial.print(scanDist[i]); }
    Serial.println();
    scanStart();
  }
}
