#include <SoftwareSerial.h>

#define RS_RO 10
#define RS_DI 11
#define RS_DE_RE 12

SoftwareSerial RS_Slave(RS_RO, RS_DI);  // RX, TX

String message;
int ft1;
int ft2;
int rt;
int lt;
int dt1;
int dt2;

void setup() {
  Serial.begin(9600);
  RS_Slave.begin(9600);
  pinMode(RS_DE_RE, OUTPUT);
  digitalWrite(RS_DE_RE, LOW);
}

void loop() {
  if (RS_Slave.available()) {
    Serial.write(RS_Slave.read());
  }

  if (Serial.available() > 0) {
    message = Serial.readStringUntil('*');
    if(message.length() == 29 || message.length() == 30){
      ft1 = (message.substring(0, 4)).toInt();
      ft2 = (message.substring(5, 9)).toInt();
      rt = (message.substring(10, 14)).toInt();
      lt = (message.substring(15, 19)).toInt();
      dt1 = (message.substring(20, 24)).toInt();
      dt2 = (message.substring(25, 29)).toInt();
      digitalWrite(RS_DE_RE, HIGH);
      for (int i = 0; i < message.length(); i++) {
        RS_Slave.write(message[i]);
      }
      digitalWrite(RS_DE_RE, LOW);
    }
    else{
      message = "1500/1500/1100/1100/1500/1500"
      ft1 = (message.substring(0, 4)).toInt();
      ft2 = (message.substring(5, 9)).toInt();
      rt = (message.substring(10, 14)).toInt();
      lt = (message.substring(15, 19)).toInt();
      dt1 = (message.substring(20, 24)).toInt();
      dt2 = (message.substring(25, 29)).toInt();
      digitalWrite(RS_DE_RE, HIGH);
      for (int i = 0; i < message.length(); i++) {
        RS_Slave.write(message[i]);
      }
      digitalWrite(RS_DE_RE, LOW);
    }
    

    
  }

  Serial.println(String(ft1) + String(ft2) + String(rt) + String(lt) + String(dt1) + String(dt2) + '/');
}
