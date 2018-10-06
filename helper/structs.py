import math


class ActionTypes:
    DefaultAction, MoveAction, MeleeAttackAction, CollectAction, UpgradeAction, StealAction, PurchaseAction, HealAction = \
        range(8)


class UpgradeType:
    CarryingCapacity, AttackPower, Defence, MaximumHealth, CollectingSpeed = range(
        5)


class PurchasableItem:
    Sword, Shield, Backpack, Pickaxe, HealthPotion = range(5)


class Point(object):

    # Constructor
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    # Overloaded operators
    def __add__(self, point):
        return Point(self.y + point.x, self.y + point.y)

    def __sub__(self, point):
        return Point(self.y - point.x, self.y - point.y)

    def __str__(self):
        return "{{{0}, {1}}}".format(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    # Distance between two Points
    @staticmethod
    def Distance(p1, p2):
        delta_x = p1.x - p2.x
        delta_y = p1.y - p2.y
        return math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))


class GameInfo(object):

    def __init__(self, json_dict):
        self.__dict__ = json_dict
        self.HouseLocation = Point(json_dict["HouseLocation"])
        self.Map = None
        self.OtherPlayers = dict()


class ActionContent(object):

    def __init__(self, action_name, content):
        self.ActionName = action_name
        self.Content = str(content)
