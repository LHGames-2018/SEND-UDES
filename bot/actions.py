import logging
from typing import List
from bot.search import Grid
from helper import *
from math import *

log = logging.getLogger("main")
from helper.aiHelper import *

UP    = Point(0, -1)
DOWN  = Point(0, 1)
LEFT  = Point(-1, 0)
RIGHT = Point(1, 0)

def calc_damage_to_enemy(us: Player, enemy: Player):

    offensive_item_damage = 0
    defensive_item_blocking = 0

    if PurchasableItem.Sword in us.CarriedItems:
        offensive_item_damage = 2

    if PurchasableItem.Shield in enemy.CarriedItems:
        defensive_item_blocking = 2

    return floor(3 + us.AttackPower + offensive_item_damage - 2 * (enemy.Defence + defensive_item_blocking) ** 0.6)



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

        if game_map.getTileAt(player_info.Position + Point(-1, 0)) == TileContent.Resource \
            or game_map.getTileAt(player_info.Position + Point(1, 0)) == TileContent.Resource \
            or game_map.getTileAt(player_info.Position + Point(0, -1)) == TileContent.Resource \
            or game_map.getTileAt(player_info.Position + Point(0, 1)) == TileContent.Resource:
                calculated_weight = 0

        return calculated_weight

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):
        closest_position = Point(-100, -100)
        closest_distance = 1000
        for resource in grid.resources.values():
            current_distance = resource.Position.dist_to(player_info.Position)
            if current_distance < closest_distance:
                closest_position = resource.Position
                closest_distance = current_distance

        next_x, next_y = grid.a_star_search(player_info.Position.to_coords(), closest_position.to_coords())

        next_position = Point(next_x, next_y)
        next_direction = next_position - player_info.Position

        if game_map.getTileAt(next_position) == TileContent.Wall:  # If its a tree, cut it down
            return create_attack_action(next_direction)

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
        direction = UP

        if game_map.getTileAt(player_info.Position + Point(-1, 0)) == TileContent.Resource:
            direction = LEFT
        elif game_map.getTileAt(player_info.Position + Point(1, 0)) == TileContent.Resource:
            direction = RIGHT
        elif game_map.getTileAt(player_info.Position + Point(0, -1)) == TileContent.Resource:
            direction = UP
        elif game_map.getTileAt(player_info.Position + Point(0, 1)) == TileContent.Resource:
            direction = DOWN

        return create_collect_action(direction)


class GoHome(ActionTemplate):

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        calculated_weight = 0

        if player_info.CarriedResources == player_info.CarryingCapacity:
            calculated_weight = 1

        return calculated_weight

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):

        next_x, next_y = grid.a_star_search(player_info.Position.to_coords(), grid.house.to_coords())

        next_position = Point(next_x, next_y)
        next_direction = next_position - player_info.Position

        if game_map.getTileAt(next_position) == TileContent.Wall:  # If its a tree, cut it down
            return create_attack_action(next_direction)

        return create_move_action(next_direction)


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
            log.info("No upgrade cuz too poor: {}".format(player_info.TotalResources))
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
        return GoHome().get_action(player_info, game_map, visible_players, grid)


class GoHunt(ActionTemplate):
    def __init__(self, last_kill: str):
        self.last_kill = last_kill
        self.target = None

    def calculate_weight(self, player_info: Player, game_map: GameMap, visible_players: List[Player]):
        return 1

    def get_action(self, player_info: Player, game_map: GameMap, visible_players: List[Player], grid: Grid):

        visible_players = [p for p in visible_players if p.Name != self.last_kill and
                           calc_damage_to_enemy(player_info, p) > 0]
        if len(visible_players) == 0:
            next_x, next_y = grid.a_star_search(player_info.Position.to_coords(), Point(-5, 0).to_coords())

            next_position = Point(next_x, next_y)
            next_direction = next_position - player_info.Position

            if game_map.getTileAt(player_info.Position + next_direction) == TileContent.Wall:  # If its a tree, cut it down
                return create_attack_action(next_direction)

            return create_move_action(next_direction)

        closest_position = Point(-100, -100)
        closest_distance = 1000
        for enemy in visible_players:
            current_distance = enemy.Position.dist_to(player_info.Position)
            if current_distance < closest_distance:
                closest_position = enemy.Position
                closest_distance = current_distance
                self.target = enemy

        next_x, next_y = grid.a_star_search(player_info.Position.to_coords(), closest_position.to_coords())

        next_position = Point(next_x, next_y)
        next_direction = next_position - player_info.Position

        if next_position == self.target.Position or game_map.getTileAt(next_position) == TileContent.Wall:  # If its a tree or a player, cut it down
            return create_attack_action(next_direction)

        self.target = None
        return create_move_action(next_direction)
