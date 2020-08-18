# wows
![Python 2](https://img.shields.io/badge/Python-2.7-blue.svg)
![Python 3](https://img.shields.io/badge/Python-3.6.8-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-v10.15.3-green.svg)
![](https://github.com/rapsealk/wows/workflows/Python%20application/badge.svg)

## CAUTION!
* Please install Mods **BEFORE** running the game client.

## Installation
```bat
git clone https://github.com/0x0184/wows.git -b feat/log --recurse-submodules [--depth 1]
cd node/ && npm install && cd ../
cd mods/ && ./migrate.bat [<REGION> [<DRIVE>]]  :: ./migrate.bat NA C
cd ../python
python main.py
```