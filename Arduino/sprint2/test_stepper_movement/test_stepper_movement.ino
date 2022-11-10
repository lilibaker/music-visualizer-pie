#include <Adafruit_MotorShield.h>
rad_x = 3; // cm
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *ZMotor = AFMS.getStepper(200, 1)
Adafruit_StepperMotor *XMotor = AFMS.getStepper(200, 2)

void setup() {
  Serial.begin(9600);
  while (!Serial); // Waiting for serial port to setup
  Serial.println("Stepper test!")

  if (!AFMS.begin()){ // if cannot connect to shield 
    Serial.printn("No Motor Shield found")
    while(1);
  }

  Serial.println("Motor Shield found");
  ZMotor->setSpeed(10); // revolution per minute
  XMotor->setSpeed(10);

  Serial.println("Enter X value: ");

}

void loop() {
  while(Serial.avalable() == 0){
  }

  int X = Serial.parseInt(); // X coordination
  int step_x = X / (2 * pi * rad_x); 
  XMotor->step(step_x, FORWARD, DOUBLE);
  //ZMotor->step(step_z, FORWARD, DOUBLE);
}
