import logging
import os
from ctypes import windll
from subprocess import run, call
from typing import Union, Tuple

import click
import win32api

logging.basicConfig(level=logging.DEBUG)


def detect_current_display() -> int:
    win_id = windll.user32.GetForegroundWindow()
    monitor_default_to_nearest = 2
    active_monitor_id = windll.user32.MonitorFromWindow(win_id, monitor_default_to_nearest)

    monitors = win32api.EnumDisplayMonitors()
    for i, monitor in enumerate(monitors):
        if monitor[0].handle == active_monitor_id:
            return i + 1


def detect_current_resolution() -> Tuple[int, int]:
    current_display = detect_current_display()
    logging.debug(f'current_display={current_display}')
    cmd = 'wmic path Win32_VideoController get VideoModeDescription'

    resolutions = ([l.strip().split('x')[:2]
                    for l in os.popen(cmd).read().split('\n') if l and 'VideoModeDescription' not in l])

    return int(resolutions[current_display - 1][0]), int(resolutions[current_display - 1][1])


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


def launch(bo2_path: str, players: int,
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

    elif players == 2:
        call('taskkill /f /im explorer.exe')

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
    screen_width, screen_height = detect_current_resolution()
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

    players = click.prompt('How many players (1-4)', type=int, default=2, show_choices=False)
    launch(bo2_path, players, screen_width, screen_height)


if __name__ == '__main__':
    main()
