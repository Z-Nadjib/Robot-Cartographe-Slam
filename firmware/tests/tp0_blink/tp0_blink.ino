/*
 * TP0 — Premier programme : LED + moniteur série
 *
 * Carte : ESP32-DevKitC V4 (module WROOM-32E). Elle n'a PAS de LED utilisateur
 * (la LED rouge ne fait que signaler l'alimentation) : on branche une LED
 * externe sur GPIO 2, dans ce sens :
 *     GPIO 2 -> résistance 220 Ω -> anode de la LED (patte longue)
 *     cathode (patte courte, côté plat) -> GND
 * Ne pas relier la LED au 3,3 V : GPIO 2 doit rester à l'état bas au démarrage,
 * sinon le téléversement peut échouer.
 *
 * But : vérifier que toute la chaîne fonctionne (IDE, pilote USB, carte,
 * téléversement, moniteur série) avant d'écrire du vrai code.
 *
 * Ce que le programme doit faire :
 *   - au démarrage, ouvrir le port série à 115200 bauds et afficher un message
 *     de bienvenue ;
 *   - faire clignoter la LED (GPIO 2) : 500 ms allumée, 500 ms éteinte ;
 *   - à chaque clignotement, afficher le temps écoulé depuis le démarrage (millis()).
 *
 * Fonctions utiles : Serial.begin, Serial.println, Serial.printf, pinMode,
 * digitalWrite, delay, millis.
 *
 * Validation : la LED clignote à 1 Hz et le moniteur série (115200 bauds)
 * affiche un temps qui augmente d'environ 1000 ms à chaque ligne.
 */
const int LED = 2;          // LED externe + 220 Ω vers GND (pas de LED utilisateur sur la DevKitC V4)

void setup() {
  // À compléter : ouvrir le port série, configurer la LED en sortie, saluer.
}

void loop() {
  // À compléter : allumer, attendre, éteindre, attendre, afficher millis().
}
