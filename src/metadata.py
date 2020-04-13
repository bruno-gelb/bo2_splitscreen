def _get_image(game_name: str):
    # todo get them from steam / gog API
    if game_name == 'borderlands2':
        return 'https://upload.wikimedia.org/wikipedia/ru/a/a6/Borderlands2.jpg'
    elif game_name == 'overcooked':
        return 'https://steamcdn-a.akamaihd.net/steam/apps/448510/capsule_616x353_japanese.jpg?t=1567203965'
    elif game_name == 'overcooked2':
        return 'https://i.ytimg.com/vi/qpzmirQllT0/maxresdefault.jpg'
    elif game_name == 'shovel_knight':
        return 'https://i.ytimg.com/vi/bhG02JG7Sns/maxresdefault.jpg'


def get_metadata(game_name: str):
    return {
        'image': _get_image(game_name)
    }
