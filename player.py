from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl


class AudioPlayer:
    def __init__(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()

        self.player.setAudioOutput(self.audio_output)

        self.current_song = None

        self.set_volume(50)

    def load(self, file_path):
        """
        Load a music file
        Supports MP3, FLAC, WAV, OGG
        """
        self.current_song = file_path

        url = QUrl.fromLocalFile(file_path)
        self.player.setSource(url)

    def play(self):
        if self.current_song:
            self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def toggle(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def set_volume(self, volume):
        """
        Volume from 0-100
        """
        self.audio_output.setVolume(volume / 100)

    def is_playing(self):
        return (
            self.player.playbackState()
            == QMediaPlayer.PlayingState
        )

    def position(self):
        """
        Current position in milliseconds
        """
        return self.player.position()

    def duration(self):
        """
        Total song length in milliseconds
        """
        return self.player.duration()

    def seek(self, position):
        """
        Jump to position in milliseconds
        """
        self.player.setPosition(position)
