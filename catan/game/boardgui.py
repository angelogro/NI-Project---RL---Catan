import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPolygon, QColor, QFont
from PyQt5.QtCore import Qt, QPoint
import numpy as np

class App(QWidget):

	def __init__(self,tiles):
		super().__init__()
		self.title = 'Catan'
		self.left = 10
		self.top = 10
		self.width = 1080
		self.height = 1080
		self.initUI()
		self.tiles = tiles

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.show()


	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.draw_hex(e, qp)
		qp.end()

	# TBD: make scalable with window size
	def draw_hex(self, e, qp):
		x= (3**0.5 / 2) #Verhältnis Höhe / Breite Hexagon
		size = 100 # whole length of hexagon
		ratio = size * x

		x_offset = self.width/3 #off set of first tile

		drawing_points = []
		tiles_in_row = [4,5,6,7,6,5,4]
		column_offset = [0, -0.5, -1, -1.5, -1, -0.5, 0]
		water_vec = []

		for j in range(len(tiles_in_row)):

			for i in range(tiles_in_row[j]):

				points = QPolygon([QPoint(x_offset+ratio*(column_offset[j]+i), (0.75*size*j)), #top corner
									QPoint(x_offset+ratio*(0.5+column_offset[j]+i), size/4 + (0.75*size*j)), #upper right corner
									QPoint(x_offset+ratio*(0.5+(column_offset[j]+i)), size/4 + size/2 + (0.75*size*j)), #lower right corner
									QPoint(x_offset+ratio*(column_offset[j] +i), size + (0.75*size*j)), #lowest corner
									QPoint(x_offset+ratio*(-0.5+column_offset[j]+i), size/4 + size/2 + (0.75*size*j)), #lower left corner
									QPoint(x_offset+ratio*(-0.5+column_offset[j]+i), size/4 + (0.75*size*j))]) #upper left corner

				drawing_points.append(points)

				if (i == range(tiles_in_row[j])[0]) or (j == 0) or (j== 6) or (i == range(tiles_in_row[j])[-1]):
					water_vec.append(True)
				else:
					water_vec.append(False)

		print(len(drawing_points))
		i = 0
		for counter, x in enumerate(drawing_points):
			print(x[0])
			if water_vec[counter]:
				qp.setBrush(QColor(0,0,200))
				qp.drawPolygon(x)

			else:
				if self.tiles[i][0] == 0:	#Fields
					qp.setBrush(QColor(68,204,0))
				elif self.tiles[i][0] == 1:	#Pasture
					qp.setBrush(QColor(255,230,102))
				elif self.tiles[i][0] == 2:	#Mountains
					qp.setBrush(QColor(190, 190, 190))
				elif self.tiles[i][0] == 3:	#Hills
					qp.setBrush(QColor(153, 77, 0))
				elif self.tiles[i][0] == 4:	#Forests
					qp.setBrush(QColor(0, 77, 38))
				elif self.tiles[i][0] == 5:	#desert
					qp.setBrush(QColor(194, 178, 128))

				qp.setPen(QColor(0, 0, 0))
				qp.setFont(QFont('Decorative', 30))
				qp.drawPolygon(x)
				qp.drawText((x[5] + x[3])/2, str(self.tiles[i][1]))

				i +=1


"""if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
else:
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
"""