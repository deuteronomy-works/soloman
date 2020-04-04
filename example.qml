import QtQuick 2.11
import QtQuick.Controls 2.3
import soloman 1.0

ApplicationWindow {
    width: 500
    height: 400
    visible: true
    title: "Hello Audio"

    Audio {
        id: aud
        saveFolder: "H:\\GitHub\\soloman\\soloman\\audio\\data\\music\\saves"

        Component.onCompleted: {
            this.play('H:\\GitHub\\soloman\\soloman\\audio\\data\\music\\f.mp3')
        }
    }

    Slider {
        from: 1.01
        to: 100
        value: 1.4

        onMoved: aud.volume = value

    }
}

