# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 07:52:16 2020

@author: Ampofo
"""
import os
import threading
from time import sleep, time
from PyQt5.QtCore import pyqtProperty, pyqtSlot, pyqtSignal
from PyQt5.QtQuick import QQuickItem
from .pyqt_inter_audio import QAudio


class QVideo(QQuickItem):

    """
    """


    def __init__(self, parent=None):
        super().__init__(parent)
        # Video
        self._source = ''
        self.folder = "H:/GitHub/soloman/ex/"
        self._current_frame = 'file:///H:/GitHub/soloman/ex/vid_lv_001.jpg'
        self._fps = 24
        self._frame_no = 0
        # controls
        self._stopped = False
        self._paused = False
        #  Timer
        self._start_time = 0
        self._total_time = 0
        self._total_elapsed_time = 0.0
        # test audio
        self.aud = QAudio()
        self.audio_file = 'H:/GitHub/soloman/soloman/audio/data/music/saves/vid.wav'
        self.aud.prepare(self.audio_file)

    frameUpdate = pyqtSignal(str, arguments=['updateFrame'])

    @pyqtSlot()
    def updater(self):
        # Avoid multiple playing instances
        self._stopped = True
        self._frame_no = 0
        sleep(0.1)

        u_thread = threading.Thread(target = self._updater)
        u_thread.daemon = True
        u_thread.start()

    def _updater(self):

        conts = os.listdir(self.folder)
        final = conts[3:]

        # if user has called the stop or pause function
        # we will need to reset it in order to restart play
        self._stopped = False
        self._paused = False

        self._start_time = time()  # set the universal start time
        self.setTime()
        self.setFrameNo()

        while not self._stopped and self._frame_no != len(final):
            
            #t1 = time()
            if not self._paused:
                self._current_frame = 'file:///' + self.folder + '/' + final[self._frame_no]
                #print(self._current_frame)
                self.updateFrame('')
                # update no
                #self._frame_no += 1
                # o.0416
                #full_time = 1/self._fps
                #t2 = time()
                #rem = full_time - (t2 - t1)
                #print('rem: ', rem)
                sleep(1/24)
                #sleep(interval)
                #print('sleep:', interval)
            else:
                sleep(1/10)
        # stop showing the last frame
        self._stopped = True  # stop all other processs; will cause no trouble
        self._current_frame = ''
        self.updateFrame('')

    @pyqtProperty('QString')
    def currentFrame(self):
        return self._current_frame

    @currentFrame.setter
    def currentFrame(self, frame):
        self._current_frame = frame

    @pyqtProperty('int')
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps):
        self._fps = fps

    @pyqtSlot()
    def pause(self):
        u_thread = threading.Thread(target = self._pause)
        u_thread.daemon = True
        u_thread.start()
    
    def _pause(self):
        self._paused = True

    @pyqtSlot()
    def resume(self):
        u_thread = threading.Thread(target = self._resume)
        u_thread.daemon = True
        u_thread.start()
    
    def _resume(self):
        self._paused = False

    def monitor(self):
        u_thread = threading.Thread(target = self._monitor)
        u_thread.daemon = True
        u_thread.start()
    
    def _monitor(self):
        total = 0
        prev = 0
        tim = 0
        for x in range(30):
            t1 = time()
            t2 = 0
            while t2-t1 < 1:
                t2 = time()
                total = self._frame_no - prev
            prev = self._frame_no
            # print(total, self._frame_no, self._total_elapsed_time, (self._total_elapsed_time/41.6))

    @pyqtSlot()
    def play(self):
        u_thread = threading.Thread(target = self._play)
        u_thread.daemon = True
        u_thread.start()

    def _play(self):
        # play video
        self.updater()
        self.monitor()

    @pyqtSlot(int)
    def seek(self, seconds):
        u_thread = threading.Thread(target = self._seek, args=[seconds])
        u_thread.daemon = True
        u_thread.start()
    
    def _seek(self, seconds):
        self._frame_no = self._fps * seconds

    @pyqtProperty('QString')
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @pyqtSlot()
    def stop(self):
        u_thread = threading.Thread(target = self._stop)
        u_thread.daemon = True
        u_thread.start()
    
    def _stop(self):
        self._stopped = True

    def setFrameNo(self):
        # start the setTime thread
        s_thread = threading.Thread(target=self._setFrameNo)
        s_thread.daemon = True
        s_thread.start()

    def _setFrameNo(self):
        # 24fps 41.6 micro
        # 10fps 100 micro
        while not self._stopped:
            self._frame_no = round(self._total_elapsed_time / 41.6)
            #print('no: ', self._frame_no, self._total_elapsed_time)
            sleep(1/2)

    def setTime(self):
        # start the setTime thread
        s_thread = threading.Thread(target=self._setTime)
        s_thread.daemon = True
        s_thread.start()

    def _setTime(self):
        # set the time every 10 milliseconds
        # this will be used to know which frame is up
        t1 = self._start_time
        while not self._stopped:
            sleep(0.1)
            t2 = time()
            tm = t2 - t1
            #t1 = t2 # this is much accurate
            micro = round(tm, 2) * 1000 # this convert to microseconds
            self._total_elapsed_time = micro

    def updateFrame(self, frame):
        self.frameUpdate.emit(frame)

