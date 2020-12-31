import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__()
		self.currentPosition = 0
		self.mediaPlayer = QMediaPlayer()
		url = QUrl.fromLocalFile("C:\\Users\\olive\\Downloads\\Glacier.mp3")
		self.mediaPlayer.setMedia(QMediaContent(url))
		self.mediaPlayer.play()
		self.mediaPlayer.mediaStatusChanged.connect(self.mediaChange)

		self.checkMusicPositionTimer = QTimer(self)
		self.checkMusicPositionTimer.setInterval(50)

		self.checkMusicPositionTimer.timeout.connect(self.updateSlider)

		self.checkMusicPositionTimer.start()

		self.initUI()

	def initUI(self):
		exitAct = QAction(QIcon('exit.png'), '&Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(qApp.quit)

		self.statusBar()

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAct)


		layout = QVBoxLayout()
		self.l1 = QLabel("Hello")
		self.l1.setAlignment(Qt.AlignCenter)
		layout.addWidget(self.l1)

		self.sl = QSlider(Qt.Horizontal)
		self.sl.setMinimum(0)
		self.sl.setMaximum(300)
		self.sl.setValue(0)
		self.sl.setTickPosition(QSlider.TicksBelow)
		self.sl.setTickInterval(5)

		layout.addWidget(self.sl)
		self.sl.valueChanged.connect(self.valuechange)

		mainWidget = QWidget()
		mainWidget.setLayout(layout)
		self.setCentralWidget(mainWidget)


		self.resize(400, 600)
		self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
		self.setWindowTitle("Music Player")
		self.show()

	def updateSlider(self):
		self.sl.setSliderPosition(self.mediaPlayer.position())

	def mediaChange(self, status):
		if status == 6:
			print("Duration: ", self.mediaPlayer.metaData("Duration"))
			self.sl.setMaximum(self.mediaPlayer.metaData('Duration'))
		else:
			print(1)

	def valuechange(self):
		# size = self.sl.value()
		# self.mediaPlayer.setPosition(size)
		pass




def main(args):
	app = QApplication(args)
	_ = MainWindow()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main(sys.argv)