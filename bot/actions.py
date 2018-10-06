import logging
from typing import List
from bot.search import Grid
from helper import *
from math import *
from helper.aiHelper import *

log = logging.getLogger("main")

UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)


def calc_damage_to_enemy(us: Player, enemy: Player):

    offensive_item_damage = 0
    defensive_item_blocking = 0

    if PurchasableItem.Sword in us.CarriedItems:
        offensive_item_damage = 2

    if PurchasableItem.Shield in enemy.CarriedItems:
        defensive_item_blocking = 2

    return floor(3 + us.AttackPower + offensive_item_damage - 2 * (enemy.Defence + defensive_item_blocking) ** 0.6)


def move(grid: Grid, from_pos: Point, to_pos: Point):
    next_x, next_y = grid.a_star_search(from_pos.to_coords(), to_pos.to_coords())

    next_position = Point(next_x, next_y)
    next_direction = next_position - from_pos

    return create_move_action(next_direction)


def is_next_to(game_map: GameMap, pos: Point, tile_type: TileContent):
    return game_map.getTileAt(pos + LEFT) == tile_type \
           or game_map.getTileAt(pos + RIGHT) == tile_type \
           or game_map.getTileAt(pos + DOWN) == tile_type \
           or game_map.getTileAt(pos + UP) == tile_type


class ActionTemplate:

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        pass

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):
        pass


class GoMine(ActionTemplate):

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        calculated_weight = 0

        if player_info.CarriedResources <= 500:
            calculated_weight = 1

        if is_next_to(game_map, player_info.Position, TileContent.Resource):
                calculated_weight = 0

        return calculated_weight

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):
        closest_position = sorted(grid.resources.values(), key=lambda r: r.Position.dist_to(player_info.Position))[0]

        return move(grid, player_info.Position, closest_position)


class Mine(ActionTemplate):

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        calculated_weight = 0

        if is_next_to(game_map, player_info.Position, TileContent.Resource):
            calculated_weight = 1

        return calculated_weight

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):
        for direction in (LEFT, RIGHT, UP, DOWN):
            if game_map.getTileAt(player_info.Position + direction) == TileContent.Resource:
                return create_collect_action(direction)

        return create_empty_action()


class GoHome(ActionTemplate):

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        calculated_weight = 0

        if player_info.CarriedResources == player_info.CarryingCapacity:
            calculated_weight = 1

        return calculated_weight

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):
        return move(grid, player_info.Position, player_info.HouseLocation)


class BuyUpgrade(ActionTemplate):

    def __init__(self):

        self.upgrade_cost = [0, 10000, 15000, 25000, 50000, 100000]
        self.health_upgrade = [10, 13, 15, 20, 25, 35]
        self.attack_upgrade = [1, 2, 4, 6, 8, 10]
        self.defense_upgrade = [1, 2, 4, 6, 8, 10]
        self.collect_speed_upgrade = [1, 1.25, 1.5, 2, 2.5, 3.5]
        self.carrying_upgrade = [1000, 1250, 1500, 2000, 3000, 5000]

        self.thing_to_upgrade = None

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):

        if player_info.TotalResources < self.upgrade_cost[1]:
            return 0
        else:
            if player_info.AttackPower < self.attack_upgrade[1]:
                self.thing_to_upgrade = UpgradeType.AttackPower
                log.warning("**********UPGRADE ATTACK TO LEVEL 1**********")
                return 1
            elif player_info.Defence < self.defense_upgrade[1]:
                self.thing_to_upgrade = UpgradeType.Defence
                log.warning("**********UPGRADE DEFENSE TO LEVEL 1**********")
                return 1
            elif player_info.MaxHealth < self.health_upgrade[1]:
                self.thing_to_upgrade = UpgradeType.MaximumHealth
                log.warning("**********UPGRADE HEALTH TO LEVEL 1**********")
                return 1
        if player_info.TotalResources < self.upgrade_cost[2]:
            if player_info.AttackPower < self.attack_upgrade[2]:
                log.warning("**********UPGRADE ATTACK TO LEVEL 2**********")
                self.thing_to_upgrade = UpgradeType.AttackPower
                return 1
            elif player_info.Defence < self.defense_upgrade[2]:
                log.warning("**********UPGRADE DEFENSE TO LEVEL 2**********")
                self.thing_to_upgrade = UpgradeType.Defence
                return 1
        log.info("No upgrade.")
        return 0

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):
        if player_info.Position == player_info.HouseLocation:
            return create_upgrade_action(self.thing_to_upgrade)
        return move(grid, player_info.Position, player_info.HouseLocation)


class GoHunt(ActionTemplate):
    def __init__(self, last_kill: str):
        self.last_kill = last_kill

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        return 1

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):

        visible_players = [p for p in visible_players if p.Name != self.last_kill and
                           calc_damage_to_enemy(player_info, p) > 0]

        if len(visible_players) == 0:
            return move(grid, player_info.Position, LEFT.mul(5))

        closest_enemy = sorted(visible_players, key=lambda p: p.Position.dist_to(player_info.Position))[0]

        return move(grid, player_info.Position, closest_enemy.Position)
