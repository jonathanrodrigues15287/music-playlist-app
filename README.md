Kivy Music Player
A mobile music player app built with Python and Kivy, designed for Android (360×640px). Features multiple artist playlists, a persistent playback bar, volume control, and Android media session integration.

Features

Multi-playlist support — browse songs by artist: Against The Current, Ghost, Judas Priest, and a Random mix
Persistent song bar — fixed bottom bar shows the current song title, a play/pause toggle, and a live progress bar
Volume control — slider in the Settings screen adjusts playback volume in real time
Pause & resume with seek — pausing saves the playback position; resuming seeks back to that position
Android Media Session — integrates with Android's system media controls and lock screen metadata (title + artist) via androidx.media
Screen navigation — Home, Playlists, and Settings screens with a persistent bottom nav bar

Requirements

Python 3.x
Kivy (pip install kivy)
For Android builds: Buildozer with androidx.media in dependencies
MP3 files placed in a songs/ directory alongside main.py

Project Structure
project/
├── main.py                  # All app logic
├── songs/                   # MP3 files (not included)
│   ├── its_my_life.mp3
│   └── ...
├── home_logo.png
├── playlist_logo.png
├── settings_logo.png
├── play_logo.png
├── pause_logo.png
└── welcome_img.png

Adding Songs
Drop the .mp3 file into the songs/ folder.
Add an entry to the SONGS dict in main.py:
python   "Song Title\n -Artist Name": "songs/filename.mp3",
Add the song string to the relevant screen's song list (e.g. AtcScreen, GhostScreen).


Adding a New Playlist
Create a new Screen subclass (follow the pattern of AtcScreen).
Register it in MyApp.build():
python   sm.add_widget(MyNewScreen(name="my_screen"))
Add a button for it in PlaylistScreen.
