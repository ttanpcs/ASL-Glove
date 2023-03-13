#include "Arduino_BMI270_BMM150.h"
#include <ArduinoJson.h>

enum class Mode { Idle, Write, Snapshot };
Mode current_mode;
bool is_start;

void setup() {
  Serial.begin(9600);
  while (!Serial);
  while (!IMU.begin());
  current_mode = Mode::Idle;
  is_start = true;
}

void readSensors() {
  float ax, ay, az;
  float gx, gy, gz;
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

  char imBuffer[2048];
  serializeJson(im, imBuffer);
  Serial.print(imBuffer);
}

void readVoltages() {
  StaticJsonDocument<200> doc;
  
  doc["A0"] = analogRead(A0);
  doc["A1"] = analogRead(A1);
  doc["A2"] = analogRead(A2);
  doc["A3"] = analogRead(A3);
  doc["A6"] = analogRead(A6);
  doc["A7"] = analogRead(A7);

  char jsonBuffer[2048];
  serializeJson(doc, jsonBuffer);
  Serial.print(jsonBuffer);
}

void loop() {
  if (Serial.available()) {
    Mode read_mode = static_cast<Mode>(Serial.parseInt());
    if (current_mode == Mode::Idle && read_mode != Mode::Idle) {
      is_start = true;
    }
    current_mode = read_mode;
  }
  if (current_mode != Mode::Idle) {
    Serial.print(is_start);
    readSensors();
    readVoltages();
    Serial.println();
    if (current_mode == Mode::Snapshot) {
      current_mode = Mode::Idle;
    }
    is_start = false;
  }
}

