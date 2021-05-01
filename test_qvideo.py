"""
Test file for QVideo class
"""
import os

from soloman import QVideo
from soloman.misc import Paths

def test_default_fps():
    """
    Test if fps can be set and used globally
    """
    q_vid = QVideo()
    assert q_vid.fps == 29.97

def test_temp_folder():
    """
    Temp folders are huge.
    There is a code that deletes the temp folder on start and
    creates a new temp folder
    This test is to check if we have a new temp folder
    """
    QVideo()
    temp_f = Paths().temp
    expected_tmp = os.path.join(temp_f, 'soloman', 'convert')
    if os.path.exists(expected_tmp):
        if 'temp' in os.listdir(expected_tmp)[0]:
            assert True

def test_user_fps():
    """
    Test User specified fps
    """
    q_vid = QVideo(frames_per=30)
    assert q_vid.fps == 30

    q_vid.fps = 24
    assert q_vid.fps == 24
