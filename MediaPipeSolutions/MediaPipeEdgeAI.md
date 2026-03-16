
Software components: Thonny
Hardware components: Webcam, Raspberry Pi
## The Usage of MediaPipe Studio
We deployed 4 out of 5 use cases from Google MediaPipe examples for Raspberry Pi. 
### Gesture Recognition:

```Python 
 
 import mediapipe as mp  
from mediapipe.tasks import python  
from mediapipe.tasks.python import vision  
import cv2  
import time  
import socket  
  
  
HOST = '10.144.113.15'  
PORT = 5000  
  
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
client.connect((HOST, PORT))  
  
model_path = '/Users/arinavardanyan/Documents/Classes/embedded_systems/MediaPipeDemo/gesture_recognizer.task'  
  
BaseOptions = mp.tasks.BaseOptions  
GestureRecognizer = mp.tasks.vision.GestureRecognizer  
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions  
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult  
VisionRunningMode = mp.tasks.vision.RunningMode  
  
cap = cv2.VideoCapture(0)  
# Create a gesture recognizer instance with the live stream mode:  
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):  
     if result.gestures:  
        gesture = result.gestures[0][0].category_name  
        confidence = result.gestures[0][0].score  
        print(f"{gesture} ({confidence:.2f})")  
        client.send(gesture.encode())  
  
options = GestureRecognizerOptions(  
    base_options=BaseOptions(model_asset_path=model_path),  
    running_mode=VisionRunningMode.LIVE_STREAM,  
    result_callback=print_result)  
with GestureRecognizer.create_from_options(options) as recognizer:  
     while cap.isOpened():  
        success, image = cap.read()  
        if not success:  
            print("Ignoring empty camera frame.")  
            # If loading a video, use 'break' instead of 'continue'.  
            continue  
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
        timestamp_ms = int(time.time() * 1000)  
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)  
        recognizer.recognize_async(mp_image, timestamp_ms)  
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))  
        if cv2.waitKey(5) & 0xFF == 27:  
            break  
cap.release()
```
### Hand Landmark:

```Python 
import cv2  
import mediapipe as mp  
  
mp_drawing = mp.solutions.drawing_utils  
mp_drawing_styles = mp.solutions.drawing_styles  
mp_hands = mp.solutions.hands  
  
cap = cv2.VideoCapture(0)  
  
with mp_hands.Hands(  
    model_complexity=0,  
    min_detection_confidence=0.5,  
    min_tracking_confidence=0.5) as hands:  
  
    while cap.isOpened():  
        success, image = cap.read()  
        if not success:  
            print("Ignoring empty camera frame.")  
            # If loading a video, use 'break' instead of 'continue'.  
            continue  
  
        image.flags.writeable = False  
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
        results = hands.process(image)  
  
        image.flags.writeable = True  
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  
        if results.multi_hand_landmarks:  
            for hand_landmarks in results.multi_hand_landmarks:  
                mp_drawing.draw_landmarks(  
                image,  
                hand_landmarks,  
                mp_hands.HAND_CONNECTIONS,  
                mp_drawing_styles.get_default_hand_landmarks_style(),  
                mp_drawing_styles.get_default_hand_connections_style())  
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))  
        if cv2.waitKey(5) & 0xFF == 27:  
            break  
  
  
cap.release()

```

### Face Detector
```Python 
import mediapipe as mp  
from mediapipe.tasks import python  
from mediapipe.tasks.python import vision  
import cv2  
import time  
  
model_path = '/Users/arinavardanyan/Documents/Classes/embedded_systems/MediaPipeDemo/blaze_face_short_range.tflite'  
  
  
BaseOptions = mp.tasks.BaseOptions  
FaceDetector = mp.tasks.vision.FaceDetector  
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions  
FaceDetectorResult = mp.tasks.vision.FaceDetectorResult  
VisionRunningMode = mp.tasks.vision.RunningMode  
  
# Create a face landmarker instance with the live stream mode:  
def print_result(result: FaceDetectorResult, output_image: mp.Image, timestamp_ms: int):  
    print("face detected")  
  
options = FaceDetectorOptions(  
    base_options=BaseOptions(model_asset_path=model_path),  
    running_mode=VisionRunningMode.LIVE_STREAM,  
    result_callback=print_result)  
  
cap = cv2.VideoCapture(0)  
  
with FaceDetector.create_from_options(options) as detector:  
     while cap.isOpened():  
        success, image = cap.read()  
        if not success:  
            print("Ignoring empty camera frame.")  
            # If loading a video, use 'break' instead of 'continue'.  
            continue  
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
        timestamp_ms = int(time.time() * 1000)  
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)  
        detector.detect_async(mp_image, timestamp_ms)  
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))  
        if cv2.waitKey(5) & 0xFF == 27:  
            break  
cap.release()
```

### Face Landmarker
```Python
import mediapipe as mp  
from mediapipe.tasks import python  
from mediapipe.tasks.python import vision  
import cv2  
import time  
  
model_path = '/Users/arinavardanyan/Documents/Classes/embedded_systems/MediaPipeDemo/blaze_face_short_range.tflite'  
  
  
BaseOptions = mp.tasks.BaseOptions  
FaceLandmarker = mp.tasks.vision.FaceLandmarker  
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions  
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult  
VisionRunningMode = mp.tasks.vision.RunningMode  
  
# Create a face landmarker instance with the live stream mode:  
def print_result(result: FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int):  
    print('face landmarker result: {}'.format(result))  
  
options = FaceLandmarkerOptions(  
    base_options=BaseOptions(model_asset_path=model_path),  
    running_mode=VisionRunningMode.LIVE_STREAM,  
    result_callback=print_result)  
  
cap = cv2.VideoCapture(0)  
  
with FaceLandmarker.create_from_options(options) as landmarker:  
     while cap.isOpened():  
        success, image = cap.read()  
        if not success:  
            print("Ignoring empty camera frame.")  
            # If loading a video, use 'break' instead of 'continue'.  
            continue  
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
        timestamp_ms = int(time.time() * 1000)  
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)  
        landmarker.detect_async(mp_image, timestamp_ms)  
        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))  
        if cv2.waitKey(5) & 0xFF == 27:  
            break  
cap.release()
```


## Hardware-Software Integration with MediaPipe

We used the code from gesture_recognition and then connected it to raspberry pi to send the gesture. Then an LED was turned on or off depending on wether the open_palm gesture was shown.

This is the code that was written in the RaspberryPi

```Python 
import socket
import RPi.GPIO as GPIO

LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

HOST = '0.0.0.0'  # listen on all interfaces
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Waiting for connection...")

conn, addr = server.accept()
print("Connected by", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    data = data.decode()
    
    if data == "Open_Palm":
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        

```
