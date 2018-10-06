from helper.structs import *
import json


def create_move_action(direction):
    """
    Creates a move action to the specified direction. You can only move
    to adjacent tiles (no diagonals).
        :param direction: The direction in which you want to move.
    """
    return _create_action("MoveAction", direction)


def create_attack_action(direction):
    """
    Creates a melee attack Action. You can only attack someone on an
    Adjacent tile. (no diagonals).
        :param direction: 
    """
    return _create_action("MeleeAttackAction", direction)


def create_collect_action(direction):
    """
    Creates a Collect Action. You can only collect resources from
    Adjacent tiles (no diagonals).
        :param direction: The direction from which you want to collect.
    """
    return _create_action("CollectAction", direction)


def create_steal_action(direction):
    """
    Creates a steal Action. You can only steal from Adjacent tiles
    (no diagonals).
        :param direction: The direction from which you want to steal.
    """
    return _create_action("StealAction", direction)


def create_heal_action():
    """
    Instanciates a heal action. The action will fail if you don't have
    any healing potions available.
    """
    return _create_action("HealAction", "")


def create_purchase_action(item):
    """
    Creates a purchase action for the specified item. You need to be ON
    a shop tile for this action to succeed. If you are on any other
    type of tile, the action will fail. You can only carry 1 of each
    item, except for health potions.
        :param item: The type of item to purchase.
    """
    return _create_action("PurchaseAction", item)


def create_empty_action():
    """
    Creates an action that does nothing.
    """
    return ""


def _create_action(action_type, target):
    """
    Private method to convert the action to a string. 
    You shouldn't call this.
    """
    actionContent = ActionContent(action_type, json.dumps(target.__dict__))
    return json.dumps(actionContent.__dict__)
