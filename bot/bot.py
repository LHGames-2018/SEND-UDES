from helper import *
import logging
log = logging.getLogger("main")
log_level = logging.DEBUG
log.setLevel(log_level)
handler = logging.StreamHandler()
handler.setLevel(log_level)
handler.setFormatter(logging.Formatter("%(asctime)-15s - %(levelname)s - line %(lineno)s - %(funcName)s: %(message)s"))
log.addHandler(handler)

UP    = Point(0, 1)
DOWN  = Point(0, -1)
LEFT  = Point(-1, 0)
RIGHT = Point(1, 0)

tick = -1
sequence = [LEFT, LEFT, LEFT, LEFT, DOWN, DOWN, DOWN, DOWN, DOWN]
return_way = [UP, UP, UP, UP, LEFT, LEFT , LEFT]
second_go = [RIGHT, RIGHT, RIGHT, DOWN, DOWN, DOWN, DOWN]

class Bot:
    def __init__(self):
        pass

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.PlayerInfo = playerInfo

    def execute_turn(self, game_map, visible_players):
        """
        This is where you decide what action to take.
            :param gameMap: The gamemap.
            :param visiblePlayers:  The list of visible players.
        """
        global tick
        log.info("game_map {}".format(game_map))
        log.info("self {}".format(self.__dict__))
        log.info("visible_players {}".format(visible_players.__dict__))
        tick += 1
        if tick < len(sequence):
            log.info("going {}".format(sequence[tick]))
            return create_move_action(sequence[tick])
        log.info("collecting")
        return create_collect_action(DOWN)

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
