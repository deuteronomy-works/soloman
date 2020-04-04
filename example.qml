import QtQuick 2.11
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import soloman 1.0

ApplicationWindow {
    width: 500
    height: 400
    visible: true
    title: "Hello Audio"

    RowLayout {
        Audio {
            id: aud
            saveFolder: "H:\\GitHub\\soloman\\soloman\\audio\\data\\music\\saves"

            Component.onCompleted: {
                this.play('H:\\GitHub\\soloman\\soloman\\audio\\data\\music\\f.mp3')
            }
        }

        Audio {
            id: audd
            saveFolder: "H:\\GitHub\\soloman\\soloman\\audio\\data\\music\\saves"

            Component.onCompleted: {
                this.play('H:\\GitHub\\soloman\\soloman\\audio\\data\\music\\s.mp3')
            }
        }
    }

    ColumnLayout {

    Slider {
        from: 1.01
        to: 100
        value: 1.4

        onMoved: aud.volume = value

    }

    RowLayout {

        Button {
            text: "Play"
            onClicked: aud.play('H:\\GitHub\\soloman\\soloman\\audio\\data\\music\\f.mp3');
        }

        Button {
            text: "Pause"
            onClicked: aud.pause();
        }

        Button {
            text: "Resume"
            onClicked: aud.resume();
        }

        Button {
            text: "Stop"
            onClicked: aud.stop();
        }

    }

    RowLayout {

        Button {
            text: "Play"
            onClicked: audd.play('H:\\GitHub\\soloman\\soloman\\audio\\data\\music\\s.mp3');
        }

        Button {
            text: "Pause"
            onClicked: audd.pause();
        }

        Button {
            text: "Resume"
            onClicked: audd.resume();
        }

        Button {
            text: "Stop"
            onClicked: audd.stop();
        }

    }

    Slider {
        from: 1.01
        to: 236
        value: 1.4

        onMoved: aud.seek(value)

    }

    }
}

