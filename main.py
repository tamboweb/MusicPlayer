import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel,
    QVBoxLayout, QHBoxLayout, QListWidget,
    QFileDialog, QSlider
)
from PySide6.QtCore import Qt
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtGui import QFont

from library import scan_music


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.resize(600, 400)

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)

        self.songs = []

        self.title = QLabel("No song selected")
        self.title.setFont(QFont("Arial", 16))

        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self.play_selected)

        self.open_button = QPushButton("Add Music Folder")
        self.open_button.clicked.connect(self.load_music)

        self.play_button = QPushButton("▶ Play")
        self.play_button.clicked.connect(self.toggle_play)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_song)

        self.volume = QSlider(Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(50)
        self.volume.valueChanged.connect(self.change_volume)

        controls = QHBoxLayout()
        controls.addWidget(self.open_button)
        controls.addWidget(self.play_button)
        controls.addWidget(self.next_button)

        layout = QVBoxLayout()
        layout.addWidget(self.title)
        layout.addWidget(self.list)
        layout.addLayout(controls)
        layout.addWidget(QLabel("Volume"))
        layout.addWidget(self.volume)

        self.setLayout(layout)

        self.audio.setVolume(0.5)

    def load_music(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Choose Music Folder"
        )

        if folder:
            self.songs = scan_music(folder)

            self.list.clear()

            for song in self.songs:
                self.list.addItem(song)

    def play_selected(self):
        index = self.list.currentRow()

        if index >= 0:
            self.player.setSource(self.songs[index])
            self.player.play()

            self.title.setText(
                self.songs[index].split("/")[-1]
            )

            self.play_button.setText("⏸ Pause")

    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText("▶ Play")
        else:
            self.player.play()
            self.play_button.setText("⏸ Pause")

    def next_song(self):
        index = self.list.currentRow()

        if index + 1 < len(self.songs):
            self.list.setCurrentRow(index + 1)
            self.play_selected()

    def change_volume(self, value):
        self.audio.setVolume(value / 100)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MusicPlayer()
    window.show()

    sys.exit(app.exec())
