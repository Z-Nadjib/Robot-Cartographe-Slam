/*
 * TP2 — Scanner du bus I2C
 *
 * But : vérifier le câblage d'un capteur I2C en listant les adresses qui
 * répondent sur le bus.
 *
 * Ce que le programme doit faire (une seule fois, dans setup) :
 *   - démarrer le bus avec Wire.begin(SDA = 21, SCL = 22) ;
 *   - pour chaque adresse de 1 à 126 : Wire.beginTransmission(adresse), puis
 *     Wire.endTransmission() ; un retour égal à 0 signifie qu'un périphérique
 *     a acquitté : afficher son adresse en hexadécimal (format 0x%02X) ;
 *   - afficher « Fin du scan. ».
 *
 * Résultat attendu : 0x29 pour le VL53L1X ; plus tard 0x68 pour le MPU6050.
 * Rien trouvé ? Vérifier SDA/SCL inversés, l'alimentation 3,3 V et la masse.
 */
#include <Wire.h>

void setup() {
  // À compléter.
}

void loop() {}
