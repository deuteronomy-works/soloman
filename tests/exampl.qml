import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3
import soloman 2.4

ApplicationWindow {
    visible: true
    width: 800
    height: 500
    title: "PyQt5 Window"

    RowLayout {
        width: parent.width
        height: parent.height

        SVideo {
            Layout.fillWidth: true
            Layout.fillHeight: true
           //width: 320
           //height: 400
           objectName: "love"
        }

        SVideo {
            Layout.fillWidth: true
            Layout.fillHeight: true
            //width: 320
            //height: 400
            objectName: "lover"
        }
    }

}
