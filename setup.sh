#!/usr/bin/env bash

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

if [ ! -f "gesture_recognizer.task" ]; then
    wget -q https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task
fi

echo "[Desktop Entry]
Type=Application
Terminal=true
Name=gCon
Icon="$PWD"/icon.png
Exec="$PWD"/gcon.sh" > ~/Desktop/NOVA.desktop

echo "[Desktop Entry]
Type=Application
Terminal=true
Name=gCon
Icon="$PWD"/icon.png
Exec="$PWD"/gcon.sh" > ~/.local/share/applications/NOVA.desktop

echo "#!/usr/bin/env bash

cd "$PWD"
source ./venv/bin/activate
python3 ./gesture-control.py" > ./assistant.sh

chmod +x ./assistant.sh

echo "gCon is installed and ready to launch."