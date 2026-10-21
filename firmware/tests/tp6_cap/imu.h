// imu.h — MPU6050 sans bibliothèque : vitesse de rotation autour de l'axe vertical Z
#pragma once
#include <Wire.h>

const uint8_t MPU = 0x68;      // AD0 relié à GND
float gzBias = 0;              // biais du gyroscope (°/s), mesuré au repos

void mpuWrite(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(MPU);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission();
}

int16_t mpuRead16(uint8_t reg) {
  Wire.beginTransmission(MPU);
  Wire.write(reg);
  Wire.endTransmission(false);             // « repeated start »
  Wire.requestFrom(MPU, (uint8_t)2);
  uint8_t hi = Wire.read();                // deux lectures séparées : l'ordre est garanti
  uint8_t lo = Wire.read();
  return (int16_t)((hi << 8) | lo);
}

float gyroZraw() { return mpuRead16(0x47) / 131.0f; }   // ±250 °/s → 131 LSB par °/s

bool imuBegin() {
  Wire.beginTransmission(MPU);
  if (Wire.endTransmission() != 0) return false;
  mpuWrite(0x6B, 0x00);        // PWR_MGMT_1 : sortie du mode veille
  mpuWrite(0x1A, 0x03);        // CONFIG : filtre passe-bas numérique ≈ 44 Hz
  mpuWrite(0x1B, 0x00);        // GYRO_CONFIG : ±250 °/s
  delay(100);
  return true;
}

void imuCalibrate(int n = 500) {           // le capteur doit être IMMOBILE (~1 s)
  double s = 0;
  for (int i = 0; i < n; i++) { s += gyroZraw(); delay(2); }
  gzBias = s / n;
}

// °/s ; positif = rotation vers la gauche vue de dessus (module à plat, composants en haut)
float gyroZ() { return gyroZraw() - gzBias; }
