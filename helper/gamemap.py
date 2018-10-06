from helper.tile import *


class GameMap:
    def __init__(self, serializedMap, xMin, yMin, wallsAreBreakable):
        self.xMin = xMin
        self.yMin = yMin
        self.wallsAreBreakable = wallsAreBreakable
        self.deserializeMap(serializedMap)
        self.initMapSize()

    def getTileAt(self, position):
        if (position.x < self.xMin or position.x >= self.xMax or
                position.y < self.yMin or position.y >= self.yMax):
            return TileContent.Empty

        x = position.x - self.xMin
        y = position.y - self.yMin
        return self.tiles[x][y].TileContent

    def initMapSize(self):
        if self.tiles is not None:
            self.xMax = self.xMin + len(self.tiles)
            self.yMax = self.yMin + len(self.tiles[0])
            self.visibleDistance = (self.xMax - self.xMin - 1) / 2

    def deserializeMap(self, serializedMap):
        serializedMap = serializedMap[1:-2]
        rows = serializedMap.split('[')
        self.tiles = []
        for i in range(len(rows) - 1):
            self.tiles.append([])
            column = rows[i + 1].split('{')
            for j in range(len(column) - 1):
                x = i + self.xMin
                y = j + self.yMin
                # Tile is not empty
                if not column[j + 1][0] == '}':
                    infos = column[j + 1].split('}')
                    # Info may contain only tile content, but could also contain additional info for specific tile types
                    if infos[0].find(',') != -1:
                        infos = infos[0].split(',')

                    # Handle tile types
                    if TileContent(int(infos[0])) == TileContent.Resource:
                        amount_left = int(infos[1])
                        density = float(infos[2])
                        self.tiles[i].append(ResourceTile(TileContent(int(infos[0])), x, y, amount_left, density))
                    else:
                        self.tiles[i].append(Tile(TileContent(int(infos[0])), x, y))
                else:
                    self.tiles[i].append(Tile(TileContent.Empty, x, y))
