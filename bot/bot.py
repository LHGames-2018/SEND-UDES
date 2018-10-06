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

UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)

tick = -1
turn_counter = -1


class Bot:
    def __init__(self):
        self.player_info = None
        self.actions = []

    def before_turn(self, player_info: Player):
        self.player_info: Player = player_info
        self.actions: List[ActionTemplate] = [BuyUpgrade(), GoHome(), GoMine(), Mine()]

    def execute_turn(self, game_map: GameMap, visible_players: List[Player]):
        log.info("Levels: Carrying: {} Speed: {}".format(self.player_info.CarryingCapacity, self.player_info.CollectingSpeed))
        log.info("Money: {}".format(self.player_info.TotalResources))
        grid = Grid(30000, 30000)
        for column in game_map.tiles:
            for t in column:
                if t.TileContent in (TileContent.Wall, TileContent.Lava):
                    grid.walls.add(t.Position.to_coords())
                if t.TileContent in (TileContent.Resource, ):
                    grid.resources[t.Position.to_coords()] = t
                    grid.resources_neighbours.update(grid.neighbors(t.Position.to_coords()))
                if t.TileContent in (TileContent.House, ):
                    grid.house = t.Position
        if self.player_info.position == self.player_info.HouseLocation:
            log.info("at home, trying to upgrade")
            if self.actions[0].calculate_weight(self.player_info, game_map, visible_players) > 0:
                log.warning("WE UPGRADEEEEEEE")
                return self.actions[0].get_action(self.player_info, game_map, visible_players, grid)
        biggest_weight = -1
        the_best_action: ActionTemplate = None
        log.info("Determining best action: {}".format(the_best_action))
        for action in self.actions:
            weight = action.calculate_weight(self.player_info, game_map, visible_players)
            log.info("Weight for action {}: {}".format(action, weight))
            if weight > biggest_weight:
                biggest_weight = weight
                the_best_action = action
        log.info("Best action: {}".format(the_best_action))
        final_action = the_best_action.get_action(self.player_info, game_map, visible_players, grid)
        log.info("Final action: {}".format(final_action))
        return final_action

    def get_mine_position(self):
        return None

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
