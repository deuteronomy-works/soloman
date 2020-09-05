import QtQuick 2.10

Rectangle {
    id: basev
    anchors.fill: parent

    property int currentIndex: 0
    property QtObject currentItem: this.children.length === currentIndex ? this.children[currentIndex] : QtObject
    property int count: 0

    function addChild(ur_l) {
        var mComp = Qt.createQmlObject('import QtQuick 2.10; Rectangle {property int index:' + basev.count +';anchors.fill: parent;color: "transparent";visible: index == parent.currentIndex;}', basev)
        basev.count += 1
        var comp = Qt.createComponent(ur_l)
        var obj = comp.createObject(mComp)
        return true;
    }

    Component.onCompleted: {
        var child = this.children
        var lent = child.length
        if(lent > 0) {
            for(var i=0; i<lent; i++) {
                this.children[i].index = i
                count++
            }
        }
    }

}
