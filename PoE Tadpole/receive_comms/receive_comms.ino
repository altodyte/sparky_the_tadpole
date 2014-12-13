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
 
  String str1 = find_next(buffer[0],4);
  float freq = atof(find_next(buffer[5]*,4).c_str());
  amp0 = atoi(find_next(*(buffer[10]),2).c_str());
  amp1 = atoi(find_next(*(buffer[13]),2).c_str());
  amp2 = atoi(find_next(*(buffer[16]),2).c_str());
  phase1 = atof(find_next(*(buffer[19]),5).c_str());
  phase2 = atof(find_next(*(buffer[24]),5).c_str());
  mode = atoi(find_next(*(buffer[29]),2).c_str());
  
  if (strncmp(buffer, "STOP", 4)){
    state = STOP;}
  else if (strncmp(buffer, "GO", 2)){
    state = STRAIGHT;}
 else if (strncmp(buffer, "CTL", 3)){
    state = CTL;}
  else if (strncmp(buffer, "CF", 2)){
    state = CSTRAIGHT;}
  else if (strncmp(buffer, "CTR", 3)){
    state = CTR;}
}

