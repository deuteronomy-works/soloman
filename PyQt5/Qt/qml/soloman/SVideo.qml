import QtQuick 2.0
import soloman 2.4

QVideo {
    id: vid

    implicitWidth: 640
    implicitHeight: 360
    aspectRatio: true

    onFrameUpdate: {
        framebox.source = vid.currentFrame
    }

    Image {
        anchors.centerIn: parent
        id: framebox
        asynchronous: false
        sourceSize: Qt.size(vid.width, vid.height)
        source: vid.currentFrame
        anchors.fill: vid
        fillMode: aspectRatio ? Image.PreserveAspectFit : Image.Stretch

    }

}
