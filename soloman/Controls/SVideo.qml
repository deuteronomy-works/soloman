import QtQuick 2.0
import soloman 2.2

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
