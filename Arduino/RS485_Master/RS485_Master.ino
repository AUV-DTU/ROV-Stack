//Master
#include <SoftwareSerial.h>
#include <Servo.h>
Servo fthruster1;
Servo fthruster2;
Servo rthruster;
Servo lthruster;
Servo dthruster1;
Servo dthruster2;

int f1, f2, d1, d2, r, l = 1500;
int prevf1, prevf2, prevr, prevl, prevd1, prevd2 = 1500;

// char ft1[BUFFER_SIZE];
// char ft2[BUFFER_SIZE];
// char lt[BUFFER_SIZE];
// char rt[BUFFER_SIZE];
// char dt1[BUFFER_SIZE];
// char dt2[BUFFER_SIZE];

#define RS_RO 10
#define RS_DI 11
#define RS_DE_RE 12

String ft1 = "";
String ft2 = "";
String lt = "";
String rt = "";
String dt1 = "";
String dt2 = "";

SoftwareSerial RS_Master(RS_RO, RS_DI);  // RX, TX

void setup() {
  Serial.begin(9600);
  RS_Master.begin(9600);
  pinMode(RS_DE_RE, OUTPUT);
  digitalWrite(RS_DE_RE, HIGH);
}

void write(String ft1, String ft2, String lt, String rt, String dt1, String dt2) {
  Serial.print("I am going to write : ");
  Serial.println(String(ft1) + String(ft2) + String(rt) + String(lt) + String(dt1) + String(dt2) + '/');
  delay(1000);
  f1 = ft1.toInt();
  //Serial.print("Surge Value :");

  if (f1 <= 1700 && f1 >= 1300) {
    prevf1 = f1;
    fthruster1.writeMicroseconds(f1);
  } else {
    ft1 = prevf1;
    fthruster1.writeMicroseconds(f1);
  }
  f2 = ft2.toInt();
  //Serial.print("Surge Value :");

  if (f2 <= 1700 && f2 >= 1300) {
    prevf2 = f2;
    fthruster2.writeMicroseconds(f2);
  } else {
    f2 = prevf2;
    fthruster2.writeMicroseconds(f2);
  }
  r = rt.toInt();
  //Serial.print("Surge Value :");

  if (r <= 1700 && r >= 1300) {
    prevr = r;
    rthruster.writeMicroseconds(r);
  } else {
    r = prevr;
    rthruster.writeMicroseconds(r);
  }
  l = lt.toInt();
  //Serial.print("Surge Value :");

  if (l <= 1700 && l >= 1300) {
    prevl = l;
    lthruster.writeMicroseconds(l);
  } else {
    l = prevl;
    lthruster.writeMicroseconds(l);
  }
  d1 = dt1.toInt();
  //Serial.print("Surge Value :");

  if (d1 <= 1700 && d1 >= 1300) {
    prevd1 = d1;
    dthruster1.writeMicroseconds(d1);
  } else {
    d1 = prevd1;
    dthruster1.writeMicroseconds(d1);
  }
  d2 = dt2.toInt();
  //Serial.print("Surge Value :");

  if (d2 <= 1700 && d2 >= 1300) {
    prevd2 = d2;
    dthruster2.writeMicroseconds(d2);
  } else {
    d2 = prevd2;
    dthruster2.writeMicroseconds(d2);
  }
}

void decode(char message[]) {
  int i;
  for (i = 0; i < 4; i++) {
    ft1 += message[i];
  }
  for (i = 5; i < 9; i++) {
    ft2 += message[i];
  }
  for (i = 10; i < 14; i++) {
    lt += message[i];
  }
  for (i = 15; i < 19; i++) {
    rt += message[i];
  }
  for (i = 20; i < 24; i++) {
    dt1 += message[i];
  }
  for (i = 25; i < 29; i++) {
    dt2 += message[i];
  }

  Serial.print("The recieved commands are : ");
  delay(1000);
  Serial.println(String(ft1) + String(ft2) + String(rt) + String(lt) + String(dt1) + String(dt2) + '/');
  delay(1000);
  write(ft1, ft2, lt, rt, dt1, dt2);
  ft1 = "";
  ft2 = "";
  lt = "";
  rt = "";
  dt1 = "";
  dt2 = "";
}



void loop() {
  if (Serial.available()) {
    digitalWrite(RS_DE_RE, HIGH);
    RS_Master.write(Serial.read());
    digitalWrite(RS_DE_RE, LOW);
  }

  if (RS_Master.available()) {
    // while(RS_Master.read() != '/'){
    const int BUFFER_SIZE = 30;
    char message[BUFFER_SIZE] = {};
    int len = RS_Master.readBytesUntil('\n', message, BUFFER_SIZE);
    // }
    // Serial.println(ft1);
    // for(int i = 0; i < len; i++){
    //   Serial.print(message[i]);
    // }
    decode(message);
    // delay(1000);
    // Serial.println();
    // Serial.write(RS_Master.read());
  }
}