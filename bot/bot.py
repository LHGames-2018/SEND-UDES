from helper import *
from actions import *
import search
import logging
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


    def execute_turn(self, game_map, visible_players):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        grid = search.Grid(game_map.visibleDistance * 2, game_map.visibleDistance * 2)
        for column in game_map.tiles:
            for tile in column:
                tile.TileContent                

        if self.PlayerInfo.CarriedRessources == self.PlayerInfo.CarryingCapacity:
            turn_counter = -3

        global tick
        global turn_counter
        log.info("game_map {}".format(game_map))
        log.info("self {}".format(self.__dict__))
        log.info("visible_players {}".format(visible_players))
        tick += 1
        turn_counter += 1

        if turn_counter < len(sequence) and turn_counter >= 0:
            log.info("going {}".format(sequence[turn_counter]))
            return create_move_action(sequence[turn_counter])
        
        if turn_counter < 0:
            log.info("going {}".format(return_way[turn_counter + 3]))
            return create_move_action(return_way[turn_counter + 3])


        log.info("collecting")
        return create_collect_action(RIGHT)


    def get_mine_position(self):
        return None

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
