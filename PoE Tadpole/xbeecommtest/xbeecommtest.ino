void setup() {
  Serial.begin(38400);
  Serial1.begin(38400);
}
void loop() {
  Serial.println("This is the future");
  Serial1.println("This is the future.");
  Serial.println(millis());
  Serial1.println(millis());
  if (Serial1.available()>0){
    int s;
    s = Serial1.read();
    Serial.println(s);   
  }
  delay(1000);
}
