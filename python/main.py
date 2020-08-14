#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import time
import json
from datetime import datetime
from PIL import ImageGrab

import cv2
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


def _dfs_group(frame, mask):
    queue = []
    groups = []
    visit = np.zeros_like(frame)
    visit[mask] = 1
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            if not visit[i, j]:
                visit[i, j] = 1
                queue.append((i, j))
                group = []
                while queue:
                    x, y = queue.pop(0)
                    visit[x, y] = 1
                    if (x, y) in group:
                        continue
                    group.append((x, y))
                    if x - 1 >= 0 and not visit[x-1, y]:
                        queue.append((x-1, y))
                    if y - 1 >= 0 and not visit[x, y-1]:
                        queue.append((x, y-1))
                    if x + 1 < frame.shape[0] and not visit[x+1, y]:
                        queue.append((x+1, y))
                    if y + 1 < frame.shape[1] and not visit[x, y+1]:
                        queue.append((x, y+1))
                groups.append(group)

    return groups


def get_detected_enemies(frame):
    frame = np.array(frame)
    frame[:, :, G:] = 0

    frame[frame < 200] = 0
    frame[:, :, G] = frame[:, :, R]
    frame[:, :, B] = frame[:, :, R]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame = cv2.blur(frame, ksize=(3, 3))

    ret, threshold = cv2.threshold(frame, 95, 255, 0)
    contours, _ = cv2.findContours(threshold,
                                   cv2.RETR_TREE,
                                   cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 0, 255), thickness=1)

    frame[frame < 200] = 0

    groups = _dfs_group(frame, (frame < 200))
    for group in [g for g in groups if len(g) <= 8]:
        for pixel in group:
            frame[pixel] = 0
    groups = [group for group in groups if len(group) > 8]
    groups.sort(key=lambda x: -len(x))  # Desc

    positions = [np.sum(group, axis=0) / len(group) / (CELL_SIZE * 10)
                 for group in groups[1:]]

    return positions


if __name__ == "__main__":
    print('[WARNING] Run this script after you join a game queue.')
    time.sleep(3)

    while True:

        while not is_battle_started():
            print('[%s] ...' % datetime.now().isoformat(' '))
            time.sleep(1)

        print('----------------------------')
        print('[%s] -*- Battle started! -*-' % datetime.now().isoformat(' '))
        print('----------------------------')

        while not get_detected_enemies(ImageGrab.grab()):
            print('[%s] ...' % datetime.now().isoformat(' '))
            time.sleep(1)

        print('----------------------------')
        print('[%s] -*- Enemy detected! -*-' % datetime.now().isoformat(' '))
        print('----------------------------')

        while not is_battle_ended():
            # TODO: Logging
            frame = ImageGrab.grab()
            # state = ...
            # action = ...
            time.sleep(1)

        print('--------------------------')
        print('[%s] -*- Battle ended! -*-' % datetime.now().isoformat(' '))
        print('--------------------------')
