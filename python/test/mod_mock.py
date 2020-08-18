#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import json
import time
import random
from datetime import datetime

with open(os.path.join(os.path.dirname(__file__),
                       '..',
                       '..',
                       'config.json')) as f:
    config = json.loads(f.read())
    MOD_DIR = config["mod"]


class ModMock:

    def __init__(self):
        self.rate = 1.0

    def run(self):
        while True:
            args = (random.randint(-100, 100),
                    random.randint(-100, 100),
                    int(time.time() * 1000))
            data = '{"dx": %d, "dy": %d, "timestamp": %d}' % args
            with open(os.path.join(MOD_DIR, 'mouse.log'), 'w') as f:
                f.write(data)
            print('[%s] Mouse: %s' % (datetime.now().isoformat(' '), data))

            args = (12345, 1, 9999, 18400, 18400, random.random(), random.random(), 1, 1)
            data = '''{"id": %d, "team_id": %d, "ship_id": %s,
                       "health": %f, "max_health": %d,
                       "yaw": %f, "speed": %f,
                       "is_visible": %r, "is_ship_visible": %r}''' % args
            print('[%s] Player: %s' % (datetime.now().isoformat(' '), data))
            with open(os.path.join(MOD_DIR, 'player.log'), 'w') as f:
                f.write(data)
            time.sleep(1.0 / self.rate)


if __name__ == "__main__":
    mock = ModMock()
    mock.run()
