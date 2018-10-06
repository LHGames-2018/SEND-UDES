import logging 
log = logging.getLogger("main")
from helper.aiHelper import *

UP    = Point(0, -1)
DOWN  = Point(0, 1)
LEFT  = Point(-1, 0)
RIGHT = Point(1, 0)

class ActionTemplate:

    def calculate_weight(self,  game_map, visible_players):
        pass

    def get_action(self, game_map, visible_players):
        pass


class GoMine(ActionTemplate):

    def calculate_weight(self,  game_map, visible_players):
        return 1

    def get_action(self, game_map, visible_players):
        return create_move_action(UP)


class Mine(ActionTemplate):

    def calculate_weight(self,  game_map, visible_players):
        return 0

    def get_action(self, game_map, visible_players):
        return create_collect_action(UP)


class GoHome(ActionTemplate):

    def calculate_weight(self,  game_map, visible_players):
        return 0

    def get_action(self, game_map, visible_players):
        return create_move_action(UP)