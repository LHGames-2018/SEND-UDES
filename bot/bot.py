import logging
import math
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
        self.player_info: Player = None
        self.actions = []
        self.last_kill: str = ""
        self.last_action = None
        self.last_score = None

    def before_turn(self, player_info: Player):
        if self.last_score is None:
            self.last_score = player_info.Score
        
        if isinstance(self.last_action, GoHunt) and player_info.Score != self.last_score:
            self.last_kill = (self.last_action.target and self.last_action.target.Name) or self.last_kill
        self.actions: List[ActionTemplate] = [GoHome(), GoHunt(self.last_kill), BuyUpgrade(), GoMine(), Mine()]
        self.player_info: Player = player_info
        log.info("Current player state: {}".format(player_info))
        log.info("Last kill: {}".format(self.last_kill))

    def execute_turn(self, game_map: GameMap, visible_players: List[Player]):
        log.info("Yes osti sava? New log mister :p")
        grid = Grid(30000, 30000)
        for column in game_map.tiles:
            for t in column:
                if t.TileContent in (TileContent.Lava, TileContent.Player, TileContent.House, TileContent.Shop):
                    grid.walls.add(t.Position.to_coords())
                if t.TileContent in (TileContent.Wall, ):
                    grid.weights[t.Position.to_coords()] = math.ceil(5 / self.player_info.AttackPower)
                if t.TileContent in (TileContent.Resource, ):
                    grid.walls.add(t.Position.to_coords())
                    grid.resources[t.Position.to_coords()] = t
                    grid.resources_neighbours.update(grid.neighbors(t.Position.to_coords(), (0, 0)))

        grid.house = self.player_info.HouseLocation
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
        self.last_action = final_action
        return final_action

    def get_mine_position(self):
        return None

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        self.last_score = self.player_info.Score
