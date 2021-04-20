import os

import pytest


PREF_PATH = './tests'

def test_tests_folder():
    exist = os.path.exists(PREF_PATH)
    assert exists == True

def test_tests_videos_folder():
    ex = os.path.exists(PREF_PATH + '/videos')
    assert exists == True

def test_tests_contents():
    conts = os.listdir(PREF_PATH + '/videos')
    assert len(conts) > 0
