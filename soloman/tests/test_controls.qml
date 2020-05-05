import QtQuick 2.12
import QtQuick.Controls 2.12
import "../Controls" as Swift

Rectangle {
    width: 400
    height: 800

    Swift.SButton {
        id: sb
        text: "Click me"
        bgcc.primary: "red"
    }

    Button {
        anchors.left: sb.right
        text: "Click me"
    }

    Button {
        anchors.top: sb.bottom
        text: "Click me"
    }

}
