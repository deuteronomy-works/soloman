import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtGraphicalEffects 1.12

Pane {
    id: ctrl

    property int radius: 4
    property int elevation
    property QtObject backgroundImage

    background: Rectangle {
        id: imp_rect
        color: Material.background
        radius: ctrl.radius

        layer.enabled: true
        layer.effect: DropShadow {
            id: dd

            property int elevation: ctrl.elevation ? ctrl.elevation : ctrl.Material.elevation
            property int rad: (elevation * 2) + 2

            horizontalOffset: 0
            verticalOffset: Math.round(elevation / 2)
            radius: rad
            samples: (rad * 2) + 1
            color: Qt.rgba(0, 0, 0, 0.35)
            source: imp_rect
        }

        Image {
            id: bg_img
            sourceSize: Qt.size(ctrl.width, ctrl.height)
            source: "background.jpg"
            clip: true
        }

        Component.onCompleted: {
            ctrl.backgroundImage = bg_img
            console.log(ctrl.backgroundImage.width)
        }

    }

}


