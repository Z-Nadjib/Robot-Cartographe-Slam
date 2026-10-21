// robot_fw.ino — firmware complet du robot (TP9 → TP13)
#include "config.h"
#include "motors.h"
#include "encoders.h"
#include "speed_pi.h"
#include "imu.h"
#include "scanner.h"
#include "comms.h"
#include "battery.h"

SpeedPI piL, piR;
float vRef = 0, wRef = 0;          // consignes reçues : mm/s et rad/s
int   pwmDirL = 0, pwmDirR = 0;    // commande directe (tests)
bool  direct = false;
float headingDeg = 0;              // cap intégré à 50 Hz à partir du gyroscope

void handleCommand(char* c) {
  switch (c[0]) {
    case 'V': { float v, w;
      if (sscanf(c, "V,%f,%f", &v, &w) == 2) { vRef = v; wRef = w / 1000.0f; direct = false; }
      break; }
    case 'M': { int a, b;
      if (sscanf(c, "M,%d,%d", &a, &b) == 2) { pwmDirL = a; pwmDirR = b; direct = true; }
      break; }
    case 'C': if (!scanBusy()) scanStart(); break;          // lancer un balayage
    case 'X': vRef = wRef = 0; direct = false; motorsOff(); break;   // arrêt
    case 'P': sendLine(String(c)); break;                    // écho pour la latence
  }
}

void controlStep(float dt) {
  static int32_t pL = 0, pR = 0;
  int32_t nL = getTicksL(), nR = getTicksR();
  float vL = (nL - pL) * MM_PER_TICK / dt;
  float vR = (nR - pR) * MM_PER_TICK / dt;
  pL = nL; pR = nR;
  headingDeg += gyroZ() * dt;

  if (millis() - lastCmdMs > 500) { vRef = wRef = 0; direct = false; }  // PC muet → arrêt
  if (direct) { setMotors(pwmDirL, pwmDirR); return; }

  float v = vRef;
  if (v > 0 && frontMm > 0 && frontMm < STOP_MM) v = 0;   // obstacle devant → on n'avance plus
  if (v == 0 && wRef == 0) { piL.reset(); piR.reset(); motorsOff(); return; }

  float refL = v - wRef * TRACK_MM / 2;                    // cinématique différentielle
  float refR = v + wRef * TRACK_MM / 2;
  setMotors(piL.update(refL, vL, dt), piR.update(refR, vR, dt));
}

void sendOdom(uint32_t now) {
  char m[112];
  snprintf(m, sizeof m, "O,%lu,%lu,%ld,%ld,%ld,%u,%d",
           (unsigned long)txSeq++, (unsigned long)now,
           (long)getTicksL(), (long)getTicksR(),
           (long)(headingDeg * 1000), frontMm, (int)(readVbat() * 1000));
  sendLine(m);
}

void sendScan() {
  String s = "S," + String(txSeq++) + "," + String(SCAN_MIN) + "," + String(SCAN_STEP);
  for (int i = 0; i < SCAN_N; i++) s += "," + String(scanDist[i]);
  sendLine(s);
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED, OUTPUT);
  Wire.begin(PIN_SDA, PIN_SCL);
  Wire.setClock(400000);
  motorsBegin();
  encodersBegin();
  if (!imuBegin())     Serial.println("ERREUR : MPU6050 absent");
  if (!scannerBegin()) Serial.println("ERREUR : VL53L1X absent");
  imuCalibrate();                    // robot IMMOBILE à l'allumage
  wifiBegin();
  digitalWrite(PIN_LED, HIGH);       // LED allumée = prêt
}

void loop() {
  char cmd[96];
  while (readCommand(cmd, sizeof cmd)) handleCommand(cmd);

  static uint32_t tCtrl = millis(), tOdom = 0;
  uint32_t now = millis();
  if (now - tCtrl >= CTRL_MS) { controlStep((now - tCtrl) / 1000.0f); tCtrl = now; }
  if (now - tOdom >= 50)      { tOdom = now; sendOdom(now); }       // télémesure 20 Hz

  scanUpdate();
  if (scanReady) { scanReady = false; sendScan(); }
}
