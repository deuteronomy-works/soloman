# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:50:44 2020

"""

from PyQt5.QtQml import qmlRegisterType

from .audio import Audio
from soloman.pyqt_inter_audio import QAudio

def register():
    qmlRegisterType(QAudio, 'soloman', 1, 0, 'Audio')
