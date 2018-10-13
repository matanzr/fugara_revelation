#include <Servo.h>
Servo motorSpeed;
int speed = 1500;
char dataString[50] = {0};

void setup() {
  // put your setup code here, to run once:
  motorSpeed.attach(10);
  //1700 ~ 5 hz, 1720 ~6hz

  Serial.begin(9600);

}

void loop() {
  if (Serial.available()){
    int new_speed = Serial.parseInt();
    if (new_speed < 1850 && new_speed > 1150) {
      speed = new_speed;      
    }    
  }
  
  delay(50);  
  motorSpeed.writeMicroseconds(speed);

  sprintf(dataString,"%d",speed);
  Serial.println(dataString);  
}
