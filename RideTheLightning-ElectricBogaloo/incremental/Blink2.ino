//2015/08/13 13:02
int led = 13;
const int LED_WHITE = 47;
const int LED_YELLOW = 46;
const int LED_RED = 40;
const int LED_GREEN = 41;
const int LED_RIGHT = 28;
const int LED_CENTER = 29;
const int LED_LEFT = 30;

int IR_1_val;
const int IR_1 = A8;

// the setup routine runs once when you press reset:
void setup() {      
//  Serial.begin(9600);  
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
  // initialize the digital pin as an output.
  pinMode(led, OUTPUT);
  establish_contact();
}

// the loop routine runs over and over again forever:
void loop() {
  digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
  IR_1_val = analogRead(IR_1);
//  Serial.println(IR_1_val);
  delay(30);               // wait for a second
  if (IR_1_val>200)
  {
    digitalWrite(LED_CENTER, HIGH);
    digitalWrite(LED_GREEN, LOW);
    Serial1.println("Found!");
    Serial1.println(IR_1_val);
  }
  else
  {
    digitalWrite(LED_CENTER, LOW);
    digitalWrite(LED_GREEN, HIGH);
  }
  if (Serial1.available())
  {
    char terminate = '!';
    String incoming = Serial1.readStringUntil(terminate);
    if (incoming=="NICTERE!")
    {
      nictare();
    } 
    Serial1.println(incoming);
    Serial1.println(IR_1_val);
  }
//  Serial.println(Serial1.read());
  digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
  delay(30);               // wait for a second
}

void establish_contact(){
  while (Serial1.available() <= 0) {
    delay(30);
  }
}

void nictare(){
  digitalWrite(LED_GREEN, HIGH);
  digitalWrite(LED_RED, HIGH);
  digitalWrite(LED_WHITE, HIGH);
  digitalWrite(LED_YELLOW, HIGH);
  digitalWrite(LED_LEFT, HIGH);
  digitalWrite(LED_CENTER, HIGH);
  digitalWrite(LED_RIGHT, HIGH);
  delay(500);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_WHITE, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_LEFT, LOW);
  digitalWrite(LED_CENTER, LOW);
  digitalWrite(LED_RIGHT, LOW);
}
