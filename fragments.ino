void readCommand0(){
	// Command "s0 s1 s2" ex: "40 90 113"
	// delay(5);
	// mode = constrain(Serial1.parseInt(),0,3);
	// p0 = constrain(Serial1.parseInt(),30,120);
	// p1 = constrain(Serial1.parseInt(),30,120);
	// p2 = constrain(Serial1.parseInt(),30,120);
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