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
    sleep(3)
    s_width, s_height = pyautogui.size()
    x = (s_width - WIDTH) / 2
    # This y calculation successfully
    # takes us to the bottom of the title bar
    y = (s_height - HEIGHT) / 2
    x_mov = 78 + x # center of the button
    y_mov = 20 + y # center of the button
    pyautogui.moveTo(x_mov, y_mov)

    # click the button
    pyautogui.click()

    print(pyautogui.position())
    sleep(3)


show_local()
auto_gui()

sleep(10)