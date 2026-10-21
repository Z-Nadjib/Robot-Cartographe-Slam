// TP2 — VL53L1X : mesure brute + filtre médian (fenêtre de 5)
#include <Wire.h>
#include <VL53L1X.h>      // bibliothèque « VL53L1X » de Pololu

VL53L1X tof;
const int N = 5;
uint16_t fenetre[N];
int idx = 0;

uint16_t mediane(const uint16_t* v, int n) {
  uint16_t t[N];
  memcpy(t, v, n * sizeof(uint16_t));
  for (int i = 1; i < n; i++) {           // tri par insertion
    uint16_t x = t[i]; int j = i - 1;
    while (j >= 0 && t[j] > x) { t[j + 1] = t[j]; j--; }
    t[j + 1] = x;
  }
  return t[n / 2];
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  Wire.setClock(400000);
  tof.setTimeout(500);
  if (!tof.init()) { Serial.println("VL53L1X introuvable !"); while (true) delay(100); }
  tof.setDistanceMode(VL53L1X::Long);          // jusqu'à ~4 m
  tof.setMeasurementTimingBudget(50000);       // 50 ms par mesure
  tof.startContinuous(50);
}

void loop() {
  uint16_t d = tof.read();                     // attend la mesure suivante
  if (tof.timeoutOccurred()) { Serial.println("timeout"); return; }
  bool valide = (tof.ranging_data.range_status == VL53L1X::RangeValid);
  fenetre[idx] = d; idx = (idx + 1) % N;
  // format CSV : temps_ms,brut_mm,filtre_mm,valide
  Serial.printf("%lu,%u,%u,%d\n", millis(), d, mediane(fenetre, N), valide);
}
