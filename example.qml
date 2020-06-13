import QtQuick 2.11
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import soloman 1.0
//import soloman.Controls 1.0

ApplicationWindow {
    width: 800
    height: 500
    visible: true
    title: "Hello Audio"

    Text {
        anchors.fill: vv
        text: vv.frame
    }

    Video {
        id: vv

    }

    Audio {
        id: aud
    }

    Row {
        anchors.top: parent.top
        Button {
            text: "play"

            onClicked: vv.play()
        }

        Button {
            text: "pause"

            onClicked: {vv.pause()}
        }

        Button {
            text: "seek"

            onClicked: {vv.seek(12)}
        }

        Button {
            text: "resume"

            onClicked: vv.resume()
        }

        Button {
            text: "stop"

            onClicked: vv.stop()
        }

    }

    Row {
        anchors.bottom: parent.bottom
        Button {
            text: "play"

            onClicked: aud.play('H:/GitHub/soloman/soloman/audio/data/music/saves/s.wav')
        }

        Button {
            text: "pause"

            onClicked: {aud.pause()}
        }

        Button {
            text: "seek"

            onClicked: {aud.seek(12)}
        }

        Button {
            text: "resume"

            onClicked: aud.resume()
        }

        Button {
            text: "stop"

            onClicked: aud.stop()
        }

    }

}

