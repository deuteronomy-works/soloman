import QtQuick 2.10

Rectangle {

    property int index

    anchors.fill: parent
    color: "transparent"
    visible: index === parent.currentIndex
    objectName: "CustTabItem"

}
