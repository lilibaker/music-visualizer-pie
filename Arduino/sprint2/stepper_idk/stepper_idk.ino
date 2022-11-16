#include <Adafruit_MotorShield.h>
int rad_x = 3; // cm
int rad_y = 3; // cm
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *YMotor = AFMS.getStepper(200, 1);
Adafruit_StepperMotor *XMotor = AFMS.getStepper(200, 2);

void setup() {
  Serial.begin(9600);
  YMotor->setSpeed(100);
  XMotor->setSpeed(100);

  AFMS.begin();
  Serial.setTimeout(99999);
}

int drawing = 0;
int max_amount = 0;
int min_amount = 0;
int x_steps = 0;
int y_steps = 0;
int draw_i = 0;
int x_last = 0;
int y_last = 0;
int x_dir = 0;
int y_dir = 0;

void loop() {
  // put your main code here, to run repeatedly:
  //XMotor->step(10, FORWARD, MICROSTEP);
  //YMotor->step(10, FORWARD, MICROSTEP);
  switch(drawing) {
    case 0: {
      float x = Serial.parseFloat() / (2 * PI * rad_x);// * 200;
      float y = Serial.parseFloat() / (2 * PI * rad_y);// * 200;

      if(x < x_last) {
        x_dir = BACKWARD;
        x = -x;
      } else {
        x_dir = FORWARD;
      }
      if(y < y_last) {
        y_dir = BACKWARD;
        y = -y;
      } else {
        y_dir = FORWARD;
      }

      min_amount = min(x - x_last, y - y_last);
      max_amount = max(x - x_last, y - y_last);

      x_last = x;
      y_last = y;

      x_steps = 1;
      y_steps = 1;
      if(x == min_amount) {
        x_steps = max_amount / min_amount;
      } else {
        y_steps = max_amount / min_amount;
      }

      draw_i = 0;
      drawing = 1;
      break;
    }
    case 1: {
      YMotor->step(x_steps, x_dir, SINGLE);
      XMotor->step(y_steps, y_dir, SINGLE);
      
      draw_i++;
      if(draw_i == min_amount) {
        drawing = 0;
      }
      break;
    }
  }
}
