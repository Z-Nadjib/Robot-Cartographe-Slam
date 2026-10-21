// motors.h — pont en H TB6612FNG : commande signée de -255 à +255 par roue
#pragma once
#include "config.h"

const uint32_t PWM_FREQ = 20000;   // 20 kHz : au-dessus de l'audible
const uint8_t  PWM_BITS = 8;       // rapport cyclique de 0 à 255

void motorsBegin() {
  int sorties[] = {PIN_AIN1, PIN_AIN2, PIN_BIN1, PIN_BIN2, PIN_STBY};
  for (int p : sorties) { pinMode(p, OUTPUT); digitalWrite(p, LOW); }
  ledcAttachChannel(PIN_PWMA, PWM_FREQ, PWM_BITS, 0);   // canaux 0 et 1 → timer 0
  ledcAttachChannel(PIN_PWMB, PWM_FREQ, PWM_BITS, 1);
}

static void driveOne(int in1, int in2, int pwmPin, int cmd) {
  cmd = constrain(cmd, -255, 255);
  digitalWrite(in1, cmd > 0);      // IN1=1, IN2=0 : sens horaire
  digitalWrite(in2, cmd < 0);      // IN1=0, IN2=1 : sens anti-horaire ; 0/0 : roue libre
  ledcWrite(pwmPin, abs(cmd));
}

void setMotors(int left, int right) {
  digitalWrite(PIN_STBY, HIGH);
  driveOne(PIN_AIN1, PIN_AIN2, PIN_PWMA, MOTOR_L_SIGN * left);
  driveOne(PIN_BIN1, PIN_BIN2, PIN_PWMB, MOTOR_R_SIGN * right);
}

void motorsOff() {
  setMotors(0, 0);
  digitalWrite(PIN_STBY, LOW);     // pont en H en veille
}
