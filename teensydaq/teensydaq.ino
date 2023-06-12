#include <Arduino.h>
#include <ADC.h>

bool writing = 0;

bool clk = 0;
const int clkPin = 11;
const int readPin = 14;
uint16_t valu;
elapsedMicros timer1;

// ADC vals
ADC *adc = new ADC();
int averages = 0;
int resolution = 13;
float mult;

// Buffer declaration
#define BUFFER_SIZE (1L << 8)
uint16_t buffer[BUFFER_SIZE];
uint8_t buffer_count = BUFFER_SIZE;

IntervalTimer myTimer,myTimer2;
volatile uint16_t valu2 = 0;
volatile boolean newTick;
void setup() {
  Serial.begin(2000000);

  pinMode(readPin, INPUT); // Read pin
  pinMode(clkPin, OUTPUT); // speed clocking
  pinMode(13, OUTPUT);

  // ADC fast setup
  adc->adc0->setAveraging(averages);
  adc->adc0->setResolution(resolution);
  adc->adc0->setConversionSpeed(ADC_CONVERSION_SPEED::HIGH_SPEED);
  adc->adc0->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);
  adc->adc0->startContinuous(readPin);

  myTimer.begin(sampling, 4); // microsecond delay between sampling
  myTimer2.begin(printSampling, 10); // microsecond delay between printing
}

// Max is 3.3 V, but so we get all resolution in 4 digits
void loop() {
  if (Serial.available()) {
    while (Serial.available()) {
      Serial.read();
    }
    digitalWriteFast(clkPin, clk = 0);
    digitalWriteFast(13, writing = !writing);
  }
}



void sampling(){
    if (adc->adc0->isComplete()){
        valu2 = adc->adc0->analogReadContinuous();
        newTick = true;
    }
}

void printSampling(){
    if (newTick && writing){
        digitalWriteFast(clkPin, clk=!clk);
        newTick = false;
        Serial.println(valu2);
    }
}
