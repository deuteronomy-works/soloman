"""
Test file for QVideo class
"""

from soloman import QVideo


def test_default_fps():
    """
    Test if fps can be set and used globally
    """
    q_vid = QVideo()
    assert q_vid.fps == 29.97

def test_user_fps():
    """
    Test User specified fps
    """
    q_vid = QVideo(frames_per=30)
    assert q_vid.fps == 30

    q_vid.fps = 24
    assert q_vid.fps == 24
