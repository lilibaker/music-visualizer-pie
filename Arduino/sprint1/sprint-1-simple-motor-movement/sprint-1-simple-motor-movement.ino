/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep
*/

#include <Servo.h>

Servo left_servo;  // create servo object to control a servo
// twelve servo objects can be created on most boards
Servo right_servo;
int pos = 0;    // variable to store the servo position

void setup() {
  left_servo.attach(13);  // attaches the servo on pin 9 to the servo object
  right_servo.attach(10);
}

void loop() {
  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    left_servo.write(pos);              // tell servo to go to position in variable 'pos'
    right_servo.write(180-pos);
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    left_servo.write(pos);     
    right_servo.write(180-pos);// tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15 ms for the servo to reach the position
  }
}
