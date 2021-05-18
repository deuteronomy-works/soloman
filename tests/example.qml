import QtQuick 2.11
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import soloman 3.0
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

            onClicked: vv.play("./ex/jpgs")
        }

        Button {
            text: "pause"

            onClicked: {vv.pause()}
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
        anchors.bottom: btm.top

        Slider {
            id: slid
            width: 800
            from: 1
            to: 100

            onMoved: {
                vv.seek(slid.value)
                console.log(slid.value)
            }
        }

    }

    Row {
        id: btm
        anchors.bottom: parent.bottom
        Text {
            text: "Audio"
        }
        Button {
            text: "play"

            onClicked: aud.play('H:/GitHub/pyffmpeg/_test/asem.mp3')
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

