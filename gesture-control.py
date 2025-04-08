#!/usr/bin/python3

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2
import pyautogui
import numpy as np

pyautogui.FAILSAFE = False

w=pyautogui.size().width
h=pyautogui.size().height

A = np.array([[1,i]for i in range(-10,0)])
print(A)
Ap = np.linalg.pinv(A)
y = np.array([1,-1])

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    v = min(max(rightMin,rightMin + (valueScaled * rightSpan)),rightMax)

    print("Value:", v)

    # Convert the 0-1 range into a value in the right range.
    return v

class statemachine:
  move = True

  def __init__(self):
    self.state = "Move"
    self.lasty = 0

  def update(self, gesture, posy):
    if(self.state == "Move"):
      if(gesture == "Pointing_Up"):
        self.state = "Click"
      elif(gesture == "Closed_Fist"):
        pyautogui.mouseDown()
        self.state = "Drag"
      elif(gesture == "Victory"):
        self.lasty = posy
        self.state = "Scroll"
    elif(self.state == "Click"):
      if(gesture == "Open_Palm"):
        self.state = "Move"
      elif(gesture == "Closed_Fist"):
        pyautogui.click()
        self.state = "Clicked"
      elif(gesture == "Victory"):
        pyautogui.rightClick()
        self.state = "Clicked"
      elif(gesture == "Victory"):
        self.lasty = posy
        self.state = "Scroll"
    elif(self.state == "Clicked"):
      if(gesture == "Open_Palm"):
        self.state = "Move"
      elif(gesture == "Pointing_Up"):
        self.state = "Click"
    elif(self.state == "Drag"):
      if(gesture == "Open_Palm"):
        pyautogui.mouseUp()
        self.state = "Move"
    elif(self.state == "Scroll"):
      if(gesture == "Open_Palm"):
        self.state = "Move"
    if(self.state == "Move"):
      self.move = True
    elif(self.state == "Click" or self.state == "Clicked" or self.state == "Scroll"):
      self.move = False
    if(self.state == "Scroll"):
      c=(self.lasty - posy)*100
      pyautogui.scroll(c, _pause=False)
      if(abs(c) >=1):
        self.lasty = posy
    print("State:", self.state)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

width, height, fps = int(640), int(460), 30

base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

sm = statemachine()

center_history = []

def get_frames():
  video_capture = cv2.VideoCapture(0)
  while video_capture.isOpened():
    # Grab a single frame of video
    ret, frame = video_capture.read()

    if(ret):
      # Resize frame of video to 1/4 size for faster face recognition processing
      small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
      small_frame = cv2.flip(small_frame, 1)
      rgb_img = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

      #frame = np.zeros((height, width, 3), np.uint8)
      #frame=cv2.flip(frame, 1)

      # Process face
      mpImg=mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_img)
      recognition_result = recognizer.recognize(mpImg)

      if(len(recognition_result.gestures) == 0):
        #print('No gesture detected')
        continue

      top_gesture = recognition_result.gestures[0][0]
      hand_landmarks = recognition_result.hand_landmarks

      gestures = top_gesture
      hand_landmarks_list = hand_landmarks

      #annotated_image = image.copy()

      for hand_landmarks in hand_landmarks_list:
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
          landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])

        center = hand_landmarks_proto.landmark[5]
        print('Gesture:', gestures.category_name)
        print('Score:', gestures.score)
        print('Center:', center)

        # Rolling average for center with length 4

        center_history.append(center)
        if len(center_history) > 10:
          center_history.pop(0)
          b = np.array([[c.x, c.y, c.z] for c in center_history])
          x = np.dot(Ap,b)
          avg_center = np.dot(y,x)
          #print(avg_center)
          center.x = avg_center[0]
          center.y = avg_center[1]
          center.z = avg_center[2]

        '''weights = [2*(i+1) for i in range(len(get_frames.center_history))]
        total_weight = sum(weights)
        avg_center = landmark_pb2.NormalizedLandmark(
          x=sum(c.x * w for c, w in zip(get_frames.center_history, weights)) / total_weight,
          y=sum(c.y * w for c, w in zip(get_frames.center_history, weights)) / total_weight,
          z=sum(c.z * w for c, w in zip(get_frames.center_history, weights)) / total_weight
        )'''

        #center = avg_center

        if(gestures.score > 0.51):
          sm.update(gestures.category_name,center.y)
          if(center.x > 0.55 and center.x < 0.9 and center.y > 0.25 and center.y < 0.85 and sm.move):
            pyautogui.moveTo(translate(center.x,0.6,0.85,0,w), translate(center.y,0.3,0.8,0,h), duration=0.0, _pause=False)

  video_capture.release()
  cv2.destroyAllWindows()

#.6 .9
#.3 .8

if __name__ == '__main__':
  get_frames()
