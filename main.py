from PyQt5 import QtWidgets
from ui.main_window import MainWindow
import sys

def main():
	# rows = int(input("How many rows do you want in the grid? "))
	app = QtWidgets.QApplication(sys.argv)
	main_window = MainWindow(3)
	sys.exit(app.exec())

if __name__ == '__main__':
	main()
	