import logging
import os
from subprocess import run
from typing import Union, Tuple

import click

logging.basicConfig(level=logging.DEBUG)


def get_screen_resolution() -> Tuple[int, int]:
    cmd = 'wmic desktopmonitor get screenwidth, screenheight'
    return tuple(map(int, os.popen(cmd).read().split()[-2::][::-1]))


def autodiscover_sandboxie() -> Union[None, str]:
    # todo implement autodiscover
    if True:
        return r'C:\Program Files\Sandboxie\Start.exe'
    else:
        return None


def autodiscover_bo2() -> Union[None, str]:
    # todo implement autodiscover
    if True:
        return 'D:\Steam\steamapps\common\Borderlands_2_RU\Binaries\Win32\Borderlands2.exe'
    else:
        return None


def launch(bo2_path: str, players: int, split_type: Union[str, None],
           screen_width: int, screen_height: int) -> None:
    half_screen_width = int(screen_width / 2)
    half_screen_height = int(screen_height / 2)

    logging.debug(f'Launching {bo2_path} for {players} players with split_type {split_type} ..')

    if players == 1:
        run([
            bo2_path,
            '-nolauncher',
            '-NoStartupMovies',
        ])

    elif players == 2 and split_type == 'vertical':
        print('This is not supported yet, sorry.')

    elif players == 2 and split_type == 'horizontal':
        # call('taskkill /f /im explorer.exe')

        logging.info('Launching the first instance ..')
        player_id = 0

        run([
            autodiscover_sandboxie(),
            f'/box:bo2_splitscreen_{player_id}',
            bo2_path,
            '-nolauncher',
            '-NoStartupMovies',
            '-WindowedFullscreen',
            '-AlwaysFocus',

            f'-ResX={screen_width}',
            f'-ResY={half_screen_height}',
            '-WindowPosX=0',
            '-WindowPosY=0',

            f'-SaveDataId={player_id}',
            f'-ControllerOffset={player_id}',
        ])

        # call('start explorer.exe')

        logging.info('Launching the second instance ..')
        player_id = 1

        run([
            autodiscover_sandboxie(),
            f'/box:bo2_splitscreen_{player_id}',
            bo2_path,
            '-nolauncher',
            '-NoStartupMovies',
            '-WindowedFullscreen',
            '-AlwaysFocus',

            f'-ResX={screen_width}',
            f'-ResY={half_screen_height}',
            '-WindowPosX=0',
            f'-WindowPosY={half_screen_height}',

            f'-SaveDataId={player_id}',
            f'-ControllerOffset={player_id}',
        ])

    elif players == 3:
        print('This is not supported yet, sorry.')

    elif players == 4:
        print('This is not supported yet, sorry.')

    logging.debug('All launched.')


@click.command()
def main():
    screen_width, screen_height = get_screen_resolution()
    logging.debug(f'Screen resolution is {screen_width}x{screen_height}')
    bo2_path = autodiscover_bo2()
    if not bo2_path:
        click.echo("Couldn't' find a path to your Borderlands2.exe")
        bo2_path = click.prompt('Please enter it:', type=str)
        while not os.path.isfile(bo2_path):
            bo2_path = click.prompt(
                "That's not a valid path: no such file exists. Please enter it once again",
                type=str
            )
    logging.debug(f'bo2_path={bo2_path}')

    if 'steamapps' in bo2_path:
        # todo autocheck if Steam is running or not. If it's not, launch the Steam first
        click.echo('WARNING: make sure Steam is running before proceeding')

    split_type = None
    players = click.prompt('How many players (1-4)', type=int, default=2, show_choices=False)
    if players == 2:
        split_type = click.prompt('How you prefer to split your screen?',
                                  type=click.Choice(['vertical', 'horizontal']),
                                  show_choices=True,
                                  default='horizontal')
    launch(bo2_path, players, split_type, screen_width, screen_height)


if __name__ == '__main__':
    main()
