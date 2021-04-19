"""
Created on 18th April, 2021
"""
import os
import subprocess
import threading
from time import sleep

import pyautogui


WIDTH = 800
HEIGHT = 600

def show_local():
    s_thread = threading.Thread(target=_show_local)
    s_thread.daemon = True
    s_thread.start()


def _show_local():
    # call local test
    print(os.system('python local_t_est.py'))


def auto_gui():
    auto_thread = threading.Thread(target=_auto_gui)
    auto_thread.daemon = True
    auto_thread.start()


def _auto_gui():
    print('dsdf')
    s_width, s_height = pyautogui.size()
    print(s_width, s_height, pyautogui)


show_local()
auto_gui()

sleep(10)