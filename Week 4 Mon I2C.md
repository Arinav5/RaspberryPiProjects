# Week 4 Mon I2C
Lab Date: Feb 2
Due Date: 2:00 pm Feb 9 

## 1. I2C - Basic Setup

* For the hardware setup we plugged in ground to ground, VCC to 5V, SCL into GPIO 3 and SDA to GPIO 2 

* We configured OS through preferences to run I2C
* We ran i2cdetect in the terminal and the result was 

![[20260202_14h21m07s_grim 1.png]]


After running i2cdetect -y 1 we saw 0x3C displayed

## 2. I2C - A Status Monitor 

1. We installed adafruit via terminal command 
``` terminal 
cao@raspberrypiCao:~ $ pip3 install adafruit-circuitpython-ssd1306 --break-system-packages
```
2.  Used the code provided to display hey there. 
3.  Then we wrote code to display the real-time temperature and time status 
```Python 
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import subprocess
from datetime import datetime
import time

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
    # Clear the display (0 for pixel off/black, 255 for pixel on/white)
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
    
    time.sleep(1)
```

4. We added emojis from google noto emoji font. We downloaded the ttf file and unzipped it in the same directory as the code
5. Finally we connected pin 0 of the analog discovery to scl and pin 1 to sda to collect the information. Then opened waveform and looked at the logic and protocol for I2C. 
![[Screenshot 2026-02-02 at 3.27.27 PM.png]]
![[Screenshot 2026-02-02 at 3.27.32 PM.png]]