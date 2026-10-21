/*
 * TP2 — Capteur laser VL53L1X : mesure brute + filtre médian (fenêtre de 5)
 *
 * But : lire les distances en continu et supprimer les valeurs aberrantes
 * isolées avec une médiane glissante.
 *
 * Ce que le programme doit faire :
 *   - setup : bus I2C sur 21/22 à 400 kHz ; tof.setTimeout(500) ; tof.init()
 *     (arrêter avec un message si le capteur ne répond pas) ; mode de distance
 *     Long (jusqu'à ~4 m) ; budget de mesure 50 ms ; startContinuous(50).
 *   - loop : lire une distance (tof.read()), détecter un timeout, savoir si la
 *     mesure est valide (tof.ranging_data.range_status == VL53L1X::RangeValid),
 *     la ranger dans un tampon circulaire de N = 5 valeurs, puis envoyer une
 *     ligne CSV :  temps_ms,brut_mm,filtre_mm,valide
 *     (c'est le format que lit pc/tools/plot_serial.py).
 *
 * mediane(v, n) : copier les n valeurs dans un tableau local, les trier (un tri
 * par insertion suffit pour 5 valeurs) et renvoyer l'élément du milieu.
 * Ne pas trier le tampon lui-même : il perdrait l'ordre d'arrivée.
 */
#include <Wire.h>
#include <VL53L1X.h>      // bibliothèque « VL53L1X » de Pololu

VL53L1X tof;
const int N = 5;
uint16_t fenetre[N];       // tampon circulaire des N dernières mesures
int idx = 0;               // prochaine case à écrire

uint16_t mediane(const uint16_t* v, int n) {
  // À compléter : copie, tri, élément central.
  return 0;
}

void setup() {
  // À compléter : port série, I2C, initialisation et réglages du capteur.
}

void loop() {
  // À compléter : mesure, validité, tampon circulaire, ligne CSV.
}
