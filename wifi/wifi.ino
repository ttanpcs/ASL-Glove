#include <SPI.h>
#include <WiFi.h>

// byte Pins[] = {1, 2, 3, 5, 14, 15, 16};
// int num_pins = 7;
byte mac[6];
void setup() {
  Serial.begin(9600);
  // pinMode(4, OUTPUT); 
  // pinMode(8, OUTPUT); 
  Serial.println("ASL-Glove");
  Serial.print("ESP Board MAC Address:  ");
  WiFi.macAddress(mac);
  Serial.print("MAC: ");
  Serial.print(mac[5],HEX);
  Serial.print(":");
  Serial.print(mac[4],HEX);
  Serial.print(":");
  Serial.print(mac[3],HEX);
  Serial.print(":");
  Serial.print(mac[2],HEX);
  Serial.print(":");
  Serial.print(mac[1],HEX);
  Serial.print(":");
  Serial.println(mac[0],HEX);
}

void loop() {
  // if (central) {
  //   Serial.print("Connected to central: ");
  //   Serial.println(central.address());
  //   int current = 0;
  //   digitalWrite(4, HIGH); 
  //   digitalWrite(8, LOW); 
  //   Serial.println("4 High, 8 Low");

  //   while (central.connected()) {
  //     Serial.println("");
  //     Serial.print(analogRead(A0));
  //     Serial.print(" ");
  //     for (int i = 0; i < num_pins; i++) {
  //         Serial.print(analogRead(Pins[i]));
  //         Serial.print(" ");
  //     }
  //     Serial.println("");
  //     if (switchCharacteristic.written()) {
  //       if (switchCharacteristic.value()) {   // any value other than 0
  //         if (current) {
  //           // Serial.println("Stop");
  //           digitalWrite(4, HIGH); 
  //           digitalWrite(8, LOW); 
  //           Serial.println("4 High, 8 Low");
  //           current = 0;
  //         } else {
  //           // Serial.println("Start");
  //           digitalWrite(4, LOW); 
  //           digitalWrite(8, HIGH); 
  //           Serial.println("8 High, 4 Low");
  //           current = 1;
  //         }
  //       } 
  //     }
  //     delay(1000);
  //   }
  //   Serial.print(F("Disconnected from central: "));
  //   Serial.println(central.address());
  // }
}
