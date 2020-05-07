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

    Image {
        anchors.centerIn: parent
        id: framebox
        asynchronous: false
        sourceSize: Qt.size(vid.width, vid.height)
        source: vid.currentFrame
    }

}
