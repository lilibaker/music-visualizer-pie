// sprint 1 main code
#include <Servo.h>

// servo 1 = up and down
Servo servoV;
// servo 2 = left and right
Servo servoH;

// initial servo positions
int servoV_pos = 0; // 0 to 180
int servoH_pos = 0; // 0 to 180

int servo_unit_of_distance = 1;

// servo max positions
const int SERVO_MAX_V = 180;
const int SERVO_MIN_V = 0;
const int SERVO_MAX_H = 180;
const int SERVO_MIN_H = 0;

// servo pins
const int servoPin1 = 9;
const int servoPin2 = 10;

// read serial input
const int BUFFER_SIZE = 2;
char buf[BUFFER_SIZE};
int audio_data = 0;

void setup() {
  Serial.begin(9600);

  // Set up servos
  servoV.attach(servoPin1);
  servoH.attach(servoPin2);
}

void loop() {
  // put your main code here, to run repeatedly:
  read_audio();
  reset_servos();
}

void read_audio(){
  // get input
  if (Serial.available() > 0){
    // change to reflect format of data
    audio_data = Serial.readBytes(buf, BUFFER_SIZE);  
  }
  
  determine_light(audio_data);
}

void determine_light(int audio_data){         // change type
  // if input of certain amplitude, draw first option
  if (audio_data != 0){
    draw_one();
  }

  // if input of certain amplitude, draw second option
  if (audio_data != 0){
    draw_two();
  }
}

void draw_one(){
   // TODO
}

void draw_two(){
  // TODO
}

void write_to_servos(){
  servoV.write(servoV_pos);
  servoH.write(servoH_pos);
}

void resetServos() {
  servoV_pos = 0;
  servoH_pos = 0;
  writeToServos();
}
