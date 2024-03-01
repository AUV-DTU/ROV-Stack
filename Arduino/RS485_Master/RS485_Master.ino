//Master
#include <SoftwareSerial.h>
#include <Servo.h>
Servo ESC;
int throttleValue;
Servo fthruster1;
Servo fthruster2;
Servo rthruster;
Servo lthruster;
Servo dthruster1;
Servo dthruster2;

int f1, f2, d1, d2 = 1500;
int r,l = 1100;
int prevf1, prevf2, prevd1, prevd2 = 1500;
int prevr, prevl = 1100;

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
  fthruster1.attach(3,1100,1900);
  fthruster2.attach(6,1100,1900);
  lthruster.attach(4,1100,1900);
  rthruster.attach(5,1100,1900);
  dthruster1.attach(7,1100,1900);
  dthruster2.attach(2,1100,1900);
  Serial.begin(9600);
  RS_Master.begin(9600);
  pinMode(RS_DE_RE, OUTPUT);
  digitalWrite(RS_DE_RE, HIGH);
}

void write(String ft1, String ft2, String lt, String rt, String dt1, String dt2) {
  Serial.print("I am going to write : ");
  Serial.println(String(ft1) + '/' + String(ft2) + '/' + String(lt) + '/' + String(rt) + '/' +  String(dt1) + '/' + String(dt2));
  // delay(1000);
  f1 = ft1.toInt();
  //Serial.print("Surge Value :");

  if (f1 <= 1700 && f1 >= 1300) {
    // prevf1 = f1;
    fthruster1.writeMicroseconds(f1);
  } else {
    f1 = prevf1;
    fthruster1.writeMicroseconds(f1);
  }
  f2 = ft2.toInt();
  //Serial.print("Surge Value :");

  if (f2 <= 1700 && f2 >= 1300) {
    // prevf2 = f2;
    fthruster2.writeMicroseconds(f2);
  } else {
    f2 = prevf2;
    fthruster2.writeMicroseconds(f2);
  }
  r = rt.toInt();
  //Serial.print("Surge Value :");

  if (r <= 1700 && r >= 1300) {
    // prevr = r;
    rthruster.writeMicroseconds(r);
  } else {
    r = prevr;
    rthruster.writeMicroseconds(r);
  }
  l = lt.toInt();
  //Serial.print("Surge Value :");

  if (l <= 1700 && l >= 1300) {
    // prevl = l;
    lthruster.writeMicroseconds(l);
  } else {
    l = prevl;
    lthruster.writeMicroseconds(l);
  }
  d1 = dt1.toInt();
  //Serial.print("Surge Value :");

  if (d1 <= 1700 && d1 >= 1300) {
    // prevd1 = d1;
    dthruster1.writeMicroseconds(d1);
  } else {
    d1 = prevd1;
    dthruster1.writeMicroseconds(d1);
  }
  d2 = dt2.toInt();
  //Serial.print("Surge Value :");

  if (d2 <= 1700 && d2 >= 1300) {
    // prevd2 = d2;
    dthruster2.writeMicroseconds(d2);
  } else {
    d2 = prevd2;
    dthruster2.writeMicroseconds(d2);
  }

  delay(1000);
}

void writeTest(String rt){
  Serial.print("I am going to write : ");
  Serial.println(String(rt));

  throttleValue = rt.toInt();
  // for(int i = 0;i<10;i++){
    throttleValue -= 450;
    Serial.println(String(throttleValue));
  // }
  // throttleValue -= 600;
  
  // throttleValue = constrain(throttleValue, 0, 180); // Ensure throttle value is within valid range (0-180)
    
    // Scale throttle value to match ESC pulse width range (1000-2000 microseconds)
  // int pulseWidth = map(throttleValue, 0, 180, 1100, 1900);
    
  lthruster.writeMicroseconds(throttleValue); // Send the pulse width to the ESC
  delay(1000); // Wait for ESC to respond (adjust delay as needed)
}

void decode(char message[]) {
  int i;
  for (i = 0; i < 4; i++) {
    ft1 += message[i];
  }
  int val = ft1.toInt();
  if(val<=1100 || val>=1900){
    ft1 = "1500"; 
  }
  for (i = 5; i < 9; i++) {
    ft2 += message[i];  
  }
  int val1 = ft2.toInt();
  if(val1<=1100 || val1>=1900){
    ft2 = "1500"; 
  }
  for (i = 10; i < 14; i++) {
    lt += message[i];
  }
  int val2 = lt.toInt();
  if(val2<=1100 || val2>=1600){
    lt = "1100"; 
  }
  for (i = 15; i < 19; i++) {
    rt += message[i];
  }
  int val3 = rt.toInt();
  if(val3<=1100 || val3>=1600){
    rt = "1100"; 
  }
  for (i = 20; i < 24; i++) {
    dt1 += message[i];
  }
  int val4 = dt1.toInt();
  if(val4<=1100 || val4>=1900){
    dt1 = "1500"; 
  }
  for (i = 25; i < 29; i++) {
    dt2 += message[i];
  }
  int val5 = dt2.toInt();
  if(val5<=1100 || val5>=1900){
    dt2 = "1500"; 
  }

  Serial.print("The recieved commands are : ");
  // delay(1000);
  Serial.println(String(ft1) + '/' + String(ft2) + '/' + String(lt) + '/' + String(rt) + '/'  +  String(dt1) + '/' + String(dt2));
  // delay(1000);
  write(ft1, ft2, lt, rt, dt1, dt2);
  // writeTest(ft1);
  ft1 = "";
  ft2 = "";
  lt = "";
  rt = "";
  dt1 = "";
  dt2 = "";
}

void decodeTest(char message[]){
  for(int i = 0;i<4;i++){
    rt += message[i];
  }
  Serial.print("The recieved commands are : ");
  Serial.println(String(rt));
  writeTest(rt);
  rt= "";

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
    int len = RS_Master.readBytesUntil('*', message, BUFFER_SIZE);
    // }
    // Serial.println(ft1);
    // for(int i = 0; i < len; i++){
    //   Serial.print(message[i]);
    // }
    if(len == 29 || len == 30){
      decode(message);
      delay(1000);
    }
    // if(len == 4 || len == 5){
    //   decodeTest(message);
    // }
    // int val = Serial.parseInt();
    // decodeTest(val);
    // delay(1000);
    // Serial.println();
    // Serial.write(RS_Master.read());
  }
}
