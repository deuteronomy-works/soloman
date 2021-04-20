import sys
import os

class Paths:

    def __init__(self):
        self.temp = ''

        # call the functions
        self.set_temp_folder()

    def set_temp_folder(self):
        # OS Temp folder
        if sys.platform.startswith('linux'):
            self.temp = os.environ['XDG_RUNTIME_DIR']
        elif sys.platform in ('win32', 'cygwin'):
            self.temp = os.environ['TEMP']
        else:
            tmps = (
                os.environ['TMPDIR'],
                os.environ['tmpdir'],
                os.environ['TEMP'],
                os.environ['XDG_RUNTIME_DIR'])

            for x in tmps:
                if os.path.exists(x):
                    self.temp = x
                    break
