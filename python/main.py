#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import time
import json
import queue
from datetime import datetime
from threading import Thread
from multiprocessing import Queue

import numpy as np
from PIL import ImageGrab

from grpc_client import QueueClient
from win32py.win32py.keyboard_hook import KeyboardHook, hook_procedure  # noqa: E402, E501
from win32py.win32py.util import get_function_pointer   # noqa: E402

BATTLE_START_TIME = time.time()
BATTLE_END_TIME = time.time()

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json'), 'r') as f:  # noqa: E501
    data = json.loads(''.join(f.readlines()))
    MOD_DIR = data["mod"]
    BATTLE_START_LOG = data["battle_start"]
    BATTLE_END_LOG = data["battle_end"]
    BATTLE_QUIT_LOG = data["battle_quit"]

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

    """
    log_file = os.path.join(MOD_DIR, BATTLE_QUIT_LOG)
    try:
        battle_quit_time = os.path.getmtime(log_file)
        if battle_quit_time > BATTLE_QUIT_TIME:
            BATTLE_QUIT_TIME = battle_quit_time
            return True
    except Exception:
        pass
    """

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
            return data["is_visible"]
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return False


class ConditionalQueue:
    def __init__(self):
        self.queue = Queue()
        self.enabled = False

    def put(self, obj):
        if self.enabled:
            self.queue.put(obj)

    def get_nowait(self):
        return self.queue.get_nowait()

    def clear(self):
        while not self.queue.empty():
            self.queue.get()


class Digest:
    def __init__(self):
        self.k_queue = ConditionalQueue()
        self.grpc = QueueClient()

        self.rate = 10.0

        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self):
        while True:

            while not is_battle_started():
                time.sleep(1)

            print('----------------------------')
            print('[%s] -*- Battle started! -*-' % datetime.now().isoformat(' '))   # noqa: E501
            print('----------------------------')

            while not is_enemy_detected():
                time.sleep(1)

            print('----------------------------')
            print('[%s] -*- Enemy detected! -*-' % datetime.now().isoformat(' '))   # noqa: E501
            print('----------------------------')

            dirpath = os.path.join(os.path.dirname(__file__), 'data')
            if not os.path.exists(dirpath):
                os.mkdir(dirpath)

            battle_id = int(time.time() * 1000)

            logdir = os.path.join(dirpath, str(battle_id))
            os.mkdir(logdir)

            header = ','.join(['image', 'health', 'max_health', 'yaw', 'speed',
                               'visible', 'ship_visible',
                               'e_health', 'e_max_health', 'e_yaw', 'e_speed',
                               'e_visible', 'e_ship_visible',
                               'key', 'mouse_x', 'mouse_y',
                               '\n'])
            with open(os.path.join(logdir, 'meta.csv'), 'a') as f:
                f.write(header)

            self.k_queue.enabled = True

            while not is_battle_ended():
                # time.sleep(1.0 / self.rate)

                # State
                timestamp = int(time.time() * 1000)
                img_path = str(timestamp) + '.png'
                ImageGrab.grab().save(os.path.join(logdir, img_path))
                player_info = self.grpc.get_player_info()
                enemy_info = self.grpc.get_player_info(is_enemy=True)

                fmt = '%f,%f,%f,%f,%s,%s'
                player_str = fmt % (player_info.health, player_info.max_health,
                                    player_info.yaw, player_info.speed,
                                    player_info.is_visible, player_info.is_ship_visible)    # noqa: E501
                enemy_str = fmt % (enemy_info.health, enemy_info.max_health,
                                   enemy_info.yaw, enemy_info.speed,
                                   enemy_info.is_visible, enemy_info.is_ship_visible)       # noqa: E501

                # Action
                try:
                    key_in = self.k_queue.get_nowait()
                except queue.Empty:
                    key_in = (timestamp, None)
                key_in = key_in[-1] or ''

                mouse = self.grpc.get_mouse_input(timestamp-1000)
                mouse = '%s,%s' % (mouse.dx, mouse.dy)

                args = (img_path, player_str, enemy_str, key_in, mouse)
                log = '%s,%s,%s,%s,%s\n' % args
                print('Logging:: %s' % log)
                with open(os.path.join(logdir, 'meta.csv'), 'a') as f:
                    f.write(log)

            self.k_queue.enabled = False
            self.k_queue.clear()

            print('--------------------------')
            print('[%s] -*- Battle ended! -*-' % datetime.now().isoformat(' '))
            print('--------------------------')


def main():
    digest = Digest()
    key_hook = KeyboardHook(queue=digest.k_queue)
    pointer = get_function_pointer(hook_procedure)
    if key_hook.install_hook_procedure(pointer):
        print("installed keyLogger")
    key_hook.run()


if __name__ == "__main__":
    main()
