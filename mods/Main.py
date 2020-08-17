API_VERSION = 'API_v1.0'
MOD_NAME = 'AutoMod'
# Python 2.7

import time     # noqa: E402

CALLBACK_TICK = 1
callback_handle = None

MAX_HEALTH = 18400
dx, dy = (0, 0)


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
    global CACHE_PLAYER, CACHE_ENEMY, dx, dy
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
    dx, dy = (0, 0)


def callback_func(*args, **kwargs):
    global dx, dy

    player = battle.getSelfPlayerInfo()     # noqa: F821
    """
    player_id = player["id"]
    player_team_id = player["teamId"]
    player_ship_id = player["shipId"]
    player_data = player["shipGameData"]
    try:
        player_knot = player_data["speed"]
    except KeyError:
        player_knot = 0
    player_health = player_data["health"]
    player_health_max = player_data["maxHealth"]
    player_yaw = player_data["yaw"]
    """
    player = PlayerInfo(player)

    players = battle.getPlayersInfo()           # noqa: F821
    bots = [battle.getPlayerInfo(bot["id"])     # noqa: F821
            for bot in players.values() if bot["id"] != player.id]

    if bots:
        with open('enemy-raw.log', 'w') as f:
            f.write(str(bots[0]))
    """
    for bot in bots:
        bot_id = bot["id"]
        bot_team_id = bot["teamId"]
        bot_ship_id = bot["shipId"]
        bot_data = bot["shipGameData"]
        bot_health = bot_data["health"]
        bot_health_max = bot_data["maxHealth"]
        bot_yaw = bot_data["yaw"]
        bot_visibility = bot_data["isVisible"]
        bot_ship_visibility = bot_data["isShipVisible"]
    """
    bots = [PlayerInfo(bot) for bot in bots]

    with open('player.log', 'w') as f:
        f.write(str(player))

    if bots:
        with open('enemy.log', 'w') as f:
            f.write(str(bots[0]))

    dx_, dy_ = (dx, dy)
    dx, dy = (0, 0)
    with open('mouse%d.log' % int(time.time() * 1000), 'w') as f:
        f.write('{"dx": %d, "dy": %d}' % (dx_, dy_))


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

    """
    if callback_handle is None:
        return

    dx, dy = (event.dx, event.dy)
    with open('mouse%s.log' % int(time.time() * 1000), 'w') as f:
        f.write('{"dx": %d, "dy": %d}' % (dx, dy))
    """
    dx += event.dx
    dy += event.dy

    # with open('mouse.log', 'w') as f:
    #     f.write('{"dx": %d, "dy": %d}' % (dx, dy))


def got_ribbon(*args, **kwargs):
    ribbons = list(args)
    with open('ribbon%s.log' % int(time.time() * 1000), 'w') as f:
        f.write('{"ribbons": %s}' % ribbons)


events.onBattleStart(battle_start)      # noqa: F821
events.onBattleEnd(battle_end)          # noqa: F821
events.onBattleQuit(battle_quit)        # noqa: F821
events.onMouseEvent(on_mouse_event)     # noqa: F821
# events.onGotRibbon(got_ribbon)          # noqa: F821
