import json
from flask import Flask, request
from helper import GameMap, Player, Point
from bot import Bot

app = Flask(__name__)

bot = Bot()


def deserialize(data):
    if "x" in data and "y" in data:
        return Point(data["x"], data["y"])
    elif "Name" in data:
        return Player(data["Health"], data["MaxHealth"], data["CarriedResources"],
                      data["CarryingCapacity"], data["CollectingSpeed"], data["TotalResources"],
                      data["AttackPower"], data["Defence"], data["Position"],
                      data["HouseLocation"], data["CarriedItems"], data["Score"], data["Name"],
                      data["UpgradeLevels"])
    elif "CustomSerializedMap" in data:
        data["GameMap"] = GameMap(
            data["CustomSerializedMap"], data["xMin"], data["yMin"], data["WallsAreBreakable"])
    return data


@app.route("/", methods=["GET"])
def ping():
    return "I am alive!"


@app.route("/", methods=["POST"])
def response():
    """
    Point d'entree appelle par le GameServer
    """
    gameInfo = json.loads(request.form["data"], object_hook=deserialize)
    player = gameInfo["Player"]
    bot.before_turn(player)
    action = bot.execute_turn(gameInfo['GameMap'], gameInfo['OtherPlayers'])
    bot.after_turn()
    print(action)
    return action


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
