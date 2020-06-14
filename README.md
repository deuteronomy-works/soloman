# soloman
For the love of python and qml

## Installation
    pip install soloman

## Usage for python

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

```qml
import QtQuick 2.14
...
import soloman 2.1

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

```qml
import QtQuick 2.14
...
import soloman 2.1

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





## Wiki

The wiki can be located [here](https://github.com/deuteronomy-works/soloman/wiki)
