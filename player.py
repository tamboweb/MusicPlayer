import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QFileDialog,
    QSlider
)

from PySide6.QtCore import Qt

from player import AudioPlayer
from library import scan_music, get_song_name


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Music Player")
        self.resize(700, 450)

        self.audio_player = AudioPlayer()

        self.songs = []

        # Title
        self.title = QLabel("No song selected")

        # Song list
        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(
            self.play_selected
        )

        # Buttons
        self.open_button = QPushButton(
            "Add Music Folder"
        )
        self.open_button.clicked.connect(
            self.load_music
        )

        self.play_button = QPushButton(
            "▶ Play"
        )
        self.play_button.clicked.connect(
            self.toggle_play
        )

        self.next_button = QPushButton(
            "Next"
        )
        self.next_button.clicked.connect(
            self.next_song
        )

        # Volume
        self.volume = QSlider(
            Qt.Horizontal
        )

        self.volume.setRange(0, 100)
        self.volume.setValue(50)

        self.volume.valueChanged.connect(
            self.audio_player.set_volume
        )

        # Layout
        buttons = QHBoxLayout()

        buttons.addWidget(
            self.open_button
        )

        buttons.addWidget(
            self.play_button
        )

        buttons.addWidget(
            self.next_button
        )

        layout = QVBoxLayout()

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.list
        )

        layout.addLayout(
            buttons
        )

        layout.addWidget(
            QLabel("Volume")
        )

        layout.addWidget(
            self.volume
        )

        self.setLayout(layout)


    def load_music(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Choose Music Folder"
        )

        if folder:
            self.songs = scan_music(folder)

            self.list.clear()

            for song in self.songs:
                self.list.addItem(
                    get_song_name(song)
                )


    def play_selected(self):
        index = self.list.currentRow()

        if index >= 0:
            song = self.songs[index]

            self.audio_player.load(
                song
            )

            self.audio_player.play()

            self.title.setText(
                get_song_name(song)
            )

            self.play_button.setText(
                "⏸ Pause"
            )


    def toggle_play(self):
        self.audio_player.toggle()

        if self.audio_player.is_playing():
            self.play_button.setText(
                "⏸ Pause"
            )
        else:
            self.play_button.setText(
                "▶ Play"
            )


    def next_song(self):
        current = self.list.currentRow()

        if current + 1 < len(self.songs):
            self.list.setCurrentRow(
                current + 1
            )

            self.play_selected()



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MusicPlayer()

    window.show()

    sys.exit(
        app.exec()
    )
