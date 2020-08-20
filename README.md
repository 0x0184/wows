# wows
![Python 2](https://img.shields.io/badge/Python-2.7-blue.svg)
![Python 3](https://img.shields.io/badge/Python-3.6.8-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-v10.15.3-green.svg)
![](https://github.com/rapsealk/wows/workflows/Python%20application/badge.svg)

## 시작에 앞서..
* 필요한 소프트웨어를 설치한다.
    - World of Warships (NA) ([LINK](https://na.wargaming.net/en/games/wows))
    - Python3 (3.6.x Recommended) ([LINK](https://www.python.org/downloads/windows/))
    - Node.js (>= 10) ([LINK](https://nodejs.org/en/))
* 게임 클라이언트
    - 해상도: 1920x1080 or 1280x720
    - 전체화면

## 설정
* Git 레포지토리를 클론한다.
```bat
wows> git clone https://github.com/0x0184/wows.git -b feat/log --recurse-submodules [--depth 1]
```
* 월드 오브 워쉽 모드를 설치한다. (클라이언트 업데이트마다 반복)
```bat
wows> cd mods\
wows\mods> ./migrate.bat
wows\mods> python config.py
```
* Python 모듈을 설치한다.
```bat
wows> cd python\
wows\python> pip install -r requirements.txt
```
* Node.js 패키지를 설치한다.
```bat
wows> cd node\
wows\node> npm install
```
* Python에서 사용할 Protobuf 클래스 파일을 생성한다.
```bat
wows> cd proto\
wows\proto> ./protoc.bat
```
* World of Warships (NA) 클라이언트를 실행한다. ([아이디 목록](https://github.com/0x0184/wows/blob/feat/log/LOGIN.md))
* 필요한 스크립트를 실행시킨다.
```bat
:: 1. Node.js
wows> cd node\
wows\node> npm run start
:: 2. Python
wows> cd python\
wows\python> python main.py
```