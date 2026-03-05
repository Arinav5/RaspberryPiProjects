# TOOLS: Python, Ultralytics, YOLO 
# Mon Computer Vision Servo Motors

## 1. Basic Setup -- Ultralytics and YOLO 

Hardware: Logitech Bri 101 webcam 
Wiring: USB connection from webcam to Pi

* First install ultralytics 
```Linux
pip install ultralytics --break-system-packages
```
* Run Python to donwload the YOLO26 model
```Python
from ultralytics import YOLO
model = YOLO("yolo26n.pt")
## n is nano model (smallest)
## .pt is the PyTorch format. 
```
* Run this Python code to set up the camera stream and detection algorithms
```Python
import cv2
from ultralytics import YOLO

model = YOLO("yolo26n.pt")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small = cv2.resize(frame, (320, 240))     # force 320x240 input
    results = model.predict(small, imgsz=320, verbose=False)  # keep img small

    annotated = results[0].plot()
    cv2.imshow("YOLO USB Cam", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

When the program is running it detect objects being displayed to the camera and names them: 
![[20260303_14h58m01s_grim.png]]

## 2. Visual Servoing with YOLO

results - ultralytics predict() calls will returna list of Results objects that represent the objects seen on the webcam. 

results[0].speed - prints the speed component of the results object which is responsible for the speed of dictionary preprocess, inference, and postprocess speeds in milliseconds per image. 

results[0].boxes - prints the object containing the detection masks of the objects the webcam sees. 

The following is the arduino code that controls the Servo motors based on the Serial connection sent from the Pi

```C
#include <Servo.h>  
  
Servo servo;  // create servo object to control a servo  
  
int angle = 90;  
const int STEP = 45;  
  
void setup() {  
  Serial.begin(115200);  
  servo.attach(9);  // attaches the servo on pin 9 to the servo objectư  
  servo.write(0);   // rotate slowly servo to 0 degrees immediately  
}  
  
void loop() {  
  if (Serial.available() > 0) {  
    String cmd = Serial.readStringUntil('\n');  
    cmd.trim();  
    if (cmd == "LEFT") {  
      angle -= STEP;  
    }  
    if (cmd == "RIGHT") {  
      angle += STEP;  
    }  
    if (cmd == "CENTER") {  
      //hold position  
    }  
    if (angle < 0) angle = 0;  
    if(angle > 180) angle = 180;  
    servo.write(angle);  
     
    Serial.print("Command");  
    Serial.print(cmd);  
    Serial.print(" Angle: ");  
    Serial.println(angle);  
  }  
}
```

This is the code for the Pi that splits the camera into three and then checks where the object is located and then sends that data to the Arduino

```Python 
import cv2
import serial
import time
from ultralytics import YOLO

# Connecting to Arduino
PORT = '/dev/ttyACM0'   # Change if needed
BAUD = 115200
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

model = YOLO("yolo26n.pt")
cap = cv2.VideoCapture(0)

W, H = 320, 240
PERSON_CLASS_ID = 0

def zone_from_cx(cx, w):
    if cx < w/3:
        return "LEFT"
    elif cx > 2*w/3:
        return "RIGHT"
    return "CENTER"

last_cmd = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small = cv2.resize(frame, (W, H))
    results = model.predict(small, imgsz=W, verbose=False)
    boxes = results[0].boxes

    cmd = "CENTER"

    # draw zones
    cv2.line(small, (W // 3, 0), (W // 3, H), (255, 255, 255), 2)
    cv2.line(small, (2 * W // 3, 0), (2 * W // 3, H), (255, 255, 255), 2)

    if boxes is not None and len(boxes) > 0:
        best_i = None
        best_conf = -1.0

        for i in range(len(boxes)):
            cls_id = int(boxes.cls[i].item())
            conf = float(boxes.conf[i].item())
            if cls_id == PERSON_CLASS_ID and conf > best_conf:
                best_conf = conf
                best_i = i

        if best_i is not None:
            x1, y1, x2, y2 = boxes.xyxy[best_i].tolist()
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0

            cmd = zone_from_cx(cx, W)

            cv2.circle(small, (int(cx), int(cy)), 6, (0, 255, 0), -1)
            cv2.putText(small, f"person {best_conf:.2f}", (int(x1), max(20, int(y1)-5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # send serial only if changed
    if cmd != last_cmd:
        ser.write((cmd + "\n").encode("utf-8"))
        last_cmd = cmd
        print("Sent:", cmd)

    cv2.putText(small, f"ZONE: {cmd}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Person Zone Tracking", small)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()

```

The following are the metrics based on the YOLO algorithm

**Width, Height:** 320, 240 
**Model Inference Time:** 93 ms
**FPS:** 1/93ms
![[20260304_13h55m47s_grim.png]]
