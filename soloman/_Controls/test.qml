import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Layouts 1.3

ApplicationWindow {
    visible: true
    width: 400
    height: 400
    color: "green"

    menuBar: TabBar {
        TabButton {
            text: "one"
            onClicked: {
                sview.currentIndex = 0
            }
        }

        TabButton {
            text: "two"

            onClicked: {
                sview.currentIndex = 1
            }

        }

        TabButton {
            text: "three"

            onClicked: {
                sview.currentIndex = 2
            }

        }

    }

    STabView {
        id: sview

        color: "green"

        STab { color: "brown"}

        Component.onCompleted: { console.log(this.addChild("TestComp.qml"))}

    }

}


