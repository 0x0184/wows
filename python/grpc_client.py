#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time
# from collections import deque
from threading import Thread, get_ident
from multiprocessing import Process, Queue

import grpc
from PIL import ImageGrab

import queue_pb2
import queue_pb2_grpc
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# from win32py import win32py     # noqa: E402
from win32py.win32py.keyboard_hook import KeyboardHook, hook_procedure  # noqa: E402
from win32py.win32py.util import get_function_pointer   # noqa: E402


class QueueClient:

    def __init__(self, queue=None, addr='127.0.0.1', port=61084):
        channel = grpc.insecure_channel('%s:%d' % (addr, port))
        self.stub = queue_pb2_grpc.QueueServiceStub(channel)

        """
        self.keys = []  # deque(maxlen=100)   # (timestamp, key)

        self.queue = queue or Queue()

        self.keyboard_hook = KeyboardHook(self.queue, digest_fn=digest_key_hook)
        # self.keyboard_hook = KeyboardHook(digest_fn=self.digest_key_hook)
        pointer = get_function_pointer(hook_procedure)
        self.keyboard_hook.install_hook_procedure(pointer, dwThreadId=get_ident())
        self.k_hook_thread = Thread(target=self.keyboard_hook.run, daemon=True)
        # self.k_hook_thread = Process(target=self.keyboard_hook.run, daemon=True)
        self.k_hook_thread.start()

        # self.k_digest_thread = Thread(target=self._digest_key_hook, args=(self.queue,), daemon=True)
        # self.k_digest_thread.start()

        self.rate = 1.0
        """

    def get_mouse_input(self, timestamp=0):
        if not timestamp:
            timestamp = int(time.time() * 1000) - 1000
        try:
            request = queue_pb2.MouseInputRequest(timestamp=timestamp)
            inp = self.stub.GetMouseInput(request)
            print('inp.data:', inp.data.dx, inp.data.dy)
            return inp.data
        except grpc._channel._InactiveRpcError as e:
            print('[Mouse] grpc._channel._InactiveRpcError:', e)
        except Exception as e:
            print('[Mouse] Exception:', e)
        return queue_pb2.MouseInput()

    """
    def get_keyboard_input(self, timestamp=0):
        if not timestamp:
            timestamp = int(time.time() * 1000)
        try:
            key = self.keys[-1][1]
            # self.keys = deque(filter(lambda x: x[0] > timestamp, self.keys), maxlen=100)
            # print('self.keys[0]:', self.keys[0])
            self.keys.clear()
            # return self.keys[0][1]
            return key
        except IndexError as e:
            print('[Keyboard] IndexError:', e)
        return None

    def run(self):
        while True:
            now = int(time.time() * 1000)
            print('[gRPC] %s' % now)
            frame = ImageGrab.grab()
            click = False
            mouse_input = self.get_mouse_input(timestamp=now) or queue_pb2.MouseInput()
            keyboard_input = self.get_keyboard_input(timestamp=now)
            args = (frame.size, click, mouse_input.dx, keyboard_input)
            print('frame=%s, click=%s, mouse.dx=%s, keyboard=%s' % args)
            time.sleep(1.0 / self.rate)
    """


"""
def digest_key_hook(queue):
    print('_digest_key_hook:')
    while True:
        item = queue.get()
        print('Key:', item, queue.size())
        # self.keys.append(queue.get())
"""


if __name__ == "__main__":
    client = QueueClient()

    # thread = Thread(target=client.run, daemon=True)
    # thread.start()

    # client.keyboard_hook.run()

    # client.run()
