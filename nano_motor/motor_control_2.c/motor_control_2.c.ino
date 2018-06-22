#include <Servo.h>
Servo motorSpeed;
int speed = 1500;

void setup() {
  // put your setup code here, to run once:
  motorSpeed.attach(10);
  //1700 ~ 5 hz, 1720 ~6hz

}

void loop() {
  // put your main code here, to run repeatedly:
  if (speed > 1370) {
    speed--;   
    motorSpeed.writeMicroseconds(speed);  
  }
  delay(15);   
}
