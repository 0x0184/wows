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
    - 함선: II Chester (`U.S.A`, `Cruiser`)

## 설정
* Git 레포지토리를 클론한다.
```bat
> git clone https://github.com/0x0184/wows.git -b feat/log --recurse-submodules
> cd wows\
```
* 월드 오브 워쉽 모드를 설치한다. (클라이언트 업데이트마다 반복)
```bat
wows> cd mods\
wows\mods> .\migrate.bat
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
wows\proto> .\protoc.bat queue.proto
```
* World of Warships (NA) 클라이언트를 실행한다. ([아이디 목록](https://github.com/0x0184/wows-authentications/blob/master/README.md))
* 필요한 스크립트를 실행시킨다.
```bat
:: 1. Node.js
wows> cd node\
wows\node> npm run start
:: 2. Python
wows> cd python\
wows\python> python main.py
```
* 게임을 진행하면 적이 발견된 시점부터 게임이 종료될 때까지 데이터가 저장된다.
* `F1`키를 누르면 파이썬 프로세스가 종료되고, 터미널에서 `Ctrl`+`c`를 입력하면 Node.js 프로세스가 종료된다.
* 로그인한 계정의 [Google Drive](https://drive.google.com/)에 데이터를 업로드한다.

## 게임 내 설정
* 인게임 환경에서 `ESC` 버튼을 눌러 메뉴에 들어간 후, `Settings` 항목을 클릭한다.
![Settings](https://github.com/0x0184/wows/blob/feat/log/resources/settings.png)
* 상단의 `Controls` 메뉴로 이동한 후, 두 가지 설정을 변경한다.
    - `Track the locked target` 옵션을 해제한다. [ ]
    - `Weapons` - `Fire` 버튼을 `LMB`에서 `Space`로 변경한다. `LMB` 버튼을 클릭한 후 스페이스바를 입력하면 된다.
    - 하단의 `Apply` 버튼을 클릭하여 변경사항을 적용한다.
![Settings_Controls](https://github.com/0x0184/wows/blob/feat/log/resources/settings_controls.png)

## 게임 진행 방법
* 상단의 모드 선택 버튼을 클릭한다. (기본 모드는 Co-op Battle이다.)
![Game mode](https://github.com/0x0184/wows/blob/feat/log/resources/01.png)
* 연습 게임을 생성하기 위하여 **Training**을 선택한다.
![Battle Type Training](https://github.com/0x0184/wows/blob/feat/log/resources/02.png)
* 하단의 `CREATE BATTLE` 버튼을 클릭한다.
![Create Battle](https://github.com/0x0184/wows/blob/feat/log/resources/03.png)
* `CREATE` 버튼을 클릭해서 기본 옵션대로 방을 생성한다.
![Create](https://github.com/0x0184/wows/blob/feat/log/resources/04.png)
* Bravo 팀의 `Add Player` 버튼을 클릭한 후, 순서대로 `Bot`->`U.S.A`->`Cruiser`->`II CHESTER`를 선택한다.
    - [x] Bot is moving
    - [x] Bot is armed
* 두 옵션을 체크한 후 `ADD` 버튼을 클릭하여 봇을 추가한다.
![Add Bot Player](https://github.com/0x0184/wows/blob/feat/log/resources/05.png)
* 봇이 추가되었음을 확인한 후, 자신의 전함도 `II CHESTER`로 설정되었음을 확인한다.
    - 원하는 전함은 더블클릭하여 선택할 수 있다.
* `READY` 버튼을 클릭한 후 상단의 `BATTLE!` 버튼을 클릭하여 게임에 입장한다.
![Ready and battle](https://github.com/0x0184/wows/blob/feat/log/resources/06.png)
* `Alpha`팀의 경우 맵의 11시 지역에서 시작하는데, 맵의 중앙지역으로 이동해서 적과 교전하면 된다.
* 데이터는 적이 발견된 시점부터 게임이 종료될 때까지 수집된다.
* 지원되는 입력은 다음과 같다.

|   종류   |   입 력   |
| -------- |:--------:|
| 속도 조절 | `w`, `s` |
|   회전   | `q`, `e` |
|   조준   | `Mouse`  |
|   발포   | `Space`  |

![In-Game](https://github.com/0x0184/wows/blob/feat/log/resources/08.png)
