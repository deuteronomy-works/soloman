"""
Created on 18th April, 2021
"""
import os
import subprocess
import threading

import pyautogui


def show_local():
    s_thread = threading.Thread(target=_show_local)
    s_thread.daemon = True
    s_thread.start()


def _show_local():
    # call local test
    print(os.system('python local_t_est.py'))


show_local()
