import QtQuick 2.10
import QtQuick.Controls 2.3

ApplicationWindow {
    visible: true
    width: 1024
    height: 700

    menuBar: TabBar {
        TabButton {
            text: "one"
            onClicked: {
                basev.currentIndex = 0
            }
        }

        TabButton {
            text: "two"

            onClicked: {
                basev.currentIndex = 1
                basev.currentItem.color = "red"
            }

        }

        TabButton {
            text: "three"

            onClicked: {
                basev.currentIndex = 2
            }

        }

    }


    Rectangle {
        id: basev
        anchors.fill: parent

        signal addChild(url ur_l)

        onAddChild: {
            var mComp = Qt.createQmlObject('import QtQuick 2.10; Rectangle {property int index:' + basev.count +';anchors.fill: parent;color: "green";visible: index == parent.currentIndex;}', basev)
            basev.count += 1
            var comp = Qt.createComponent(ur_l)
            var obj = comp.createObject(mComp)
        }

        property int currentIndex: 0
        property QtObject currentItem: this.children[currentIndex]
        property int count: 0

        Component.onCompleted: {
            var child = this.children
            var lent = child.length
            if(lent > 0) {
                for(var i=0; i<lent; i++) {
                    print(this.children[i].objectName)
                    this.children[i].index = i
                    count++
                }
            }

            addChild("TestComp.qml")
            addChild("TestComp.qml")
        }

        CustTabItem {}

        /*Rectangle {

            property int index

            anchors.fill: parent
            color: "gold"
            visible: index == parent.currentIndex
        }

        Rectangle {

            property int index

            anchors.fill: parent
            visible: index == parent.currentIndex
        }*/

    }


}
