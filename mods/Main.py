API_VERSION = 'API_v1.0'
MOD_NAME = 'AutoMod'
# Python 2.7

import time     # noqa: E402

CALLBACK_TICK = 1
callback_handle = None

MAX_HEALTH = 18400
dx, dy = (0, 0)
tick = 0
ribbon_number = 0


class PlayerInfo:
    def __init__(self, dict_):
        self.id = dict_["id"]
        self.team_id = dict_["teamId"]
        self.ship_id = dict_["shipId"]

        data = dict_["shipGameData"]
        self.health = data["health"] or MAX_HEALTH
        self.health_max = data["maxHealth"] or MAX_HEALTH
        self.yaw = data["yaw"] or 0
        try:
            self.speed = data["speed"] or 0
        except:     # noqa: E722, KeyError
            self.speed = 0

        self.is_visible = data["isVisible"] or False
        self.is_ship_visible = data["isShipVisible"] or 0

    def __str__(self):
        args = (self.id, self.team_id, self.ship_id,
                self.health, self.health_max, self.yaw, self.speed,
                self.is_visible, self.is_ship_visible)
        return '''{"id": %d, "teamId": %d, "shipId": %s,
                   "health": %f, "maxHealth": %d,
                   "yaw": %f, "speed": %f,
                   "isVisible": %r, "isShipVisible": %r}''' % args

    def assign(self, info):
        self.__dict__ = info.__dict__


# def parse_player(dict_):
#     pass
def reset():
    global CACHE_PLAYER, CACHE_ENEMY, dx, dy, tick, ribbon_number
    obj = {
        "id": -1,
        "teamId": -1,
        "shipId": -1,
        "shipGameData": {
            "health": MAX_HEALTH,
            "maxHealth": MAX_HEALTH,
            "yaw": 0,
            "speed": 0,
            "isVisible": False,
            "isShipVisible": False
        }
    }
    CACHE_PLAYER = PlayerInfo(obj)
    CACHE_ENEMY = PlayerInfo(obj)
    with open('enemy.log', 'w') as f:
        f.write(str(CACHE_ENEMY))

    dx, dy = (0, 0)
    tick = 0
    ribbon_number = 0


def callback_func(*args, **kwargs):
    global dx, dy, tick

    player = battle.getSelfPlayerInfo()     # noqa: F821
    player = PlayerInfo(player)

    with open('player.log', 'w') as f:
        f.write(str(player))

    players = battle.getPlayersInfo()           # noqa: F821
    bots = [battle.getPlayerInfo(bot["id"])     # noqa: F821
            for bot in players.values() if bot["id"] != player.id]
    bots = [PlayerInfo(bot) for bot in bots]

    if bots:
        with open('enemy.log', 'w') as f:
            f.write(str(bots[0]))

    dx_, dy_ = (dx, dy)
    dx, dy = (0, 0)
    tick = (tick + 1) % 4
    with open('mouse%d.log' % tick, 'w') as f:
        f.write('{"dx": %d, "dy": %d, "timestamp": %d}' % (dx_, dy_, int(time.time() * 1000)))  # noqa: E501


def battle_start(*args, **kwargs):
    global callback_handle

    with open('battle_start.log', 'w') as f:
        f.write('')

    reset()

    callback_handle = callbacks.callback(CALLBACK_TICK, callback_func)  # noqa: F821, E501


def battle_end(*args, **kwargs):
    global callback_handle

    with open('battle_end.log', 'w') as f:
        f.write('%s' % args[0])

    callbacks.cancel(callback_handle)   # noqa: F821
    callback_handle = None


def battle_quit(*args, **kwargs):
    global callback_handle

    with open('battle_quit.log', 'w') as f:
        f.write('')

    callbacks.cancel(callback_handle)   # noqa: F821
    callback_handle = None


def on_mouse_event(event):
    global dx, dy

    if callback_handle is None:
        return

    dx += event.dx
    dy += event.dy


def got_ribbon(*args, **kwargs):
    global ribbon_number

    ribbons = list(args)
    ribbon_number += 1
    with open('ribbon%d.log' % ribbon_number, 'w') as f:
        f.write('{"ribbons": %s}' % ribbons)


events.onBattleStart(battle_start)      # noqa: F821
events.onBattleEnd(battle_end)          # noqa: F821
events.onBattleQuit(battle_quit)        # noqa: F821
events.onMouseEvent(on_mouse_event)     # noqa: F821
# events.onGotRibbon(got_ribbon)          # noqa: F821
