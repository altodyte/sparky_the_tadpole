// tadpole_wstop
// Michael Bocamazo
// 2014/12/12
#include <Servo.h> 
 
Servo servo_0, servo_1, servo_2;
const int servo_0_pin = 10;
const int servo_1_pin = 11;
const int servo_2_pin = 12;
int p0 = 90;
int p1 = 90;
int p2 = 90;
const int IR_left = A0;
const int IR_center = A1;
const int IR_right = A2;
int threshold_lateral = 300;
int threshold_center = 300;
int IR_left_val, IR_center_val, IR_right_val;
const int LED_left = 30;
const int LED_center = 31;
const int LED_right = 32;
const int LED_red = 40;
const int LED_yellow = 41;
const int LED_green = 42;
const int LED_white = 43;

int state;
const int STOP = 0;
const int TL = 1;  
const int STRAIGHT = 2;
const int TR = 3;
const int CTL = 4;
const int CSTRAIGHT = 5;
const int CTR = 6;

//hard code SSwim parameters before optimization
float freq_all = 2;
float amp0 = 60;
float amp1 = 80;
float amp2 = 80;
float phase1 = 1.57;
float phase2 = 1.57; //phases should be relative

void setup() 
{ 
  state = STRAIGHT;
  Serial.begin(9600);
  pinMode(LED_red, OUTPUT);
  pinMode(LED_yellow, OUTPUT);
  pinMode(LED_green, OUTPUT);
  pinMode(LED_white, OUTPUT);
  pinMode(LED_left, OUTPUT);
  pinMode(LED_center, OUTPUT);
  pinMode(LED_right, OUTPUT);

  servo_0.attach(servo_0_pin);
  servo_1.attach(servo_1_pin);
  servo_2.attach(servo_2_pin);
  servo_0.write(p0);
  servo_1.write(p1);
  servo_2.write(p2);
  //startup test display of lights
  delay(100);
  digitalWrite(LED_red, HIGH);
  digitalWrite(LED_yellow, HIGH);
  digitalWrite(LED_green, HIGH);
  digitalWrite(LED_white, HIGH);
  delay(500);
  digitalWrite(LED_red, LOW);
  digitalWrite(LED_yellow, LOW);
  digitalWrite(LED_green, LOW);
  digitalWrite(LED_white, LOW);
  digitalWrite(LED_left, HIGH);
  digitalWrite(LED_center, HIGH);
  digitalWrite(LED_right, HIGH);
  digitalWrite(13,HIGH);
  delay(500);
  digitalWrite(LED_left, LOW);
  digitalWrite(LED_center, LOW);
  digitalWrite(LED_right, LOW);
  digitalWrite(13,LOW);
  delay(500);
}  
 
void loop() 
{ 
  read_in_sensor_vals();
  print_sensor_vals();
  set_directional_lights();
  if (Serial.available()>0) {
    receive_comms();
  }
  switch(state){
    case STOP:     STOP_fcn();      break;
    case TL:       TL_fcn();        break;
    case STRAIGHT: STRAIGHT_fcn();  break;
    case TR:       TR_fcn();        break;
    case CTL:      CTL_fcn();       break;
    case CSTRAIGHT: CSTRAIGHT_fcn(); break;
    case CTR:      CTR_fcn();       break; 
    default:
    STOP_fcn();
    Serial.println("SWITCH CASE ERROR");
    digitalWrite(LED_red, HIGH);
    digitalWrite(LED_yellow, HIGH);
    digitalWrite(LED_green, HIGH);
  }
  Serial.print("[STP TL STR TR CTL CSTR CTR] State: ");
  Serial.println(state);  
  delay(10);
}
void receive_comms()
{
  char buffer[64];
  int i, ch, val;
  long j, num;

  for (i = 0; i<63; i++) {
    for (ch = Serial.read(); ch==-1; ch = Serial.read()) {}
    if (ch==';')
      break;
    buffer[i] = (char)ch;
  }
  buffer[i] = '\0';
  if (strncmp(buffer, "STOP", 4)){
    state = STOP;}
  else if (strncmp(buffer, "GO", 2)){
    state = STRAIGHT;}
  else if (strncmp(buffer, "CTL", 3)){
    state = CTL;}
  else if (strncmp(buffer, "CF", 2)){
    state = CSTRAIGHT;}
  else if (strncmp(buffer, "CTR", 3)){
    state = CTR;}
}
    
  
  ((!strncmp(buffer, "ao0", 3)) || (!strncmp(buffer, "AO0", 3))) {
    ao0 = atoi(buffer+3);
    rwm.DACwriteChannel(0, ao0);
  
}

void STOP_fcn()
{
  reset_state_lights();
  digitalWrite(LED_red, HIGH);
  digitalWrite(LED_white, HIGH);
  //servos aren't rewritten here
}
void TL_fcn()
{
  reset_state_lights();
  digitalWrite(LED_yellow, HIGH);
  p0 = 160;
  servo_0.write(p0);
  CSwim();
  if ((IR_right_val < threshold_lateral)&&(IR_center_val< threshold_center)){
//    Serial.println("From TL goto STRAIGHT");
    state = STRAIGHT;}
}
void TR_fcn()
{
  reset_state_lights();
  digitalWrite(LED_yellow, HIGH);
  p0 = 20;
  servo_0.write(p0);
  CSwim();
  if ((IR_left_val < threshold_lateral)&&(IR_center_val< threshold_center)){
//    Serial.println("From TR goto STRAIGHT");
    state = STRAIGHT;}
}
void CSwim()//
{
  float time = millis()/1000.0;
  int amplitude = 60;
  float frequency = 1.5;
  float pos;
  pos = amplitude*sin(frequency*time)+90.0;
  servo_1.write(p1);
  servo_2.write(p2);
}
void STRAIGHT_fcn()
{
  reset_state_lights();
  digitalWrite(LED_green, HIGH);
  SSwim();
  if (IR_left_val > threshold_lateral){
//    Serial.println("From STRAIGHT goto TR");
    state = TR;}
  if (IR_right_val > threshold_lateral){
//    Serial.println("From STRAIGHT goto TL");
    state = TL;}
  if (IR_center_val > threshold_center){
    if (IR_left_val > IR_right_val){
//      Serial.println("From STRAIGHT goto TR, bc center");
      state = TR;}
    else {state = TL;}
  }
}
void SSwim()
{
  float time = millis()/1000.0;
  p0 = amp0*sin(freq_all*time)+90;//no phase offset
  p1 = amp1*sin(freq_all*time+phase1)+90;
  p2 = amp2*sin(freq_all*time+phase1+phase2)+90; //phase offset should be r
  servo_0.write(p0);
  servo_1.write(p1);
  servo_2.write(p2);
}
void CTL_fcn()
{
  reset_state_lights();
  digitalWrite(LED_yellow, HIGH);
  digitalWrite(LED_white, HIGH);
  p0 = 160;
  servo_0.write(p0);
  CSwim();
}
void CTR_fcn()
{
  reset_state_lights();
  digitalWrite(LED_yellow, HIGH);
  digitalWrite(LED_white, HIGH);
  p0 = 20;
  servo_0.write(p0);
  CSwim();
}
void CSTRAIGHT_fcn()
{
  reset_state_lights();
  digitalWrite(LED_green, HIGH);
  digitalWrite(LED_white, HIGH);
  SSwim();
}

void reset_state_lights()
{
  digitalWrite(LED_red, LOW);
  digitalWrite(LED_yellow, LOW);
  digitalWrite(LED_green, LOW);
  digitalWrite(LED_white, LOW);
}  

void print_sensor_vals()
{
  Serial.print("IR Left: ");
  Serial.print(IR_left_val);
  Serial.print(" IR Center: ");
  Serial.print(IR_center_val);
  Serial.print(" IR Right: ");
  Serial.println(IR_right_val);
}
void read_in_sensor_vals()
{
  IR_left_val = analogRead(IR_left);
  IR_center_val = analogRead(IR_center);
  IR_right_val = analogRead(IR_right);
}
void set_directional_lights()
{
  if (IR_left_val>threshold_lateral){digitalWrite(LED_left, HIGH);}
  else{digitalWrite(LED_left, LOW);}
  if (IR_right_val>threshold_lateral){digitalWrite(LED_right, HIGH);}
  else{digitalWrite(LED_right, LOW);}    
  if (IR_center_val>threshold_center){digitalWrite(LED_center, HIGH);}
  else{digitalWrite(LED_center, LOW);}
}

/*
void command() {
  char buffer[64];
  int i, ch, val;
  long j, num;

  for (i = 0; i<63; i++) {
    for (ch = Serial.read(); ch==-1; ch = Serial.read()) {}
    if (ch==';')
      break;
    buffer[i] = (char)ch;
  }
  buffer[i] = '\0';
  if ((!strncmp(buffer, "ao0?", 4)) || (!strncmp(buffer, "AO0?", 4))) {
    Serial.print("AO0 = ");
    Serial.println(ao0, DEC);
  } else if ((!strncmp(buffer, "ao0", 3)) || (!strncmp(buffer, "AO0", 3))) {
    ao0 = atoi(buffer+3);
    rwm.DACwriteChannel(0, ao0);
  } else if ((!strncmp(buffer, "ao1?", 4)) || (!strncmp(buffer, "AO1?", 4))) {
    Serial.print("AO1 = ");
    Serial.println(ao1, DEC);
  } else if ((!strncmp(buffer, "ao1", 3)) || (!strncmp(buffer, "AO1", 3))) {
    ao1 = atoi(buffer+3);
    rwm.DACwriteChannel(1, ao1);
  } else if ((!strncmp(buffer, "ai0?", 4)) || (!strncmp(buffer, "AI0?", 4))) {
    Serial.print("AI0 = ");
    Serial.println(rwm.ADCreadChannel(0), DEC);
  } else if ((!strncmp(buffer, "ai1?", 4)) || (!strncmp(buffer, "AI1?", 4))) {
    Serial.print("AI1 = ");
    Serial.println(rwm.ADCreadChannel(1), DEC);
  } else if ((!strncmp(buffer, "ai2?", 4)) || (!strncmp(buffer, "AI2?", 4))) {
    Serial.print("AI2 = ");
    Serial.println(rwm.ADCreadChannel(2), DEC);
  } else if ((!strncmp(buffer, "ai3?", 4)) || (!strncmp(buffer, "AI3?", 4))) {
    Serial.print("AI3 = ");
    Serial.println(rwm.ADCreadChannel(3), DEC);
  } else if ((!strncmp(buffer, "aid0?", 5)) || (!strncmp(buffer, "AID0?", 5))) {
    Serial.print("AID0 = ");
    Serial.println(rwm.ADCreadChannelDiff(0), DEC);
  } else if ((!strncmp(buffer, "aid1?", 5)) || (!strncmp(buffer, "AID1?", 5))) {
    Serial.print("AID1 = ");
    Serial.println(rwm.ADCreadChannelDiff(1), DEC);
  } else if ((!strncmp(buffer, "interval?", 9)) || (!strncmp(buffer, "INTERVAL?", 9))) {
    Serial.print("interval = ");
    Serial.println(interval, DEC);
  } else if ((!strncmp(buffer, "interval", 8)) || (!strncmp(buffer, "INTERVAL", 8))) {
    interval = (unsigned long)atol(buffer+8);
  } else if ((!strncmp(buffer, "samples?", 8)) || (!strncmp(buffer, "SAMPLES?", 8))) {
    Serial.print("samples = ");
    Serial.println(samples, DEC);
  } else if ((!strncmp(buffer, "samples", 7)) || (!strncmp(buffer, "SAMPLES", 7))) {
    samples = (unsigned long)atol(buffer+7);
  } else if ((!strncmp(buffer, "clear", 5)) || (!strncmp(buffer, "CLEAR", 5))) {
    rwm.EEPROMwriteEnable();
    rwm.EEPROMchipErase();
  } else if ((!strncmp(buffer, "address?", 8)) || (!strncmp(buffer, "ADDRESS?", 8))) {
    Serial.print("address = ");
    Serial.println(address, DEC);
  } else if ((!strncmp(buffer, "address", 7)) || (!strncmp(buffer, "ADDRESS", 7))) {
    address = (unsigned long)atol(buffer+7);
  } else if ((!strncmp(buffer, "writebyte", 9)) || (!strncmp(buffer, "WRITEBYTE", 9))) {
    val = atoi(buffer+9);
    rwm.EEPROMwriteByte(address, (byte)val);
  } else if ((!strncmp(buffer, "readbyte?", 9)) || (!strncmp(buffer, "READBYTE?", 9))) {
    Serial.print("EEPROM[");
    Serial.print(address, DEC);
    Serial.print("] = ");
    Serial.println(rwm.EEPROMreadByte(address), DEC);
  } else if ((!strncmp(buffer, "writeint", 8)) || (!strncmp(buffer, "WRITEINT", 8))) {
    val = atoi(buffer+9);
    rwm.EEPROMwriteInt(address, val);
  } else if ((!strncmp(buffer, "readint?", 8)) || (!strncmp(buffer, "READINT?", 8))) {
    Serial.print("EEPROM[");
    Serial.print(address, DEC);
    Serial.print("] = ");
    Serial.println(rwm.EEPROMreadInt(address), DEC);
  } else if ((!strncmp(buffer, "readbytes", 9)) || (!strncmp(buffer, "READBYTES", 9))) {
    num = atol(buffer+9);
    for (j = 0; j<num; j++) {
      Serial.print(rwm.EEPROMreadByte(address+j), DEC);
      if (j+1==num)
        Serial.println("");
      else
        Serial.print(",");
    }
  } else if ((!strncmp(buffer, "readints", 8)) || (!strncmp(buffer, "READINTS", 8))) {
    num = atol(buffer+9);
    for (j = 0; j<num; j++) {
      Serial.print(rwm.EEPROMreadInt(address+j), DEC);
      if (j+1==num)
        Serial.println("");
      else
        Serial.print(",");
    }
  } else if ((!strncmp(buffer, "log", 3)) || (!strncmp(buffer, "LOG", 3))) {
    Serial.println("Clearing the EEPROM.");
    rwm.EEPROMwriteEnable();
    rwm.EEPROMchipErase();
    rwm.EEPROMwriteByte(0x1FFFC, 1);
    rwm.EEPROMwriteByte(0x1FFFD, lowByte(word(interval&0xFFFF)));
    rwm.EEPROMwriteByte(0x1FFFE, highByte(word(interval&0xFFFF)));
    rwm.EEPROMwriteByte(0x1FFFF, byte(interval>>16));
    Serial.println("Disconnect the USB cable and reset the Arduino to start logging data.");
  } else if ((!strncmp(buffer, "dump", 4)) || (!strncmp(buffer, "DUMP", 4))) {
    dumpdata();
  }
}

*/
