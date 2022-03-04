# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 2020 12:50:44

"""
import os
import shutil

from qtpy.QtQml import qmlRegisterType

# import Audio and Video here so people can import it without
# going into the audio and video packages to access them
from .audio import Audio
from .video import Video
from soloman.pyqt_inter_audio import QAudio
from soloman.pyqt_inter_video import QVideo
from soloman.fps_clocks import *
from soloman.misc import Paths


def register():

    # Delete the contents of our Temp folder
    temp = Paths().temp
    path = os.path.join(temp, 'soloman', 'convert')
    path2 = os.path.join(temp, 'soloman', 'converts')
    if os.path.exists(path):
        # os.system('RD "' + path + '" /S /Q') // windows code
        shutil.rmtree(path)
    # I broke my path system. Keep backward compactibility
    elif os.path.exists(path2):
        shutil.rmtree(path2)

    qmlRegisterType(QAudio, 'soloman', 3, 0, 'SAudio')
    qmlRegisterType(QVideo, 'soloman', 3, 0, 'QVideo')


register()
