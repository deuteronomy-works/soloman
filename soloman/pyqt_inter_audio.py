# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 21:33:24 2020

@author: Ampofo
"""
import threading
from PyQt5.QtCore import pyqtProperty, QObject, pyqtSlot
from .audio import Audio

class QAudio(QObject):


    """
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.aud = Audio()
        print(self.aud)

        self._save_folder = ''
        self._volume_level = 1.4

    def _delay_play(self, u_delay):
        pass

    def _pause(self):
        pass

    def _play(self, filename):
        self.aud.play(filename)

    def _prepare(self, filename):
        pass

    def _resume(self):
        pass

    def _seek(self, seconds):
        pass

    def _stop(self):
        pass

    def _t_played(self):
        pass

    @pyqtSlot(int)
    def delay_play(self, u_delay):
        pass

    @pyqtSlot()
    def pause(self):
        pass

    @pyqtSlot(str)
    def play(self, filename):
        play_thread = threading.Thread(target=self._play, args=[filename])
        play_thread.daemon = True
        play_thread.start()

    @pyqtSlot(str)
    def prepare(self, filename):
        pass

    @pyqtSlot()
    def resume(self):
        pass

    @pyqtProperty('QString')
    def saveFolder(self):
        return self._save_folder

    @saveFolder.setter
    def saveFolder(self, folder_name):
        self._save_folder = folder_name
        self.aud.save_folder = self._save_folder

    @pyqtSlot(int)
    def seek(self, seconds):
        pass

    @pyqtSlot()
    def stop(self):
        pass

    @pyqtSlot()
    def t_played(self):
        pass

    @pyqtProperty(int)
    def volume(self):
        return self._volume_level

    @volume.setter
    def volume(self, level):
        self._volume_level = level
        self.aud.controlVolume(self._volume_level)
