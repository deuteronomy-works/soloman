import os

import pytest

def test_tests_folder():
    pref_path = './tests'
    ex = os.path.exists(pref_path)
    assert ex == True
