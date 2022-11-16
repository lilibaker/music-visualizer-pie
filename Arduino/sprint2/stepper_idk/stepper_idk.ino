#include <Adafruit_MotorShield.h>
float rad_x = 0.03; // cm
float rad_y = 0.03; // cm
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *YMotor = AFMS.getStepper(200, 1);
Adafruit_StepperMotor *XMotor = AFMS.getStepper(200, 2);

void setup() {
  Serial.begin(9600);
  YMotor->setSpeed(1000);
  XMotor->setSpeed(1000);

  AFMS.begin();
  Serial.setTimeout(99999);
  pinMode(LED_BUILTIN, OUTPUT);
}

int drawing = 0;
float max_amount = 0;
float min_amount = 0;
float x_steps = 0;
float y_steps = 0;
int draw_i = 0;
float x_last = 0;
float y_last = 0;
float temp_x = 0;
float temp_y = 0;
int x_dir = 0;
int y_dir = 0;

void loop() {
  digitalWrite(LED_BUILTIN, drawing);
  switch(drawing) {
    case 0: {
      float x = Serial.parseFloat() / (2 * PI * rad_x) * 200;
      float y = Serial.parseFloat() / (2 * PI * rad_y) * 200;

      if(x < x_last) {
        x_dir = BACKWARD;
        temp_x = x;
        x = -x;
      } else {
        x_dir = FORWARD;
        temp_x = x;
      }
      if(y < y_last) {
        y_dir = BACKWARD;
        temp_y = y;
        y = -y;
      } else {
        y_dir = FORWARD;
        temp_y = y;
      }
      

      min_amount = min(abs(x - x_last), abs(y - y_last));
      max_amount = max(abs(x - x_last), abs(y - y_last));
      if(min_amount == 0) {
        min_amount = 1;
      }

      x_steps = 1;
      y_steps = 1;
      if(abs(x - x_last) == max_amount) {
        x_steps = max_amount / min_amount;
      } else {
        y_steps = max_amount / min_amount;
      }

      x_last = temp_x;
      y_last = temp_y;

      draw_i = 0;
      drawing = 1;
      break;
    }
    case 1: {
      YMotor->step(x_steps, x_dir, SINGLE);
      XMotor->step(y_steps, y_dir, SINGLE);
      
      draw_i++;
      if(draw_i >= min_amount) {
        drawing = 0;
      }
      break;
    }
  }
}
