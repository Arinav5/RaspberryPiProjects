# Week 3 Wed GPIO
Lab Date: Jan 28 Wednesday
Due Date: 2:00 PM February 2

# 1. GPIO Pins

1. Type pinout in terminal and pinout will be printed out 

![[20260128_15h49m44s_grim.png]]
## 2. GPIO Zero Library 

###### LED Control 
1. Plug in the power wire to pin 17, the ground wire to pin 39, connect the power wire to resistor, resistor to LED, and LED to ground.
2. Write the Python code in Thonny IDE 
```Python 
from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)
```
3. Execute the code and the LED will blink 

**Read Button State**
1. Plug in ground (pin 39) to the top left pin of the button, plug in power (pin 2) to the bottom left pin of the button
2. Write the code below
```Python 
from gpiozero import Button 
from time import sleep

button = Button(2)

while True:
    if button.is_pressed:
        print("Pressed")
    else:
        print("Released")
    sleep(1)
```
3. Run the code and the code prints out released, press the button, prints out pressed. 

**Control an LED with a Button**

1. Plug in the power wire to pin 17, the ground wire to pin 39, connect the power wire to resistor, resistor to LED, and LED to ground. Plug in ground (pin 39) to the top left pin of the button, plug in power (pin 2) to the bottom left pin of the button. 
2. Write the code below
``` Python
from gpiozero import LED, Button

led = LED(17)
button = Button(2)

while True:
    if button.is_pressed:
        led.on()
    else:
        led.off()
```
3. Run the code the LED lights up when the button is pressed

## 3. Create A Python Class

1. Plug in the power wire to pin 17, the ground wire to pin 39, connect the power wire to resistor, resistor to LED, and LED to ground. Plug in the power wire to pin 27, the ground wire to pin 39, connect the power wire to resistor, resistor to LED, and LED to ground.
2. Write the code below 
```Python 
from gpiozero import LED
from time import sleep

class double_LED:
    def __init__(self, pin1, pin2):
        self.led1 = LED(pin1)
        self.led2 = LED(pin2)
        
    def blink_together(self):
        self.led1.on()
        self.led2.on()
        sleep(1)
        
        self.led1.off()
        self.led2.off()
        sleep(1)
        
    def blink_one_by_one(self):
        self.led1.on()
        sleep(1)
        self.led1.off()
        
        self.led2.on()
        sleep(1)
        self.led2.off()
        
        
my_LED = double_LED(17, 27)

while True:
    #my_LED.blink_together()
    my_LED.blink_one_by_one()
```

4. Run the functions in the while loop one by one