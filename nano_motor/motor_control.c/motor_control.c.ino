#include <Servo.h>
Servo motorSpeed;

void setup() {
  // put your setup code here, to run once:
  motorSpeed.attach(10);
  motorSpeed.writeMicroseconds(1690);

}

void loop() {
  // put your main code here, to run repeatedly:

}
