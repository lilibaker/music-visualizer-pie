#include <Adafruit_MotorShield.h>
int rad_x = 3; // cm
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *ZMotor = AFMS.getStepper(200, 1);
Adafruit_StepperMotor *XMotor = AFMS.getStepper(200, 2);

void setup() {
  Serial.begin(9600);
  while (!Serial); // Waiting for serial port to setup
  Serial.println("Stepper test!");

  if (!AFMS.begin()){ // if cannot connect to shield 
    Serial.println("No Motor Shield found");
    while(1);
  }

  Serial.println("Motor Shield found");
  ZMotor->setSpeed(10); // revolution per minute
  XMotor->setSpeed(10);

  Serial.println("Enter X value: ");

}

void loop() {

  //int X = Serial.parseInt(); // X coordination
  int X = 300;
  int step_x = X / (2 * PI * rad_x); 
  // XMotor->step(step_x, FORWARD, DOUBLE);
  //ZMotor->step(step_z, FORWARD, DOUBLE);
  for (int i = 0; i < 500; i++) {
    XMotor->step(2.4, FORWARD, MICROSTEP);
    ZMotor->step(2, FORWARD, MICROSTEP);
    Serial.println("step");
  }
}
