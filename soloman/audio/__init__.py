# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 11:41:43 2020

@author: Ampofo
"""
import os
from time import sleep, time
import threading
import wave
import struct

import numpy as np
import pyaudio

from pyffmpeg import FFmpeg

class Audio:


    """
    """


    def __init__(self, saveFolder=None):
        self.file = ''
        self.file_size = 0
        self.frame_rate = 0
        self._play_bits = 0
        self.overwrite = False
        self.app_running = True
        self._not_paused = True
        self.playing = self._not_paused
        self._not_stopped = False
        self.t_size = 0
        self.tt_played = 0
        self.volume_val = 1.4
        self._seek_int = 0
        parent_folder = os.path.dirname(__file__)
        if saveFolder:
            self.save_folder = os.path.realpath(saveFolder)
        else:
            self.save_folder = os.path.realpath(
                os.path.join(parent_folder,'data', 'music', 'saves'))
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)
        self.ff = FFmpeg(self.save_folder)
        self.ff.overwrite = False

    def __str__(self):
        return 'soloman.Audio'

    def converter(self, file_path):

        """
        Converts the audio file to a .wav format
        """

        file = os.path.split(file_path)[1]
        split = os.path.splitext(file)
        pos_wav_file = split[0] + '.wav'
        ext = split[1]
        save_file = os.path.join(self.save_folder, pos_wav_file)

        if not os.path.exists(save_file):
            ff = self.ff.convert(file_path, pos_wav_file)
            return ff
        else:
            return save_file

    def delay_play(self, u_delay):

        """
        """

        # play should stop all playing songs before
        # playing this one
        self._not_stopped = False
        t1 = time()
        delay = float(u_delay)
        # Use a tenth (x/10) or use this 0.0156042575836182
        if u_delay == 0:
            r = 0
        elif u_delay < 0.1:
            r = 0.00000000000001#0.0156042575836182
        else:
            r = 0.001
        delay = delay - r
        sleep(delay)
        play_thread = threading.Thread(target=self._play)
        play_thread.start()
        t2 = time()

        f_delay = t2-t1
        return(f_delay)

    def play(self, file):

        """
        """

        # play should stop all playing songs before
        # playing this one
        self._not_stopped = False
        sleep(0.1)
        self.file = self.converter(file)
        if self.file:
            self.file_size = os.stat(self.file).st_size
            play_thread = threading.Thread(target=self._play)
            play_thread.start()

    def _play(self):

        """
        """

        pyaud = pyaudio.PyAudio()

        wf = wave.open(self.file, mode='rb')

        stream = pyaud.open(format=pyaud.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

        self.frame_rate = wf.getframerate()
        self._play_bits = int(self.frame_rate / 10)

        self._not_stopped = True
        self._not_paused = True

        a = wf.readframes(1)
        while self.app_running and len(a) != 0:

            if self._not_stopped and self._not_paused:

                stream.write(a)
                #a = wf.readframes(self._play_bits)

                # Set seek position if set
                if self._seek_int:
                    wf.setpos(self._seek_int)

                a = (np.fromstring(wf.readframes(self._play_bits), np.int16) )
                self.t_played()
                a = [int(float(x) / self.volume_val) for x in a ]
                a = struct.pack('h'*len(a), *a)

            elif not self._not_stopped:
                # stop
                break
                
            else:
                #pause
                sleep(.1)

        wf.close()
        stream.stop_stream()
        stream.close()

        pyaud.terminate()
        self.complete()

    def prepare(self, file):

        """
        """

        self.file = self.converter(file)
        if self.file:
            self.file_size = os.stat(self.file).st_size
        return True

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

    def _pause(self):

        """
        """

        self._not_paused = False
        return

    def resume(self):

        """
        """

        resume_thread = threading.Thread(target=self._resume)
        resume_thread.start()

    def _resume(self):

        """
        """

        self._not_paused = True
        return

    def complete(self):

        """
        """

        if self._not_paused:
            pass
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
        This takes in a decimal
        Decimal should range from 1.01 to 100
        It can't be more than 100
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


        self.tt_played += self._play_bits
        per = self.tt_played / self.file_size * 100
        return per

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

    def seek(self, seconds):

        seek_int = self.frame_rate * seconds
        final_seek = int(seek_int)
        # to avoid overpass
        if final_seek == 0:
            final_seek = 1
        self._seek_int = final_seek
        # Reset seek so that we don't keep seeking.
        sleep(0.1)
        self._seek_int = 0
