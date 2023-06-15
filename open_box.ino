#include <Servo.h>
#define trigPin 12
#define echoPin 11

Servo servo;
int sound = 250;


void setup() {
  // put your setup code here, to run once:

Serial.begin (9600);
pinMode(trigPin,OUTPUT);
pinMode(echoPin,INPUT);
servo.attach(9);
servo.write(140);

}

void loop() {
  int pos;
  // put your main code here, to run repeatedly:
    long duration, distance;
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin,LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = (duration/2) / 29.1;
    if (distance < 10) {
      Serial.println("the distance is less than 10");
      for (pos = 140; pos >45; pos -= 1) {
      servo.write(pos);
      delay(25);
    }

    delay(10000);

    for (pos = 45; pos < 140; pos += 1) {
      servo.write(pos);
      delay(25);
    }
    }
    else if (distance > 60 || distance <= 0) {
      Serial.println("The distance is more than 60");
    }

    else {
    servo.write(140);
    Serial.print(distance);
    Serial.println(" cm");
    }
    delay(1000); 
}
