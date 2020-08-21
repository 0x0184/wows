#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import datetime

DRIVES = ['C', 'D', 'E', 'F']
GAME_PATH = ['Games', 'World_of_Warships_NA', 'bin']
MOD_NAME = 'AutoMod'

if __name__ == "__main__":
    installed_path = ''
    for drive in DRIVES:
        path = os.path.join(drive + ':\\', *GAME_PATH)
        print('[%s] Check: %s' % (datetime.datetime.now().isoformat(' '), path))    # noqa: E501
        if os.path.exists(path):
            installed_path = path
            break
    if not installed_path:
        print('Game not found')
        sys.exit(-1)
    else:
        print('Installed at:', path)

    build_numbers = os.listdir(installed_path)
    path = os.path.join(path, build_numbers[-1], 'res_mods')

    versions = os.listdir(path)
    path = os.path.join(path, versions[-1], 'PnFMods', MOD_NAME)

    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as f:
        config = json.loads(f.read())
    config['mod'] = path
    with open(config_path, 'w') as f:
        f.write(json.dumps(config))
