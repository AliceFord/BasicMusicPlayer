import os
import sys

from pathlib import Path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *

# https://accounts.spotify.com/authorize?client_id=386a3771ccef433aa358c10d234bec34&response_type=code&redirect_uri=https:%2F%2Fgoogle.com%2F


class MainWindow(QMainWindow):
	possibleDataSources = ["Local File", "Local Playlist", "Internet File"]  # TODO: Spotify

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		dataSource, notExit = QInputDialog.getItem(self, "Select Data Source", "Data Source: ", self.possibleDataSources, editable=False)
		if not notExit:
			sys.exit()
		if dataSource == self.possibleDataSources[0]:
			filter = "MP3 File (*.mp3)"
			file, fileType = QFileDialog.getOpenFileUrl(self, "Audio File", filter=filter)
			self.initMediaPlayer(dataSource, file=file)
		elif dataSource == self.possibleDataSources[1]:
			directory = QFileDialog.getExistingDirectory(self, "Open Playlist", options=QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
			self.initMediaPlayer(dataSource, directory=directory)
		self.initUI()

	def initMediaPlayer(self, dataSource, file=None, directory=None):
		self.mediaPlayer = QMediaPlayer()
		self.playlist = QMediaPlaylist(self.mediaPlayer)
		if dataSource == self.possibleDataSources[0]:
			self.playlist.addMedia(QMediaContent(file))
			self.playlist.setCurrentIndex(0)
			self.mediaPlayer.setPlaylist(self.playlist)
			#self.mediaPlayer.setMedia(QMediaContent(file))
		elif dataSource == self.possibleDataSources[1]:
			for file in sorted(Path(directory).iterdir(), key=os.path.getmtime, reverse=True):
				if os.path.splitext(file)[1] == ".mp3":
					self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(str(file))))
			self.playlist.setCurrentIndex(0)
			self.mediaPlayer.setPlaylist(self.playlist)
		self.mediaPlayer.setVolume(int(QAudio.convertVolume(50/100, QAudio.LogarithmicVolumeScale, QAudio.LinearVolumeScale)*100))
		self.mediaPlayer.play()
		self.mediaPlayer.mediaStatusChanged.connect(self.mediaChange)

		self.checkMusicPositionTimer = QTimer(self)
		self.checkMusicPositionTimer.setInterval(50)

		self.checkMusicPositionTimer.timeout.connect(self.updateSlider)

		self.checkMusicPositionTimer.start()

	def initUI(self):
		## Menu Stuff
		exitAct = QAction(QIcon('exit.png'), '&Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(qApp.quit)

		self.statusBar()

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAct)

		# Layout Stuff
		layout = QVBoxLayout()

		# Widget creation
		self.sl = MainSlider(self.mediaPlayer, Qt.Horizontal)

		# Buttons
		self.groupBox = ControlButtons("Controls", self.mediaPlayer)


		# More Layout Stuff
		layout.addWidget(self.sl)
		layout.addWidget(self.groupBox)

		mainWidget = QWidget()
		mainWidget.setLayout(layout)
		self.setCentralWidget(mainWidget)

		# General Setup Stuff
		self.resize(400, 200)
		self.setWindowTitle("Music Player")
		self.show()

	def updateSlider(self):
		self.sl.setSliderPosition(self.mediaPlayer.position())

	def mediaChange(self, status):
		if status == 6:
			print("Duration: ", self.mediaPlayer.metaData("Duration"))
			self.sl.setMaximum(self.mediaPlayer.metaData('Duration'))
		else:
			print("Status Changed: ", status)


class ControlButtons(QGroupBox):
	def __init__(self, title: str, mediaPlayer: QMediaPlayer, parent=None):
		super().__init__(title, parent)
		self.mediaPlayer = mediaPlayer

		self.startButton = QPushButton("Start")
		self.pauseButton = QPushButton("Pause")
		self.stopButton = QPushButton("Stop")
		self.volumeLabel = QLabel("Volume:")
		self.volumeControl = QSlider(Qt.Horizontal)

		# Volume slider setup
		self.volumeControl.setMinimum(0)
		self.volumeControl.setMaximum(100)
		self.volumeControl.setValue(50)

		self.startButton.clicked.connect(self.__startButtonClicked)
		self.pauseButton.clicked.connect(self.__pauseButtonClicked)
		self.stopButton.clicked.connect(self.__stopButtonClicked)
		self.volumeControl.valueChanged.connect(self.__volumeChanged)

		self.buttonBox = QGridLayout()

		self.buttonBox.addWidget(self.startButton, 0, 0)
		self.buttonBox.addWidget(self.pauseButton, 0, 1)
		self.buttonBox.addWidget(self.stopButton, 0, 2)
		self.buttonBox.addWidget(self.volumeLabel, 1, 1, alignment=Qt.AlignCenter)
		self.buttonBox.addWidget(self.volumeControl, 2, 0, 1, 3)
		self.setLayout(self.buttonBox)

	def __startButtonClicked(self):
		self.mediaPlayer.play()

	def __pauseButtonClicked(self):
		self.mediaPlayer.pause()

	def __stopButtonClicked(self):
		self.mediaPlayer.stop()

	def __skipButtonClicked(self):
		pass

	def __volumeChanged(self):
		self.mediaPlayer.setVolume(int(QAudio.convertVolume(self.volumeControl.value()/100, QAudio.LogarithmicVolumeScale, QAudio.LinearVolumeScale)*100))


class MainSlider(QSlider):
	def __init__(self, mediaPlayer, parent=None):
		QSlider.__init__(self, parent)
		self.mediaPlayer = mediaPlayer
		self.setMinimum(0)
		self.setMaximum(300)
		self.setValue(0)
		self.setTickPosition(QSlider.TicksBelow)
		self.setTickInterval(5)
		self.valueChanged.connect(self.valuechange)

	def valuechange(self):
		if self.value() != self.mediaPlayer.position():
			size = self.value()
			self.mediaPlayer.setPosition(size)


def main(args):
	app = QApplication(args)
	_ = MainWindow()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main(sys.argv)
