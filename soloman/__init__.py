# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:50:44 2020

"""
import os
from PyQt5.QtQml import qmlRegisterType

# import Audio here so people can import it without
# going int the audio package to access it
from .audio import Audio
from soloman.pyqt_inter_audio import QAudio
from soloman.pyqt_inter_video import QVideo

def register():

    directory = __file__.replace('\\soloman\\__init__.py', '')
    if 'QML2_IMPORT_PATH' in os.environ:
        os.environ['QML2_IMPORT_PATH'] += ';' + directory
    else:
        os.environ['QML2_IMPORT_PATH'] = directory

    qmlRegisterType(QAudio, 'soloman', 1, 0, 'SAudio')
    qmlRegisterType(QVideo, 'soloman', 1, 0, 'QVideo')


register()
