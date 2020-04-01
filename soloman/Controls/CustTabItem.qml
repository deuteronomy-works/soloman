import QtQuick 2.10

Rectangle {

    property int index

    anchors.fill: parent
    color: "dodgerblue"
    visible: index == parent.currentIndex
    objectName: "CustTabItem"
}
