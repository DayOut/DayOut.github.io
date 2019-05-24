#include <DHT.h>
#include <DHT_U.h>
#include <MQ135.h> // подключение библиотеки
#define analogPin A0 // аналоговый выход MQ135 подключен к пину A0 Arduino

/*
  The lastest real version of weino
*/

#define DHTPIN 2 //thermometr

#define DHTTYPE DHT22 // model of thermometer

MQ135 gasSensor = MQ135(analogPin); // инициализация объекта датчика

DHT dht(2, DHT22);

String jsonAdd (String str, String name, String value){
  if(str[1]){
    str += ", ";
  }
  str += "\"" + name + "\": \"" + value + "\"";
  return str;
}

void setup() {
  Serial.begin(9600); 
  Serial.println("DHTxx test!");
 
  dht.begin();
}

int count = 0;
String testvar = "";

void loop() {
  String jsonAnswer = "";
  String s = String(count++) + ": " + String( "123");
  //Serial.println(s);
  delay(600);
  jsonAnswer += "{";
  jsonAnswer = jsonAdd(jsonAnswer, "status", String(count));
  while (Serial.available() > 0) {
      // look for the next valid integer in the incoming serial stream:
      testvar = Serial.readStringUntil('\n');
      //testvar = );
      Serial.println("arduino: " + testvar);
      jsonAnswer = jsonAdd(jsonAnswer, "arduino", testvar);
  }
  //Serial.println("arduino: finished while\n");

  
  //---------------------thermometer----------------------------------------
  // Wait a few seconds between measurements.
  delay(2000);
  //Serial.println("thermometer");
  
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  
  // Read temperature as Celsius
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  jsonAnswer = jsonAdd(jsonAnswer, "humidity", String(h));
  jsonAnswer = jsonAdd(jsonAnswer, "temperature", String(t));
  //---------------------/thermometer----------------------------------------
  //---------------------MQ135-----------------------------------------------
  float ppm = gasSensor.getCorrectedPPM(t,h);
  jsonAnswer = jsonAdd(jsonAnswer, "ppm", String(ppm));
  //---------------------/MQ135-----------------------------------------------
  
  //send response
  jsonAnswer += "}";
  Serial.println(jsonAnswer);
}
