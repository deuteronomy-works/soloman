# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 21:33:24 2020

@author: Ampofo
"""
import threading
from PyQt5.QtCore import pyqtProperty, QObject, pyqtSlot, Qt, QRect, QRectF
from PyQt5.QtQuick import QQuickPaintedItem, QQuickItem
from PyQt5.QtGui import QPainter, QFont, QImage, QColor, QPixmap, QPicture
from .audio import Audio


class QVideo(QQuickPaintedItem):

    """
    """


    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot()
    def paint(self, painter):
        img = QImage()
        img.load('./img.jpg')
        size = img.size()
        target = QRectF(0, 0, self.width(), self.height())
        source = QRectF(0, 0, size.width(), size.height())
        painter.drawImage(target, img, source)

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
        self.aud.delay_play(u_delay)

    def _pause(self):
        self.aud.pause()

    def _play(self, filename):
        self.aud.play(filename)

    def _prepare(self, filename):
        self.aud.prepare(filename)

    def _resume(self):
        self.aud.resume()

    def _seek(self, seconds):
        self.aud.seek(seconds)

    def _stop(self):
        self.aud.stop()

    def _t_played(self):
        self.aud.t_played()

    @pyqtSlot(int)
    def delay_play(self, u_delay):
        delay_thread = threading.Thread(target=self._delay_play, args=[u_delay])
        delay_thread.daemon = True
        delay_thread.start()

    @pyqtSlot()
    def pause(self):
        pause_thread = threading.Thread(target=self._pause)
        pause_thread.daemon = True
        pause_thread.start()

    @pyqtSlot(str)
    def play(self, filename):
        play_thread = threading.Thread(target=self._play, args=[filename])
        play_thread.daemon = True
        play_thread.start()

    @pyqtSlot(str)
    def prepare(self, filename):
        prepare_thread = threading.Thread(target=self._prepare, args=[filename])
        prepare_thread.daemon = True
        prepare_thread.start()

    @pyqtSlot()
    def resume(self):
        resume_thread = threading.Thread(target=self._resume)
        resume_thread.daemon = True
        resume_thread.start()

    @pyqtProperty('QString')
    def saveFolder(self):
        return self._save_folder

    @saveFolder.setter
    def saveFolder(self, folder_name):
        self._save_folder = folder_name
        self.aud.save_folder = self._save_folder

    @pyqtSlot(int)
    def seek(self, seconds):
        seek_thread = threading.Thread(target=self._seek, args=[seconds])
        seek_thread.daemon = True
        seek_thread.start()

    @pyqtSlot()
    def stop(self):
        stop_thread = threading.Thread(target=self._stop)
        stop_thread.daemon = True
        stop_thread.start()

    @pyqtSlot()
    def t_played(self):
        t_thread = threading.Thread(target=self._t_played)
        t_thread.daemon = True
        t_thread.start()

    @pyqtProperty(int)
    def volume(self):
        return self._volume_level

    @volume.setter
    def volume(self, level):
        self._volume_level = level
        print('level: ', level)
        self.aud.controlVolume(self._volume_level)
