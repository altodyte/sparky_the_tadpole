const int userLED = 13;
const int LED_1 = 47;

boolean userLED_state = false;
unsigned long userLED_start = millis();
boolean LED_1_state = false;
unsigned long LED_1_start = millis();

// commands are periods in ms
int userLED_command = 1000;
int LED_1_command = 1000;

void setup(){
  Serial.begin(38400);
  Serial1.begin(38400);
  Serial1.println("Tadpole Command, this is Tadpole.");
  pinMode(userLED, OUTPUT);
  pinMode(LED_1, OUTPUT);
  
}

void loop(){
  if (Serial1.available()>4){
    byte c = 'c';
    while (c!='$'){
      c = Serial1.read();
    }
    userLED_command = Serial1.parseInt();
    LED_1_command = Serial1.parseInt();
  }
  userLED_update();
  LED_1_update();
}
  
void userLED_update(){
  if (millis()>userLED_start+userLED_command){
    userLED_state = !userLED_state;
    digitalWrite(userLED,userLED_state);
    userLED_start = millis();
  }  
}

void LED_1_update(){
  if (millis()>LED_1_start+LED_1_command){
    LED_1_state = !LED_1_state;
    digitalWrite(LED_1,LED_1_state);
    LED_1_start = millis();
  }  
}
