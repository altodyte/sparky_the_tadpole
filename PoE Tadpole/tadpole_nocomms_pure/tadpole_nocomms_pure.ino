// Sensorcap
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
const int window = 20; 
int index = 0, left_total = 0, left_average = 0;
int center_total = 0, center_average = 0;
int right_total = 0, right_average = 0;
int IR_left_history[window];
int IR_center_history[window];
int IR_right_history[window];

const int LED_left = 28;
const int LED_center = 29;
const int LED_right = 30;
const int LED_red = 40;
const int LED_yellow = 46;
const int LED_green = 41;
const int LED_white = 47;

int state = 2;
const int STOP = 0;
const int TL = 1;  
const int STRAIGHT = 2;
const int TR = 3;
const int CTL = 4;
const int CSTRAIGHT = 5;
const int CTR = 6;

//hard code SSwim parameters before optimization
float freq = 2.5;
float amp0 = 60;
float amp1 = 80;
float amp2 = 80;
float phase1 = 1.57;
float phase2 = 1.57; //phases should be relative

float smooth_constant = 20;
float turn_duration = 1.5*6.28/freq*1000;//three cycles of CSwim at least
float turn_time;
/*
boolean IR_L_prev = false;
boolean IR_L_hit = false;
boolean IR_C_prev = false;
boolean IR_C_hit = false;
boolean IR_R_prev = false;
boolean IR_R_hit = false;
*/
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

  for (int j = 0; j < window; j++){
    IR_left_history[j] = 0;
    IR_center_history[j] = 0;
    IR_right_history[j] = 0;     
  }
}  
 
void loop() 
{ 
  Serial.println('hello');
  read_in_sensor_vals();
  set_directional_lights();
  print_sensor_vals();
  //READ IN COMMUNICATION
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
  write_servo_pos_smoothed();
  Serial.print("[STP TL STR TR CTL CSTR CTR] State: ");
  Serial.println(state);  
  delay(10);
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
  CSwim();
  p2 = 90;
  if ((IR_right_val < threshold_lateral)&&(IR_center_val< threshold_center)&&(millis()>turn_time)){
//    Serial.println("From TL goto STRAIGHT");
    state = STRAIGHT;}
}
void TR_fcn()
{
  reset_state_lights();
  digitalWrite(LED_yellow, HIGH);
  p0 = 20;
  CSwim();
  p2 = 90;
  if ((IR_left_val < threshold_lateral)&&(IR_center_val< threshold_center)&&(millis()>turn_time)){
//    Serial.println("From TR goto STRAIGHT");
    state = STRAIGHT;}
}
void CSwim()//
{
  float time = millis()/1000.0;
  int amplitude_C = 80;
  float frequency_C = 2.5;
  float pos;
  p1 = amplitude_C*sin(frequency_C*time)+90.0;
  p2 = amplitude_C*sin(frequency_C*time)+90.0;
}
void STRAIGHT_fcn()
{
  reset_state_lights();
  digitalWrite(LED_green, HIGH);
  SSwim();
  if (IR_left_val>threshold_lateral){
//    Serial.println("From STRAIGHT goto TR");
    state = TR;
    turn_time = millis()+turn_duration;}
  if (IR_right_val>threshold_lateral){
//    Serial.println("From STRAIGHT goto TL");
    state = TL;
    turn_time = millis()+turn_duration;}
  if (IR_center_val>threshold_center){
    turn_time = millis()+turn_duration;
    if (IR_left_val > IR_right_val){
//      Serial.println("From STRAIGHT goto TR, bc center");
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
void CTL_fcn()
{
  reset_state_lights();
  digitalWrite(LED_yellow, HIGH);
  digitalWrite(LED_white, HIGH);
  p0 = 160;
  CSwim();
}
void CTR_fcn()
{
  reset_state_lights();
  digitalWrite(LED_yellow, HIGH);
  digitalWrite(LED_white, HIGH);
  p0 = 20;  
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
  left_total = left_total - IR_left_history[index];
  IR_left_history[index] = analogRead(IR_left);
  left_total = left_total + IR_left_history[index];
  left_average = left_total/window;
  IR_left_val = left_average;
  // IR_left_val = analogRead(IR_left);
//  if ((IR_left_val>threshold_lateral)&&(IR_L_prev>threshold_lateral)){
  //  IR_L_hit = true;}
//  else{IR_L_hit = false;}
//  IR_L_prev = IR_left_val;
center_total = center_total - IR_center_history[index];
  IR_center_history[index] = analogRead(IR_center);
    center_total = center_total + IR_center_history[index];
  // IR_center_val = analogRead(IR_center);
  center_average = center_total/window;
  IR_center_val = center_average;
  //if ((IR_center_val>threshold_lateral)&&(IR_C_prev>threshold_center)){
    //  IR_C_hit = true;}
//  else{IR_C_hit = false;}
  //IR_C_prev = IR_center_val;
  right_total = right_total - IR_right_history[index];
  IR_right_history[index] = analogRead(IR_right);
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
void set_directional_lights()
{
  if (IR_left_val>threshold_lateral){digitalWrite(LED_left, HIGH);}
  else{digitalWrite(LED_left, LOW);}
  if (IR_right_val>threshold_lateral){digitalWrite(LED_right, HIGH);}
  else{digitalWrite(LED_right, LOW);}    
  if (IR_center_val>threshold_center){digitalWrite(LED_center, HIGH);}
  else{digitalWrite(LED_center, LOW);}
}

