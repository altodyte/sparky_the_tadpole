//Based on comma-delimited lines read from Serial, variables are set
void receive_comms()
{
  //Initialize variables
  char buffer[64];
  int i, ch, val;
  long j, num;

  //Read bytes from Serial
  for (i = 0; i<63; i++) {
    for (ch = Serial.read(); ch==-1; ch = Serial.read()) {}
    if (ch==';')
      break;
    buffer[i] = (char)ch;
  }
  
  //Split comma-delimted line
  char *str;
  char *ind=buffer;
  int counter = 0;
  
  //Set variable based on the counter
  String stateVar;
  while ((str = strtok_r(ind, ",", &ind)) != NULL){
   if(str=="x" || counter > 7) break;
   switch(counter){
     case 0:
       stateVar = str;
       break;
     case 1:
       freq = atof(str);
       break;
     case 2:
       amp0 = atoi(str);
       break;
     case 3:
       amp1 = atoi(str);
       break;
     case 4:
       amp2 = atoi(str);
       break;
     case 5:
       phase1 = atof(str);
       break;
     case 6:
       phase2 = atof(str);
       break;
     case 7:
       mode = atoi(str);
       break;
     default:
       break;
    }
    counter++;
  }
  
  // Set the state based on stateVar variable
  if (stateVar=="STOP"){
    state = STOP;
  }
  else if (stateVar=="GO"){
    state = STRAIGHT;
  }
 else if (stateVar=="CTL"){
    state = CTL;
  }
  else if (stateVar=="CF"){
    state = CSTRAIGHT;
  }
  else if (stateVar=="CTR"){
    state = CTR;
  }
}

