"""
This module contains the helper functions for opencv users
so their application will loop not less than the needed time
for the various fps rates
The sleep should happen faster than the fps rate
"""
from time import sleep

def fps_24():
    """
    now set at 1/40
    """
    sleep(1/40)
    return True

def fps_30():
    """
    now set at 1/60
    """
    sleep(1/60)
    return True

def fps_60():
    """
    now set at 1/120
    """
    sleep(1/120)
    return True
