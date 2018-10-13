#include <Servo.h>
Servo motorSpeed;
int speed = 1500;
int target_speed = speed;
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
      target_speed = new_speed;      
    } else if (new_speed == 1) {
      sprintf(dataString,"%d",speed);
      Serial.println(dataString);  
    }
  }

  if (speed < target_speed) {
    speed+= 3;
  } else if ( speed > target_speed) {
    speed-= 3;
  }
  
  delay(15);  
  motorSpeed.writeMicroseconds(speed);
  
}
