#include <Servo.h> 

Servo servo_0, servo_1, servo_2;

// PIN DEFINITION
const int servoZeroPin = 10;
const int servoOnePin = 11;
const int servoTwoPin = 12;

const int IR_left = A0;
const int IR_center = A1;
const int IR_right = A2;

const int LED_left = 28;
const int LED_center = 29;
const int LED_right = 30;
const int LED_red = 40;
const int LED_yellow = 46;
const int LED_green = 41;
const int LED_white = 47;

// STATE VARIABLES
// Servos
int p0 = 90, p0min = 30, p0max = 120;
int p1 = 90, p1min = 30, p1max = 120;
int p2 = 90, p2min = 30, p2max = 120;
// IR Sensors
int threshold_lateral = 300;
int threshold_center = 300;
int IR_left_val, IR_center_val, IR_right_val;
// State-Mode
const int STOP = 0;
const int TL = 1;  
const int STRAIGHT = 2;
const int TR = 3;
const int CTL = 4;
const int CSTRAIGHT = 5;
const int CTR = 6;
int mode = STOP; 

// GAIT PARAMETERS

//hard code SSwim parameters before optimization
float freq = 2;
float amp0 = 40;
float amp1 = 60;
float amp2 = 60;
float phase1 = 1.57;
float phase2 = 1.57; //phases are relative to phase0

float smooth_constant = 20;
float turn_duration = 1.5*6.28/freq*1000;//three cycles of CSwim at least
float turn_time;

// ------------------------------ MAIN FUNCTIONS ----------------------------------------

void setup(){
	// Setup Serial Connections
	Serial.begin(38400); // with PC via USB
	Serial1.begin(38400); // with PC via XBee
	Serial1.println("Tadpole Command, this is Tadpole.");
	// Setup Servos
	servo_0.attach(servoZeroPin);
	servo_1.attach(servoOnePin);
	servo_2.attach(servoTwoPin);
	setServos();
	// Setup LEDs
	pinMode(LED_red, OUTPUT);
	pinMode(LED_yellow, OUTPUT);
	pinMode(LED_green, OUTPUT);
	pinMode(LED_white, OUTPUT);
	pinMode(LED_left, OUTPUT);
	pinMode(LED_center, OUTPUT);
	pinMode(LED_right, OUTPUT);
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

}

void loop(){
	// m s0 s1 s2 f a0 a1 a2 p1 p2 = 19
	if (Serial1.available()>=19) {
		readCommand();
	}
	switch (mode) {
		case STOP: // STOP
			reset_state_lights();
			digitalWrite(LED_red, HIGH);
 			digitalWrite(LED_white, HIGH);
			break;
		case TL: // AUTO LEFT TURN (Obstacle avoidance)
			TL_func();
			break;
		case STRAIGHT: // AUTO FORWARD MOTION
			STRAIGHT_func();
			break;
		case TR: // AUTO RIGHT TURN (Obstacle avoidance)
			TR_func();
			break;
		case CTL: // MANUAL LEFT TURN
			CTL_func();
			break;
		case CSTRAIGHT: // MANUAL FORWARD MOTION
			CSTRAIGHT_func();
			break;
		case CTR: // MANUAL RIGHT TURN
			CTR_func();
			break;
		default:
			Serial.println("SOMETHING BAD HAPPENED. MODE NOT RIGHT");
			break;
	}
	read_in_sensor_vals();
	print_sensor_vals();
	set_directional_lights();
	sendStatus();
	// For debugging
	if (Serial.available()>=19) { // should adjust threshold based on command string length
		readCommand0();
		setServos();
	}
}

// --------------------- CASE/SWITCH STATE-MODE FUNCTIONS ----------------------------------------

void TL_func(){
	reset_state_lights();
	digitalWrite(LED_yellow, HIGH);
	p0 = p0max;
	CSwim();
	if ((IR_right_val < threshold_lateral)&&(IR_center_val< threshold_center)&&(millis()>turn_time)){
	//    Serial.println("From TL goto STRAIGHT");
		mode = STRAIGHT;
	}
	setServos();
}
void STRAIGHT_func(){
	reset_state_lights();
	digitalWrite(LED_green, HIGH);
	SSwim();
	if (IR_left_val>threshold_lateral){
	//    Serial.println("From STRAIGHT goto TR");
	    mode = TR;
	    turn_time = millis()+turn_duration;
	}
	if (IR_right_val>threshold_lateral){
	//    Serial.println("From STRAIGHT goto TL");
	    mode = TL;
	    turn_time = millis()+turn_duration;
	}
	if (IR_center_val>threshold_center){
	    turn_time = millis()+turn_duration;
	    if (IR_left_val > IR_right_val){
	//      Serial.println("From STRAIGHT goto TR, bc center");
	      mode = TR;
	  	} else {mode = TL;}
	}
	setServos();
}
void TR_func(){
	reset_state_lights();
	digitalWrite(LED_yellow, HIGH);
	p0 = p0min;
	CSwim();
	if ((IR_left_val < threshold_lateral)&&(IR_center_val< threshold_center)&&(millis()>turn_time)){
	//    Serial.println("From TR goto STRAIGHT");
		mode = STRAIGHT;
	}
	setServos();
}
void CTL_func(){
	reset_state_lights();
	digitalWrite(LED_yellow, HIGH);
	digitalWrite(LED_white, HIGH);
	p0 = p0max;
	CSwim();
	setServos();
}
void CSTRAIGHT_func(){
	reset_state_lights();
	digitalWrite(LED_green, HIGH);
	digitalWrite(LED_white, HIGH);
	SSwim();
	setServos();
}
void CTR_func(){
	reset_state_lights();
	digitalWrite(LED_yellow, HIGH);
	digitalWrite(LED_white, HIGH);
	p0 = p0min;
	CSwim();
	setServos();
}

void readCommand(){
	// Command "m s0 s1 s2 f a0 a1 a2 p1 p2" ex: "5 40 90 113 2 40 60 60 1.57 1.57"
	// should do more elegant scanning by having start / stop characters
	delay(1);
	int i = Serial1.parseInt();
	mode = constrain(i,0,6);
	// Serial1.println(String(i)+" "+String(p0));
	i = Serial1.parseInt();
	p0 = constrain(i,p0min,p0max);
	// Serial1.println(String(i)+" "+String(p0));
	i = Serial1.parseInt();
	p1 = constrain(i,p1min,p1max);
	// Serial1.println(String(i)+" "+String(p1));
	i = Serial1.parseInt();
	p2 = constrain(i,p2min,p2max);
	// Serial1.println(String(i)+" "+String(p2));
	float f = Serial1.parseFloat();
	freq = f;
	f = Serial1.parseFloat();
	amp0 = f;
	f = Serial1.parseFloat();
	amp1 = f;
	f = Serial1.parseFloat();
	amp2 = f;
	f = Serial1.parseFloat();
	phase1 = f;
	f = Serial1.parseFloat();
	phase2 = f;
}

void sendStatus(){
	// FOR HUMANS
	Serial1.println("Mode: "+String(mode)+" || Servos Command (Actual): "+String(p0)
		+" ("+String(constrain(p0,p0min,p0max))+") "+String(p1)+" ("+String(constrain(p0,p0min,p0max))+") "
		+String(p2)+" ("+String(constrain(p0,p0min,p0max))+") || f: "+doubleToString(freq)+" a0: "+doubleToString(amp0)+
		" a1: "+doubleToString(amp1)+" a2: "+doubleToString(amp2)+" p1: "+doubleToString(phase1)+" p2: "+doubleToString(phase2));
	// FOR COMPUTERS
	/*
	Serial1.println(String(mode)+" "+String(p0)+" "+C+" "+String(p1)+" "+C+" "+String(p2)+" "+C+" "+
			doubleToString(freq)+" "+doubleToString(amp0)+" "+doubleToString(amp1)+" "+doubleToString(amp2)+" "+
			doubleToString(phase1)+" "+doubleToString(phase2));
	*/
	// For debugging
	// Serial.println("Mode: "+String(mode)+" | Servos: "+String(p0)+" "+String(p1)+" "+String(p2));
}

void setServos(){
	servo_0.write(constrain(p0,p0min,p0max));
	servo_1.write(constrain(p1,p1min,p1max));
	servo_2.write(constrain(p2,p2min,p2max));
}

// --------------------- SWIMMING PATTERN FUNCTIONS ----------------------------------------
void SSwim()
{
  float time = millis()/1000.0;
  p0 = amp0*sin(freq*time)+90;//no phase offset
  p1 = amp1*sin(freq*time+phase1)+90;
  p2 = amp2*sin(freq*time+phase1+phase2)+90; //phase offset should be relative
  // p0 = constrain(p0,p0min,p0max);
  // p1 = constrain(p1,p1min,p1max);
  // p2 = constrain(p2,p2min,p2max);
}

void CSwim()//
{
  float time = millis()/1000.0;
  int amplitude_C = 60;
  float frequency_C = 1.5;
  float pos;
  p1 = amplitude_C*sin(frequency_C*time)+90.0;
  p2 = amplitude_C*sin(frequency_C*time)+90.0;
}

// ---------------------------- ADDITONAL FUNCTIONS ----------------------------------------


void read_in_sensor_vals()
{
	IR_left_val = analogRead(IR_left);
//  if ((IR_left_val>threshold_lateral)&&(IR_L_prev>threshold_lateral)){
  //  IR_L_hit = true;}
//  else{IR_L_hit = false;}
//  IR_L_prev = IR_left_val;
	IR_center_val = analogRead(IR_center);
  //if ((IR_center_val>threshold_lateral)&&(IR_C_prev>threshold_center)){
    //  IR_C_hit = true;}
//  else{IR_C_hit = false;}
  //IR_C_prev = IR_center_val;
	IR_right_val = analogRead(IR_right);
//  if ((IR_right_val>threshold_lateral)&&(IR_R_prev>threshold_lateral)){
  //    IR_R_hit = true;}
//  else{IR_R_hit = false;}
//  IR_R_prev = IR_right_val;
}

void reset_state_lights()
{
	digitalWrite(LED_red, LOW);
	digitalWrite(LED_yellow, LOW);
	digitalWrite(LED_green, LOW);
	digitalWrite(LED_white, LOW);
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

void print_sensor_vals()
{
  Serial.print("IR Left: ");
  Serial.print(IR_left_val);
  Serial.print(" IR Center: ");
  Serial.print(IR_center_val);
  Serial.print(" IR Right: ");
  Serial.println(IR_right_val);
}

String doubleToString(float input){ // secretly float to string
	int decimalPlaces = 2;
	if(decimalPlaces!=0){
		String string = String((int)(input*pow(10,decimalPlaces)));
		if(abs(input)<1){
			if(input>0)
				string = "0"+string;
			else if(input<0)
				string = string.substring(0,1)+"0"+string.substring(1);
			}
			return string.substring(0,string.length()-decimalPlaces)+"."+string.substring(string.length()-decimalPlaces);
		}
	else {
		return String((int)input);
	}
}

void readCommand0(){
	// Command "s0 s1 s2" ex: "40 90 113"
	delay(5);
	int i = Serial.parseInt();
	mode = constrain(i,0,3);
	Serial.println(String(i)+" "+String(p0));
	i = Serial.parseInt();
	p0 = constrain(i,30,120);
	Serial.println(String(i)+" "+String(p0));
	i = Serial.parseInt();
	p1 = constrain(i,30,120);
	Serial.println(String(i)+" "+String(p1));
	i = Serial.parseInt();
	p2 = constrain(i,30,120);
	Serial.println(String(i)+" "+String(p2));
}