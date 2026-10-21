/*
 * TP1 — PWM matériel (LEDC), interruption et tâches non bloquantes
 *
 * But : faire « respirer » la LED avec une PWM matérielle, compter les appuis
 * sur le bouton BOOT par interruption, et faire tourner deux tâches à des
 * rythmes différents SANS jamais appeler delay().
 *
 * Ce que le programme doit faire :
 *   1. PWM : attacher la LED à un canal LEDC (5 kHz, 8 bits, donc 0..255) avec
 *      ledcAttachChannel(broche, fréquence, résolution, canal), puis régler le
 *      rapport cyclique avec ledcWrite(broche, valeur).
 *   2. Interruption : le bouton BOOT (GPIO 0) est actif à l'état bas. Le
 *      configurer en INPUT_PULLUP et lui attacher une ISR sur front descendant.
 *      L'ISR (IRAM_ATTR) ne fait qu'incrémenter un compteur « volatile » :
 *      jamais de Serial ni de delay dans une ISR.
 *   3. Ordonnancement non bloquant dans loop() :
 *        - toutes les 20 ms : faire varier le rapport cyclique de ±5 et
 *          inverser le sens aux bornes 0 et 255 ;
 *        - toutes les 1000 ms : afficher le rapport cyclique et le nombre d'appuis.
 *      Méthode : mémoriser l'instant du dernier passage (millis()) et ne faire
 *      la tâche que si « maintenant - dernier >= période ».
 *
 * Validation : la LED s'allume et s'éteint progressivement (~2 s par cycle),
 * chaque appui sur BOOT incrémente le compteur, même pendant la variation.
 */
const int LED    = 2;
const int BOUTON = 0;              // bouton BOOT de la carte (actif à l'état bas)
const int LED_CH = 4;              // canal LEDC n°4 (timer 2)

volatile uint32_t appuis = 0;

void IRAM_ATTR onBouton() {
  // À compléter : une seule ligne.
}

void setup() {
  // À compléter : port série, bouton + interruption, canal PWM de la LED.
}

void loop() {
  // À compléter : les deux tâches périodiques décrites plus haut.
}
