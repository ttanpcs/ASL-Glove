#include "Arduino_BMI270_BMM150.h"
#include <ArduinoJson.h>

void setup() {
  Serial.begin(9600);
  while (!Serial);
  while (!IMU.begin());
}

void loop() {
  float ax, ay, az;
  float gx, gy, gz;
  StaticJsonDocument<200> doc;
  StaticJsonDocument<200> im;
  while (!IMU.accelerationAvailable());
  IMU.readAcceleration(ax, ay, az);
  im["ax"] = ax;
  im["ay"] = ay;
  im["az"] = az;

  while (!IMU.gyroscopeAvailable());
  IMU.readGyroscope(gx, gy, gz);
  im["gx"] = gx;
  im["gy"] = gy;
  im["gz"] = gz;
  
  doc["A0"] = analogRead(A0);
  doc["A1"] = analogRead(A1);
  doc["A2"] = analogRead(A2);
  doc["A3"] = analogRead(A3);
  doc["A6"] = analogRead(A6);
  doc["A7"] = analogRead(A7);

  char jsonBuffer[2048];
  char imBuffer[2048];
  serializeJson(doc, jsonBuffer);
  serializeJson(im, imBuffer);
  Serial.println(jsonBuffer);
  Serial.println(imBuffer);
}

