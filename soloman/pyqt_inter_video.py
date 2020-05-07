# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 07:52:16 2020

@author: Ampofo
"""
import os
import threading
from time import sleep
from PyQt5.QtCore import pyqtProperty, pyqtSlot, pyqtSignal
from PyQt5.QtQuick import QQuickItem


class QVideo(QQuickItem):

    """
    """


    def __init__(self, parent=None):
        super().__init__(parent)
        # Video
        self._source = ''
        self.folder = "H:/GitHub/soloman/ex/"
        self._current_frame = 'file:///H:/GitHub/soloman/ex/vid_lv_001.jpg'
        self._fps = 24
        # controls
        self._stopped = False
        self._paused = False

    frameUpdate = pyqtSignal(str, arguments=['updateFrame'])

    @pyqtSlot()
    def updater(self):
        u_thread = threading.Thread(target = self._updater)
        u_thread.daemon = True
        u_thread.start()

    def _updater(self):

        conts = os.listdir(self.folder)
        final = conts[3:]
        # Use no to evaluate
        no = 0

        # Avoid multiple playing instances
        self._stopped = True
        sleep(.3)
        # if user has called the stop function
        # we will need to reset it in order to restart play
        self._stopped = False

        while not self._stopped and no != len(final):
            if not self._paused:
                self._current_frame = 'file:///' + self.folder + '/' + final[no]
                self.updateFrame('')
                # update no
                no += 1
                sleep(1/24)
            else:
                sleep(1/10)
        # stop showing the last frame
        self._current_frame = ''
        self.updateFrame('')

    @pyqtProperty('QString')
    def currentFrame(self):
        return self._current_frame

    @currentFrame.setter
    def currentFrame(self, frame):
        self._current_frame = frame

    @pyqtProperty('int')
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps):
        self._fps = fps

    @pyqtSlot()
    def pause(self):
        u_thread = threading.Thread(target = self._pause)
        u_thread.daemon = True
        u_thread.start()
    
    def _pause(self):
        self._paused = True

    @pyqtSlot()
    def resume(self):
        u_thread = threading.Thread(target = self._resume)
        u_thread.daemon = True
        u_thread.start()
    
    def _resume(self):
        self._paused = False

    @pyqtSlot()
    def play(self):
        u_thread = threading.Thread(target = self._play)
        u_thread.daemon = True
        u_thread.start()

    def _play(self):
        # play video
        self.updater()

    @pyqtProperty('QString')
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @pyqtSlot()
    def stop(self):
        u_thread = threading.Thread(target = self._stop)
        u_thread.daemon = True
        u_thread.start()
    
    def _stop(self):
        self._stopped = True

    def updateFrame(self, frame):
        self.frameUpdate.emit(frame)

