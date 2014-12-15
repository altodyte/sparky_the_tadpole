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
 
  String str1 = find_next(buffer,4);
  freq = atof(find_next(&(buffer[5]),4).c_str());
  amp0 = atoi(find_next(&(buffer[10]),2).c_str());
  amp1 = atoi(find_next(&(buffer[13]),2).c_str());
  amp2 = atoi(find_next(&(buffer[16]),2).c_str());
  phase1 = atof(find_next(&(buffer[19]),5).c_str());
  phase2 = atof(find_next(&(buffer[25]),5).c_str());
  mode = atoi(find_next(&(buffer[31]),2).c_str());
  
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

