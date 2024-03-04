/*
 * Authors : @Cl3m3nt0n1 - @RomainH27
 * Licence : GPL3
 */
#include <Arduino.h>

// Define addresses for each potentiometer
#define POT1_ADDR 1
#define POT2_ADDR 2
#define POT3_ADDR 3
#define POT4_ADDR 4
#define POT5_ADDR 5
#define POT6_ADDR 6
const char* specialString = "READY?";


// Variables to store potentiometer values
int pot1Val = 0;
int pot2Val = 0;
int pot3Val = 0;
int pot4Val = 0;
int pot5Val = 0;
int pot6Val = 0;

// Analog pin assignments for each potentiometer
unsigned char pot1 = A0;
unsigned char pot2 = A1;
unsigned char pot3 = A2;
unsigned char pot4 = A3;
unsigned char pot5 = A4;
unsigned char pot6 = A5;


/**
 * @brief Prepares a string representation of a potentiometer value.
 *
 * This function takes the analog pin address of a potentiometer, reads its
 * value, and creates a formatted string to represent the address and value.
 *
 * @param potAddr The analog pin address of the potentiometer.
 * @return A formatted string containing the address and value.
 */
String preparePot(unsigned char potAddr)
{
    String stringToPrint = "@";
    switch (potAddr)
    {
    case A0:
        stringToPrint += POT1_ADDR;
        stringToPrint += "/";
        stringToPrint += pot1Val;
        return stringToPrint;
        break;

    case A1:
        stringToPrint += POT2_ADDR;
        stringToPrint += "/";
        stringToPrint += pot2Val;
        return stringToPrint;
        break;

    case A2:
        stringToPrint += POT3_ADDR;
        stringToPrint += "/";
        stringToPrint += pot3Val;
        return stringToPrint;
        break;

    case A3:
        stringToPrint += POT4_ADDR;
        stringToPrint += "/";
        stringToPrint += pot4Val;
        return stringToPrint;
        break;

    case A4:
        stringToPrint += POT5_ADDR;
        stringToPrint += "/";
        stringToPrint += pot5Val;
        return stringToPrint;
        break;

    case A5:
        stringToPrint += POT6_ADDR;
        stringToPrint += "/";
        stringToPrint += pot6Val;
        return stringToPrint;
        break;

    default:
        return "";
        break;
    }
}

/**
 * @brief Initializes the timer for periodic interrupt handling.
 *
 * This function configures Timer1 with a prescaler and initial counter value
 * to generate periodic interrupts for handling potentiometer readings.
 * Period = 10ms
 */
void initTimer()
{
    TCCR1A = 0;          // Init Timer1A
    TCCR1B = 0;          // Init Timer1B
    TCCR1B |= B00000010; // Prescaler = 8
    TCNT1 = 45535;       // Timer Preloading
    TIMSK1 |= B00000001; // Enable Timer Overflow Interrupt
}

/**
 * @brief Handles the timer interrupt to read potentiometer values and send them via UART.
 *
 * This function is called whenever the timer overflows, and it reads the values of all
 * potentiometers and sends them via UART (Serial).
 */
void handleInterrupt()
{
    // Get values from all potentiometers
    pot1Val = analogRead(pot1);
    pot2Val = analogRead(pot2);
    pot3Val = analogRead(pot3);
    pot4Val = analogRead(pot4);
    pot5Val = analogRead(pot5);
    pot6Val = analogRead(pot6);

    // Send data to UART
    Serial.println(preparePot(pot1));
    Serial.println(preparePot(pot2));
    Serial.println(preparePot(pot3));
    Serial.println(preparePot(pot4));
    Serial.println(preparePot(pot5));
    Serial.println(preparePot(pot6));
}

/**
 * @brief Negotiation function.
 *
 * This function wait for inputs on Serial port.
 * If input is 'OK', initiate the communication and
 * begin to send Pots values.
 */
unsigned char negotiate()
{
    if (Serial.available() >  0) { 
    String receivedString = Serial.readStringUntil('\n'); 
    receivedString.trim();
    if (receivedString == specialString) {
      delay(1200);
      Serial.println("OK");
      delay(1000);
      return 1; 
    }
    else
      return 0;
  }
}

/**
 * @brief Setup function called once at the beginning of the program.
 *
 * This function initializes Serial communication, sets up the timer, and enables interrupts.
 */
void setup()
{

    Serial.begin(115200);
    while(!negotiate());
    initTimer();

    // Enable global interrupts
    interrupts();

}

/**
 * @brief Loop function called repeatedly in the main program.
 *
 * This function is intentionally left empty as all operations are handled in the timer interrupt.
 */
void loop() {}

/**
 * @brief Timer1 Overflow Interrupt Service Routine.
 *
 * This function is called whenever Timer1 overflows, triggering the periodic
 * reading and sending of potentiometer values.
 */
ISR(TIMER1_OVF_vect)
{
    TCNT1 = 45535; // Timer Preloading
    // Handle The Timer Overflow Interrupt
    handleInterrupt();
}
