import sys
import os

from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlApplicationEngine, QQmlEngine, QQmlPropertyMap

import soloman

app = QGuiApplication(sys.argv)


# Create a QML engine.
#register()

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)

engine.load(QUrl('example.qml'))


sys.exit(app.exec_())
