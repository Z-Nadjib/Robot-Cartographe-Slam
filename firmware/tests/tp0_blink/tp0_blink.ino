/*
 * TP0 — Premier programme : LED + moniteur série
 *
 * But : vérifier que toute la chaîne fonctionne (IDE, pilote USB, carte,
 * téléversement, moniteur série) avant d'écrire du vrai code.
 *
 * Ce que le programme doit faire :
 *   - au démarrage, ouvrir le port série à 115200 bauds et afficher un message
 *     de bienvenue ;
 *   - faire clignoter la LED intégrée (GPIO 2) : 500 ms allumée, 500 ms éteinte ;
 *   - à chaque clignotement, afficher le temps écoulé depuis le démarrage (millis()).
 *
 * Fonctions utiles : Serial.begin, Serial.println, Serial.printf, pinMode,
 * digitalWrite, delay, millis.
 *
 * Validation : la LED clignote à 1 Hz et le moniteur série (115200 bauds)
 * affiche un temps qui augmente d'environ 1000 ms à chaque ligne.
 */
const int LED = 2;          // LED bleue intégrée à la carte DevKit

void setup() {
  // À compléter : ouvrir le port série, configurer la LED en sortie, saluer.
}

void loop() {
  // À compléter : allumer, attendre, éteindre, attendre, afficher millis().
}
