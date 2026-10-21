// TP6 — Cap du robot par intégration du gyroscope
#include "imu.h"

float cap = 0;                  // degrés
uint32_t tPrev;

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  Wire.setClock(400000);
  if (!imuBegin()) { Serial.println("MPU6050 introuvable"); while (true) delay(100); }
  Serial.println("Ne pas bouger : calibration...");
  imuCalibrate();
  Serial.printf("biais = %.3f deg/s\n", gzBias);
  tPrev = micros();
}

void loop() {
  uint32_t now = micros();
  float dt = (now - tPrev) * 1e-6f;
  tPrev = now;
  float gz = gyroZ();
  cap += gz * dt;               // intégration (méthode des rectangles)

  static uint32_t tLog = 0;
  if (millis() - tLog >= 50) {  // CSV : temps_ms,vitesse_deg_s,cap_deg
    tLog = millis();
    Serial.printf("%lu,%.2f,%.2f\n", millis(), gz, cap);
  }
  delay(5);
}
