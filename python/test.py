#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import datetime
import queue
from threading import Thread
from multiprocessing import Queue

from PIL import ImageGrab

from grpc_client import QueueClient
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from win32py.win32py.keyboard_hook import KeyboardHook, hook_procedure  # noqa: E402, E501
from win32py.win32py.util import get_function_pointer   # noqa: E402


class Digest:
    def __init__(self):
        self.queue = Queue()
        self.grpc = QueueClient()

        self.rate = 1.0

        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    def digest_queue(self, queue):
        while True:
            item = queue.get()
            frame = ImageGrab.grab()
            mouse = self.grpc.get_mouse_input()
            print('digest:', item, frame.size, (mouse.dx, mouse.dy))
            # print('self.queue.size:', self.queue.qsize(), queue.qsize(), self.queue == queue)

    def run(self):
        while True:
            try:
                item = self.queue.get_nowait()
            except queue.Empty:
                item = None
            frame = ImageGrab.grab()
            mouse = self.grpc.get_mouse_input()
            print('[%s] %s, %s, %s' % (datetime.datetime.now().isoformat(' '), item, frame, (mouse.dx, mouse.dy)))
            time.sleep(1.0 / self.rate)


def main():
    digest = Digest()
    key_hook = KeyboardHook(queue=digest.queue)     # , digest_fn=digest.digest_queue)
    pointer = get_function_pointer(hook_procedure)
    if key_hook.install_hook_procedure(pointer):
        print("installed keyLogger")
    key_hook.run()


if __name__ == "__main__":
    # grpc_ = QueueClient()
    thread = Thread(target=main, daemon=True)
    thread.start()

    while True:
        time.sleep(0.1)
