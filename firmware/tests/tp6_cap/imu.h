/*
 * imu.h — MPU6050 sans bibliothèque : vitesse de rotation autour de l'axe vertical Z
 *
 * Rôle : dialoguer directement avec les registres du MPU6050 en I2C (adresse
 * 0x68) pour lire le gyroscope Z en °/s, corrigé de son biais.
 *
 * Registres utiles (fiche « MPU-6000 Register Map ») :
 *   0x6B PWR_MGMT_1   écrire 0x00 pour sortir du mode veille
 *   0x1A CONFIG       0x03 : filtre passe-bas numérique ≈ 44 Hz
 *   0x1B GYRO_CONFIG  0x00 : pleine échelle ±250 °/s, soit 131 LSB par °/s
 *   0x47 / 0x48       GYRO_ZOUT_H / GYRO_ZOUT_L (entier signé 16 bits)
 *
 * À implémenter :
 *   mpuWrite(reg, val)  beginTransmission, write(reg), write(val), endTransmission.
 *   mpuRead16(reg)      écrire le numéro de registre, endTransmission(false)
 *                       (« repeated start »), requestFrom 2 octets, lire l'octet
 *                       haut puis l'octet bas (deux lectures séparées : l'ordre
 *                       d'évaluation d'une expression n'est pas garanti en C++),
 *                       et les assembler en int16_t.
 *   gyroZraw()          valeur brute convertie en °/s.
 *   imuBegin()          vérifier que le capteur acquitte, puis écrire les trois
 *                       registres de configuration ; false si absent.
 *   imuCalibrate(n)     robot IMMOBILE : moyenne de n lectures (≈ 1 s) -> gzBias.
 *   gyroZ()             gyroZraw() - gzBias.
 */
#pragma once
#include <Wire.h>

const uint8_t MPU = 0x68;      // AD0 relié à GND
float gzBias = 0;              // biais du gyroscope (°/s), mesuré au repos

void mpuWrite(uint8_t reg, uint8_t val) {
  // À compléter.
}

int16_t mpuRead16(uint8_t reg) {
  // À compléter.
  return 0;
}

float gyroZraw() {
  // À compléter.
  return 0;
}

bool imuBegin() {
  // À compléter.
  return false;
}

void imuCalibrate(int n = 500) {           // le capteur doit être IMMOBILE (~1 s)
  // À compléter.
}

// °/s ; positif = rotation vers la gauche vue de dessus (module à plat, composants en haut)
float gyroZ() {
  // À compléter.
  return 0;
}
