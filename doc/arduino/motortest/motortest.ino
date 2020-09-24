#include <Wire.h>

int BIN_1 = 10;
int BIN_2 = 9;
int AIN_1 = 5;
int AIN_2 = 6;

void setup() {
  pinMode(BIN_1, OUTPUT);
  pinMode(BIN_2, OUTPUT);
  pinMode(AIN_1, OUTPUT);
  pinMode(AIN_2, OUTPUT);
}

void loop() {
  
  //rightmotor
  analogWrite(AIN_1, 200);
  analogWrite(AIN_2, 0);
  //leftmotor
  analogWrite(BIN_1, 200);
  analogWrite(BIN_2, 0);
}
