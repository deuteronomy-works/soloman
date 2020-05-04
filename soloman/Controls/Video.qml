import QtQuick 2.0
import soloman 1.0

QVideo {
    id: vid
    anchors.centerIn: parent
    width: 600
    height: 400

    onChangeTimerStatus: {
        var status = timerStatus
        timer.running = status
    }


    Timer {
        id: timer
        interval: 1000/24; running: false; repeat: true;
        onTriggered: {
            framebox.source = vid.currentFrame
        }
    }

    Rectangle {
        width: framebox.width
        height: framebox.height
        color: "black"

        Image {
            id: framebox
            asynchronous: false
            sourceSize: Qt.size(vid.width, vid.height)
            source: vid.currentFrame
        }

    }

}
