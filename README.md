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
from soloman import register
...
engine = QQmlApplicationEngine()
...
register()
engine.load('example.qml')

```

```qml
import QtQuick 2.10
...
import soloman

Audio {
    id: aud
}

Button {
    text: "Play"
    onClicked: aud.play('path/to/music.mp3')
}

```

## Wiki
The wiki can be located [here](https://github.com/deuteronomy-works/soloman/wiki)
