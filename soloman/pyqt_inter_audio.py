# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 21:33:24 2020

@author: Ampofo
"""
from PyQt5.QtCore import pyqtProperty, QObject
from .audio import Audio

class QAudio(QObject):


    """
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.aud = Audio()
        print(self.aud)

        self._save_folder = ''

    @pyqtProperty('QString')
    def saveFolder(self):
        return self._save_folder

    @saveFolder.setter
    def saveFolder(self, folder_name):
        self._save_folder = folder_name
        self.aud.save_folder = self._save_folder
