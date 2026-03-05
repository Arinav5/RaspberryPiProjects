# Week 4 Wed SPI

Lab Date : Feb 4 Wednesday
Due Date: 2:00pm Feb 9 

## 1. SPI - Basic Set-up 

* First we wired the LCD display connecting ground to pin6, VCC to pin1, DIN to pin 19, clock to pin 23, SC to pin 24, DC to pin 22, RST to pin 13, BL to pin 12. 
* Then we configured the PI OS to work with SPI. 


## 2.  SPI - Simple Image Display 

*  Downloaded the sample code from waveshare 
* Navigated to the LCD_Module_RPI_code/RaspberryPi/python/example and ran 2inch_LCD_test.py and modified the open instruction to open LCD_2inch.jpg 

## 3. SPI - A News Displayer

The following is the code to print the images from ECS news by parsing image tags. 
```Python
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from  urllib.request import urlopen
from urllib.parse import urljoin
import sys 
import time
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_2inch

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_2inch.LCD_2inch(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = LCD_2inch.LCD_2inch()
    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()
    #Set the backlight to 100
    disp.bl_DutyCycle(50)
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()

url = "https://ecs.syracuse.edu/about/news/archive"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

img_tags = soup.find_all("img")
image_urls = []
# image_urls = [
#     "https://www.syracuse.com/resizer/v2/BE7QISLMAZBKXMUJSQJAAOS5IE.jpg?auth=300212341e9559dfb623bc5078e95ee7baba393a9a86cf25b1c99cc9a08d4367&width=1280&smart=true&quality=90",
#     "https://ecs.syracuse.edu/wp-content/uploads/2026/02/BioInspired-Photo-Crop-700x576.jpg",
#     "https://ecs.syracuse.edu/wp-content/uploads/2026/01/Paulo-Shakarian-crop-2-700x576.jpg"]
# for img in img_tags:
#     src = img.get("src")
#     if src:
#         full_url = urljoin(url, src)
#         image_urls.append(full_url)
start = 0
end = 20 
for i, img in enumerate(img_tags[start:end], start = 1):
    src = img.get("src")
    print(src)
    if src:
        image_urls.append(src)


LCD_WIDTH = 320
LCD_HEIGHT = 240


images = [] 
for url in image_urls:
    try: 
        images.append(Image.open(urlopen(url)))
    except Exception as e:
        print("error ", e)
        
print(images)
while True: 
    for image in images:
        image = image.resize((LCD_WIDTH, LCD_HEIGHT))
        print(image)
        disp.ShowImage(image)
        time.sleep(3)
```

