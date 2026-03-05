## Week 5 Wed Arduino SensorMotor
Lab Date: Feb 9 Monday
Due Date: 2:00pm Feb 16

## 1. Sensor Integration 
* Connect Arduino to laptop
* Download libraries for arduino 
	* Adafruit MPU6050
	* Adafruit BusIO
	* Adafruit Unified Sensor
* Then upload the code to the arduino
```C++
// Basic demo for accelerometer readings from Adafruit MPU6050

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }

  Serial.println("");
  delay(100);
}

void loop() {

  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  /* Print out the values */
  Serial.print("Acceleration X: ");
  Serial.print(a.acceleration.x);
  Serial.print(", Y: ");
  Serial.print(a.acceleration.y);
  Serial.print(", Z: ");
  Serial.print(a.acceleration.z);
  Serial.println(" m/s^2");

  Serial.print("Rotation X: ");
  Serial.print(g.gyro.x);
  Serial.print(", Y: ");
  Serial.print(g.gyro.y);
  Serial.print(", Z: ");
  Serial.print(g.gyro.z);
  Serial.println(" rad/s");

  Serial.print("Temperature: ");
  Serial.print(temp.temperature);
  Serial.println(" degC");

  Serial.println("");
  delay(500);
}
```

* Connect the arduino to the raspberryPi 
* Find where the Pi connects to the arduino 
```terminal
ls /dev/ttyACM*
```
* Write the code to run on the Pi
```Python
import serial

PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

ser = serial.Serial(PORT, BAUD_RATE, timeout=1)

while True:
  line = ser.readline().decode(errors='ignore').strip()
  if line:
      print(line)
```

## 2. Design a Vibration Alarm System 
* Write code for the arduino to detect when the sensor is in alarm mode 
``` C++ 
// Basic demo for accelerometer readings from Adafruit MPU6050

  

#include <Adafruit_MPU6050.h>

#include <Adafruit_Sensor.h>

#include <Wire.h>

  

Adafruit_MPU6050 mpu;
bool alarmMode = false;
unsigned long stableStartTime = 0;

  
void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens
  

  Serial.println("Adafruit MPU6050 test!");
  

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");


  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  Serial.print("Accelerometer range set to: ");
  switch (mpu.getAccelerometerRange()) {
  case MPU6050_RANGE_2_G:
    Serial.println("+-2G");
    break;
  case MPU6050_RANGE_4_G:
    Serial.println("+-4G");
    break;
  case MPU6050_RANGE_8_G:
    Serial.println("+-8G");
    break;
  case MPU6050_RANGE_16_G:
    Serial.println("+-16G");
    break;
  }
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  Serial.print("Gyro range set to: ");
  switch (mpu.getGyroRange()) {
  case MPU6050_RANGE_250_DEG:
    Serial.println("+- 250 deg/s");
    break;
  case MPU6050_RANGE_500_DEG:
    Serial.println("+- 500 deg/s");
    break;
  case MPU6050_RANGE_1000_DEG:
    Serial.println("+- 1000 deg/s");
    break;
  case MPU6050_RANGE_2000_DEG:
    Serial.println("+- 2000 deg/s");
    break;
  }

  
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.print("Filter bandwidth set to: ");
  switch (mpu.getFilterBandwidth()) {
  case MPU6050_BAND_260_HZ:
    Serial.println("260 Hz");
    break;
  case MPU6050_BAND_184_HZ:
    Serial.println("184 Hz");
    break;
  case MPU6050_BAND_94_HZ:
    Serial.println("94 Hz");
    break;
  case MPU6050_BAND_44_HZ:
    Serial.println("44 Hz");
    break;
  case MPU6050_BAND_21_HZ:
    Serial.println("21 Hz");
    break;
  case MPU6050_BAND_10_HZ:
    Serial.println("10 Hz");
    break;
  case MPU6050_BAND_5_HZ:
    Serial.println("5 Hz");
    break;
  }


  Serial.println("");
  delay(100);
}


void loop() {
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  float ax = a.acceleration.x;
  float ay = a.acceleration.y;
  float az = a.acceleration.z;
  float gx = g.gyro.x/131.0;
  float gy = g.gyro.y/131.0;
  float gz = g.gyro.z/131.0;
  float accelMagnitude = sqrt(ax*ax + ay*ay + az*az);
  bool strongAccel = abs(accelMagnitude - 1.0) > 50;   // > ~1.8g total
  bool strongGyro  = abs(gx) > 0.05 || abs(gy) > 0.05 || abs(gz) > 0.05;
  /* Print out the values */


  if(strongAccel || strongGyro) {
    alarmMode = true; 
    stableStartTime = 0; 
  }

  if (alarmMode) {
    Serial.println("1");


//    Serial.print("Accel (g): ");
//    Serial.print(ax); Serial.print(" ");
//    Serial.print(ay); Serial.print(" ");
//    Serial.println(az);
//
//    Serial.print("Gyro (deg/s): ");
//    Serial.print(gx); Serial.print(" ");
//    Serial.print(gy); Serial.print(" ");
//    Serial.println(gz);
  

    // Check if stable again
    if (!strongAccel && !strongGyro) {
      if (stableStartTime == 0) {
        stableStartTime = millis();
      }
  
      if (millis() - stableStartTime > 2000) { // 2 seconds stable
        alarmMode = false;
        Serial.println("0");
      }
    }
  }
  
  //NORMAL MODE
  else {
    Serial.println("0");
  }
  delay(500);
}
```

* Write the code for the Pi
```Python
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import subprocess
from datetime import datetime
import time
import serial 


#MPU Setup
PORT = '/dev/ttyACM0'
BAUD_RATE = 115200

#Port setup
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)

# Create the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
# Create the SSD1306 OLED class
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# # Clear the display (0 for pixel off/black, 255 for pixel on/white)
oled.fill(0)
oled.show()

# Create a blank image for drawing (mode '1' for 1-bit color/black & white)
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)


#Emojis
emoji_font_path = "NotoEmoji-VariableFont_wght.ttf"  
emoji_font = ImageFont.truetype(emoji_font_path, 10)

# Draw the text
# syntax: draw.text((x, y), text, font=font, fill=255)
font = ImageFont.load_default()
while True:
    line = ser.readline().decode(errors='ignore').strip()
    if line == "1":
        oled.fill(0)
        oled.show()
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)
        
        draw.text((40, 0), "ALARM MODE", font=font, fill=255)
        
        oled.image(image)
        oled.show()
    # Clear the display (0 for pixel off/black, 255 for pixel on/white)
    else:
        oled.fill(0)
        oled.show()
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)
        

        temp = subprocess.check_output("vcgencmd measure_temp",shell=True)
        # temp = temp.split("temp=")[1]
        temp = temp.decode().strip()
        temp = temp.replace("temp=", "").replace("'C", "")
        print(temp)

        time_now = datetime.now().strftime("%H:%M:%S")
        
        draw.text((40, 0), "Temp:  " + temp + "c", font=font, fill=255)
        draw.text((40, 30), "Time:  " + time_now, font=font, fill=255)
        draw.text((20, 30), "\U0001F319", font=emoji_font, fill=255)
        draw.text((20, 0), "\U0001F321", font=emoji_font, fill=255)

        # Display the image
        oled.image(image)
        oled.show()
    
    time.sleep(0.1)

```

The arduino will send 0 for normal mode and 1 for alarm mode. Alarm mode occurs when the sensor is being shaked. The Pi detects when the sensor is shaking and prints alarm mode. And when the sensor is not being shaken it prints the time and temperature. 