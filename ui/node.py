from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QWidget, QGraphicsItem
from PyQt5.QtGui import QPainter, QPen, QBrush
from enum import Enum
from queue import PriorityQueue

class Modes(Enum):
	EMPTY = Qt.white
	STARTPOINT = Qt.cyan
	ENDPOINT = Qt.red
	WEIGHT = Qt.lightGray
	OBSTACLE = Qt.darkGray

class Node(QGraphicsItem):
	def __init__(self, row, column, size, parent = None):
		super().__init__(parent)

		# The width and height of the node
		self.color = Qt.white
		self.size = size
		self.row = row
		self.column = column
		self.rect = QRectF(0, 0, self.size, self.size)
		self.setPos(row*self.size, column*self.size)
		self.type = Modes.EMPTY
		self.neighbors = PriorityQueue(4)
		# self.parent = None
		
		self.visited = False
		self.priority = 1

	def paint(self, painter, option, widget):
		painter.setPen(QPen(Qt.black, 4, Qt.SolidLine))
		painter.setBrush(self.color)
		painter.drawRect(self.rect)

	def boundingRect(self):
		return self.rect

	def check_neighbors(self):
		if self.type == Modes.OBSTACLE or self.visited:
			return False
		else:
			self.visited = True
			if self.type == Modes.ENDPOINT:
				return True
			else:
				done = False
				while not(self.neighbors.empty() or done):
					n = self.neighbors.get()
					done = n.check_neighbors()
				return done

	def __lt__(self, other):
		return self.priority < other.priority
