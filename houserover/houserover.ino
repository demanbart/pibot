#include <Servo.h>
#include <Wire.h>

Servo leftRightServo;
Servo upDownServo;
int settings[4];
int command[6];

int BIN_1 = 5;
int AIN_1 = 6;
int MAX_PWM_VOLTAGE = 100;
int MAX_SERVO_ANGLE = 180;

void setup() {
  //servo's powered by 5V drawn from the arduino
  leftRightServo.attach(11);
  upDownServo.attach(12);
  pinMode(BIN_1, OUTPUT);
  pinMode(AIN_1, OUTPUT);
  
  leftRightServo.write(90);
  upDownServo.write(90);
  settings[0] = 0;
  settings[0] = 0;
  settings[2] = 90;
  settings[3] = 90;

  //setup I2C
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void loop() {
  // put your main code here, to run repeatedly:
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int speed)
{
  int pos = 0;
  int tmp;
  Serial.println(Wire.available());
  while (0 < Wire.available()) // loop through all but the last
  {
    char i = Wire.read(); // receive byte as a character
    tmp = int(byte(i));
    command[pos] = tmp;
    pos++;
  }

  //bit one has the left motor value
  settings[0] = (command[2] > MAX_PWM_VOLTAGE)?MAX_PWM_VOLTAGE:command[2];
  settings[1] = (command[3] > MAX_PWM_VOLTAGE)?MAX_PWM_VOLTAGE:command[3];
  settings[2] = (command[4] > MAX_SERVO_ANGLE)?MAX_SERVO_ANGLE:command[4];
  settings[3] = (command[5] > MAX_SERVO_ANGLE)?MAX_SERVO_ANGLE:command[5];
  
  leftRightServo.write(settings[3]);
  upDownServo.write(settings[2]);
  //rightmotor
  analogWrite(AIN_1, settings[0]);
  //leftmotor
  analogWrite(BIN_1, settings[1]);

  Serial.print(settings[0]);
  Serial.print("|");
  Serial.print(settings[1]);
  Serial.print("|");
  Serial.print(settings[2]);
  Serial.print("|");
  Serial.println(settings[3]);
}
