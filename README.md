# soloman    [![Downloads](https://pepy.tech/badge/soloman/month)](https://pepy.tech/project/soloman)
For the love of Artificial Intelligence, Python and QML


[refer to milestone](https://github.com/deuteronomy-works/soloman/milestone/12)



## Installation
    pip install soloman



## Python Usage



### Play audio
```python
from soloman import Audio


aud = Audio()
aud.play('/path/to/music.mp3')
```

## Qml Usage
example.py
```python
import soloman
...
engine = QQmlApplicationEngine()
...
engine.load('example.qml')

```

### Play audio
*example.qml*


**Qt6**
```qml
import QtQuick
...
import soloman

SAudio {
    id: aud
}

Button {
    text: "Play"
    onClicked: aud.play('path/to/music.mp3')
}

```


**Qt5**
```qml
import QtQuick 2.15
...
import soloman 3.0

SAudio {
    id: aud
}

Button {
    text: "Play"
    onClicked: aud.play('path/to/music.mp3')
}

```

### Play videos
*example.qml*

#### Play a video file

**Qt6**

```qml
import QtQuick
...
import soloman

SVideo {
    id: vid
}

Button {
    text: "Play video"
    onClicked: vid.play('path/to/video.mp4')
}
```

**Qt5**

```qml
import QtQuick 2.15
...
import soloman 3.0

SVideo {
    id: vid
}

Button {
    text: "Play video"
    onClicked: vid.play('path/to/video.mp4')
}
```

### Play stills

##### Option one

```qml
...
    onClicked: vid.play('path/to/video_stills_01.jpg') # possibly the first image
...
```

##### Option two

```qml
...
    onClicked: vid.play('path/to/') # make sure folder contains only stills
...
```




### Show cv2 frame

example.py

```python
import sys
import cv2
import threading
from time import sleep

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml QQmlApplicationEngine
import soloman

app = QGuiApplication(sys.argv)

# Create a QML engine.
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load(QUrl('example.qml'))

# Get SVideo
vid = soloman.Video(engine)
vid.get_SVideo('screen_01')  # objectName goes here

# Capture
capture = cv2.VideoCapture(0)  # capture camera

def start_capt():
    # start thread
    o_thread = threading.Thread(target=_start_capt)
    o_thread.daemon = True
    o_thread.start()

def _start_capt():

    while True:

        ret, frame = capture.read()

        if not ret:
            break

        vid.show_frame(frame)
        sleep(1/24)

# Call to start capturing
start_capt()

# Run the app
ret_value = app.exec_()
capture.release()
sys.exit(0)
```

example.qml

**Qt6**

```qml
import QtQuick
import QtQuick.Controls.Basic
import solomon

ApplicationWindow {
	visible: true
	width: 800
	height: 500

    SVideo {
        objectName: "screen_01"  // declare objectName to be used in python
    }
    
}
```

**Qt5**

```qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import solomon 3.0

ApplicationWindow {
	visible: true
	width: 800
	height: 500

    SVideo {
        objectName: "screen_01"  // declare objectName to be used in python
    }
    
}
```





## Wiki

The wiki can be located [here](https://github.com/deuteronomy-works/soloman/wiki)
