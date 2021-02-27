/*
  Electrical Conductivity and pH Sensor

  Using an Uno 3 board to read the analog data from the 
  Electrical Conductivity and pH sensors, then pass the
  values on to the Raspberry Pi every 60 seconds

*/

#define ph_sensor 0
#define ec_sensor 1
#define offset 0.00
// Variables to be passed to Pi
unsigned long int avg_ph;
float nutrient_level = 0.0;

// Assigning pins to sensors

int ec_sensor = A1;

void setup() {
  // Open Serial port for communication with Pi
  Serial.begin(9600);
}

void loop() {
  nutrient_level = analogRead(ec_sensor);
  
  int buf[10];                //buffer to hold ph sensor values
  for(int i=0;i<10;i++)       //Get 10 samples from the sensor to get better accuracy
  { 
    buf[i]=analogRead(ph_sensor);
    delay(10);
  }
  avg_ph=0;
  for(int i=0;i<10;i++)                     //adds together all samples to get an average
    avg_ph+=buf[i];
  float ph_level=(float)avg_ph*5.0/1024/6;    //convert analog input into millivolt
  ph_level=3.5*ph_level+Offset;               //convert millivolts into pH value
  // Sends data through serial port
  Serial.println(ph_level,2);
  Serial.println(nutrient_level);

  // Wait 60 seconds before updating levels again
  delay(60000);
}