//2015/08/13 
#include <Servo.h>

Servo servo_0, servo_1, servo_2;
const int servo_0_pin = 2;
const int servo_1_pin = 12;
const int servo_2_pin = 11;
int p0 = 90;
int p1 = 90;
int p2 = 130;

int led = 13;
const int LED_WHITE = 47;
const int LED_YELLOW = 46;
const int LED_RED = 40;
const int LED_GREEN = 41;
const int LED_RIGHT = 28;
const int LED_CENTER = 29;
const int LED_LEFT = 30;

int IR_threshold = 300;
int IR_left_val, IR_right_val, IR_center_val;
const int IR_LEFT = A0;
const int IR_CENTER = A1;
const int IR_RIGHT = A2;
const int window = 20; 
int index = 0, left_total = 0, left_average = 0;
int center_total = 0, center_average = 0;
int right_total = 0, right_average = 0;
int IR_left_history[window];
int IR_center_history[window];
int IR_right_history[window];

int state = 0;
const int STOP = 0;
const int TL = 1;
const int STRAIGHT = 2;
const int TR = 3;
const int CTL = 4;
const int CSTRAIGHT = 5;
const int CTR = 6;

float freq = 2;
float amp0 = 60;
float amp1 = 80;
float amp2 = 80;
float phase1 = 1.57;
float phase2 = 1.57;

float smooth_constant = 20;
float turn_duration = 1.5*6.28/freq*1000;//three cycles of CSwim at least
float turn_time;
float turn_center;

// the setup routine runs once when you press reset:
void setup() {      
  Serial.begin(9600);  
  Serial1.begin(38400);
  while (!Serial1){
    ;
  }

  pinMode(LED_CENTER, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_LEFT, OUTPUT);
  pinMode(LED_RIGHT, OUTPUT);
  pinMode(LED_WHITE, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(led, OUTPUT);
  //initialize history of sensor readings
  for (int j = 0; j < window; j++){
    IR_left_history[j] = 0;
    IR_center_history[j] = 0;
    IR_right_history[j] = 0;     
  }
  
  //servo_0.attach(servo_0_pin);
  servo_1.attach(servo_1_pin);
  servo_2.attach(servo_2_pin);
  //servo_0.write(p0);
  servo_1.write(p1);
  servo_2.write(p2);
  //nictare();
  digitalWrite(LED_WHITE, HIGH);
  digitalWrite(LED_RED, HIGH);
  Serial.println("waiting to establish contact");
  establish_contact();
  LEDs_all_off();
  Serial.println("roger");
}

// the loop routine runs over and over again forever:
void loop() {
  digitalWrite(LED_WHITE, HIGH);   // turn the LED on (HIGH is the voltage level)
  read_in_sensor_vals();
  set_directionals();
  parse_commands();
  switch(state){
    case STOP:     STOP_fcn();      break;
    case TL:       TL_fcn();        break;
    case STRAIGHT: STRAIGHT_fcn();  break;
    case TR:       TR_fcn();        break;
    case CTL:      CTL_fcn();       break;
    case CSTRAIGHT: CSTRAIGHT_fcn(); break;
    case CTR:      CTR_fcn();       break; 
    default:
    dormire();
  }
  digitalWrite(LED_WHITE, LOW);    // turn the LED off by making the voltage LOW
  write_servo_pos_smoothed();
  delay(10);
}

void establish_contact(){
  while (Serial1.available() <= 0) {
    delay(30);
  }
  Serial1.println("EGO RANUNCULUS");
}

void nictare(){
  LEDs_all_on();
  delay(1000);
  LEDs_all_off();
  Serial1.println("NICTO");
}
void dormire(){
  boolean sleeping = true;
  LEDs_all_off();
  while(sleeping){
    Serial1.println("DORMIO");
    digitalWrite(LED_WHITE, HIGH);
    delay(200);
    digitalWrite(LED_WHITE, LOW);
    delay(2000);
    if (Serial1.available()){
    char terminate = '!';
    String incoming = Serial1.readStringUntil(terminate);
    if (incoming=="EXPERGISCERE"){ 
      Serial1.println("EXPERGISCOR");  
      sleeping = false;
    }
    }
  }
}
void dicere(){
  Serial1.println("DICO");
  Serial1.print("State: ");
  Serial1.println(state);
  Serial1.print("IR LEFT: ");
  Serial1.print(IR_left_val);
  Serial1.print("; IR CENTER: ");
  Serial1.print(IR_center_val);
  Serial1.print("; IR RIGHT: ");
  Serial1.println(IR_right_val);
  Serial1.print("P0: ");
  Serial1.print(p0);
  Serial1.print("; P1: ");
  Serial1.print(p1);
  Serial1.print("; P2: ");
  Serial1.println(p2);
  Serial1.print("Freq: ");
  Serial1.print(freq);
  Serial1.print("; Amp0: ");
  Serial1.print(amp0);
  Serial1.print("; Amp1: ");
  Serial1.print(amp1);
  Serial1.print("; Amp2: ");
  Serial1.print(amp2);
  Serial1.print("; Phase1: ");
  Serial1.print(phase1);
  Serial1.print("; Phase2: ");
  Serial1.print(phase2);
}
void audire(){
  float params[6];
  Serial1.println("AUDIO");
  Serial1.println("freq, amp0, 1, 2, phase 1, 2");
  boolean full_parse = true;
  for (int to_read = 5; to_read >= 0; to_read--){
    char terminate = ',';
    String incoming = Serial1.readStringUntil(terminate);
    if (incoming == "X"){
    full_parse = false;
    Serial1.println("NON ACTUM");
    break;}
    char floatbuf[32];
    incoming.toCharArray(floatbuf, 10);
    params[to_read]  = atof(floatbuf);
  }
  if (full_parse){
    freq = params[5];
    amp0 = params[4];
    amp1 = params[3];
    amp2 = params[2];
    phase1 = params[1];
    phase2 = params[0];
    Serial1.println("AUDIVI");
    dicere();
  }  
}
void read_in_sensor_vals()
{
  left_total = left_total - IR_left_history[index];
  IR_left_history[index] = analogRead(IR_LEFT);
  left_total = left_total + IR_left_history[index];
  left_average = left_total/window;
  IR_left_val = left_average;
  // IR_left_val = analogRead(IR_left);
//  if ((IR_left_val>threshold_lateral)&&(IR_L_prev>threshold_lateral)){
  //  IR_L_hit = true;}
//  else{IR_L_hit = false;}
//  IR_L_prev = IR_left_val;
center_total = center_total - IR_center_history[index];
  IR_center_history[index] = analogRead(IR_CENTER);
    center_total = center_total + IR_center_history[index];
  // IR_center_val = analogRead(IR_center);
  center_average = center_total/window;
  IR_center_val = center_average;
  //if ((IR_center_val>threshold_lateral)&&(IR_C_prev>threshold_center)){
    //  IR_C_hit = true;}
//  else{IR_C_hit = false;}
  //IR_C_prev = IR_center_val;
  right_total = right_total - IR_right_history[index];
  IR_right_history[index] = analogRead(IR_RIGHT);
    right_total = right_total + IR_right_history[index];
    right_average = right_total/window;
    IR_right_val = right_average;
  // IR_right_val = analogRead(IR_right);
//  if ((IR_right_val>threshold_lateral)&&(IR_R_prev>threshold_lateral)){
  //    IR_R_hit = true;}
//  else{IR_R_hit = false;}
//  IR_R_prev = IR_right_val;
  index = (index+1)%window;
}
void set_directionals(){
  if (IR_left_val>IR_threshold){
    digitalWrite(LED_LEFT, HIGH);}
  else{
    digitalWrite(LED_LEFT, LOW);}
  if (IR_right_val>IR_threshold){
    digitalWrite(LED_RIGHT, HIGH);}
  else{
    digitalWrite(LED_RIGHT, LOW);}
  if (IR_center_val>IR_threshold){
    digitalWrite(LED_CENTER, HIGH);}
  else{
    digitalWrite(LED_CENTER, LOW);}
}
void parse_commands(){
  if (Serial1.available())
  {
    char terminate = '!';
    String incoming = Serial1.readStringUntil(terminate);
//    Serial1.println(incoming);
    if (incoming=="NICTERE"){   
      nictare();
      Serial1.println("NICTO");} 
    if (incoming=="DORMI"){
      dormire();}
    if (incoming=="DIC"){
      dicere();}   
    if (incoming=="SINISTER"){
      state = CTL;}
    if (incoming=="DEXTER"){
      state = CTR;}
    if (incoming=="DESISTE"){
      Serial1.println("DESISTO");
      state = STOP;}
    if (incoming=="ITE"){
      Serial1.println("EO");
      state = STRAIGHT;}
    if (incoming=="AGGREDERE"){
      Serial1.println("AGGREDIOR");
      state = CSTRAIGHT;}
    if (incoming=="X"){
      Serial1.println("DESISTO");
      state = STOP;}      
    if (incoming=="AUDI"){
      audire();}
  }
}
void write_servo_pos()
{
  servo_0.write(p0);
  servo_1.write(p1);
  servo_2.write(p2);
}
void LEDs_all_on()
{
  digitalWrite(LED_GREEN, HIGH);
  digitalWrite(LED_RED, HIGH);
  digitalWrite(LED_WHITE, HIGH);
  digitalWrite(LED_YELLOW, HIGH);
  digitalWrite(LED_LEFT, HIGH);
  digitalWrite(LED_CENTER, HIGH);
  digitalWrite(LED_RIGHT, HIGH);
}
void LEDs_all_off()
{
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_WHITE, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_LEFT, LOW);
  digitalWrite(LED_CENTER, LOW);
  digitalWrite(LED_RIGHT, LOW);
}
void write_servo_pos_smoothed()
{
  if (abs(p0-servo_0.read())>smooth_constant)
  {
    int sgn = (p0-servo_0.read())/abs(p0-servo_0.read());
    p0 = p0 - sgn*smooth_constant;
  }
  if (abs(p1-servo_1.read())>smooth_constant)
  {
    int sgn = (p1-servo_1.read())/abs(p1-servo_1.read());
    p1 = p1 - sgn*smooth_constant;
  }
  if (abs(p2-servo_2.read())>smooth_constant)
  {
    int sgn = (p2-servo_2.read())/abs(p2-servo_2.read());
    p2 = p2 - sgn*smooth_constant;
  }
  servo_0.write(p0);
  servo_1.write(p1);
  servo_2.write(p2);
}
void reset_state_lights()
{
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_WHITE, LOW);
}  
void STOP_fcn()
{
  reset_state_lights();
  digitalWrite(LED_RED, HIGH);
  digitalWrite(LED_WHITE, HIGH);
  //servos aren't rewritten here
}
void TL_fcn()
{
  reset_state_lights();
  digitalWrite(LED_YELLOW, HIGH);
  p0 = 160;
  CSwim();
  p2 = 90;
  if ((IR_right_val < IR_threshold)&&(IR_center_val< IR_threshold)&&(millis()>turn_time)){
//    Serial.println("From TL goto STRAIGHT");
    state = STRAIGHT;
    Serial1.println("EO");}
}
void TR_fcn()
{
  reset_state_lights();
  digitalWrite(LED_YELLOW, HIGH);
  p0 = 20;
  CSwim();
  p2 = 90;
  if ((IR_left_val < IR_threshold)&&(IR_center_val< IR_threshold)&&(millis()>turn_time)){
//    Serial.println("From TR goto STRAIGHT");
    state = STRAIGHT;
    Serial1.println("EO");}
}
void CSwim()//
{
  float time = millis()/1000.0;
  int amplitude_C = 60;
  float frequency_C = 2.5;
  float pos;
  p2 = amplitude_C*sin(frequency_C*time)+turn_center;
  //p2 = 90; //amplitude_C*sin(frequency_C*time)+90.0;
}
void CTL_fcn()
{
  reset_state_lights();
  digitalWrite(LED_YELLOW, HIGH);
  digitalWrite(LED_WHITE, HIGH);
  p0 = 150;
  p1 = 150;
  
  turn_center = 120;
  //CSwim();
}
void CTR_fcn()
{
  reset_state_lights();
  digitalWrite(LED_YELLOW, HIGH);
  digitalWrite(LED_WHITE, HIGH);
  p0 = 30;  
  p1 = 30;
  p2 = 30;
  turn_center = 60;
  //CSwim();
}
void STRAIGHT_fcn()
{
  reset_state_lights();
  digitalWrite(LED_GREEN, HIGH);
  SSwim();
  if (IR_left_val>IR_threshold){
    Serial1.println("From STRAIGHT goto TR");
    state = TR;
    turn_time = millis()+turn_duration;}
  if (IR_right_val>IR_threshold){
    Serial1.println("From STRAIGHT goto TL");
    state = TL;
    turn_time = millis()+turn_duration;}
  if (IR_center_val>IR_threshold){
    turn_time = millis()+turn_duration;
    if (IR_left_val > IR_right_val){
      Serial1.println("From STRAIGHT goto TR, bc center");
      state = TR;}
    else {state = TL;}
  }
}
void SSwim()
{
  float time = millis()/1000.0;
  p0 = amp0*sin(freq*time)+90;//no phase offset
  p1 = amp1*sin(freq*time+phase1)+90;
  p2 = amp2*sin(freq*time+phase1+phase2)+90; //phase offset should be relative
}

void CSTRAIGHT_fcn()
{
  reset_state_lights();
  digitalWrite(LED_GREEN, HIGH);
  digitalWrite(LED_WHITE, HIGH);
  SSwim();
}
