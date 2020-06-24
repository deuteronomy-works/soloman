# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:50:44 2020

"""
import os
from time import sleep
from PyQt5.QtQml import qmlRegisterType

# import Audio here so people can import it without
# going int the audio package to access it
from .audio import Audio
from .video import Video
from soloman.pyqt_inter_audio import QAudio
from soloman.pyqt_inter_video import QVideo

def FPS_24():
    sleep(1/40)
    return True

def register():

    directory = __file__.replace('\\soloman\\__init__.py', '')
    if 'QML2_IMPORT_PATH' in os.environ:
        os.environ['QML2_IMPORT_PATH'] += ';' + directory
    else:
        os.environ['QML2_IMPORT_PATH'] = directory

    # Delete the contents of our Temp folder
    path = os.path.join(os.environ['TEMP'], 'soloman', 'converts')
    if os.path.exists(path):
        os.system('RD "' + path + '" /S /Q')

    qmlRegisterType(QAudio, 'soloman', 2, 2, 'SAudio')
    qmlRegisterType(QVideo, 'soloman', 2, 2, 'QVideo')


register()
