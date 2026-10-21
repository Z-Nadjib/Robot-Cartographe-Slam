// TP0 — Premier programme : LED + moniteur série
const int LED = 2;          // LED bleue intégrée à la carte DevKit

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  Serial.println("Bonjour, ESP32 pret !");
}

void loop() {
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);
  delay(500);
  Serial.printf("Temps ecoule : %lu ms\n", millis());
}
