# Kivy Music Player

A mobile music player built with Python and Kivy, targeting Android. Features artist-based playlists, playback controls, a persistent song bar, and optional pygame audio backend.


## Features

- **Multi-playlist support** — browse songs by artist:
  - Against The Current
  - Ghost
  - Judas Priest
  - Random Mix

- **Search and Top Songs**
  - Search for songs directly from the Home screen
  - Tracks play counts via SQLite to dynamically manage song popularity

- **Playlist play & shuffle**
  - Play playlists in order
  - Shuffle directly from the playlist header

- **Persistent song bar**
  - Fixed bottom playback bar
  - Displays current song title
  - Play/Pause toggle
  - Live progress bar with drag-to-seek support

- **Auto-advance**
  - Automatically plays the next track
  - Loops back to the start of the playlist

- **Volume control**
  - Real-time volume slider in the Settings screen

- **Android Media Session & Background Service**
  - True background playback on Android via a dedicated Python service (`service.py`)
  - Inter-Process Communication (IPC) between UI and Service via OSC protocol
  - Lock screen metadata support
  - Android system media controls via `androidx.media`

- **Screen navigation**
  - Home screen
  - Playlist screen
  - Settings screen
  - Persistent bottom navigation bar

---

## Requirements

- Python 3.x
- Kivy  
- Pygame
- oscpy (for IPC)
For Android builds: Buildozer with androidx.media in dependencies
MP3 files placed in a songs/ directory alongside main.py

## Project Structure

```text
project/
├── main.py
├── service.py              # Background audio service (Android)
├── db.py                   # SQLite database operations
├── songs/                  # MP3 files (not included)
│   ├── its_my_life.mp3
│   └── ...
├── home_logo.png
├── playlist_logo.png
├── settings_logo.png
├── play_logo.png
├── pause_logo.png
├── playlist_play_logo.png
├── playlist_shuffle_logo.png
└── welcome_img.png
```

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
