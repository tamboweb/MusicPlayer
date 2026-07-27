import os


SUPPORTED_FORMATS = [
    ".mp3",
    ".flac",
    ".wav",
    ".ogg"
]


def scan_music(folder_path):
    """
    Scan a folder and return a list of supported audio files.
    """

    songs = []

    for root, directories, files in os.walk(folder_path):
        for file in files:
            extension = os.path.splitext(file)[1].lower()

            if extension in SUPPORTED_FORMATS:
                full_path = os.path.join(
                    root,
                    file
                )

                songs.append(full_path)

    return sorted(songs)


def get_song_name(file_path):
    """
    Returns a clean song name without the file extension.
    """

    filename = os.path.basename(file_path)

    return os.path.splitext(filename)[0]


def get_artist_folder(file_path):
    """
    Gets the folder name (useful for organising artists/albums).
    """

    folder = os.path.dirname(file_path)

    return os.path.basename(folder)
