const int ButtonPort = 2;

int potValue;
int ldrValue;
boolean isLocal = true;
int buttonState = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(ButtonPort, INPUT);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
}

union sensorValue_tag {
   float temp_float ; 
   byte temp_byte[4] ;
} sensorValue;

void loop()
{
  buttonState = digitalRead(ButtonPort);

  if(buttonState == HIGH) {
    isLocal = !isLocal;
  }
  
  potValue = analogRead(A0);
  ldrValue = analogRead(A1);
  
  if(isLocal == true) {
    sensorValue.temp_float = potValue;
  }
  else {
    sensorValue.temp_float = ldrValue;
  }
  
  Serial.write(sensorValue.temp_byte[0]); 
  Serial.write(sensorValue.temp_byte[1]);
  Serial.write(sensorValue.temp_byte[2]);
  Serial.write(sensorValue.temp_byte[3]);
  delay(1000);
}
