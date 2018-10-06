import logging
from typing import List

from helper import *

log = logging.getLogger("main")
from helper.aiHelper import *

UP    = Point(0, -1)
DOWN  = Point(0, 1)
LEFT  = Point(-1, 0)
RIGHT = Point(1, 0)

class ActionTemplate:

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        pass

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        pass


class GoMine(ActionTemplate):

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        return 1

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        return create_move_action(UP)


class Mine(ActionTemplate):

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        return 0

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        return create_collect_action(UP)


class GoHome(ActionTemplate):

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        return 0

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        return create_move_action(UP)