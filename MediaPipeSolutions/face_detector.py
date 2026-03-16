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

