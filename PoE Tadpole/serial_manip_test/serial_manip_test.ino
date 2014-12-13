//char buffer[64];
void setup()
{
  Serial.begin(9600);
}
void loop()
{
  Serial.write("GO\n");
  receive_comms();
/*
//  char str[] ="- This, a sample string.";
  char * pch;
//  Serial.println("Splitting string \"%s\" into tokens:\nf",buffer);
  pch = strtok (buffer," ,.-");
  while (pch != NULL)
  {
    Serial.println(pch);
    pch = strtok (NULL, " ,.-");
  }*/
}
void receive_comms()
{
  char buffer[64];
  int i, ch, val;
  long j, num;
  Serial.println("start the parse");
  Serial.write("morebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytesmorebytes");
  for (i = 0; i<63; i++) {
    for (ch = Serial.read(); ch==-1; ch = Serial.read()) {}
    if (ch==';')
      break;
    buffer[i] = (char)ch;
  }
  Serial.println("parsing finished");
  buffer[i] = '\0';
  Serial.println(buffer);
  if (strncmp(buffer, "STOP", 4)){
    Serial.println("read in stop");}
  else if (strncmp(buffer, "GO", 2)){
    Serial.println("read in go");}
  else if (strncmp(buffer, "CTL", 3)){
    Serial.println("read in ctl");}
  else if (strncmp(buffer, "CF", 2)){
    Serial.println("read in ctl");}
  else if (strncmp(buffer, "CTR", 3)){
    Serial.println("read in ctr");}
}
