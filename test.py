#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import unittest
import os
from PIL import Image

import auto
from auto import MOD_DIR, BATTLE_START_LOG, BATTLE_END_LOG


class BattleTest(unittest.TestCase):

    def test_battle_started(self):
        try:
            open(os.path.join(MOD_DIR, BATTLE_START_LOG), 'x')
        except FileExistsError:
            pass
        self.assertTrue(auto.is_battle_started())

    def test_battle_ended(self):
        try:
            with open(os.path.join(MOD_DIR, BATTLE_END_LOG), 'w') as f:
                f.write('0')
        except FileExistsError:
            pass
        self.assertTrue(auto.is_battle_ended())

    def test_replay_button_enabled(self):
        frame = Image.open('images/replay_enabled.png')
        self.assertTrue(auto.is_replay_button_enabled(frame))
        frame = Image.open('images/replay_not_enabled.png')
        self.assertFalse(auto.is_replay_button_enabled(frame))


if __name__ == "__main__":
    import sys
    assert sys.platform == 'win32'

    unittest.main()
