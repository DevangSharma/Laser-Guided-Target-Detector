

#include <Servo.h>

Servo horizontal,vertical;  // create servo object to control a servo
 String input = ".";
 
int pos = 0;   

int x = 90, y = 90;// variable to store the servo position

void setup() {
  Serial.begin(115200);
 Serial.setTimeout(0.5); 
  horizontal.attach(9);  // attaches the servo on pin 9 to the servo object
  vertical.attach(6); 
  
  horizontal.write(x); 
  vertical.write(y); // attaches the servo on pin 6 to the servo object
}

void loop() {

 
  
   if (Serial.available() > 0) {
    // read the incoming byte:
    input = Serial.readString();

    

    // say what you got:
    if(input == "r")
    {
      horizontal.write(--x); 
    }

    else if(input == "l")
    {
      horizontal.write(++x); 
    }

    else if(input == "d")
    {
      vertical.write(++y); 
    }

    else if(input == "u")
    {
      vertical.write(--y); 
    }

  }
}
