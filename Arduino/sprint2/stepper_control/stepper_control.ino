#include <Adafruit_MotorShield.h>
rad_x = 3; // cm
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *ZMotor = AFMS.getStepper(200, 1)
Adafruit_StepperMotor *XMotor = AFMS.getStepper(200, 2)

// current positions (angle or cartesian?); not currently used
int x_current = 0;
int z_current = 0;

int x_amount = 0;
int z_amount = 0;

void setup() {
  Serial.begin(9600);

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
//  while(Serial.avalable() == 0){
//  }


}

void draw(int x_target, int z_target){
  translate_coordinate(x_target, z_target);
  update_speeds(x_amount, z_amount);
  move_both_motors(x_amount, z_amount);
}

void translate_coordinate(int x_target, int z_target){
  x_amount = x_target / (2 * pi * rad_x);
  z_amount = z_target / (2 * pi * rad_z);
}
 
void move_both_motors(int x_amount, int z_amount){
  update_speeds(x_amount, z_amount);
  XMotor->step(x_amount, FORWARD, DOUBLE);
  ZMotor->step(z_amount, FORWARD, DOUBLE);
}


// might need to set speeds for arriving at same time
void update_speeds(int x_amount, int z_amount){
  XMotor->setSpeed(x_amount / (x_amount + z_amount));
  ZMotor->setSpeed(z_amount / (x_amount + z_amount));
}
