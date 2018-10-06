import logging
from typing import List

from bot import *
from bot.actions import *
from helper import *
from bot.search import *

log = logging.getLogger("main")
log_level = logging.DEBUG
log.setLevel(log_level)
handler = logging.StreamHandler()
handler.setLevel(log_level)
handler.setFormatter(logging.Formatter("%(asctime)-15s - %(levelname)s - line %(lineno)s - %(funcName)s: %(message)s"))
log.addHandler(handler)

UP    = Point(0, -1)
DOWN  = Point(0, 1)
LEFT  = Point(-1, 0)
RIGHT = Point(1, 0)

tick = -1
turn_counter = -1

class Bot:
    def __init__(self):
        pass

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo
        self.actions = [GoHome(), GoMine(), Mine()]


    def execute_turn(self, game_map: GameMap, visible_players: List[Player]):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        grid = Grid(game_map.visibleDistance * 2, game_map.visibleDistance * 2)
        for column in game_map.tiles:
            for tile in column:
                tile.TileContent
        biggest_weight = -1
        the_best_action: ActionTemplate = None
        for action in self.actions:
            weight = action.calculate_weight(self.PlayerInfo, game_map, visible_players)
            if weight > biggest_weight:
                biggest_weight = weight
                the_best_action = action
        return the_best_action.get_action(self.PlayerInfo, game_map, visible_players)

    def get_mine_position(self):
        return None

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
