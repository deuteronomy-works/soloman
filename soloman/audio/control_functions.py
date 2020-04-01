

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:41:43 2020

@author: Ampofo
"""
import os
from time import sleep, time
import threading
import wave
import numpy as np
import struct
import pyaudio
from ffmpeg import Ffmpeg

class Controls:


    """
    """


    def __init__(self):
        self.file = ''
        self.file_size = 0
        self.app_running = True
        self._not_paused = True
        self._not_stopped = False
        self.t_size = 0
        self.tt_played = 0
        self.volume_val = 1.4
        self.ff = Ffmpeg()

    def play(self, file, fFormat, size):

        """
        """

        self._not_stopped = False
        sleep(2)
        self.file = file
        self.file_size = int(size)
        play_thread = threading.Thread(target=self._play, args=[fFormat])
        play_thread.start()

    def _play(self, fFormat):

        """
        """

        splits = os.path.split(self.file)
        filename = splits[1].replace(fFormat, 'wav')
        file = self.ff.sav_dir + '/' + filename

        if self.app_running:
            self.ff.convert(self.file, fFormat)

        else:
            return 1


        pyaud = pyaudio.PyAudio()

        wf = wave.open(file, mode='rb')

        stream = pyaud.open(format=pyaud.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

        # self.playing()
        self._not_stopped = True
        self._not_paused = True

        a = wf.readframes(1)

        while self.app_running and len(a) != 0:


            if self._not_stopped:
                if self._not_paused:
                    print('not paused')

                    stream.write(a)
                    #a = wf.readframes(512)

                    a = (np.fromstring(wf.readframes(512), np.int16) )
                    self.t_played()
                    b = []
                    for x in a:
                        var = int(float(x) / self.volume_val)
                        b.append(var)
                    a = b
                    a = struct.pack('h'*len(a), *a)

                else:

                    #pause
                    sleep(.1)
            else:
                break

        wf.close()
        stream.stop_stream()
        stream.close()

        pyaud.terminate()
        self.complete()

    def stop(self):

        """
        """

        stop_thread = threading.Thread(target=self._stop)
        stop_thread.start()
        # implement a wait
        sleep(1)


    def _stop(self):

        """
        """

        self._not_stopped = False
        return

    def pause(self):

        """
        """

        pause_thread = threading.Thread(target=self._pause)
        pause_thread.start()
        sleep(1)


    def _pause(self):

        """
        """

        print('paused init')
        self._not_paused = False
        return

    def resume(self):

        """
        """

        resume_thread = threading.Thread(target=self._resume)
        resume_thread.start()
        sleep(1)


    def _resume(self):

        """
        """

        self._not_paused = True
        return

    def complete(self):

        """
        """

        print('complete')
        if self._not_paused:
            print('complete')
        elif self._not_stopped:
            pass
        else:
            pass
            #self.completedPlaying.emit('')

    def controlVolume(self, deci):

        """
        """

        cont = threading.Thread( target=self._controlVolume, args=[deci] )
        cont.start()

    def _controlVolume(self, deci):

        """
        """

        vol = float(deci)
        vol = format(100 / vol, '.1f')
        r_vol = float(vol)
        self.volume_val = r_vol

    def t_played(self):


        """
        """


        t_play = threading.Thread( target = self._t_played )
        t_play.start()

    def _t_played(self):


        """
        """


        self.tt_played += 512
        per = self.tt_played / self.file_size * 100
        print(per)
        print(self.file_size)
        print(self.tt_played)
        return

    def propertyNotify(self, prop):


        self.prop = prop

        propNoti = threading.Thread(target = self._propertyNotify)
        propNoti.start()

    def propertyNotifier(self, result):


        #self.propertyChanged.emit(result)
        pass

    def _propertyNotify(self):

        while self.app_running and self._not_stopped:

            sleep(.3)

            count = self.prop
            if count > self.filesPrevCount:
                self.filesPrevCount = count
                self.propertyNotifier([count, self.prop])

    def endPropertyChange(self):

        sleep(1)
        count = len(self.prop)
        result = [count, '']

        # emit the end of property
        #self.endOfPropertyChange.emit(result)

    def endProperty(self):

        self.now_crawling = False

        self.endPropertyChange()

        endProp = threading.Thread( target = self._endProperty )
        endProp.start()

    def _endProperty(self):

        sleep(15)
        self.prop = 0
        self.propertyEnded()

    def propertyEnded(self):

        result = []
        #self.propertyEnd.emit(result)
