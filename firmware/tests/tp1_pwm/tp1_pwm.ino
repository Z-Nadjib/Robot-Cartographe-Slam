// TP1 — PWM matériel (LEDC), interruption et tâches non bloquantes
const int LED    = 2;
const int BOUTON = 0;              // bouton BOOT de la carte (actif à l'état bas)
const int LED_CH = 4;              // canal LEDC n°4 (timer 2)

volatile uint32_t appuis = 0;
void IRAM_ATTR onBouton() { appuis++; }   // ISR : très courte, jamais de Serial ici

void setup() {
  Serial.begin(115200);
  pinMode(BOUTON, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(BOUTON), onBouton, FALLING);
  ledcAttachChannel(LED, 5000, 8, LED_CH);   // 5 kHz, résolution 8 bits (0..255)
}

void loop() {
  static uint32_t tPwm = 0, tLog = 0;
  static int duty = 0, pas = 5;
  uint32_t now = millis();

  if (now - tPwm >= 20) {          // tâche 1 : toutes les 20 ms
    tPwm = now;
    duty += pas;
    if (duty <= 0 || duty >= 255) pas = -pas;
    ledcWrite(LED, constrain(duty, 0, 255));
  }
  if (now - tLog >= 1000) {        // tâche 2 : toutes les secondes
    tLog = now;
    Serial.printf("duty=%d  appuis=%lu\n", duty, appuis);
  }
}
