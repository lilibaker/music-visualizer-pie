// Testing audio input

// set up pins
const int RED_LED = 10;
const int GREEN_LED = 11;

// read serial input
const int BUFFER_SIZE = 2;
char buf[BUFFER_SIZE];
int audio_data = 0;

void setup() {
  // initialize digital pins as output
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  read_audio();

}

void read_audio(){
  // get input
  
  if (Serial.available() > 0){
    // change to reflect format of data
    audio_data = Serial.readBytes(buf, BUFFER_SIZE);  
  }
  
  determine_light();
}

void determine_light(){         // change type
  //audio_data = (int)((int *)audio_data);
  int data = (buf[1] << 8) + buf[0];
  int brightness = map(data, -pow(2, 8), pow(2, 8), 0, 255);
  // if input of certain amplitude, light red
  if (data != 0){
    light_on(RED_LED, brightness);
  }

  // if input of certain amplitude, light green
  if (data != 0){
    light_on(GREEN_LED, brightness);
  }
}

void light_on(int led, int brightness){
   analogWrite(led, brightness);
//   delay(500);
//   analogWrite(led, brightness);
}
