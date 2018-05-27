#include <Servo.h>
Servo motorSpeed;

void setup() {
  // put your setup code here, to run once:
  motorSpeed.attach(10);
  motorSpeed.writeMicroseconds(1700); //1700 ~ 5 hz, 1720 ~6hz

}

void loop() {
  // put your main code here, to run repeatedly:

}
