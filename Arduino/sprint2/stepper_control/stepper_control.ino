#include <Adafruit_MotorShield.h>
int rad_x = 3; // cm
int rad_y = 3; // cm
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *YMotor = AFMS.getStepper(200, 1);
Adafruit_StepperMotor * XMotor = AFMS.getStepper(200, 2);

// previous positions (angle or cartesian?); not previously used
int x_previous = 0;
int y_previous = 0;

int x_amount = 0;
int y_amount = 0;

void setup() {
  Serial.begin(9600);
  YMotor->setSpeed(10); // revolution per minute
  XMotor->setSpeed(10);

}

void loop() {
  //  while(Serial.avalable() == 0){
  //  }
  draw(500, 500);
}

void draw(int x_target, int y_target) {
  // Serial.print("here");
  translate_coordinate(x_target, y_target);
  //  update_speeds(x_amount, y_amount);
  move_both_motors(x_amount, y_amount);
}

void translate_coordinate(int x_target, int y_target) {
  // define target coordinate in terms of previous coordinate
  // x_target = x_target - x_previous;
  // y_target = y_target - y_previous;
  
  // // update previous coordinate
  // x_previous = x_target;
  // y_previous = y_target;
  
  // translate to step amounts
  x_amount = x_target / (2 * PI * rad_x) * 200;
  y_amount = y_target / (2 * PI * rad_y) * 200;
}

// might have to go one step at a time in order to have them move at the same time
void move_both_motors(int x_amount, int y_amount) {
  //update_speeds(x_amount, y_amount);
  Serial.print("here");
  //  XMotor->step(x_amount, FORWARD, DOUBLE);
  //  YMotor->step(y_amount, FORWARD, DOUBLE);

  // determine minimum and maximu distance for motors
  int min_amount = min(x_amount, y_amount);
  int max_amount = max(x_amount, y_amount);
  // set up amount of steps needed in each for loop iteration
  int x_steps = 1;
  int y_steps = 1;
  // if x distance is the greatest, it should move max/min times
  if (x_amount == max_amount) {
    x_steps = max_amount / min_amount;
  } else {
    // if y distance is the greatest, it should move max/min times
    y_steps = max_amount / min_amount;
  }
  Serial.print(min_amount);
  Serial.print(" ");
  Serial.println(max_amount);
  // for min_amount times, move the determined amount of steps
  for (int i = 0; i < min_amount; i++) {
    XMotor->step(x_steps, FORWARD, MICROSTEP);
    YMotor->step(y_steps, FORWARD, MICROSTEP);
  }
  //  for (int i = 0; i < 1200; i++) {
  //    XMotor->step(1, BACKWARD, MICROSTEP);
  //    YMotor->step(1, BACKWARD, MICROSTEP);
  //  }
}


// might need to set speeds for arriving at same time
void update_speeds(int x_amount, int y_amount) {
  //XMotor->setSpeed(x_amount / (x_amount + y_amount));
  //YMotor->setSpeed(y_amount / (x_amount + y_amount));
}
