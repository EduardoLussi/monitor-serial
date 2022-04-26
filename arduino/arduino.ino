char a[10] = {0x12, 0xAA, 0xA8, '7', '4', '2', '2', '0', '0', '0'}; //fire alarm
char t1[16] = {'1', '0', '9', '8', '8', '8', '9', '8', '7', '9', '1', '2', '3', '5', '5', '5'};
char t0[16] = {'2', '2', '1', '1', '1', '1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '2'};

void setup() {
 Serial.begin(115200);
}

void loop() {
  for (int i = 0; i < 4; i++) {
    Serial.println(a);
    delay(500);
  }
  for (int i = 0; i < 16; i++) {
    Serial.println(a);
    a[5] = t0[i];
    a[6] = t1[i];
    delay(1000); 
  }
}
