#include <Arduino_LSM6DS3.h>

#include <ArduinoECCX08.h>
#include <ArduinoJson.h>
#include <ArduinoBearSSL.h>
#include <ArduinoMqttClient.h>
#include <WiFiNINA.h> 

#include "credentials.h"

WiFiClient    wifiClient;            
BearSSLClient sslClient(wifiClient); 
MqttClient    mqttClient(sslClient);

unsigned long lastMillis = 0;
boolean shouldPublish = false;
unsigned long currentNumber = 0;
int type = 1;

String readLine() {
  String line;

  while (1) {
    if (Serial.available()) {
      char c = Serial.read();

      if (c == '\r') {
        // ignore
      } else if (c == '\n') {
        break;
      }

      line += c;
    }
  }

  line.trim();

  return line;
}

void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT); 
  pinMode(6, OUTPUT); 
  while (!Serial);
  Serial.println("Enter last database number");
  currentNumber = readLine().toInt();
  Serial.println(currentNumber);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
  if (!ECCX08.begin()) {
    Serial.println("No ECCX08 present!");
    while (1);
  }
  
  ArduinoBearSSL.onGetTime(getTime);
  sslClient.setEccSlot(0, certificate);
  mqttClient.setId("GloveIO");
  mqttClient.onMessage(onMessageReceived);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  if (!mqttClient.connected()) {
    connectMQTT();
  }
  mqttClient.poll();

  if (shouldPublish) {
    publishMessage();
  }
}

unsigned long getTime() {
  // get the current time from the WiFi module  
  return WiFi.getTime();
}

void connectWiFi() {
  Serial.print("Attempting to connect to SSID: ");
  Serial.print(ssid);
  Serial.print(" ");

  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }
  Serial.println();

  Serial.println("You're connected to the network");
  Serial.println();
}

void connectMQTT() {
  Serial.print("Attempting to MQTT broker: ");
  Serial.print(broker);
  Serial.println(" ");

  while (!mqttClient.connect(broker, 8883)) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }
  Serial.println();

  Serial.println("You're connected to the MQTT broker");
  Serial.println();

  // subscribe to a topic
  mqttClient.subscribe("gloveio/sub");
}

void publishMessage() {
  float ax, ay, az;
  float gx, gy, gz;
  StaticJsonDocument<200> doc;
  StaticJsonDocument<200> accel;
  if (type == 1) {
    digitalWrite(2, LOW);   
    digitalWrite(6, HIGH); 
  } else {
    digitalWrite(2, HIGH);   
    digitalWrite(6, LOW);     
  }
  doc["control"] = type;
  type = type * -1;
  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(ax, ay, az);
    accel["ax"] = ax;
    accel["ay"] = ay;
    accel["az"] = az;
  }
  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(gx, gy, gz);
    accel["gx"] = gx;
    accel["gy"] = gy;
    accel["gz"] = gz;
  }
  
  doc["currentNumber"] = currentNumber;
  doc["time"] = millis() - lastMillis;
  doc["A0"] = analogRead(A0);
  doc["A1"] = analogRead(A1);
  doc["A2"] = analogRead(A2);
  doc["A3"] = analogRead(A3);
  doc["A6"] = analogRead(A6);
  doc["A7"] = analogRead(A7);
  char jsonBuffer[2048];
  char accelBuffer[2048];
  serializeJson(doc, jsonBuffer);
  serializeJson(accel, accelBuffer);
  mqttClient.beginMessage("gloveio/pub");
  mqttClient.print("{\"a\":");
  mqttClient.print(jsonBuffer);
  mqttClient.print(", \"b\":");
  mqttClient.print(accelBuffer);
  mqttClient.print("}");
  mqttClient.endMessage();
}

void onMessageReceived(int messageSize) {
  Serial.println("Message Recieved");
  if (!shouldPublish) {
    currentNumber++;
    Serial.println(currentNumber);
  }
  shouldPublish = !shouldPublish;
  lastMillis = millis();
}
