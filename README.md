# gCon

gCon is a simple gesture control application, replacing the mouse input with hand tracking. 

The project uses the locally running Google Mediapipe API.

## Installation

1. After downloading the files from GitHub, unpack them to the directory wou want gCon to recide in.
2. In that directry, run the *setup.sh* installation script. This will create a python venv, install all dependancies and download the hand tracking model. It also creates a desktop shortcut.
   
## Useage

1. Make shure, no other program is using your camera.
2. Using either the *assistant.sh* file or the desktop shortcut, start the application.
3. When waving your open hand infront of the camera, you should notice the cursor following.

### Gestures

* The Base gesture is the open hand.
* Left click:
  * Point upwards with your index finger, then transition into a fist
  * For a double click, return to pointing upwards and make a fist again.
* Right click:
  * Point upwards with your index finger, then transition to the "victory" symbol
* Draging
  * Form a fist, keep this gesture while moving your hand.
* Scrolling
  * Make the "victory" symbol and move your hand up or down. You can transition into a fist.
* All mouse actions are ended by returning to the open hand.

### Limitations

* gCon blocks the camera, other applications can not access it while gCon is running
* gCon only works, when the hand is illuminated.
* gCon is currently only tested for Ubuntu.

## ToDo

* Make hand-screen mapping changeable