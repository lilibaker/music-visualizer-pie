// sprint 1 main code
#include <Servo.h>

// servo 1 = left servo
Servo servoL;
// servo 2 = right servo
Servo servoR;

// initial servo positions
int servoL_pos = 0; // 0 to 180
int servoR_pos = 0; // 0 to 180
int options = 0;

const int SERVO_UNIT_OF_DISTANCE = 1;

// servo max positions
const int SERVO_MAX_L = 180;
const int SERVO_MIN_L = 0;
const int SERVO_MAX_R = 180;
const int SERVO_MIN_R = 0;

// servo pins
const int servoPin1 = 13;
const int servoPin2 = 10;

// read serial input
const int BUFFER_SIZE = 2;
char buf[BUFFER_SIZE];
int audio_data = 0;

void setup() {
  Serial.begin(9600);

  // Set up servos
  servoL.attach(servoPin1);
  servoR.attach(servoPin2);
  reset_servos();
}

void loop() {
  // put your main code here, to run repeatedly:
//  read_audio();
//  reset_servos();
//  determine_shape();
  draw_one();
}

void read_audio(){
  // get input
//  if (Serial.available() > 0){
//    // change to reflect format of data
//    audio_data = Serial.readBytes(buf, BUFFER_SIZE);  
//  }
//  
  determine_shape();
}

void determine_shape(){         // add input for audio data
  // if input of certain amplitude, draw first option
  
//  if (audio_data != 0){
//    draw_one();
//  }
//
//  // if input of certain amplitude, draw second option
//  if (audio_data != 0){
//    draw_two();
//  }

  if (options % 2 == 0){
    draw_one();
  }
  else {
    draw_two();
  }
  options += 1;
}

void draw_one(){
  // Draw diagonal from left?
   for (servoL_pos = SERVO_MIN_L; servoL_pos <= SERVO_MAX_L; servoL_pos = servoL_pos + SERVO_UNIT_OF_DISTANCE){
    write_to_servos();
   }
}

void draw_two(){
  // Draw diagonal from right?
  for (servoR_pos = SERVO_MIN_R; servoR_pos <= SERVO_MAX_R; servoR_pos = servoR_pos + SERVO_UNIT_OF_DISTANCE) {
    // update servo position
    write_to_servos();
  }
   
}

void write_to_servos(){
  servoL.write(servoL_pos);
//  servoR.write(servoR_pos);
}

void reset_servos() {
  servoL_pos = SERVO_MIN_L;
  servoR_pos = SERVO_MIN_R;
  write_to_servos();
}
