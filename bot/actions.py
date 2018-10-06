import logging
from typing import List
from bot.search import Grid
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

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):
        pass


class GoMine(ActionTemplate):

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        calculated_weight = 0

        if player_info.CarriedResources == 0:
            calculated_weight = 1

        return calculated_weight

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):
        closest_position = Point(-100, -100)
        closest_distance = 1000
        for resource in grid.resources.values():
            current_distance = resource.Position.dist_to(player_info.Position)
            if current_distance < closest_distance:
                closest_position = resource.Position
                closest_distance = current_distance

        next_direction = grid.a_star_search(player_info.Position.to_coords(), closest_position.to_coords())

        return create_move_action(next_direction)


class Mine(ActionTemplate):

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        calculated_weight = 0

        if game_map.getTileAt(player_info.Position + Point(-1, 0)) == TileContent.Resource\
                or game_map.getTileAt(player_info.Position + Point(1, 0)) == TileContent.Resource\
                or game_map.getTileAt(player_info.Position + Point(0, -1)) == TileContent.Resource\
                or game_map.getTileAt(player_info.Position + Point(0, 1)) == TileContent.Resource:
            calculated_weight = 1

        return calculated_weight

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):
        return create_collect_action(UP)


class GoHome(ActionTemplate):

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        calculated_weight = 0

        if player_info.CarriedResources == player_info.CarryingCapacity:
            calculated_weight = 1

        return calculated_weight

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):

        return create_move_action(UP)