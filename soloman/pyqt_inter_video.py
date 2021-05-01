# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 07:52:16 2020

@author: Ampofo
"""
import os
import threading
from random import randrange
from time import sleep, time

import cv2
from PyQt5.QtCore import pyqtProperty, pyqtSlot, pyqtSignal
from PyQt5.QtQuick import QQuickItem
from pyffmpeg import FFmpeg, FFprobe

from .pyqt_inter_audio import QAudio
from .misc import Paths


class QVideo(QQuickItem):

    """
    """


    def __init__(self, parent=None, frames_per=None):
        super().__init__(parent)
        temp_f = Paths().temp
        self.convert_folder = self.fix_splashes(temp_f) + '/soloman/convert'
        self.temp_folder = self.convert_folder + '/temp' + str(randrange(1, 1000000))
        os.makedirs(self.temp_folder)
        self._same_session = False
        # Video
        self._source = ''
        self.folder = ""
        self._current_frame = ''
        if frames_per:
            self.fps = frames_per
        else:
            self.fps = 29.97
        self._frame_no = 0
        self._supported_vid_files = [
            'mp4', "asf", "avi", "flv",
            "gif", "mov", "3gp", "3gpp",
            "mkv", "webm"]
        self._stills_content = []
        self._curr_stills_index = 0
        self._stills_len = 10000000
        self._stills_type = ""
        self._stills_converted = False
        self.sync = True
        # controls
        self._stopped = False
        self._paused = False
        #  Timer
        self._start_time = 0
        self._total_time = 0
        self._total_elapsed_time = 0.0
        # Opencv
        self._cv2_frames_len = 0
        self._cv2_tmp_frames_len = 0
        self._cv2_session = False
        # Qml property
        self._aspect_ratio = True
        self._current_frame = ''
        self._delay = 0.0
        self._tile = 0
        self._tile_enumeration = False

    aboutToPlay = pyqtSignal(float, arguments=['delayValue'])
    aspectRatioChanged = pyqtSignal(bool, arguments=['aspectRatio'])
    delayChanged = pyqtSignal(int, arguments=['delay'])
    frameUpdate = pyqtSignal(str, arguments=['updateFrame'])
    tileChanged = pyqtSignal(int, arguments=['tileChange'])
    tileEnumChanged = pyqtSignal(bool, arguments=['tileEnum'])
    destroyed = pyqtSignal()

    @pyqtSlot()
    def updater(self):
        # Avoid multiple playing instances
        self._stopped = True
        self._frame_no = 0
        sleep(0.3)

        u_thread = threading.Thread(target = self._updater)
        u_thread.daemon = True
        u_thread.start()

    def _updater(self):

        #conts = os.listdir(self.folder)

        # if user has called the stop or pause function
        # we will need to reset it in order to restart play
        self._stopped = False
        self._paused = False

        # initialize remaining delay
        rem_delay = 0.0

        # Make sure convertion has started
        if len(self._stills_content) < 1:
            rem_delay = self._delay - 1.5
            sleep(1.5)

        if rem_delay < 0:
            rem_delay = self._delay

        # about to play
        self.aboutToPlay.emit(rem_delay)

        # Delay
        if self._delay:
            # sleep remaining delay
            sleep(rem_delay)

        self._start_time = time()  # set the universal start time
        self.setTime()
        self.setFrameNo()

        while not self._stopped and self._frame_no != self._stills_len:

            #t1 = time()
            filename = f'vid_{str(self._frame_no+1)}.jpg'  # use still type
            if not self._paused:
                self._current_frame = f"file:///{self.folder}/{filename}"
                self.updateFrame('')
                sleep(1/self.fps) # sleep equivalent of FPS
            else:
                sleep(1/10)

        # stop showing the last frame
        self._stopped = True  # stop all other processs; will cause no trouble
        self._current_frame = ''
        self.updateFrame('')

    @pyqtProperty(bool, notify=aspectRatioChanged)
    def aspectRatio(self):
        return self._aspect_ratio

    @aspectRatio.setter
    def aspectRatio(self, value):
        self._aspect_ratio = value

    @pyqtProperty('QString', notify=frameUpdate)
    def currentFrame(self):
        return self._current_frame

    @currentFrame.setter
    def currentFrame(self, frame):
        self._current_frame = frame

    @pyqtProperty(bool, notify=delayChanged)
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value

    @pyqtProperty(int, notify=tileChanged)
    def tile(self):
        return self._tile

    @tile.setter
    def tile(self, value):
        self._tile = value
        if self._tile > 2 and self._tile < 6:
            self._tile_enumeration = value

    @pyqtProperty(int, notify=tileEnumChanged)
    def tileEnumeration(self):
        return self._tile_enumeration

    @tileEnumeration.setter
    def tileEnumeration(self, value):
        pass

    def append_stills_content(self):
        if self.sync:
            a_thread = threading.Thread(target=self._append_stills_content)
            a_thread.daemon = True
            a_thread.start()
        else:
            self._append_stills_content()

    def _append_stills_content(self):

        # wait for the FFmpeg to start at least
        sleep(1)
        while self.sync and not self._stills_converted:
            listed = os.listdir(self.folder)
            self._stills_content.extend(listed[self._curr_stills_index:])
            self._curr_stills_index = len(listed) - 1
            sleep(0.1)
        else:
            self._stills_content = os.listdir(self.folder)

    def convert_to_stills(self, fileName):
        if self.sync:
            c_thread = threading.Thread(
                target=self._convert_to_stills, args=[fileName])
            c_thread.daemon = True
            c_thread.start()
        else:
            self._convert_to_stills(fileName)

    def _convert_to_stills(self, fileName):
        """
        convert the video files to stills
        """
        self.folder = self.convert_folder + "/" + str(randrange(1000, 4000)) + "/"
        os.makedirs(self.folder)
        self._stills_type = 'jpg'

        ff = FFmpeg()
        out = self.folder + "vid_%01d.jpg"
        ff.options("-i " + fileName + " -r " + str(self.fps) + " " + out)
        # Signal and end to conversion
        sleep(0.1)
        self._stills_converted = True
        # send length of the stills
        self._stills_len = len(os.listdir(self.folder))


    def fix_splashes(self, fileName):
        """
        Replace backslash with forward slash
        """
        abs_path = os.path.abspath(fileName)
        return abs_path.replace("\\", '/')

    def is_stills(self, fileName):
        ext = os.path.splitext(fileName)[1][1:]
        if ext not in self._supported_vid_files:
            # stills
            try:
                os.listdir(fileName)
                self.folder = fileName
            except:
                self.folder = os.path.dirname(fileName)

            self._stills_type = ext
            return True
        else:
            # video
            return False

    @pyqtProperty('int')
    def framesPerSecond(self):
        return self.fps

    @framesPerSecond.setter
    def framesPerSecond(self, fps):
        self.fps = fps

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
        micro = round(1000 / self.fps, 2)
        for x in range(30):
            t1 = time()
            t2 = 0
            while t2-t1 < 1:
                t2 = time()
                total = self._frame_no - prev
            prev = self._frame_no
            print(
                'Total: {}, Frame no: {}, Elapsed time: {}, Elapsed Time / {}: {}'.format(total,
                self._frame_no,
                self._total_elapsed_time,
                micro,
                (self._total_elapsed_time/micro))
            )

    @pyqtSlot(str)
    def play(self, fileName):
        u_thread = threading.Thread(target = self._play, args=[fileName])
        u_thread.daemon = True
        u_thread.start()
 
    def _play(self, fileName):
        # play video
        if not self._same_session:
            filename = self.fix_splashes(fileName)
            if self.is_stills(filename):
                # stills
                pass
            else:
                # not stills
                # set fps based on file
                fps = FFprobe(filename).fps

                # remove later
                if not fps:
                    fps = 24

                if abs(fps - self.fps) > 1:
                    self.fps = fps

                self.convert_to_stills(filename)
                self.append_stills_content()

            self._same_session = True

        self.updater()
        # self.monitor() # allow this only in debug mode

    def get_current_frame(self):
        return self._current_frame

    @pyqtSlot(int)
    def seek(self, seconds):
        u_thread = threading.Thread(target = self._seek, args=[seconds])
        u_thread.daemon = True
        u_thread.start()

    def _seek(self, seconds):
        self._frame_no = self.fps * seconds

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
        """
        Sets the frame based on the current time. For instance;
        for 24fps if the current time is the first second, the current
        frame should be frame no. 24, on the second second, the current
        frame is 48 and so on.
        """
        # 24fps 41.6 micro
        # 10fps 100 micro
        refresh_time = 1000 / self.fps
        sleep_time = 1 / (self.fps)

        while not self._stopped:

            if self._paused:
                sleep(0.1)
                continue

            self._frame_no = round(self._total_elapsed_time / refresh_time)
            sleep(sleep_time)

    def setTime(self):
        # start the setTime thread
        s_thread = threading.Thread(target=self._setTime)
        s_thread.daemon = True
        s_thread.start()

    def _setTime(self):
        # set the time every 10 milliseconds
        # this will be used to know which frame is up
        t1 = self._start_time
        tm = 0
        while not self._stopped:
            # *** very very important code; The speed at which
            # the time will be refreshed.
            if self._paused:
                # reset the time to pause the frame
                ts = time() - t1 - tm
                t1 += ts
                sleep(0.1)
                continue

            sleep(0.01)
            # ***
            t2 = time()
            tm = t2 - t1
            #t1 = t2 # this is much accurate
            micro = round(tm, 2) * 1000 # this convert to microseconds
            self._total_elapsed_time = micro

    def start_cv2(self):
        sleep(1/randrange(10, 40))  # in case of multiple threaded instances
        if os.path.exists(self.convert_folder):
            fold_len = len(os.listdir(self.convert_folder)) + 1
        else:
            fold_len = 1
        self.folder = self.convert_folder + "/" + str(fold_len)
        os.makedirs(self.folder)
        self.cv2_updater()

    def make_cv2_frame(self, frame):
        c_thread = threading.Thread(target=self._make_cv2_frame, args=[frame])
        c_thread.daemon = True
        c_thread.start()

    def _make_cv2_frame(self, frame):
        # create the frame image
        self._cv2_frames_len += 1
        filename = self.folder + "/" + str(self._cv2_frames_len) + ".jpg"
        cv2.imwrite(filename, frame)

    def _make_temp_cv2_frame(self, frame):
        # create the frame image
        self._cv2_tmp_frames_len += 1
        filename = self.temp_folder + "/" + str(self._cv2_tmp_frames_len) + ".jpg"
        cv2.imwrite(filename, frame)
        return filename

    def show_cv2_frame(self, frame):
        c_thread = threading.Thread(target=self._show_cv2_frame, args=[frame])
        c_thread.daemon = True
        c_thread.start()

    def _show_cv2_frame(self, frame):
        name = self._make_temp_cv2_frame(frame)
        self._current_frame = 'file:///' + name
        self.updateFrame('')

    def cv2_updater(self):
        # Avoid multiple playing instances Not multiple objects though
        self._stopped = True
        self._frame_no = 0
        sleep(0.5)

        u_thread = threading.Thread(target = self._cv2_updater)
        u_thread.daemon = True
        u_thread.start()

    def _cv2_updater(self):
        """
        The updater for cv2
        """

        # if user has called the stop or pause function
        # we will need to reset it in order to restart play
        self._stopped = False
        self._paused = False

        self._start_time = time()  # set the universal start time
        self.setTime()
        self.setFrameNo()

        # if no show frame has been called sleep and loop
        while self._cv2_frames_len == 0:
            sleep(1/3)

        # Avoid showing frame 0
        if self._frame_no == 0:
            self._frame_no += 1

        while not self._stopped and self._frame_no <= self._cv2_frames_len:

            if not self._paused:
                self._current_frame = 'file:///' + self.folder + '/' + str(self._frame_no) + ".jpg"
                self.updateFrame('')
                sleep(1/self.fps)
            else:
                sleep(1/10)

        # stop showing the last frame
        self._current_frame = ''
        self.updateFrame('')

        self._stopped = True  # stop all other processs; will cause no trouble
        self._cv2_session = False

    def updateFrame(self, frame):
        self.frameUpdate.emit(frame)
