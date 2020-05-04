import QtQuick 2.0
import soloman 1.0

QVideo {
    id: vid
    anchors.centerIn: parent
    width: 600
    height: 400

    onFrameUpdate: {
        framebox.source = vid.currentFrame
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
