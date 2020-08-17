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

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json'), 'r') as f:  # noqa: E501
    data = json.loads(''.join(f.readlines()))
    MOD_DIR = data["mod"]
    BATTLE_START_LOG = data["battle_start"]
    BATTLE_END_LOG = data["battle_end"]

R, G, B = (0, 1, 2)
WIDTH, HEIGHT = (1920, 1080)
CELL_SIZE = 24


def is_battle_started():
    global BATTLE_START_TIME
    try:
        path = os.path.join(MOD_DIR, BATTLE_START_LOG)
        battle_start_time = os.path.getmtime(path)
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
    y = HEIGHT - 92
    x = WIDTH - 360
    frame = frame[y:y+28, x:x+96]

    frame[:, :, G] = 0
    frame[:, :, B] = 0
    frame[frame < 128] = 0

    return np.mean(frame) >= 44


def is_enemy_detected():
    try:
        path = os.path.join(MOD_DIR, 'enemy.log')
        with open(path, 'r') as f:
            data = json.loads(f.read())
            return data["isVisible"]
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return False


if __name__ == "__main__":
    print('[WARNING] Run this script after you join a game queue.')
    time.sleep(3)

    while True:

        while not is_battle_started():
            time.sleep(1)

        print('----------------------------')
        print('[%s] -*- Battle started! -*-' % datetime.now().isoformat(' '))
        print('----------------------------')

        while not is_enemy_detected():
            time.sleep(1)

        print('----------------------------')
        print('[%s] -*- Enemy detected! -*-' % datetime.now().isoformat(' '))
        print('----------------------------')

        while not is_battle_ended():
            # TODO: Logging
            #frame = ImageGrab.grab()
            # state = ...
            # action = ...
            time.sleep(1)

        print('--------------------------')
        print('[%s] -*- Battle ended! -*-' % datetime.now().isoformat(' '))
        print('--------------------------')
