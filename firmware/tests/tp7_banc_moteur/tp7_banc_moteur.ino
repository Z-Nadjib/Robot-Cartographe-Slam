// TP7 — Banc moteur (roues en l'air) : boucle ouverte, réponse indicielle, régulation PI
#include "config.h"
#include "motors.h"
#include "encoders.h"
#include "speed_pi.h"

SpeedPI piL, piR;
enum { STOP, OUVERT, FERME } mode = STOP;
float consigne = 0;                 // PWM (mode OUVERT) ou mm/s (mode FERME)

void lireCommande() {
  if (!Serial.available()) return;
  String l = Serial.readStringUntil('\n');
  l.trim();
  if (l.startsWith("p"))      { mode = OUVERT; consigne = l.substring(1).toFloat(); }
  else if (l.startsWith("v")) { mode = FERME;  consigne = l.substring(1).toFloat(); piL.reset(); piR.reset(); }
  else if (l == "t")          { Serial.printf("ticks G=%ld D=%ld\n", (long)getTicksL(), (long)getTicksR()); }
  else                        { mode = STOP;   consigne = 0; }
}

void setup() {
  Serial.begin(115200);
  motorsBegin();
  encodersBegin();
  Serial.println("Commandes : p <pwm> | v <mm/s> | t (ticks) | s (stop)");
}

void loop() {
  lireCommande();
  static uint32_t t = millis();
  static int32_t pL = 0, pR = 0;
  if (millis() - t < CTRL_MS) return;
  float dt = (millis() - t) / 1000.0f;
  t = millis();

  int32_t nL = getTicksL(), nR = getTicksR();
  float vL = (nL - pL) * MM_PER_TICK / dt;      // vitesses en mm/s
  float vR = (nR - pR) * MM_PER_TICK / dt;
  pL = nL; pR = nR;

  int uL = 0, uR = 0;
  if (mode == OUVERT) { uL = uR = (int)consigne; }
  if (mode == FERME)  { uL = piL.update(consigne, vL, dt); uR = piR.update(consigne, vR, dt); }
  if (mode == STOP) motorsOff(); else setMotors(uL, uR);

  if (mode != STOP)   // CSV : temps_ms,consigne,vG,vD,pwmG,pwmD
    Serial.printf("%lu,%.0f,%.1f,%.1f,%d,%d\n", millis(), consigne, vL, vR, uL, uR);
}
