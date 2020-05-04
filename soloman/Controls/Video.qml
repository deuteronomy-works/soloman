import QtQuick 2.0
import soloman 1.0

QVideo {
    id: vid
    anchors.centerIn: parent
    width: 600
    height: 400



    Timer {
        interval: 500; running: true; repeat: true;
        onTriggered: {
            framebox.source = vid.currentFrame
        }
    }

    Rectangle {
        anchors.fill: parent
        color: "black"

        Image {
            id: framebox
            asynchronous: false
            sourceSize: Qt.size(parent.width, parent.height)
            source: vid.currentFrame
        }

    }

}
