API_VERSION = 'API_v1.0'
MOD_NAME = 'AutoMod'
# Python 2.7

import time     # noqa: E402

CALLBACK_TICK = 1
callback_handle = None


def callback_func(*args, **kwargs):
    print 'callback(args=%s, kwargs=%s)' % (args, kwargs)


def battle_start(*args, **kwargs):
    global callback_handle

    with open('battle_start.log', 'w') as f:
        f.write('')

    callback_handle = callbacks.callback(CALLBACK_TICK, callback_func)  # noqa: F821


def battle_end(*args, **kwargs):
    with open('battle_end.log', 'w') as f:
        f.write('%s' % args[0])

    callbacks.cancel(callback_handle)   # noqa: F821
    callback_handle = None


def battle_quit(*args, **kwargs):
    with open('battle_quit.log', 'w') as f:
        f.write('')

    callbacks.cancel(callback_handle)   # noqa: F821
    callback_handle = None


def on_mouse_event(event):
    if callback_handle is None:
        return

    dx, dy = (event.dx, event.dy)
    with open('mouse%s.log' % time.time(), 'w') as f:
        f.write('{"dx": %d, "dy": %d}' % (dx, dy))


def got_ribbon(*args, **kwargs):
    ribbons = list(args)
    with open('rib%s.log' % time.time(), 'w') as f:
        f.write('{"ribbons": %s}' % ribbons)


events.onBattleStart(battle_start)      # noqa: F821
events.onBattleEnd(battle_end)          # noqa: F821
events.onMouseEvent(on_mouse_event)     # noqa: F821
events.onGotRibbon(got_ribbon)          # noqa: F821
