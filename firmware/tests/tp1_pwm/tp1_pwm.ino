/*
 * TP1 — PWM matériel (LEDC), interruption et tâches non bloquantes
 *
 * Carte : ESP32-DevKitC V4 (WROOM-32E). Câblage :
 *   - LED externe : GPIO 2 -> 220 Ω -> anode ; cathode -> GND (comme au TP0) ;
 *   - fil de mesure : GPIO 2 relié à GPIO 4 (partie D) ;
 *   - bouton : le bouton BOOT de la carte, déjà relié à GPIO 0.
 * Aucun oscilloscope n'est nécessaire : l'ESP32 mesure lui-même sa PWM.
 *
 * Le travail se fait en parties successives (voir le manuel) ; chaque partie
 * ajoute un morceau à ce même fichier.
 *
 *   A. PWM fixe : attacher la LED à un canal LEDC (5 kHz, 8 bits, donc 0..255)
 *      avec ledcAttachChannel(broche, fréquence, résolution, canal) et afficher
 *      la valeur renvoyée (true = configuration acceptée). Régler le rapport
 *      cyclique avec ledcWrite(broche, valeur). Essayer 0, 64, 128, 191, 255.
 *   B. Tâches non bloquantes dans loop(), SANS delay() :
 *        - toutes les 20 ms : rapport cyclique ± 5, sens inversé aux bornes 0 et 255 ;
 *        - toutes les 1000 ms : afficher le rapport cyclique et le nombre d'appuis.
 *      Méthode : mémoriser l'instant du dernier passage et ne faire la tâche que
 *      si « maintenant - dernier >= période » (soustraction en uint32_t : elle
 *      reste juste quand millis() repasse par zéro, au bout de 49 jours).
 *   C. Interruption : le bouton BOOT (GPIO 0) est actif à l'état bas. Le configurer
 *      en INPUT_PULLUP et lui attacher une ISR sur front descendant. L'ISR
 *      (IRAM_ATTR) ne fait qu'incrémenter un compteur « volatile » : jamais de
 *      Serial ni de delay dans une ISR. Puis anti-rebond : ignorer un front arrivé
 *      moins de 50 ms après le précédent accepté (millis() est utilisable dans
 *      une ISR sur l'ESP32).
 *   D. Mesure de la PWM sans oscilloscope : mesurerPwm() lit sur GPIO 4 la durée
 *      de l'état haut et celle de l'état bas avec pulseIn(MESURE, HIGH / LOW, délai)
 *      (en µs ; 0 si rien n'arrive avant le délai), puis en déduit la période, la
 *      fréquence et le rapport cyclique, et les affiche. Attendu à 5 kHz :
 *      période 200 µs, temps haut = valeur / 255 × 200 µs.
 *   E. Pour le traceur série de l'IDE : envoyer une ligne « duty:<valeur> » à
 *      chaque pas de la tâche des 20 ms pour voir le triangle du rapport cyclique.
 *
 * Validation : la LED s'allume et s'éteint progressivement (≈ 2 s par cycle),
 * chaque appui sur BOOT compte une fois, la mesure par l'ESP32 et celle du
 * multimètre concordent avec le calcul.
 */
const int LED    = 2;              // LED externe + 220 Ω vers GND
const int BOUTON = 0;              // bouton BOOT de la carte (actif à l'état bas)
const int MESURE = 4;              // relié à GPIO 2 par un fil : mesure de la PWM (partie D)
const int LED_CH = 4;              // canal LEDC n°4 (timer 2)

volatile uint32_t appuis = 0;

void IRAM_ATTR onBouton() {
  // À compléter (partie C) : incrémenter le compteur, puis ajouter l'anti-rebond.
}

void mesurerPwm() {
  // À compléter (partie D).
}

void setup() {
  // À compléter : port série, canal PWM de la LED (partie A), entrée de mesure,
  // bouton + interruption (partie C).
}

void loop() {
  // À compléter : les tâches périodiques (parties B, D et E).
}
