API_VERSION = 'API_v1.0'
MOD_NAME = 'AutoMod'


def battle_start(*args, **kwargs):
    with open('battle_start.log', 'w') as f:
        f.write('')


def battle_end(*args, **kwargs):
    with open('battle_end.log', 'w') as f:
        f.write('%s' % args[0])


events.onBattleStart(battle_start)
events.onBattleEnd(battle_end)
