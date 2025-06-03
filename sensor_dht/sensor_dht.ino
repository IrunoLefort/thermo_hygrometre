#include "DHT.h"
#define DHTpin A0
#define DHTtype DHT11

DHT my_sensor(DHTpin, DHTtype);
float tempF;
float tempC;
float humidity;

void setup() {
  Serial.begin(9600);
  my_sensor.begin();
  delay(500);
}

void loop() {
  tempC = my_sensor.readTemperature();
  tempF = my_sensor.readTemperature(true);
  humidity = my_sensor.readHumidity();
  Serial.print(tempC);
  Serial.print(",");
  Serial.println(humidity);
  delay(1000);
}