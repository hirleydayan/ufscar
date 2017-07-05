#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include <gpio.h>

#define TOUCH "GPIO-A"
#define LED "GPIO-C"

int main()
{
  int x;
  int t = 0;
  int last_t = 0;
  int led_state = HIGH;
 
  if(gpio_open(gpio_id(LED), "out")){
    return (-1);
  }
  if (gpio_open(gpio_id(TOUCH), "in")){
    return(-1);
  }

  while(1){
    t = digitalRead(gpio_id(TOUCH));
    if (t && !last_t){
      digitalWrite(gpio_id(LED), led_state);
      usleep(100000);
      led_state=(led_state==HIGH)?LOW:HIGH;
    }
    last_t = t;
    usleep(1);
  }
  digitalWrite(gpio_id(LED), LOW);
  return EXIT_SUCCESS;
}
