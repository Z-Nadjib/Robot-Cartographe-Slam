<div align="center">

<img src="docs/assets/banner.svg" width="100%" alt="Robot Cartographe SLAM"/>

<br/>

<img src="docs/assets/typing.svg" alt="Balayer une pièce, construire la carte, se recaler sur des marqueurs ArUco, rejoindre plusieurs points"/>

<p>
  <img src="docs/assets/badges/tps.svg" alt="14 TPs guidés"/>
  <img src="docs/assets/badges/phases.svg" alt="Phase A sur table, phase B sur la voiture"/>
  <img src="docs/assets/badges/budget.svg" alt="Budget d'environ 100 €"/>
</p>
<p>
  <img src="docs/assets/badges/esp32.svg" alt="ESP32, Arduino core 3.x"/>
  <img src="docs/assets/badges/python.svg" alt="Python 3.10+"/>
  <img src="docs/assets/badges/opencv.svg" alt="OpenCV ArUco"/>
  <img src="docs/assets/badges/reseau.svg" alt="UDP sur Wi-Fi"/>
  <img src="docs/assets/badges/langue.svg" alt="En français"/>
</p>

<p>
  <a href="#le-manuel"><b>Manuel</b></a> &nbsp;·&nbsp;
  <a href="#installation"><b>Installation</b></a> &nbsp;·&nbsp;
  <a href="#utilisation"><b>Utilisation</b></a> &nbsp;·&nbsp;
  <a href="#le-parcours-en-14-tps"><b>TPs</b></a> &nbsp;·&nbsp;
  <a href="#architecture"><b>Architecture</b></a> &nbsp;·&nbsp;
  <a href="#protocole"><b>Protocole</b></a> &nbsp;·&nbsp;
  <a href="#matériel"><b>Matériel</b></a>
</p>

</div>

<br/>

**Robot Cartographe SLAM** est un projet de Travaux Avant Projet de L3 Électronique à l'USTHB. On y construit un petit robot à deux roues qui fait du **SLAM** simplifié, c'est-à-dire qu'il se localise et cartographie en même temps.

Le robot balaye la pièce avec un laser monté sur un servomoteur, et le PC en tire une **grille d'occupation**. Une caméra lit des **marqueurs ArUco** collés aux murs pour corriger la dérive de l'odométrie. On clique ensuite des points sur la carte, et le robot s'y rend seul grâce à **A\***.

Le dépôt contient le manuel des 14 TPs, le firmware de l'ESP32 et l'application Python du PC.

<p align="center">
  <img src="docs/assets/features.svg" width="100%" alt="Un manuel en un seul fichier, 14 TPs guidés, deux phases (table puis voiture), firmware ESP32 temps réel, SLAM léger en Python, navigation multi-points"/>
</p>

## Comment ça marche

Le robot répète quatre étapes. Il s'arrête pour balayer, le PC ajoute ce balayage à la carte, la caméra recale la position estimée, puis A\* trace le chemin vers le but suivant.

<p align="center">
  <img src="docs/assets/comment.svg" width="100%" alt="1 balayer au laser, 2 construire la grille d'occupation, 3 se recaler sur un marqueur ArUco avec l'EKF, 4 naviguer avec A*"/>
</p>

<br/>

## Le manuel

Tout le manuel tient dans un seul fichier : **[`index.html`](index.html)**. Il suffit de cloner le dépôt, ou de le télécharger en ZIP, puis d'ouvrir ce fichier dans Chrome, Firefox ou Edge.

Le manuel n'a besoin d'aucun serveur. Seules les polices et la coloration du code viennent d'internet. Les cases cochées dans les checklists restent mémorisées dans le navigateur d'une séance à l'autre.

<p align="center">
  <img src="docs/captures/accueil.png" alt="Page d'accueil du manuel" height="380"/>
  &nbsp;
  <img src="docs/captures/mobile.png" alt="Le manuel sur téléphone" height="380"/>
</p>

| Chapitre | Contenu |
|---|---|
| Accueil | Ce que fera le robot, les deux phases, le lien avec les modules du semestre |
| Matériel détaillé | Liste d'achat, fiches techniques, outillage, logiciels |
| Architecture | Vue d'ensemble, entrées et sorties de chaque bloc, brochage, alimentation, budget de courant |
| Modules | Circulation des données, modules du firmware et du PC, ce qui est codé à la main |
| Protocole | Réseau, messages, caméra HTTP, choix techniques à justifier dans le rapport |
| TP 0 à TP 13 | Objectif, matériel, câblage, étapes, code complet, critères de validation chiffrés, pièges fréquents, checklist |

<br/>

## Installation

### Firmware (Arduino IDE 2)

1. Ajouter les cartes **ESP32 d'Espressif, version 3.x**, et la bibliothèque **VL53L1X de Pololu**.
2. Ouvrir un dossier de [`firmware/tests/`](firmware/tests/), choisir la carte *ESP32 Dev Module* et téléverser.
3. Pour le robot complet, ouvrir [`firmware/robot_fw/`](firmware/robot_fw/), puis renseigner le Wi‑Fi dans [`comms.h`](firmware/robot_fw/comms.h), la géométrie et les gains du PI dans [`config.h`](firmware/robot_fw/config.h).

### PC (Python 3.10 ou plus récent)

```bash
git clone https://github.com/Z-Nadjib/Robot-Cartographe-Slam.git
cd Robot-Cartographe-Slam
python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate
pip install -r pc/requirements.txt
```

Cela installe `numpy`, `matplotlib`, `opencv-contrib-python` (4.7 ou plus, pour ArUco) et `pyserial`.

> [!TIP]
> Le réseau conseillé est le **partage de connexion d'un téléphone en 2,4 GHz**. Le PC, le robot et l'ESP32‑CAM s'y connectent tous les trois.

<br/>

## Utilisation

Les scripts se lancent depuis `pc/robot/`, où ils trouvent `markers.json` et `calib.npz`. L'adresse IP du robot s'affiche sur le moniteur série au démarrage de l'ESP32.

### Un script par étape

| TP | Commande | Ce que fait le script |
|:---:|---|---|
| 2 | `python ../tools/plot_serial.py /dev/ttyUSB0` | Trace le laser brut et filtré, enregistre un CSV |
| 3 | `python ../tools/radar_serial.py /dev/ttyUSB0` | Affiche le radar reçu sur le port série |
| 4 | `python ../tools/udp_radar.py IP_ROBOT` | Affiche le radar reçu en UDP, compte les pertes, mesure la latence |
| 5 | `python ../tools/calibrate.py http://IP_CAM/capture` | Calibre la caméra sur un damier 9 × 6 et écrit `calib.npz` |
| 5 | `python aruco_cam.py http://IP_CAM/capture` | Détecte les marqueurs, donne leur distance et leur angle |
| 7 | `python ../tools/analyse_echelon.py echelon.csv` | Ajuste un modèle du premier ordre et propose KP et KI |
| 9 | `python teleop.py IP_ROBOT` | Pilotage au clavier (Z Q S D) et tracé de l'odométrie |
| 10 | `python map_live.py IP_ROBOT` | Téléopération et carte en direct, touche **C** pour balayer |
| 11 | `python fusion_test.py IP_ROBOT http://IP_CAM/capture` | Compare l'odométrie seule et l'EKF sur un même trajet |
| 12 | `python app.py IP_ROBOT http://IP_CAM/capture` | Application finale |

### L'application finale

```bash
cd pc/robot
python app.py 192.168.43.50 http://192.168.43.51/capture
```

| Action | Effet |
|---|---|
| Clic gauche sur la carte | Ajoute un but ; les buts sont visités dans l'ordre |
| <kbd>C</kbd> | Lance un balayage |
| <kbd>E</kbd> | Enregistre l'image de la carte |
| <kbd>Échap</kbd> | Arrête le robot et quitte |

À chaque but atteint, le robot s'arrête et balaye avant de repartir. Un but inaccessible est signalé puis ignoré.

<br/>

## Le parcours en 14 TPs

Le projet avance en deux phases. En **phase A**, chaque brique est validée seule sur une plaque d'essai. En **phase B**, tout est assemblé sur la voiture.

<p align="center">
  <img src="docs/assets/parcours.svg" width="100%" alt="Phase A : TP 0 à 7 sur table. Phase B : TP 8 à 13 sur la voiture."/>
</p>

Chaque TP met en pratique un ou plusieurs modules du semestre :

| Module | Dans le projet | TPs |
|---|---|:---:|
| **Fonctions Électroniques** | Pont en H, encodeurs, régulation 5 V, pont diviseur, modèle du moteur | 7, 8 |
| **Traitement du Signal** | Filtre médian, intégration du gyroscope, traitement d'image, filtre de Kalman | 2, 3, 5, 6, 11 |
| **Systèmes Microprocesseurs** | PWM (LEDC), interruptions, timers, I2C, ADC, ordonnancement non bloquant | 1, 3, 7, 9 |
| **Réseaux Informatiques Locaux** | IP, sockets UDP, protocole applicatif, latence et pertes, HTTP, Wireshark | 4, 5, 9 |

<br/>

## Architecture

L'ESP32 ne fait que ce qui exige du **temps réel** : régulation des roues, comptage des encodeurs, intégration du cap et balayage. Tout ce qui demande de la mémoire ou du calcul tourne sur le **PC**. Les deux ne communiquent que par Wi‑Fi.

<p align="center">
  <img src="docs/assets/architecture.svg" width="100%" alt="Le robot (capteurs, ESP32, TB6612, ESP32-CAM) envoie télémesure et balayages en UDP au PC (réception, odométrie, EKF, grille, A*), qui renvoie les consignes ; la caméra envoie ses images en HTTP"/>
</p>

| | Module | Rôle |
|:---:|---|---|
| ESP32 | [`motors.h`](firmware/robot_fw/motors.h) | Pont en H TB6612, PWM à 20 kHz, commande de −255 à +255 |
| ESP32 | [`encoders.h`](firmware/robot_fw/encoders.h) | Quadrature x4 sur interruptions, table de décodage |
| ESP32 | [`speed_pi.h`](firmware/robot_fw/speed_pi.h) | PI de vitesse par roue, sans intégration en saturation |
| ESP32 | [`imu.h`](firmware/robot_fw/imu.h) | MPU6050 lu en I2C sans bibliothèque, biais mesuré au démarrage |
| ESP32 | [`scanner.h`](firmware/robot_fw/scanner.h) | Machine à états servo + laser, 61 mesures sur 180° |
| ESP32 | [`comms.h`](firmware/robot_fw/comms.h) | Wi‑Fi et UDP texte, chien de garde de 500 ms |
| PC | [`odometry.py`](pc/robot/odometry.py) | Pose (x, y, θ) à partir des ticks et du cap du gyroscope |
| PC | [`grid_map.py`](pc/robot/grid_map.py) | Grille log-odds de 6 × 6 m en cases de 5 cm, rayons tracés par Bresenham |
| PC | [`aruco_cam.py`](pc/robot/aruco_cam.py) | Détection ArUco et `solvePnP`, d'où la distance et l'angle du marqueur |
| PC | [`ekf.py`](pc/robot/ekf.py) | Filtre de Kalman étendu, test du χ² contre les mesures aberrantes |
| PC | [`planner.py`](pc/robot/planner.py) | Obstacles gonflés, puis recherche A* sur 8 voisins |
| PC | [`controller.py`](pc/robot/controller.py) | Suivi de point : s'orienter vers la cible, puis avancer |

<details>
<summary><b>Brochage de l'ESP32</b></summary>
<br/>

| GPIO | Fonction | Relié à |
|:---:|---|---|
| `21` / `22` | SDA / SCL (I2C) | VL53L1X (0x29), MPU6050 (0x68) |
| `13` | PWM 50 Hz | Servo SG90 |
| `25` `26` `27` | PWMA, AIN1, AIN2 | TB6612, moteur gauche |
| `18` `16` `17` | PWMB, BIN1, BIN2 | TB6612, moteur droit |
| `23` | STBY | TB6612 |
| `34` `35` / `36` `39` | Encodeurs A, B | Encodeurs gauche / droit (tirage de 10 kΩ vers 3,3 V) |
| `33` | ADC1 | Pont diviseur 100 kΩ / 33 kΩ de la batterie |
| `2` | LED | LED d'état intégrée |

<img src="docs/captures/brochage.png" alt="Brochage de l'ESP32 dans le manuel" width="100%"/>
</details>

<br/>

## Protocole

Chaque message est une ligne de texte envoyée dans un seul datagramme UDP. Les champs sont séparés par des virgules.

| Sens | Message | Rôle |
|---|---|---|
| Robot → PC (5005) | `O,seq,t_ms,ticksG,ticksD,cap_mdeg,avant_mm,vbat_mV` | Télémesure à 20 Hz |
| Robot → PC (5005) | `S,seq,angle0,pas,d0,…,d60` | Un balayage de 61 distances en mm |
| PC → robot (5006) | `V,v_mm_s,w_mrad_s` | Consigne de vitesse, à répéter |
| PC → robot (5006) | `C` · `X` · `M,pwmG,pwmD` · `P,…` | Balayer · arrêter · commande directe · écho |
| Caméra → PC (HTTP) | `GET /capture` | Une image JPEG |

> [!IMPORTANT]
> Le robot s'arrête de lui-même dans deux cas : s'il ne reçoit plus de consigne pendant 500 ms, ou si un obstacle se trouve à moins de 150 mm devant lui.

<br/>

## Matériel

<table>
  <tr>
    <td align="center" width="25%"><img src="docs/assets/materiel/esp32.jpg" alt="ESP32 DevKit" width="100%"/><br/><b>ESP32 DevKit V1</b><br/><sub>Cerveau du robot, Wi‑Fi</sub></td>
    <td align="center" width="25%"><img src="docs/assets/materiel/esp32cam.jpg" alt="ESP32-CAM" width="100%"/><br/><b>ESP32‑CAM</b><br/><sub>Images pour les marqueurs ArUco</sub></td>
    <td align="center" width="25%"><img src="docs/assets/materiel/sg90.jpg" alt="Servo SG90" width="100%"/><br/><b>Servo SG90</b><br/><sub>Balayage du laser sur 180°</sub></td>
    <td align="center" width="25%"><img src="docs/assets/materiel/mpu6050.jpg" alt="MPU6050 GY-521" width="100%"/><br/><b>MPU6050 (GY‑521)</b><br/><sub>Gyroscope, mesure du cap</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="docs/assets/materiel/tb6612.jpg" alt="TB6612FNG" width="100%"/><br/><b>TB6612FNG</b><br/><sub>Pont en H double</sub></td>
    <td align="center"><img src="docs/assets/materiel/accu18650.jpg" alt="Accu 18650" width="100%"/><br/><b>2 accus 18650</b><br/><sub>Alimentation 2S, 7,4 V</sub></td>
    <td align="center"><img src="docs/assets/materiel/abaisseur.jpg" alt="Abaisseur DC-DC" width="100%"/><br/><b>Abaisseur DC‑DC</b><br/><sub>5 V / 3 A pour l'électronique</sub></td>
    <td align="center"><img src="docs/assets/materiel/chassis.jpg" alt="Châssis de voiture robot" width="100%"/><br/><b>Châssis 2 roues</b><br/><sub>Base mobile et roue folle</sub></td>
  </tr>
</table>

<sub>Photos d'illustration issues de Wikimedia Commons, sous licences CC BY-SA et CC0. Auteurs et licences : [`docs/assets/materiel/CREDITS.md`](docs/assets/materiel/CREDITS.md).</sub>

| Composant | Quantité | Rôle |
|---|:---:|---|
| ESP32 DevKit V1 | 2 | Cerveau du robot ; la seconde sert de secours |
| Capteur laser VL53L1X | 1 | Distances jusqu'à 4 m |
| Servo SG90 ou MG90S | 1 | Balayage sur 180° |
| ESP32‑CAM AI‑Thinker + carte ESP32‑CAM‑MB | 1 | Images pour les marqueurs ArUco |
| MPU6050 (GY‑521) | 1 | Vitesse de rotation, donc le cap |
| TB6612FNG | 1 | Pont en H double |
| Motoréducteur 6 V **avec encodeur** | 2 | Propulsion et odométrie |
| Châssis 2 roues + roue folle | 1 | Base mobile |
| Accu 18650 | 2 | Alimentation 2S, 7,4 V |
| Support 2S + chargeur | 1 | Logement et recharge des accus |
| Abaisseur DC‑DC 5 V / 3 A, fusible, interrupteur | 1 | Distribution de l'énergie |

Le budget est d'**environ 100 €**, ESP32 de secours et accessoires compris. Le chapitre *Matériel détaillé* du manuel indique ce qu'il faut vérifier avant chaque achat.

<br/>

## Structure du projet

```
Robot-Cartographe-Slam
|-- index.html              le manuel complet, à ouvrir dans un navigateur
|-- firmware
|   |-- tests               un croquis Arduino par TP de la phase A
|   `-- robot_fw            firmware final du robot (TP9 à TP13)
|-- pc
|   |-- requirements.txt
|   |-- tools               tracés, calibration, marqueurs, analyse de l'échelon
|   `-- robot               odométrie, carte, EKF, A*, application
|-- mesures                 courbes, CSV et photos pour le rapport
`-- docs
    |-- captures            captures d'écran du manuel
    `-- assets              figures et photos de cette page
```

Les figures de cette page sont générées par [`docs/assets/make_figures.py`](docs/assets/make_figures.py).

<br/>

## État du projet

- [x] Manuel complet : matériel, schémas, modules, protocole, 14 TPs
- [x] Code ESP32 et Python de tous les TPs
- [ ] Phase A validée sur table
- [ ] Robot assemblé (phase B)
- [ ] Carte, fusion et navigation validées
- [ ] Rapport et soutenance

> [!NOTE]
> Le code est une base de départ. La syntaxe du firmware a été vérifiée et les modules Python ont été testés sur des données simulées, mais rien n'a encore tourné sur le vrai matériel. Des ajustements sont à prévoir pendant les TPs : c'est le rôle des étapes de validation.

## Auteur

**Zahaf Boualem Nadjib**, Licence 3 Électronique, Université des Sciences et de la Technologie Houari Boumediene (USTHB).

<div align="center">
<br/>
<img src="docs/assets/footer.svg" width="100%" alt=""/>
</div>
