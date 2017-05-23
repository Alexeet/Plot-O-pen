#include <CheapStepper.h>
#include <Servo.h>

int nombreDePas = 4096;
int tour = 2048;
CheapStepper moteurX (5,4,3,2); 
CheapStepper moteurY (6,7,8,9); 
int X,Y,dx,dy,maximum;
float mx,my;
const int switchX = 11;
const int switchY = 12;
int swX,swY ;
boolean moveClockwise = true;
int pos = 20;
String nX,nY,nE;
boolean E = false;
boolean sensX;
boolean sensY;
int Xmax =40000;
int Ymax =40000;
String data="";
Servo servo;

void setup() {
  Serial.begin(9600);
  Servo.attach(10);
  pinMode(switchX, INPUT);
  pinMode(switchY, INPUT);
  moteurX.setRpm(13);
  moteurY.setRpm(13);
  
  calibrate();
}

void loop() {
  getSerial();
  goTo(X,Y,dx,dy,E);
}

void calibrate(){
  swX=digitalRead(switchX);
  while(swX==0){
    moteurX.moveTo (true, -1);
    swX=digitalRead(switchX);
  }
  swY=digitalRead(switchY);
    while(swY==0){
    moteurY.moveTo (true, -1);
    swY=digitalRead(switchY);
  }
  X=0;
  Y=0;
}


void getSerial(){
  while(!Serial.available()){
    delay(1);
  }
  data=Serial.readString();
  
  int nextspace = data.indexOf(" ");
  dx = data.substring(1,nextspace-1).toInt();
  int nextspace2 = data.indexOf(" ",nextspace+1);
  dy = data.substring(nextspace+2,nextspace2-1).toInt();
  E = (data.substring(data.length())=="1" ? true : false);
  //X20 Y3000 E1
}


boolean isIn(int X, int Y, int dx, int dy){
   X= X+dx;
   Y= Y+dy;
   if(X<0 || Y<0 || X>Xmax || Y>Ymax){
    Serial.println("ERROR");
    return false;
   }
   else{
    return true;
   }
}


int goTo(int X,int Y,int dx,int dy, boolean E) { 
    if(isIn(X,Y,dx,dy)==true){
     if(E==true){
      if(pos!=0){
       pos=90;
       servo.write(pos);              
       delay(15);
      }
     }
     else{
       if(pos!=20){
       pos=50;
       servo.write(pos);              
       delay(15);
       }
     }
     maximum = max(abs(dx),abs(dy));
      if (maximum==abs(dx)){
          mx=1 ; 
          my=dy/dx ;
       }
       else{
          mx=dx/dy;
          my=1;
       }
       sensX=(dx<0 ? false : true);
       sensY=(dy<0 ? false: true);
    for (int i=1; i<maximum;i++){
       moteurX.moveTo(sensX, int(mx*i)-int(mx*(i-1)) );
       moteurY.moveTo(sensY, int(my*i)-int(my*(i-1)) );
    }
   }
   else{
    Serial.println("ERROR");
   }
}
