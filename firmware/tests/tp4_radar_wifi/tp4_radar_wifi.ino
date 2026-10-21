// TP4 — Radar sans fil : balayages envoyés au PC en UDP + écho pour mesurer la latence
#include "scanner.h"
#include "comms.h"

void sendScan() {
  String s = "S," + String(txSeq++) + "," + String(SCAN_MIN) + "," + String(SCAN_STEP);
  for (int i = 0; i < SCAN_N; i++) s += "," + String(scanDist[i]);
  sendLine(s);
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  Wire.setClock(400000);
  wifiBegin();
  if (!scannerBegin()) { Serial.println("VL53L1X introuvable"); while (true) delay(100); }
  scanStart();
}

void loop() {
  char cmd[64];
  while (readCommand(cmd, sizeof cmd)) {
    if (cmd[0] == 'P') sendLine(String(cmd));   // ping : renvoyé tel quel au PC
  }
  scanUpdate();
  if (scanReady) { scanReady = false; sendScan(); scanStart(); }
}
