from timeit import timeit
from time import sleep

import pytest

import soloman

@pytest.mark.parametrize('func', [
    (soloman.fps_24),
    (soloman.fps_30),
    (soloman.fps_60)])
def test_fps_availability(func):
    assert func() == True

@pytest.mark.parametrize('func,duration', [
    (soloman.fps_24, 1/40),
    (soloman.fps_30, 1/60),
    (soloman.fps_60, 1/120)])
def test_fps_sleep_durations(func, duration):
    dura = timeit(func, number=1)
    assert round(dura,4) <= round((duration + (duration/10)), 4)
