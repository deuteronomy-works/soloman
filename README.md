# soloman
For the love of python and qml

## Installation
    pip install soloman

## Usage
```python
from soloman import Audio


aud = Audio()
aud.play('/path/to/music.mp3')
```

## Usage for Qml
```python
import soloman
...
engine = QQmlApplicationEngine()
...
engine.load('example.qml')

```

```qml
import QtQuick 2.10
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

## Wiki
The wiki can be located [here](https://github.com/deuteronomy-works/soloman/wiki)
