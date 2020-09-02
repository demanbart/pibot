#include <Servo.h>
#include <Wire.h>

Servo leftRightServo;
Servo upDownServo;

void setup() {
  //servo's powered by 5V drawn from the ardion
  leftRightServo.write(90);
  upDownServo.write(90);
  leftRightServo.attach(12);
  upDownServo.attach(13);

  //setup I2C
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int speed)
{
  int command[] = {0,0,0,0};
  int pos = 0;  
  int tmp = 0;
  
  while(0 < Wire.available()) // loop through all but the last
  {
   char i = Wire.read(); // receive byte as a character

   tmp = int(byte(i));
   if(tmp > 180)
   {
    command[pos] = 180;         // print the character
   }
   else
   {
    command[pos] = tmp;
   }
   pos++;
  }
  leftRightServo.write(command[3]);
  Serial.print("left right:");
  Serial.println(command[3]);
  upDownServo.write(command[2]);
  Serial.print("up down:");
  Serial.println(command[2]);
  
}
