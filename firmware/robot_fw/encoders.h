// encoders.h — comptage des encodeurs en quadrature (x4) par interruptions
#pragma once
#include "config.h"

// Table de décodage : index = (ancien état AB << 2) | nouvel état AB
static const int8_t QDEC[16] = {0,-1,1,0, 1,0,0,-1, -1,0,0,1, 0,1,-1,0};
volatile int32_t ticksL = 0, ticksR = 0;
volatile uint8_t stL = 0, stR = 0;

void IRAM_ATTR isrL() {
  stL = ((stL << 2) | (digitalRead(PIN_ENC_LA) << 1) | digitalRead(PIN_ENC_LB)) & 0x0F;
  ticksL += QDEC[stL];
}
void IRAM_ATTR isrR() {
  stR = ((stR << 2) | (digitalRead(PIN_ENC_RA) << 1) | digitalRead(PIN_ENC_RB)) & 0x0F;
  ticksR += QDEC[stR];
}

void encodersBegin() {
  int entrees[] = {PIN_ENC_LA, PIN_ENC_LB, PIN_ENC_RA, PIN_ENC_RB};
  for (int p : entrees) pinMode(p, INPUT);        // tirage externe 10 kΩ obligatoire
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_LA), isrL, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_LB), isrL, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_RA), isrR, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_ENC_RB), isrR, CHANGE);
}

int32_t getTicksL() { return ENC_L_SIGN * ticksL; }   // lecture 32 bits : atomique sur ESP32
int32_t getTicksR() { return ENC_R_SIGN * ticksR; }
