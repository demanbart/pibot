#include <Servo.h>
#include <Wire.h>

Servo leftRightServo;
Servo upDownServo;
int settings[4];

void setup() {
  //servo's powered by 5V drawn from the arduino
  leftRightServo.attach(11);
  upDownServo.attach(12);
  leftRightServo.write(90);
  upDownServo.write(90);
  settings[2] = 90;
  settings[3] = 90;

  //setup I2C
  Wire.begin(4);                // join i2c bus with address #4
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int speed)
{
  int command[] = {0, 0, 0, 0};
  int cEqS[] = {0, 0, 0, 0};
  int done = 0;
  int pos = 0;
  int tmp = 0;

  while (0 < Wire.available()) // loop through all but the last
  {
    char i = Wire.read(); // receive byte as a character

    tmp = int(byte(i));
    tmp = tmp - tmp%5;
    
    if (tmp > 180)
    {
      command[pos] = 180;         // print the character
    }
    else
    {
      command[pos] = tmp;
    }
    pos++;
  }

  do
  {
    if(command[0]==settings[0])
    {
      cEqS[0] = 1;
    }
    else
    {
      settings[0] = settings[0] + ((settings[0]<command[0])?5:-5);
    }

    if(command[1]==settings[1])
    {
      cEqS[1] = 1;
    }
    else
    {
      settings[1] = settings[1] + ((settings[1]<command[1])?5:-5);
    }

    if(command[2]==settings[2])
    {
      cEqS[2] = 1;
    }
    else
    {
      settings[2] = settings[2] + ((settings[2]<command[2])?5:-5);
    }

    if(command[3]==settings[3])
    {
      cEqS[3] = 1;
    }
    else
    {
      settings[3] = settings[3] + ((settings[3]<command[3])?5:-5);
    }

    for(int i = 0; i < 4; i++)
    {
      done += cEqS[i];
    }
    leftRightServo.write(settings[3]);
    upDownServo.write(settings[2]);
    
  } while(done<4);
}
