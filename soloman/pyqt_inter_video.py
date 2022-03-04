# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 07:52:16 2020

@author: Ampofo
"""
import os
import threading
from random import randrange
from time import sleep, time

# Just in case user won't need it
try:
    import cv2
except:
    pass

from qtpy.QtCore import Property, Slot, Signal
from qtpy.QtQuick import QQuickItem
from pyffmpeg import FFmpeg, FFprobe

from .pyqt_inter_audio import QAudio
from .audio import Audio
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
        # FFmpeg
        self._ffmpeg_inst = FFmpeg()
        # Video
        self._source = ''
        self._curr_file = ""
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
        self._user_stills = False
        self._stills_content = []
        self._curr_stills_index = 0
        self._stills_len = 10000000
        self._stills_type = ""
        self._stills_converted = False
        self.sync = True
        self._seeked = False
        self._seek_frame = 0
        self._seek_calls = 0
        # Audio
        self._audio_inst = Audio(saveFolder=self.temp_folder)
        self._has_audio = True
        self._play_audio = True
        self._sync_audio = True
        self.auto_sync_time: int = 3
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
        self._duration: str = ''
        self._tile = 0
        self._tile_enumeration = False

    aboutToPlay = Signal(float, arguments=['delayValue'])
    aspectRatioChanged = Signal(bool, arguments=['aspectRatio'])
    delayChanged = Signal(int, arguments=['delay'])
    durationChanged = Signal(str, arguments=['duration'])
    frameUpdate = Signal(str, arguments=['updateFrame'])
    tileChanged = Signal(int, arguments=['tileChange'])
    tileEnumChanged = Signal(bool, arguments=['tileEnum'])
    destroyed = Signal()

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
            self._stills_len = len(self._stills_content)

    def auto_sync_audio(self):
        a_thread = threading.Thread(target=self._auto_sync_audio)
        a_thread.daemon = True
        a_thread.start()

    def _auto_sync_audio(self):
        while not self._stopped:
            if self._paused:
                sleep(1)
            else:
                seconds = int(self._total_elapsed_time / 1000)
                self._audio_inst.seek(seconds+0.7)
            sleep(self.auto_sync_time)

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
        rand_str = str(randrange(1000, 4000))
        self.folder = self.convert_folder + "/" + rand_str + "/"
        os.makedirs(self.folder)
        self._stills_type = 'jpg'

        out = self.folder + "vid_%01d.jpg"
        cmd = f"-i {fileName} -r {str(self.fps)} {out}"
        self._ffmpeg_inst.options(cmd)
        # Signal and end to conversion
        if self._seeked:
            sleep(0.1)
            self._stills_converted = True

        self._stills_converted = True
        self._stills_len = len(os.listdir(self.folder))

    def convert_seeked(self, time: str, start_frame: int):
        c_thread = threading.Thread(
            target=self._convert_seeked,
            args=[time, start_frame])
        c_thread.daemon = True

        if self._seek_calls > 1:
            return

        c_thread.start()

    def _convert_seeked(self, time: str, start_frame: int):

        """
        This function seeks to a point in time of the video
        and then start converting from that time.
        time -> means that time that it should seek to: hh:mm::ss.ms
        start_frame -> means that frame number that corresponds with
        the time for instance start_frame = 96 corresponds with 00:00:04
        if the video has a framerate of 24 fps
        """

        out = self.folder + "vid_%01d.jpg"
        start_frame = str(start_frame)
        cmd = f"-ss {time} -i {self._curr_file}"
        cmd += f" -r {str(self.fps)} -start_number {start_frame} {out}"
        sleep(0.1)
        # self._ffmpeg_inst.quit()
        self._ffmpeg_inst.options(cmd)

        if self._seek_calls > 1:
            return

        # Signal and end to conversion
        sleep(0.1)
        self._stills_converted = True
        # send length of the stills
        lists = os.listdir(self.folder)
        lists.sort(key=lambda item: int(item.split('_')[1].split('.')[0]))
        l_ind = lists[-1].split('vid_')[1].split('.')[0]
        self._stills_len = int(l_ind)

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

    def fix_splashes(self, fileName):
        """
        Replace backslash with forward slash
        """
        abs_path = os.path.abspath(fileName)
        return abs_path.replace("\\", '/')

    def get_current_frame(self):
        return self._current_frame

    def is_stills(self, fileName):
        ext = os.path.splitext(fileName)[1][1:]
        if ext not in self._supported_vid_files:
            # stills
            self._user_stills = True
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

    def _pause(self):
        self._paused = True
        if self._sync_audio:
            self._audio_inst._not_paused = False

    def _play(self, fileName):
        # play video
        self._curr_file = fileName
        if not self._same_session:
            self._user_stills = False
            filename = self.fix_splashes(fileName)

            if self.is_stills(filename):
                self._stills_converted = True
                self._append_stills_content()  # call without a thread
                self.stills_updater()
                return

            else:
                # not stills
                # set fps based on file
                probe = FFprobe(filename)
                fps = probe.fps
                self._duration = probe.duration

                # remove later
                if not fps:
                    fps = 24

                if abs(fps - self.fps) > 1:
                    self.fps = fps

                if self._has_audio:
                    self._prepare_audio_file()

                self.convert_to_stills(filename)
                self.append_stills_content()

            self._same_session = True

        self.updater()
        # self.monitor() # allow this only in debug mode

    def prepare_audio_file(self):
        a_thread = threading.Thread(target=self._prepare_audio_file)
        a_thread.daemon = True
        a_thread.start()

    def _prepare_audio_file(self):
        fileName = self.fix_splashes(self._curr_file)
        self._audio_inst.prepare(fileName)
        print(self._audio_inst.file)

    def play_audio_file(self, delay: float):
        a_thread = threading.Thread(
            target=self._play_audio_file,
            args=[delay])
        a_thread.daemon = True
        a_thread.start()

    def _play_audio_file(self, delay: float):
        print('delay: ', delay)
        self._audio_inst.delay_play(delay)
        self.auto_sync_audio()

    def _resume(self):
        self._paused = False
        if self._sync_audio:
            self._audio_inst._not_paused = True

    def _seek(self, seconds):
        status = 'continue'
        t1 = time()
        while round(time() - t1, 2) * 1000 < 100:
            if self._seek_calls > 1:
                status = ''
                self._seek_calls -= 1
                break

        if status:
            self._seek_handler(seconds)

    def _seek_handler(self, seconds):
        # sleep to ensure we can reset
        if self._seek_calls > 1:
            return
        sleep(0.1)
        self._ffmpeg_inst.quit()
        sleep(0.2)
        self._seeked = True
        self._seek_calls = 1

        frame_no = int(self.fps * seconds)

        # Calculate the time string
        h_dec = seconds / 3600
        hrs, m_dec = str(h_dec).split('.')
        m_dec = '.' + m_dec
        mins, s_dec = str(float(m_dec) * 60).split('.')
        s_dec = '.' + s_dec
        secs = float(s_dec) * 60

        if int(hrs) < 10:
            hrs_str = '0' + hrs
        else:
            hrs_str = str(hrs)

        if int(mins) < 10:
            mins_str = '0' + mins
        else:
            mins_str = str(mins)

        if secs < 10:
            secs_str = '0' + str(int(secs))
        else:
            secs_str = str(secs)

        s_time = f"{hrs_str}:{mins_str}:{secs_str}"

        if self._seek_calls > 1:
            return

        self.convert_seeked(s_time, frame_no)

        fpsth = f'vid_{str(int(frame_no + self.fps))}.{self._stills_type}'
        f_path = os.path.join(self.folder, fpsth)

        sleep(0.5)  # just in case it was a reverse seek
        while not os.path.exists(f_path) and self._seek_calls < 2:
            sleep(1)

        if self._seek_calls > 1:
            return

        # self._total_elapsed_time = seconds * 1000
        self._seeked = False
        self._seek_calls -= 1  # maybe should be zero
        self._seek_frame = frame_no
        self._start_time = time()
        self.setTime()
        if self._sync_audio:
            print('heres, ', seconds)
            self._audio_inst.seek(seconds)

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

            elap = self._total_elapsed_time / refresh_time
            self._frame_no = round(elap) + self._seek_frame
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

            if self._seeked:
                break

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

    def show_cv2_frame(self, frame):
        c_thread = threading.Thread(target=self._show_cv2_frame, args=[frame])
        c_thread.daemon = True
        c_thread.start()

    def _show_cv2_frame(self, frame):
        name = self._make_temp_cv2_frame(frame)
        self._current_frame = 'file:///' + name
        self.updateFrame('')

    def start_cv2(self):
        sleep(1/randrange(10, 40))  # in case of multiple threaded instances
        if os.path.exists(self.convert_folder):
            fold_len = len(os.listdir(self.convert_folder)) + 1
        else:
            fold_len = 1
        self.folder = self.convert_folder + "/" + str(fold_len)
        os.makedirs(self.folder)
        self.cv2_updater()

    def stills_updater(self):
        # Avoid multiple playing instances
        self._stopped = True
        self._frame_no = 0
        sleep(0.3)

        u_thread = threading.Thread(target = self._stills_updater)
        u_thread.daemon = True
        u_thread.start()

    def _stills_updater(self):

        self._stopped = False
        self._paused = False
        self._seek_frame = 0

        # initialize remaining delay
        rem_delay = 0.0

        # Make sure convertion is done
        if len(self._stills_content) < 1:
            return

        if rem_delay < 0:
            rem_delay = self._delay

        # about to play
        self.aboutToPlay.emit(rem_delay)

        # Delay
        if self._delay:
            # sleep remaining delay
            sleep(rem_delay)

        # print(self._audio_inst.playing, 'yep')
        self._start_time = time()  # set the universal start time
        self.setTime()
        self.setFrameNo()

        while not self._stopped and self._frame_no != self._stills_len:

            #t1 = time()
            filename = self._stills_content[self._frame_no]  # use still type
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

    def _stop(self):
        self._stopped = True
        if self._sync_audio:
            self._audio_inst._not_stopped = False
        self._ffmpeg_inst.quit()

    def updateFrame(self, frame):
        self.frameUpdate.emit(frame)

    def _updater(self):
    
        #conts = os.listdir(self.folder)

        # if user has called the stop or pause function
        # we will need to reset it in order to restart play
        self._stopped = False
        self._paused = False
        self._seek_frame = 0

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

        # Play audio
        if self._play_audio and self._has_audio:
            self.play_audio_file(rem_delay)

        # Delay
        if self._delay:
            # sleep remaining delay
            sleep(rem_delay)

        if self._play_audio and self._has_audio:
            while not self._audio_inst.playing:
                sleep(0.1)
            sleep(0.5)

        # print(self._audio_inst.playing, 'yep')
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

    @Property(bool, notify=aspectRatioChanged)
    def aspectRatio(self):
        return self._aspect_ratio

    @aspectRatio.setter
    def aspectRatio(self, value):
        self._aspect_ratio = value

    @Property('QString', notify=frameUpdate)
    def currentFrame(self):
        return self._current_frame

    @currentFrame.setter
    def currentFrame(self, frame):
        self._current_frame = frame

    @Property(bool, notify=delayChanged)
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        self._delay = value

    @Property(str, notify=durationChanged)
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @Property('int')
    def framesPerSecond(self):
        return self.fps

    @framesPerSecond.setter
    def framesPerSecond(self, fps):
        self.fps = fps

    @Slot()
    def pause(self):
        u_thread = threading.Thread(target = self._pause)
        u_thread.daemon = True
        u_thread.start()

    @Slot(str)
    def play(self, fileName):
        u_thread = threading.Thread(target = self._play, args=[fileName])
        u_thread.daemon = True
        u_thread.start()

    @Slot()
    def resume(self):
        u_thread = threading.Thread(target = self._resume)
        u_thread.daemon = True
        u_thread.start()

    @Slot(int)
    def seek(self, seconds):
        u_thread = threading.Thread(target = self._seek, args=[seconds])
        u_thread.daemon = True
        self._seek_calls += 1
        u_thread.start()

    @Property('QString')
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    @Slot()
    def stop(self):
        u_thread = threading.Thread(target = self._stop)
        u_thread.daemon = True
        u_thread.start()

    @Property(int, notify=tileChanged)
    def tile(self):
        return self._tile

    @tile.setter
    def tile(self, value):
        self._tile = value
        if self._tile > 2 and self._tile < 6:
            self._tile_enumeration = value

    @Property(int, notify=tileEnumChanged)
    def tileEnumeration(self):
        return self._tile_enumeration

    @tileEnumeration.setter
    def tileEnumeration(self, value):
        pass

    @Slot()
    def updater(self):
        # Avoid multiple playing instances
        self._stopped = True
        self._frame_no = 0
        sleep(0.3)

        u_thread = threading.Thread(target = self._updater)
        u_thread.daemon = True
        u_thread.start()
