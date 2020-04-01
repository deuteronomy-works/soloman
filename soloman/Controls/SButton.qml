import QtQuick 2.10
import QtQuick.Controls 2.3
import QtQuick.Controls.impl 2.3
import "../Properties" as Prop

Button {
    id: ctrl

    Prop.Colors { id: colors }

    property QtObject bgcolor: QtObject {
        property color primary: colors.btn_default
        property color hover: colors.btn_default
        property color click: colors.btn_click
    }
    property QtObject one: bgcolor

    property QtObject color: QtObject {
        property color primary: "black"
        property color hover: "black"
        property color click: "black"
    }
    property color icon_label_color
    property int radius: 0

    contentItem: IconLabel {
        spacing: ctrl.spacing
        mirrored: ctrl.mirrored
        display: ctrl.display

        icon: ctrl.icon
        text: ctrl.text
        font: ctrl.font
        color: icon_label_color
    }

    background: Rectangle {
        id: nos
        implicitWidth: 100
        implicitHeight: 40
        color: if(ctrl.down) {icon_label_color = ctrl.color.click; bgcolor.click }
               else if( ctrl.hovered) {icon_label_color = ctrl.color.hover;  bgcolor.hover}
               else {icon_label_color = ctrl.color.primary; bgcolor.primary}
        radius: ctrl.radius
    }

}
