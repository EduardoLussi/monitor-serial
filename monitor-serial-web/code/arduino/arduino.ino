#include <TimerOne.h>

//char a[12] = {0x11, 0xAA, 0xA8, 0x37, 0x34, 0x32, 0x35, 0x39, 0x39, 0x31, 0x39};
char a[10] = {0x12, 0xAA, 0xA8, 0x37, 0x34, 0x32, 0x35, 0x39, 0x39, 0x31}; //fire alarm
//char a[9] = {0x14, 0xAA, 0xA8, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30};

int x=500;
int cont = 0;

void setup() {
 Serial.begin(115200);

 //Timer1.initialize(5000000); // Inicializa o Timer1 e configura para um período de 0,5 segundos
 //Timer1.attachInterrupt(decrease_x); // Configura a função callback() como a função para ser chamada a cada interrupção do Timer1
}

void loop() {
  
//  Serial.println(a);
//  delay(1000);
//  Serial.println(a);
//  delay(1000);
//  Serial.println(a);
//  
//  delay(5000); 
//  a[4] = 0x31; a[5] = 0x31; a[6] = 0x39; a[7] = 0x33; // 1193
//  Serial.println(a);
//  
//  delay(2000);
//  a[4] = 0x31; a[5] = 0x35; a[6] = 0x31; a[7] = 0x33; // 1513
//  Serial.println(a);
//  
//  delay(2000);
//  a[4] = 0x33; a[5] = 0x36; a[6] = 0x39; a[7] = 0x30; // 3690
//  Serial.println(a);
//  
//  delay(4000);
//  a[4] = 0x35; a[5] = 0x39; a[6] = 0x32; a[7] = 0x35; a[8] = 0x31; // 5925
//  Serial.println(a);
//  
//  delay(13000);
//  a[4] = 0x37; a[5] = 0x38; a[6] = 0x38; a[7] = 0x34; a[8] = 0x30; // 7884
//  Serial.println(a);
//
//  delay(1000);
//  a[3] = 0x31; a[4] = 0x31; a[5] = 0x31; a[6] = 0x33; a[7] = 0x35; a[8] = 0x31; // 11135
//  Serial.println(a);
//
//  delay(1000);
//  a[3] = 0x31; a[4] = 0x31; a[5] = 0x32; a[6] = 0x30; a[7] = 0x38; a[8] = 0x30; // 11208
//  Serial.println(a);
//
//  delay(7000);
//  a[3] = 0x31; a[4] = 0x32; a[5] = 0x31; a[6] = 0x35; a[7] = 0x34; // 12154
//  Serial.println(a);
//
//  delay(1000);
//  a[3] = 0x31; a[4] = 0x33; a[5] = 0x37; a[6] = 0x34; a[7] = 0x37; // 13747
//  Serial.println(a);
//
//  delay(1000);
//  a[3] = 0x31; a[4] = 0x35; a[5] = 0x33; a[6] = 0x30; a[7] = 0x39; // 15309
//  Serial.println(a);
//
//  delay(1000);
//  a[3] = 0x31; a[4] = 0x35; a[5] = 0x36; a[6] = 0x34; a[7] = 0x36; // 15646
//  Serial.println(a);
//
//  delay(5000);
//  a[3] = 0x31; a[4] = 0x36; a[5] = 0x30; a[6] = 0x37; a[7] = 0x34; // 16074
//  Serial.println(a);
//
//  delay(1000);
//  a[3] = 0x32; a[4] = 0x31; a[5] = 0x33; a[6] = 0x36; a[7] = 0x38; a[8] = 0x31; // 21368
//  Serial.println(a);
//
//  delay(1000);
//  a[3] = 0x32; a[4] = 0x31; a[5] = 0x36; a[6] = 0x36; a[7] = 0x38; a[8] = 0x30; // 21668
//  Serial.println(a);
//
//  delay(100000);

  if (a[6] == 0x36) {
    a[6] = 0x35;
  } else if (a[6] == 0x35) {
    a[6] = 0x34;
  } else if (a[6] == 0x34) {
    a[6] = 0x30;
  } else {
    a[6] = 0x35;
  }
 
  Serial.println(a);
  //Serial.println(cont);
  //cont++;
//  delay(1);
  
}

void decrease_x() {
  if (x == 500) { // 2 - 4
    x = 250;
  } else if (x == 250) { // 4 - 10
    x = 100;
  } else if (x == 100) { // 10 - 20
    x = 50;
  } else if (x == 50) { // 20 - 50
    x = 20;
  } else if (x == 20) { // 50 - 100
    x = 10;
  } else if (x == 10) { // 100 - 200
    x = 5;
  } else if (x == 5) { // 200 - 500
    x = 2;
  } else if (x == 2) { // 500 - 1000
    x = 1;
  } else if (x == 1) { // 100 - MAX
    x = 0;
  }
}
