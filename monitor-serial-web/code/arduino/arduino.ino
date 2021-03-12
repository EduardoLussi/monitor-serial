#include <TimerOne.h>

int x = 1000;
//char a[12] = {0x11, 0xAA, 0xA8, 0x37, 0x34, 0x32, 0x35, 0x39, 0x39, 0x31, 0x39};
char a[10] = {0x12, 0xAA, 0xA8, 0x37, 0x34, 0x32, 0x35, 0x39, 0x39, 0x31}; //fire alarm

void setup() {
 Serial.begin(115200);

 //Timer1.initialize(5000000); // Inicializa o Timer1 e configura para um período de 0,5 segundos
// Timer1.attachInterrupt(decrease_x); // Configura a função callback() como a função para ser chamada a cada interrupção do Timer1
}

void loop() {

  Serial.println(a);

  if (a[6] == 0x36) {
    a[6] = 0x35;
  } else if (a[6] == 0x35) {
    a[6] = 0x34;
  } else if (a[6] == 0x34) {
    a[6] = 0x30;
  } else {
    a[6] = 0x35;
  }
  
  //Serial.println(x); 
  delay(x);
  
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
