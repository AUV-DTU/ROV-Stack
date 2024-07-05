#include <Ethernet.h> //Load Ethernet Library
#include <EthernetUdp.h> //Load UDP Library
#include <SPI.h> //Load the SPI Library
#include <Servo.h>

Servo ESC;
int throttleValue;
Servo fthruster1;
Servo fthruster2;
Servo rthruster;
Servo lthruster;
Servo dthruster1;
Servo dthruster2;

int f1, f2, l, r, d1, d2 = 1500;
int prevf1, prevf2, prevl , prevr, prevd1, prevd2 = 1500;

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xEE}; //Assign a mac address
IPAddress ip(192,168,0,178); //Assign my IP adress
unsigned int localPort = 5000; //Assign a Port to talk over
char packetBuffer[30];
String datReq; //String for our data
int packetSize; //Size of Packet
EthernetUDP Udp; //Define UDP Object

String message;
String ft1 = "";
String ft2 = "";
String lt = "";
String rt = "";
String dt1 = "";
String dt2 = "";

void setup() {
  fthruster1.attach(5,1100,1900);
  fthruster2.attach(9,1100,1900);
  lthruster.attach(4,1100,1900);
  rthruster.attach(5,1100,1900);
  dthruster1.attach(3,1100,1900);
  dthruster2.attach(6,1100,1900);
  
Serial.begin(9600); //Turn on Serial Port
Ethernet.begin(mac, ip); //Initialize Ethernet
Udp.begin(localPort); //Initialize Udp

//random
randomSeed(analogRead(0));
}

void write(String ft1, String ft2, String lt , String rt, String dt1, String dt2) {
  Serial.print("I am going to write : ");
  Serial.println(String(ft1) + '/' + String(ft2) + '/' + String(lt) + '/' + String(rt) + '/' +  String(dt1) + '/' + String(dt2));
  // delay(1000);
  f1 = ft1.toInt();
  //Serial.print("Surge Value :");

  if (f1 <= 1900 && f1 >= 1100) {
    // prevf1 = f1;
    fthruster1.writeMicroseconds(f1);
  } else {
    f1 = prevf1;
    fthruster1.writeMicroseconds(f1);
  }
  f2 = ft2.toInt();
  //Serial.print("Surge Value :");

  if (f2 <= 1900 && f2 >= 1100) {
    // prevf2 = f2;
    fthruster2.writeMicroseconds(f2);
  } else {
    f2 = prevf2;
    fthruster2.writeMicroseconds(f2);
  }

  d1 = dt1.toInt();
  //Serial.print("Surge Value :");

  if (d1 <= 1900 && d1 >= 1100) {
    // prevd1 = d1;
    dthruster1.writeMicroseconds(d1);
  } else {
    d1 = prevd1;
    dthruster1.writeMicroseconds(d1);
  }
  d2 = dt2.toInt();
  //Serial.print("Surge Value :");

  if (d2 <= 1900 && d2 >= 1100) {
    // prevd2 = d2;
    dthruster2.writeMicroseconds(d2);
  } else {
    d2 = prevd2;
    dthruster2.writeMicroseconds(d2);
  }

  // delay(1000);
}


void decode(String message) {
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
  if(val2<=1100 || val2>=1900){
    l = "1500"; 
  }
  for (i = 15; i < 19; i++) {
    rt += message[i];
  }
  int val3 = rt.toInt();
  if(val3<=1100 || val3>=1900){
    r = "1500"; 
  }
  for (i = 20; i < 24; i++) {
    dt1 += message[i];
  }
  int val4 = dt1.toInt();
  if(val4<=1100 || val4>=1900){
    d1 = "1500"; 
  }
  for (i = 25; i < 29; i++) {
    dt2 += message[i];
  }
  int val5 = dt2.toInt();
  if(val5<=1100 || val5>=1900){
    d2 = "1500"; 
  }

  Serial.print("The recieved commands are : ");
  // delay(1000);
  Serial.println(String(ft1) + '/' + String(ft2) + '/' + String(lt) + '/' + String(rt) + '/' +  String(dt1) + '/' + String(dt2));
  // delay(1000);
  write(ft1, ft2, lt,rt, dt1, dt2);
  // writeTest(ft1);
  ft1 = "";
  ft2 = "";
  lt = "";
  rt = "";
  dt1 = "";
  dt2 = "";
}

void loop() {
  
  packetSize = Udp.parsePacket(); //Read theh packetSize
  
  if(packetSize>0){ //Check to see if a request is present
  
  Udp.read(packetBuffer, 30); //Reading the data request on the Udp
  String datReq(packetBuffer); //Convert packetBuffer array to string datReq
  message = datReq.substring(0,29);
  decode(message);
  Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());  //Initialize Packet send
    Udp.print(String(random(0,50))); //Send string back to client 
    Udp.endPacket();
    
  // if (datReq.length() == 29 || datReq.length() == 30){
  //   message = datReq;
  //   ft1 = (message.substring(0, 4)).toInt();
  //   ft2 = (message.substring(5, 9)).toInt();
  //   rt = (message.substring(10, 14)).toInt();
  //   lt = (message.substring(15, 19)).toInt();
  //   dt1 = (message.substring(20, 24)).toInt();
  //   dt2 = (message.substring(25, 29)).toInt();
  //   Serial.println(message);
  //   Serial.println('\n');
  //   delay(1000);
  // }
  memset(packetBuffer, 0, 30);
}
// else{
//   Serial.println("Not Received");
// }
}