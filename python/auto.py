#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import time
import json
from datetime import datetime
from PIL import ImageGrab

import numpy as np

from win32py import win32py

BATTLE_START_TIME = time.time()
BATTLE_END_TIME = time.time()

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json'), 'r') as f:
    data = json.loads(''.join(f.readlines()))
    MOD_DIR = data["mod"]
    BATTLE_START_LOG = data["battle_start"]
    BATTLE_END_LOG = data["battle_end"]

R, G, B = (0, 1, 2)
WIDTH, HEIGHT = (1920, 1080)


def is_battle_started():
    global BATTLE_START_TIME
    try:
        battle_start_time = os.path.getmtime(os.path.join(MOD_DIR, BATTLE_START_LOG))
        if battle_start_time > BATTLE_START_TIME:
            BATTLE_START_TIME = battle_start_time
            return True
    except FileNotFoundError:
        pass
    return False


def is_battle_ended():
    global BATTLE_END_TIME
    log_file = os.path.join(MOD_DIR, BATTLE_END_LOG)
    try:
        battle_end_time = os.path.getmtime(log_file)
        if battle_end_time > BATTLE_END_TIME:
            BATTLE_END_TIME = battle_end_time
            return True
    except FileNotFoundError:
        pass
    except ValueError:
        pass
    return False


def is_replay_button_enabled(frame):
    # assert frame.size == (WIDTH, HEIGHT)
    frame = np.array(frame)
    frame = frame[HEIGHT-92:HEIGHT-64, WIDTH-360:WIDTH-264]

    frame[:, :, G] = 0
    frame[:, :, B] = 0
    frame[frame < 128] = 0

    # Image.fromarray(frame).show()
    # print(np.mean(frame))

    return np.mean(frame) >= 44


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

        while is_replay_button_enabled(ImageGrab.grab()):
            win32py.Mouse.move(1608, 1002)
            win32py.Mouse.click(0x0002)
            win32py.Mouse.click(0x0004)
            time.sleep(1)
