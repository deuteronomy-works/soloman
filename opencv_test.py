# -*- coding: utf-8 -*-
import sys
import cv2
import numpy as np
import threading
from time import sleep
import os

from PyQt5.QtCore import QUrl, QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlApplicationEngine, QQmlEngine, QQmlPropertyMap

import soloman

app = QGuiApplication(sys.argv)


# Create a QML engine.
#register()

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)

engine.load(QUrl('tests/example.qml'))




sol = soloman.Video(engine)
sol.get_QVideo('lover')

# Capture
source = "ex/vid.mp4"
capture = cv2.VideoCapture(source)

fgbg = cv2.createBackgroundSubtractorMOG2(50, 200, True)



def ok():
    o_thread = threading.Thread(target=_ok)
    o_thread.daemon = True
    o_thread.start()

def _ok():

    frameCount = 0

    while True:

        ret, frame = capture.read()

        frameCount += 1

        if not ret:
            break

        #resized = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

        #mask = fgbg.apply(resized)
        """cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == 27:
            break"""
        sol.update(frame)
        sleep(1/100)

ok()


app.exec_()
capture.release()
cv2.destroyAllWindows()
sys.exit(0)
