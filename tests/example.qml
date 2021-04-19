import QtQuick 2.11
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import soloman 2.5
//import soloman.Controls 1.0

ApplicationWindow {
    width: 800
    height: 600
    visible: true
    title: "Hello Audio"

    Rectangle {
        anchors.centerIn: parent
        width: 400
        height: 400
        border.color: "black"

        SVideo {
            id: vv
            objectName: "lover"
            anchors.fill: parent

        }
    }

    SAudio {
        id: aud
    }

    Row {
        anchors.top: parent.top
        Text {
            id: tt
            text: "Video"
        }
        Button {
            text: "play"

            onClicked: vv.play("H:/GitHub/soloman/ex/countdown640.mp4")
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
        Text {
            text: "Audio"
        }
        Button {
            text: "play"

            onClicked: aud.play('H:/GitHub/soloman/ex/vid.wav')
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

    Component.onCompleted: {
        print('window loaded')
    }

}

