import QtQuick 2.0
import soloman 2.2

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
        sourceSize: Qt.size(parent.width, parent.height)
        source: vid.currentFrame


    }

}
