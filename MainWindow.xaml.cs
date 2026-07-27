using System;
using System.Collections.Generic;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace MusicPlayer
{
    public partial class MainWindow : Window
    {
        private MediaPlayer player = new MediaPlayer();

        private List<string> songs = new List<string>();
        private int currentSong = -1;


        public MainWindow()
        {
            InitializeComponent();

            player.Volume = 0.5;
        }


        private void OpenFolder_Click(object sender, RoutedEventArgs e)
        {
            using (var dialog = new System.Windows.Forms.FolderBrowserDialog())
            {
                if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                {
                    LoadMusic(dialog.SelectedPath);
                }
            }
        }


        private void LoadMusic(string folder)
        {
            songs.Clear();
            SongList.Items.Clear();


            string[] files = Directory.GetFiles(
                folder,
                "*.*",
                SearchOption.AllDirectories
            );


            foreach (string file in files)
            {
                string extension = Path.GetExtension(file)
                    .ToLower();


                if (extension == ".mp3" ||
                    extension == ".wav" ||
                    extension == ".flac" ||
                    extension == ".ogg")
                {
                    songs.Add(file);

                    SongList.Items.Add(
                        Path.GetFileNameWithoutExtension(file)
                    );
                }
            }
        }


        private void SongList_SelectionChanged(
            object sender,
            SelectionChangedEventArgs e)
        {
            currentSong = SongList.SelectedIndex;

            if (currentSong >= 0)
            {
                PlaySong();
            }
        }


        private void PlaySong()
        {
            if (currentSong < 0)
                return;


            player.Open(
                new Uri(
                    songs[currentSong]
                )
            );

            player.Play();


            NowPlaying.Text =
                Path.GetFileNameWithoutExtension(
                    songs[currentSong]
                );
        }


        private void Play_Click(
            object sender,
            RoutedEventArgs e)
        {
            player.Play();
        }


        private void Pause_Click(
            object sender,
            RoutedEventArgs e)
        {
            player.Pause();
        }


        private void Next_Click(
            object sender,
            RoutedEventArgs e)
        {
            if (songs.Count == 0)
                return;


            currentSong++;


            if (currentSong >= songs.Count)
                currentSong = 0;


            SongList.SelectedIndex = currentSong;

            PlaySong();
        }


        private void VolumeSlider_ValueChanged(
            object sender,
            RoutedPropertyChangedEventArgs<double> e)
        {
            player.Volume =
                VolumeSlider.Value / 100;
        }
    }
}
