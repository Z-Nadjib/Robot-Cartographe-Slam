// TP2 — Scanner du bus I2C : affiche l'adresse de chaque capteur branché
#include <Wire.h>

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);               // SDA, SCL
  delay(200);
  Serial.println("Scan du bus I2C...");
  for (uint8_t a = 1; a < 127; a++) {
    Wire.beginTransmission(a);
    if (Wire.endTransmission() == 0) Serial.printf("  peripherique trouve en 0x%02X\n", a);
  }
  Serial.println("Fin du scan.");   // attendu : 0x29 (VL53L1X), plus tard 0x68 (MPU6050)
}

void loop() {}
