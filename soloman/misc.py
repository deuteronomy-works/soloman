import sys
import os


class Paths:

    def __init__(self):
        self.temp = ''

        # call the functions
        self._set_temp_folder()

    def _set_temp_folder(self):
        # OS Temp folder
        if sys.platform in ('win32', 'cygwin'):
            self.temp = os.environ['USERPROFILE']
        else:
            self.temp = os.environ['HOME']
