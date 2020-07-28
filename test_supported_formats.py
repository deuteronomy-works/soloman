"""
Test for supported formats
"""
import os
import pytest
from soloman import QVideo

EXAMPLE_PATH = os.path.join(os.path.dirname(__file__), 'tests', 'videos')

@pytest.mark.parametrize('file_name', [
    (str(os.path.join(EXAMPLE_PATH, 'countdown.mp4')))
    ])
def test_supported_formats(file_name):
    """
    The main function to test the supported formats
    """

    q_vid = QVideo()
    q_vid.convert_to_stills(file_name)

    # check number of files
    count = len(os.listdir(q_vid.folder))

    # Delete the contents before assert
    os.system('RD "' + q_vid.folder + '" /S /Q')

    assert count != 0
