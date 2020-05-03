# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 07:52:16 2020

@author: Ampofo
"""
import os
import threading
from time import sleep
from PyQt5.QtCore import pyqtProperty, QUrl, pyqtSlot
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtQml import QQmlEngine, QQmlComponent, QQmlContext, QQmlPropertyMap, QQmlProperty

class QVideo(QQuickItem):

    """
    """


    def __init__(self, parent=None):
        super().__init__(parent)
        self._source = ''
        self.folder = "H:/GitHub/soloman/ex/"
        self._current_frame = 'file:///H:/GitHub/soloman/ex/vid_lv_014.jpg'

    @pyqtSlot()
    def updater(self):
        u_thread = threading.Thread(target = self._updater)
        u_thread.daemon = True
        u_thread.start()

    def _updater(self):
        sleep(2)
        conts = os.listdir(self.folder)

        print(self.currentFrame)
        for each in conts[3:]:
            self._current_frame = 'file:///' + self.folder + '/' + each
            sleep(1/24)

    @pyqtProperty('QString')
    def currentFrame(self):
        return self._current_frame

    @currentFrame.setter
    def currentFrame(self, frame):
        self._current_frame = frame

    @pyqtProperty('QString')
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source




