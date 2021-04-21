import threading
from time import sleep

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickItem


class Video():


    """
    Provides interface between qml SVideo and QVideo
    """

    def __init__(self, engine=None):
        self._engine = engine
        self._root_object = self._engine.rootObjects()[0]
        self.QVideo = ()

    def __str__(self):
        return 'soloman.Video'

    def get_SVideo(self, obj_name):
        g_thread = threading.Thread(target=self._get_SVideo, args=[obj_name])
        g_thread.daemon = True
        g_thread.start()

    def show_frame(self, frame):
        if frame is not None:
            g_thread = threading.Thread(target=self._show_frame, args=[frame])
            g_thread.daemon = True
            g_thread.start()

    def _show_frame(self, frame):
        self.QVideo.show_cv2_frame(frame)

    def _get_SVideo(self, obj_name):
        """
        Get the SVideo's QVideo object
        """
        self.QVideo = self._root_object.findChild(QQuickItem, obj_name)
        self.QVideo.start_cv2()

    def update(self, frame):
        g_thread = threading.Thread(target=self._update, args=[frame])
        g_thread.daemon=True
        g_thread.start()

    def _update(self, frame):
        """
        Updates the QVideo frames
        """
        self.QVideo.make_cv2_frame(frame)
