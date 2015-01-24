//#include <Servo.h>

int i1 = 0;
float f1 = 2.51;
char c1 = 'd';
String s1 = "This string";
int state = 0;
int color = 0;
const int LED_left = 30;
const int LED_center = 31;
const int LED_right = 32;
const int LED_red = 40;
const int LED_yellow = 41;
const int LED_green = 42;
const int LED_white = 43;

void setup()
{
  Serial.begin(9600);
  Serial1.begin(38400);
  pinMode(LED_red, OUTPUT);
  pinMode(LED_yellow, OUTPUT);
  pinMode(LED_green, OUTPUT);
  pinMode(LED_white, OUTPUT);
  pinMode(LED_left, OUTPUT);
  pinMode(LED_center, OUTPUT);
  pinMode(LED_right, OUTPUT);
  Serial1.println("setup function");
}
void loop()
{
  digitalWrite(LED_white, HIGH);
  delay(500);
  digitalWrite(LED_white, LOW);
  delay(100);
  state = (state+1)%3;
  display_state();
  display_color();
  Serial.println(millis());
    
}

/*
String find_next(char *ptr,int bytes){
  String toRet = "";
  for(int i = 0; i < bytes; i++){
    if((ptr[i]>='0'&&ptr[i]<='9')||ptr[i]=='.'||(ptr[i]>='A'&&ptr[i]<='Z')) toRet+=ptr[i];
  }
  return toRet;
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
 
  String stateVar = find_next(buffer,4);
  freq = atof(find_next(&(buffer[5]),4).c_str());
  amp0 = atoi(find_next(&(buffer[10]),2).c_str());
  amp1 = atoi(find_next(&(buffer[13]),2).c_str());
  amp2 = atoi(find_next(&(buffer[16]),2).c_str());
  phase1 = atof(find_next(&(buffer[19]),5).c_str());
  phase2 = atof(find_next(&(buffer[25]),5).c_str());
  mode = atoi(find_next(&(buffer[31]),2).c_str());
  Serial1.println(stateVar);
  if (stateVar=="STOP"){
    state = STOP;}
  else if (stateVar=="GO"){
    state = STRAIGHT;}
 else if (stateVar=="CTL"){
    state = CTL;}
  else if (stateVar=="CF"){
    state = CSTRAIGHT;}
  else if (stateVar=="CTR"){
    state = CTR;}
}
*/
void display_state()
{
  digitalWrite(LED_right, LOW);
  digitalWrite(LED_center, LOW);
  digitalWrite(LED_left, LOW);
  if (state == 0) {digitalWrite(LED_right, HIGH);}
  if (state == 1) {digitalWrite(LED_center, HIGH);}
  if (state == 2) {digitalWrite(LED_left, HIGH);}
  delay(500);
}

void display_color()
{
  digitalWrite(LED_red, LOW);
  digitalWrite(LED_green, LOW);
  digitalWrite(LED_yellow, LOW);
  if (color == 0) {digitalWrite(LED_red, HIGH);}
  if (color == 1) {digitalWrite(LED_yellow, HIGH);}
  if (color == 2) {digitalWrite(LED_green, HIGH);}
  delay(500);
}

