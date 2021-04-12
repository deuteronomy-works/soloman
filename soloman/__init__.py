# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 2020 12:50:44

"""
import os
from time import sleep

from PyQt5.QtQml import qmlRegisterType

# import Audio and Video here so people can import it without
# going into the audio and video packages to access them
from .audio import Audio
from .video import Video
from soloman.pyqt_inter_audio import QAudio
from soloman.pyqt_inter_video import QVideo
from soloman.fps_clocks import *


def register():

    # Delete the contents of our Temp folder
    path = os.path.join(os.environ['TEMP'], 'soloman', 'converts')
    if os.path.exists(path):
        os.system('RD "' + path + '" /S /Q')

    qmlRegisterType(QAudio, 'soloman', 2, 5, 'SAudio')
    qmlRegisterType(QVideo, 'soloman', 2, 5, 'QVideo')


register()
