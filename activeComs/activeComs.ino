#include <Servo.h> 

Servo servo_0, servo_1, servo_2;

const int servoZeroPin = 2;
const int servoOnePin = 3;
const int servoTwoPin = 4;

int p0 = 90, p0min = 30, p0max = 120;
int p1 = 90, p1min = 30, p1max = 120;
int p2 = 90, p2min = 30, p2max = 120;

// 0: STOP 1: etc. (Currently range 0 - 3)
int mode = 0; 

//hard code SSwim parameters before optimization
float freq = 2;
float amp0 = 40;
float amp1 = 60;
float amp2 = 60;
float phase1 = 1.57;
float phase2 = 1.57; //phases should be relative

void setup(){
	Serial.begin(38400);
	Serial1.begin(38400);
	Serial1.println("Tadpole Command, this is Tadpole.");

	servo_0.attach(servoZeroPin);
	servo_1.attach(servoOnePin);
	servo_2.attach(servoTwoPin);
	setServos();
}

void loop(){
	// # # # # = 7
	if (Serial1.available()>=7) {
    	readCommand();
  	}
  	switch (mode) {
		case 0: // STOP
			break;
		case 1: // FORWARD S
			SSwim();
			setServos();
			break;
		default:
			break;
	}
  	sendStatus();
  	// For debugging
  	if (Serial.available()>=7) { // should adjust threshold based on command string length
    	readCommand0();
    	setServos();
  	}
}

void readCommand(){
	// Command "s0 s1 s2" ex: "40 90 113"
	// can do more elegant scanning by having start / stop characters
	delay(1);
	int i = Serial1.parseInt();
	mode = constrain(i,0,3);
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
}

void setServos(){
	servo_0.write(constrain(p0,p0min,p0max));
	servo_1.write(constrain(p1,p1min,p1max));
	servo_2.write(constrain(p2,p2min,p2max));
}

void sendStatus(){
	Serial1.println("Mode: "+String(mode)+" | Servos Command (Actual): "+String(p0)
		+" ("+String(constrain(p0,p0min,p0max))+") "+String(p1)+" ("+String(constrain(p0,p0min,p0max))+") "
		+String(p2)+" ("+String(constrain(p0,p0min,p0max))+")");
	// For debugging
	Serial.println("Mode: "+String(mode)+" | Servos: "+String(p0)+" "+String(p1)+" "+String(p2));
}

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