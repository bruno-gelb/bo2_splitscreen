import yaml


class _Config(object):
    def __init__(self):
        with open(r'config.yml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            self.games = config['games']


config = _Config()
