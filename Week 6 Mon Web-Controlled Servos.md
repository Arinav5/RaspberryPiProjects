## Week 6 Mon: Web-Controlled Servos
Lab Date: Feb 16
Due Date: 2:00pm Feb 23

## 1. Basic Setup: Servo and Arduino 

Hardware Components used: Arduino Uno, Wires, two servo motors, breadboard, 5v Power supply

Wiring Connections: Connected 5V power supply to motor through the breadboard, ground is connected to the breadboard which is connected to the arduino, servos connected to pin 4 and 5. 

Code Implementation for Arduino: 

```C 
#include <Servo.h>  
  
Servo servo_one;  
Servo servo_two;  
  
void setup() {  
  // put your setup code here, to run once:  
  servo_one.attach(4);  
  servo_two.attach(5);  
}  
  
void loop() {  
  // put your main code here, to run repeatedly:  
  servo_one.write(180);  
  servo_two.write(90);  
  delay(1000);  
  // Servo is stationary for 1 second.  
  servo_one.write(90);  
  servo_two.write(180);  
  delay(1000);  
  // Servo spins in reverse at full speed for 1 second.  
  servo_one.write(0);  
  servo_two.write(90);  
  delay(1000);  
  // Servo is stationary for 1 second.  
  servo_one.write(90);  
  servo_two.write(0);  
  delay(1000);  
}
```
Results:

The motors move at different angles continuously and at the same time
First motor moves to positions: 180, 90, 0, 90
The second motor moves to positions: 90, 180, 90, 0


## 2. Web Controlled Servos

Hardware components: Arduino, Two servo motors, Pi, power supply 
Wiring Connection: Connected 5V power supply to motor through the breadboard, ground is connected to the breadboard which is connected to the arduino, servos connected to pin 4 and 5, Arduino connected to Pi via USB. 

Code Implementation for Arduino: 

```C
#include <Servo.h>  
  
Servo servo_one;  
Servo servo_two;  
String inputString = "";  
  
void setup() {  
  // put your setup code here, to run once:  
  servo_one.attach(4);  
  servo_two.attach(5);  
  Serial.begin(115200);  
  servo_one.write(0);  
  servo_two.write(0);  
}  
  
void loop() {  
  if (Serial.available() > 0) {  
    String data = Serial.readStringUntil('\n');  
    data.trim();  
    Serial.println(data);  
    inputString = data;  
  }  
    int commaIndex = inputString.indexOf(',');  
    if (commaIndex > 0) {  
      int angle1 = inputString.substring(0, commaIndex).toInt();  
      int angle2 = inputString.substring(commaIndex + 1).toInt();  
  
       
      Serial.println(angle1);  
      Serial.println(angle2);  
      delay(1000);  
  
      servo_one.write(angle1);  
      servo_two.write(angle2);  
 }    
}
```

Code Implementation for Flask on Pi 

```Python
from flask import Flask, request, render_template
import serial
import time
 
app = Flask(__name__)
 
#Arduino Setup
PORT = '/dev/ttyACM1'
BAUD_RATE = 115200 
angles = ""
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)
@app.route('/', methods=['GET', 'POST'])
def servo_angles():
    if request.method == 'POST':
        angle_one = request.form['angle_servo_one']
        angle_two = request.form['angle_servo_two']
        angles = f"{angle_one}, {angle_two}\n"
        
        #data sent to the Arduino
        ser.write(angles.encode())
        
        #data received by the Arduino
        if ser.in_waiting:
           print(ser.readline().decode())
        return f"{angle_one}, {angle_two}"
    return render_template('main_page.html')
 
if __name__ == '__main__':
    app.run() 
```

Code implementation for HTML for UI

```HTML
<!DOCTYPE html>
<html>
<body>
    <form method="post">
        <h3>Enter Servo One Angle</h3>
        <input type="text" name="angle_servo_one" required>
        <h3>Enter Servo Two Angle</h3>
        <input type="text" name="angle_servo_two" required>
        <br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
```

Results: 

User is presented with following UI 
![[20260218_14h40m02s_grim.png]]

User inputs angles for each motor clicks submit, a POST request is sent to the Pi, the Pi sends the angles via serial connection to the servos, and the motors change positions based on the specified angles. 