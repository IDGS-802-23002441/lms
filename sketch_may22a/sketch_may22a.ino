#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Mega_2.4G_HGT3";
const char* password = "diegosa9";

// Tu API en MonsterASP
const char* serverName = "https://lmsidgs902.runasp.net/api/sensores";

// Pines para el sensor ultrasónico HC-SR04
const int trigPin = 5;
const int echoPin = 18;

// Variables para calcular la distancia
long duracion;
float distanciaCm;

void setup() {
  Serial.begin(115200);

  // Configuración de los pines del sensor
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT);  

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado");
}

void loop() {
  // 1. Generar el pulso ultrasónico
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // 2. Medir el tiempo que tarda en regresar el eco
  duracion = pulseIn(echoPin, HIGH);
  
  // 3. Calcular la distancia en centímetros
  // Fórmula: velocidad del sonido (0.034 cm/us) dividida entre 2 (ida y vuelta)
  distanciaCm = duracion * 0.0343 / 2.0;

  // Control de errores: si está fuera de rango
  if (distanciaCm >= 400 || distanciaCm <= 2) {
    Serial.println("Lectura fuera de rango o error en el sensor");
  } else {
    Serial.print("Distancia: ");
    Serial.print(distanciaCm);
    Serial.println(" cm");

    // 4. Enviar los datos a la API si hay conexión WiFi
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;

      http.begin(serverName);
      http.addHeader("Content-Type", "application/json");

      // Cambié el nombre del sensor a "HC-SR04" y mandamos la distancia flotante
      String json = "{\"sensor\":\"HC-SR04\",\"valor\":" + String(distanciaCm, 2) + "}";

      int responseCode = http.POST(json);

      Serial.print("Código de respuesta HTTP: ");
      Serial.println(responseCode);

      String response = http.getString();
      Serial.println("Respuesta del servidor: " + response);

      http.end();
    } else {
      Serial.println("Error: Conexión WiFi perdida");
    }
  }

  delay(5000); // Muestreo cada 5 segundos
}