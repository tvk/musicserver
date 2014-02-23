// Mapping of pins to the hour they represent. Pin 8 is not used
// due to the circuit board layout
int hours[] = {0,1,2,3,4,5,6,7,9,10,11,12};


/**
 * Initializes the board
 */
void setup()
{
  // Initialize the led's
  for (int i = 0; i < 12; i++)
    pinMode(hours[i], OUTPUT);     
  //Serial.begin(115200);
}

/**
 * The main loop.
 * Reads a byte from the serial stream. Each byte represents a bitmask which led's 
 * should light.
 *
 * As a single bitmask can not hold the information for 12 states, those two bitmasks
 * can be sent:
 *
 * For 0 o'clock to 5 o'clock send:
 * [0 | 0 hr | 1 hr | 2 hr | 3 hr | 4 hr | 5 hr]
 * For 6 o'clock to 11 o'clock send:
 * [1 | 6 hr | 7 hr | 8 hr | 9 hr | 10 hr | 11 hr]
 *
 * Examples:
 * 2 o'clock should light: Send pow(2,3) = 8
 * 8 o'clock should light: Send pow(2,0) + pow(2,3) = 9
 * 8 o'clock and 11 o'clock should light: Send pow(2,0) + pow(2,3) + pow(2,6) = 73
 */
void loop()
{
    while (Serial.available() > 0) 
    {
      int mask = Serial.read();            
      int offset = (mask % 2 == 0) ? 0 : 6;
      for (int hour = 0; hour < 6; hour++)
          digitalWrite(hours[hour + offset], mask & intPow(2,1 + hour));
    }    
}
 

/**
 * Returns x to the power of y, accepts and returns only
 * int values.
 */
int intPow(int x, int y)
{
  return (y > 0) ? x * intPow(x, y - 1) : 1;
}
