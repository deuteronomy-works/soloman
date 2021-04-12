import QtQuick 2.0
import soloman 2.5

QVideo {
    id: vid

    implicitWidth: 640
    implicitHeight: 360

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
        fillMode: vid.aspectRatio | vid.tile ? Image.PreserveAspectFit | vid.tileEnumeration : vid.aspectRatio ? Image.PreserveAspectFit : vid.tile ? tileEnumeration : Image.Stretch
    }

}
