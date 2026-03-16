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
