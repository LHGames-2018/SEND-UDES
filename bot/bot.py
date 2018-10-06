import logging
import math
from typing import List
import pickle
import os.path

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
SIDE_MOVE_ACTIONS = {create_move_action(d): d for d in (UP, DOWN, LEFT, RIGHT)}

tick = -1
turn_counter = -1


class Bot:
    def __init__(self):
        self.player_info: Player = None
        self.actions = []
        self.last_kill: str = ""
        self.last_target = None
        self.last_score = None

    def before_turn(self, player_info: Player):
        if os.path.exists("last_score"):
            with open("last_score", "br") as fp:
                self.last_score = pickle.load(fp)
        if os.path.exists("last_kill"):
            with open("last_kill", "br") as fp:
                self.last_kill = pickle.load(fp)
        if os.path.exists("last_action"):
            with open("last_action", "br") as fp:
                self.last_action = pickle.load(fp)

        if self.last_score is None:
            self.last_score = player_info.Score
        
        if self.last_target is not None and player_info.Score != self.last_score:
            self.last_kill = self.last_target.Name or self.last_kill
            log.info("Detected score change!!!!!!")
        self.actions: List[ActionTemplate] = [GoHome(), GoHunt(self.last_kill), BuyUpgrade(), GoMine(), Mine()]
        self.player_info: Player = player_info
        self.last_target = None
        log.info("Current player state: {}".format(player_info))
        log.info("Last score was: {}".format(self.last_score))
        log.info("Last kill: {}".format(self.last_kill))

    def execute_turn(self, game_map: GameMap, visible_players: List[Player]):
        grid = Grid(30000, 30000, visible_players)
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
        for action in self.actions:
            weight = action.calculate_weight(self.player_info, game_map, visible_players)
            if weight > biggest_weight:
                biggest_weight = weight
                the_best_action = action
        log.info("Best action: {}".format(the_best_action))
        final_action = the_best_action.get_action(self.player_info, game_map, visible_players, grid)
        final_move_direction = SIDE_MOVE_ACTIONS.get(final_action)
        if final_move_direction is not None:
            going_to = self.player_info.Position + final_move_direction
            if going_to.to_coords() in grid.weights:
                # Cut down trees in our path
                final_action = create_attack_action(final_move_direction)
            else:
                for p in visible_players:
                    if p.Position == going_to:
                        self.last_target = p
                        final_action = create_attack_action(final_move_direction)

        log.info("Final action: {}".format(final_action))
        return final_action

    def get_mine_position(self):
        return None

    def after_turn(self):
        self.last_score = self.player_info.Score
        with open("last_score", "bw") as fp:
            pickle.dump(self.last_score, fp)
        with open("last_kill", "bw") as fp:
            pickle.dump(self.last_kill, fp)
        with open("last_action", "bw") as fp:
            pickle.dump(self.last_action, fp)
