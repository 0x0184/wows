#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import time
from datetime import datetime
from PIL import ImageGrab

import numpy as np

from win32py import win32py

MOD_DIR = 'F:\\Games\\World_of_Warships_ASIA\\res_mods\\0.9.5.0\\PnFMods\\AutoMod'
BATTLE_START_LOG = 'battle_start.log'
BATTLE_END_LOG = 'battle_end.log'

R, G, B = (0, 1, 2)
WIDTH, HEIGHT = (1920, 1080)


def is_battle_started():
    log_file = os.path.join(MOD_DIR, BATTLE_START_LOG)
    flag = os.path.exists(log_file)
    if flag:
        os.remove(log_file)
    return flag


def is_battle_ended():
    log_file = os.path.join(MOD_DIR, BATTLE_END_LOG)
    flag = os.path.exists(log_file)
    if flag:
        os.remove(log_file)
    return flag


def is_replay_button_enabled(frame):
    assert frame.size == (WIDTH, HEIGHT)
    frame = np.array(frame)
    frame = frame[HEIGHT-92:HEIGHT-64, WIDTH-360:WIDTH-264]

    frame[:, :, G] = 0
    frame[:, :, B] = 0
    frame[frame < 128] = 0

    # Image.fromarray(frame).show()
    # print(np.mean(frame))

    return np.mean(frame) >= 48


if __name__ == "__main__":
    print('[WARNING] Run this script after you joined a game queue.')
    time.sleep(3)

    while True:

        while not is_battle_started():
            print('[%s] ...' % datetime.now().isoformat(' '))
            time.sleep(1)

        print('----------------------------')
        print('[%s] -*- Battle started! -*-' % datetime.now().isoformat(' '))
        print('----------------------------')

        while not is_battle_ended():
            win32py.Keyboard.click(0x11)
            time.sleep(1)

        print('--------------------------')
        print('[%s] -*- Battle ended! -*-' % datetime.now().isoformat(' '))
        print('--------------------------')

        while not is_replay_button_enabled(ImageGrab.grab()):
            time.sleep(1)

        print('---------------------------')
        print('[%s] -*- Replay enabled! -*-' % datetime.now().isoformat(' '))
        print('---------------------------')

        win32py.Mouse.move(1608, 1002)
        win32py.Mouse.click(0x0002)
        win32py.Mouse.click(0x0004)
