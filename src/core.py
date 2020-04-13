from typing import Union

from handlers.borderlands2 import bo2_handler


def resolve_handler(game_name: str) -> Union[None, object]:
    if game_name == 'borderlands2':
        return bo2_handler
