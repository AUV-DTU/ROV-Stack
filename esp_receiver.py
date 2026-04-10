#include <Arduino.h>
#include <Wire.h>
#include <Servo.h>
#include "MS5837.h"

#define NUM_MOTORS 8

// ESC pins
int escPins[NUM_MOTORS] = {13, 12, 14, 27, 26, 25, 33, 32};

// Servo objects
Servo esc[NUM_MOTORS];

// Sensor
MS5837 sensor;

// PWM value (in microseconds)
int pwmValue = 1500;

// =============================
// SETUP
// =============================
void setup() {
  Serial.begin(115200);

  // Attach ESCs
  for (int i = 0; i < NUM_MOTORS; i++) {
    esc[i].attach(escPins[i]);
  }

  // Arm ESCs
  Serial.println("Arming ESCs...");
  for (int i = 0; i < NUM_MOTORS; i++) {
    esc[i].writeMicroseconds(1000);
  }
  delay(3000);

  // Init sensor
  Wire.begin();

  if (!sensor.init()) {
    Serial.println("MS5837 not found!");
    while (1);
  }

  sensor.setModel(MS5837::MS5837_30BA);
  sensor.setFluidDensity(997);

  Serial.println("Setup complete");
}

// =============================
// LOOP
// =============================
void loop() {

  // Read sensor
  sensor.read();
  float pressure = sensor.pressure();
  float temperature = sensor.temperature();

  Serial.print("Pressure: ");
  Serial.print(pressure);
  Serial.print("  Temp: ");
  Serial.println(temperature);

  // Basic mapping (placeholder logic)
  pwmValue = 1500 + (pressure - 1000) * 0.1;

  // Clamp
  pwmValue = constrain(pwmValue, 1100, 1900);

  // Send to all ESCs
  for (int i = 0; i < NUM_MOTORS; i++) {
    esc[i].writeMicroseconds(pwmValue);
  }

  delay(50);
}