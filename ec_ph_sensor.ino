/*
  Electrical Conductivity and pH Sensor

  Using an Uno 3 board to read the analog data from the 
  Electrical Conductivity and pH sensors, then pass the
  values on to the Raspberry Pi every 60 seconds

*/

// Variables to be passed to Pi
float ph_level = 0.0;
float nutrient_level = 0.0;

// Assigning pins to sensors
int ph_sensor = A0;
int ec_sensor = A1;

void setup() {
  // Open Serial port for communication with Pi
  Serial.begin(9600);
}

void loop() {
  ph_level = analogRead(ph_sensor);
  nutrient_level = analogRead(ec_sensor);
  
  // Sends data through serial port
  Serial.println(ph_level);
  Serial.println(nutrient_level);

  // Wait 60 seconds before updating levels again
  delay(60000);
}