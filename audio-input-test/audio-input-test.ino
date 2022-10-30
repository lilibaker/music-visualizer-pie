// Testing audio input

// set up pins
const int RED_LED = 12;
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
  
  determine_light(audio_data);
}

void determine_light(int audio_data){         // change type
  // if input of certain amplitude, light red
  if (audio_data > 20){
    light_on(RED_LED);
  }

  // if input of certain amplitude, light green
  if (audio_data > 20){
    light_on(GREEN_LED);
  }
}

void light_on(int led){
   digitalWrite(led, HIGH);
   delay(500);
   digitalWrite(led, LOW);
}
