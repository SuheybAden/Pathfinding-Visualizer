from queue import PriorityQueue, Queue
import math
import time
from .node import Node, Modes
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt, QPoint, QRectF
import os

class MainWindow(QtWidgets.QWidget):
	def __init__(self, rows) -> None:
		super().__init__()

		self.startNode = None
		self.endNode = None
		self.mode = Modes.EMPTY
		self.rows = rows
		self.size = int(1000/self.rows)

		self.load_ui()
		self.scene = QGraphicsScene()
		self.create_nodes()
		self.show()

	def load_ui(self):
		cwd = os.getcwd()
		filename = os.path.splitext(os.path.basename(__file__))[0]
		uic.loadUi(cwd + "\\ui_files\\" + filename + ".ui", self)
		self.canvas.mousePressEvent = self.mousePress
		self.connect_all()

	def create_nodes(self):
		for i in range(self.rows):
			for j in range(self.rows):
				n = Node(i, j, self.size)
				self.scene.addItem(n)

		self.canvas.setScene(self.scene)

	# Assigns neighbors and marks all nodes as unvisited
	def prepare_nodes(self):
		if self.startNode == None or self.endNode == None:
			print("Assign both a start and end node")
			return

		self.get_neighbors()

	def get_neighbors(self):
		for i in range(self.rows):
			for j in range(self.rows):
				node = self.canvas.itemAt(i*self.size, j*self.size)
				print("Node at: " + str(i*self.size) + ", " + str(j*self.size))
				if(node != None):
					for x in range(4):
						angle = x * math.pi/2
						x = node.x() + node.size/2
						y = node.y() + node.size/2
						neighbor = self.canvas.itemAt(x + (math.cos(angle) * self.size * 1.5), 
												y + (math.sin(angle) * self.size * 1.5))
						if neighbor != None:
							node.neighbors.put((1, neighbor))
							print("Neighbor at: " + str(neighbor.x()) + ", " + str(neighbor.y()))



	def connect_all(self):
		self.startPoint_btn.clicked.connect(self.startPoint_clicked)
		self.endPoint_btn.clicked.connect(self.endPoint_clicked)
		self.obstacles_btn.clicked.connect(self.obstacles_clicked)
		self.weights_btn.clicked.connect(self.weights_clicked)
		self.path_btn.clicked.connect(self.find_path)

	def startPoint_clicked(self):
		if self.mode == Modes.STARTPOINT:
			self.mode = Modes.EMPTY
		else:
			self.mode = Modes.STARTPOINT

	def endPoint_clicked(self):
		if self.mode == Modes.ENDPOINT:
			self.mode = Modes.EMPTY
		else:
			self.mode = Modes.ENDPOINT

	def obstacles_clicked(self):
		if self.mode == Modes.OBSTACLE:
			self.mode = Modes.EMPTY
		else:
			self.mode = Modes.OBSTACLE

	def weights_clicked(self):
		if self.mode == Modes.WEIGHT:
			self.mode = Modes.EMPTY
		else:
			self.mode = Modes.WEIGHT

	def mousePress(self, event):
		pos = event.pos()
		node = self.canvas.itemAt(pos)

		if node == None:
			return

		if self.mode == Modes.STARTPOINT:
			if self.startNode != None:
				self.startNode.color = Qt.white
				self.startNode.type = Modes.EMPTY
			self.startNode = node
		elif self.mode == Modes.ENDPOINT:
			if self.endNode != None:
				self.endNode.color = Qt.white
				self.endNode.type = Modes.EMPTY
			self.endNode = node

		node.color = self.mode.value
		node.type = self.mode

		self.scene.update()
		self.canvas.update()

	def find_path(self):
		if self.prepare_nodes():
			return

		text = self.algorithms_combo.currentText()
		if text == "BFS":
			self.BFS()
		elif text == "DFS":
			self.DFS()
		elif text == "Dijkstra":
			self.Dijkstra()
		elif text == "A*":
			self.A_Star()

	def BFS(self):
		print("Starting BFS")
		self.startNode.visited = True

		q = []
		q.append(self.startNode)

		# while q:
		# 	current = q.pop(0)

		# 	if(current.type == Modes.ENDPOINT):
		# 		print("Reached end")
		# 		break
			
		# 	while not current.neighbors.empty():
		# 		neighbor = current.neighbors.get()[1]
		# 		if not neighbor.visited:
		# 			neighbor.parent = current
		# 			neighbor.visited = True
		# 			q.append(neighbor)

		# self.getPath(self.endNode)

	def getPath(self, node):
		node.color = Qt.darkGreen
		self.getPath(node.parent)
		
		if node.type == Modes.STARTPOINT:
			self.scene.update()
			self.canvas.update()

				

	def DFS(self):
		pass

	def Dijkstra(self):
		pass

	def A_Star(self):
		pass