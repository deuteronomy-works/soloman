"""
Created on 18th April, 2021
"""
import subprocess
import threading
from time import sleep

import pytest
import pyautogui


WIDTH = 800
HEIGHT = 600

class show:


    def __init__(self):
        self.subP = ()
        self.info = ''
        self.subP = subprocess.Popen(
            'python local_t_est.py',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False)

    def get_status(self):
        s_thread = threading.Thread(target=self._get_status)
        s_thread.daemon = True
        s_thread.start()

    def _get_status(self):

        a = self.subP.stderr.readline()
        self.info = str(a.strip(), 'utf-8')


def test_auto_gui():
    ss = show()
    ss.get_status()
    sleep(2)
    # wait till UI is showing
    while ss.info != 'qml: window loaded':
        print('UI not ready. Sleeping for 1 second')
        sleep(1)

    print('UI is ready')
    # UI is ready lets contine
    s_width, s_height = pyautogui.size()
    x = (s_width - WIDTH) / 2
    # This y calculation successfully
    # takes us to the bottom of the title bar
    y = (s_height - HEIGHT) / 2
    x_mov = 78 + x # center of the button
    y_mov = 20 + y # center of the button
    pyautogui.moveTo(x_mov, y_mov)

    # click the play button
    pyautogui.click()

    # Pixel Match
    pixel_match = False
    while not pixel_match:
        print('Pixel not ready sleep 7 seconds and repeat')
        sleep(7)
        ux = int(250+x)
        uy = int(250+y)
        pixel_match = pyautogui.pixelMatchesColor(ux, uy, (0, 0, 0))

    print('Pixel Matched successfully')
    # close out
    x_end = x + WIDTH - 25
    y_end = y - 20
    pyautogui.moveTo(x_end, y_end)
    sleep(5)
    # close
    pyautogui.click()
    print('closed')

    assert pixel_match == True

