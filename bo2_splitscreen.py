import asyncio
import logging
import os
import threading
from ctypes import windll
from subprocess import run, call
from typing import Union, Tuple

import click
import psutil
import win32api


def detect_current_display() -> int:
    win_id = windll.user32.GetForegroundWindow()
    monitor_default_to_nearest = 2
    active_monitor_id = windll.user32.MonitorFromWindow(win_id, monitor_default_to_nearest)
    logging.debug(f'active_monitor_id={active_monitor_id}')

    monitors = win32api.EnumDisplayMonitors()
    logging.debug(f'monitors={monitors}')
    for i, monitor in enumerate(monitors):
        logging.debug(win32api.GetMonitorInfo(monitor[0].handle))
        display_id = int(win32api.GetMonitorInfo(monitor[0].handle)['Device'].split('DISPLAY')[-1])
        if monitor[0].handle == active_monitor_id:
            logging.debug(f'display_id={display_id}')
            return display_id


def detect_current_resolution() -> Tuple[int, int]:
    current_display = detect_current_display()
    logging.debug(f'current_display={current_display}')
    cmd = 'wmic path Win32_VideoController get VideoModeDescription'

    resolutions = list(reversed([l.strip().split('x')[:2]
                                 for l in os.popen(cmd).read().split('\n') if l and 'VideoModeDescription' not in l]))

    logging.debug(f'resolutions={resolutions}')

    return int(resolutions[current_display - 1][0]), int(resolutions[current_display - 1][1])


logging.basicConfig(level=logging.DEBUG)
ASYNCIO_TIMEOUT = 5
SCREEN_WIDTH, SCREEN_HEIGHT = detect_current_resolution()
HALF_SCREEN_WIDTH = int(SCREEN_WIDTH / 2)
HALF_SCREEN_HEIGHT = int(SCREEN_HEIGHT / 2)


def autodiscover_sandboxie() -> Union[None, str]:
    # todo implement autodiscover
    if True:
        return r'C:\Program Files\Sandboxie\Start.exe'
    else:
        return None


def hide_taskbar() -> None:
    call('taskkill /f /im explorer.exe')


def show_taskbar() -> None:
    call(r'.\show_taskbar.bat')


def periodic(period):
    def scheduler(fcn):
        async def wrapper(*args, **kwargs):
            while True:
                asyncio.create_task(fcn(*args, **kwargs))
                await asyncio.sleep(period)

        return wrapper

    return scheduler


@periodic(ASYNCIO_TIMEOUT)
async def hide_taskbar_when_game_is_up(*args, **kwargs) -> None:
    await asyncio.sleep(ASYNCIO_TIMEOUT)
    for p in psutil.process_iter(attrs=['pid', 'name']):
        if p.info['name'] == 'Borderlands2.exe':
            hide_taskbar()

            this = asyncio.ensure_future(hide_taskbar_when_game_is_up())
            this.cancel()

            await show_taskbar_when_game_is_over()


@periodic(ASYNCIO_TIMEOUT)
async def show_taskbar_when_game_is_over(*args, **kwargs) -> None:
    await asyncio.sleep(ASYNCIO_TIMEOUT)
    for p in psutil.process_iter(attrs=['pid', 'name']):
        if p.info['name'] == 'explorer.exe':
            return
        if p.info['name'] == 'Borderlands2.exe':
            return
    show_taskbar()


def autodiscover_bo2() -> Union[None, str]:
    # todo implement autodiscover
    if True:
        return 'D:\Steam\steamapps\common\Borderlands_2_RU\Binaries\Win32\Borderlands2.exe'
    else:
        return None


def loop_in_thread(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(hide_taskbar_when_game_is_up())


def launch_for_player(bo2_path: str, player_id: int,
                      width: int = SCREEN_WIDTH, height: int = SCREEN_HEIGHT,
                      w_position: int = 0, h_position: int = 0) -> None:
    logging.info(f'Launching the player {player_id + 1} instance ..')
    run([
        autodiscover_sandboxie(),
        f'/box:bo2_splitscreen_{player_id}',
        bo2_path,
        '-nolauncher',
        '-NoStartupMovies',
        '-WindowedFullscreen',
        '-AlwaysFocus',

        f'-SaveDataId={player_id}',
        f'-ControllerOffset={player_id}',

        f'-ResX={width}',
        f'-ResY={height}',
        f'-WindowPosX={w_position}',
        f'-WindowPosY={h_position}',
    ])


def launch_splitscreen(bo2_path: str, players: int) -> None:
    logging.debug(f'{players} players selected. Launching ..')

    if players == 1:
        player_id = 0
        launch_for_player(bo2_path, player_id)

    elif players == 2:
        player_id = 0
        launch_for_player(bo2_path, player_id,
                          height=HALF_SCREEN_HEIGHT)

        player_id = 1
        launch_for_player(bo2_path, player_id,
                          height=HALF_SCREEN_HEIGHT, h_position=HALF_SCREEN_HEIGHT)

    elif players >= 3:
        player_id = 0
        launch_for_player(bo2_path, player_id,
                          width=HALF_SCREEN_WIDTH, height=HALF_SCREEN_HEIGHT)

        player_id = 1
        launch_for_player(bo2_path, player_id,
                          width=HALF_SCREEN_WIDTH, height=HALF_SCREEN_HEIGHT,
                          w_position=HALF_SCREEN_WIDTH)

        player_id = 2
        launch_for_player(bo2_path, player_id,
                          width=HALF_SCREEN_WIDTH, height=HALF_SCREEN_HEIGHT,
                          h_position=HALF_SCREEN_HEIGHT)

        if players == 4:
            player_id = 3
            launch_for_player(bo2_path, player_id,
                              width=HALF_SCREEN_WIDTH, height=HALF_SCREEN_HEIGHT,
                              w_position=HALF_SCREEN_WIDTH, h_position=HALF_SCREEN_HEIGHT)


@click.command()
def main():
    logging.debug(f'Screen resolution is {SCREEN_WIDTH}x{SCREEN_HEIGHT}')

    bo2_path = autodiscover_bo2()
    if not bo2_path:
        click.echo("Couldn't' find a path to your Borderlands2.exe")
        bo2_path = click.prompt('Please enter it', type=str)
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

    loop = asyncio.get_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop,))
    t.start()

    launch_splitscreen(bo2_path, players)


if __name__ == '__main__':
    main()
