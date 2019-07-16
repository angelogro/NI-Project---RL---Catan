import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPolygon, QColor, QFont
from PyQt5.QtCore import Qt, QPoint, QSize
import numpy as np


class Board(QWidget):

    def __init__(self, tiles, roads, building_state, road_state):
        super().__init__()
        self.title = 'Catan'
        self.left = 10
        self.top = 10
        self.width = 1080
        self.height = 1080
        self.initUI()

        self.tiles = tiles
        self.building_state, self.road_state = building_state, road_state
        self.coordinates, self.water = self.init_coordinates()  # has QPolygon Objects
        self.building_coord = [self.coordinates[5][0], self.coordinates[5][1], self.coordinates[5][2],
                               self.coordinates[6][1], self.coordinates[6][2],
                               self.coordinates[7][1], self.coordinates[7][2],

                               self.coordinates[10][0], self.coordinates[10][1], self.coordinates[10][2],
                               self.coordinates[11][1], self.coordinates[11][2],
                               self.coordinates[12][1], self.coordinates[12][2],
                               self.coordinates[13][1], self.coordinates[13][2],

                               self.coordinates[16][0], self.coordinates[16][1], self.coordinates[16][2],
                               self.coordinates[17][1], self.coordinates[17][2],
                               self.coordinates[18][1], self.coordinates[18][2],
                               self.coordinates[19][1], self.coordinates[19][2],
                               self.coordinates[20][1], self.coordinates[20][2],

                               self.coordinates[16][5], self.coordinates[16][4], self.coordinates[16][3],
                               self.coordinates[17][4], self.coordinates[17][3],
                               self.coordinates[18][4], self.coordinates[18][3],
                               self.coordinates[19][4], self.coordinates[19][3],
                               self.coordinates[20][4], self.coordinates[20][3],

                               self.coordinates[23][5], self.coordinates[23][4], self.coordinates[23][3],
                               self.coordinates[24][4], self.coordinates[24][3],
                               self.coordinates[25][4], self.coordinates[25][3],
                               self.coordinates[26][4], self.coordinates[26][3],

                               self.coordinates[29][5], self.coordinates[29][4], self.coordinates[29][3],
                               self.coordinates[30][4], self.coordinates[30][3],
                               self.coordinates[31][4], self.coordinates[31][3]]

        self.road_coord = self.init_road_coord(roads)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def init_coordinates(self):
        x = (3 ** 0.5 / 2)  # Verhältnis Höhe / Breite Hexagon
        size = 100  # whole length of hexagon
        ratio = size * x

        x_offset = self.width / 3  # off set of first tile

        drawing_points = []
        tiles_in_row = [4, 5, 6, 7, 6, 5, 4]
        column_offset = [0, -0.5, -1, -1.5, -1, -0.5, 0]
        water_vec = []

        # for first hex at data rep board:
        # 0, 1, 2, 10, 9, 8 first "coordinates" object

        for j in range(len(tiles_in_row)):

            for i in range(tiles_in_row[j]):

                points = QPolygon([QPoint(x_offset + ratio * (-0.5 + column_offset[j] + i),
                                          size / 4 + (0.75 * size * j)),  # upper left corner
                                   QPoint(x_offset + ratio * (column_offset[j] + i),
                                          (0.75 * size * j)),  # top corner
                                   QPoint(x_offset + ratio * (0.5 + column_offset[j] + i),
                                          size / 4 + (0.75 * size * j)),  # upper right corner
                                   QPoint(x_offset + ratio * (0.5 + (column_offset[j] + i)),
                                          size / 4 + size / 2 + (0.75 * size * j)),  # lower right corner
                                   QPoint(x_offset + ratio * (column_offset[j] + i),
                                          size + (0.75 * size * j)),  # lowest corner
                                   QPoint(x_offset + ratio * (-0.5 + column_offset[j] + i),
                                          size / 4 + size / 2 + (0.75 * size * j))])  # lower left corner

                drawing_points.append(points)

                if (i == range(tiles_in_row[j])[0]) or (j == 0) or (j == 6) or (i == range(tiles_in_row[j])[-1]):
                    water_vec.append(True)
                else:
                    water_vec.append(False)

        return drawing_points, water_vec

    def init_road_coord(self, roads):
        road_coord = []
        for x in roads:
            road_coord.append([self.building_coord[x[0]], self.building_coord[x[1]]])
        return road_coord

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_hex(e, qp)
        self.draw_settlements(e, qp)
        qp.end()

    # TBD: make scalable with window size
    def draw_hex(self, e, qp):
        print(len(self.coordinates))
        i = 0
        for counter, x in enumerate(self.coordinates):

            if self.water[counter]:
                qp.setBrush(QColor(0, 0, 200))
                qp.drawPolygon(x)

            else:
                if self.tiles[i][0] == 0:  # Fields
                    qp.setBrush(QColor(68, 204, 0))
                elif self.tiles[i][0] == 1:  # Pasture
                    qp.setBrush(QColor(255, 230, 102))
                elif self.tiles[i][0] == 2:  # Mountains
                    qp.setBrush(QColor(190, 190, 190))
                elif self.tiles[i][0] == 3:  # Hills
                    qp.setBrush(QColor(153, 77, 0))
                elif self.tiles[i][0] == 4:  # Forests
                    qp.setBrush(QColor(0, 77, 38))
                elif self.tiles[i][0] == 5:  # desert
                    qp.setBrush(QColor(194, 178, 128))

                qp.setPen(QColor(0, 0, 0))
                qp.setFont(QFont('Decorative', 30))
                qp.drawPolygon(x)
                qp.drawText((x[0] + x[4]) / 2, str(self.tiles[i][1]))

                i += 1

    def draw_settlements(self, e, qp):

        # print("Coordinates: ", self.coordinates[0][0])
        # print(len(self.building_coord))

        for counter, building in enumerate(self.building_state):
            self.player_color(building, qp)

            if 0 < building < 5:
                qp.drawEllipse(self.building_coord[counter], 10, 10)
            elif 4 < building < 9:
                qp.drawRect(self.building_coord[counter].x() - 10, self.building_coord[counter].y() - 10, 20, 20)

        """
        Building type: 0 - no building, 1 - Settlement P1, 2 - Settlement P2, 3 - Settlement P3, 4 - Settlement P4
                5 - City P1, 6 - City P2, 7 - City P3, 8 - City P4, 9 - No building possible
        """
    # refresh building and road state
    def draw_road(self):

        pass

    def refresh_building_road_states(self, building_state, road_state):
        self.building_state = building_state
        self.road_state = road_state

    def player_color(self, player, qp):
        if player == 1 or player == 5:
            qp.setPen(QColor(0, 0, 0))
            qp.setBrush(QColor(0, 0, 0))

        elif player == 2 or player == 6:
            qp.setPen(QColor(153, 0, 76))
            qp.setBrush(QColor(153, 0, 76))

        elif player == 3 or player == 7:
            qp.setPen(QColor(204, 153, 255))
            qp.setBrush(QColor(204, 153, 255))

        elif player  == 4 or player == 8:
            qp.setPen(QColor(50, 255, 255))
            qp.setBrush(QColor(50, 255, 255))

"""

hex6 -> 0,1,2,10,9,8
hex7 -> 2,3,4,12,11,10
hex8 -> 4,5,6,14,13,12

hex11-> 7,8,9,19,18,17
hex12-> 9,10,11,21,20,19
hex13-> 11,12,13,23,22,21
hex14-> 13,14,15,25,24,23

hex17 -> 16,17,18,29,28,27
hex18 -> 18,19,20,31,30,29
hex19 -> 20,21,22,33.32.31
hex20 -> 22,23,24,35,34,33
hex21 -> 24,25,26,37,36,35 --
"""
"""if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
else:
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
"""
