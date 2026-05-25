# Kivy Music Player

A mobile music player built with Python and Kivy, targeting Android. Features artist-based playlists, playback controls, a persistent song bar, and optional pygame audio backend.


## Features

- **Multi-playlist support** — browse songs by artist:
  - Against The Current
  - Ghost
  - Judas Priest
  - Random Mix

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

- **Pause & resume with seek**
  - Saves playback position when paused
  - Resumes from the saved timestamp

- **Android Media Session integration**
  - Lock screen metadata support
  - Android system media controls via `androidx.media`

- **Dual audio backend**
  - Uses `pygame.mixer` when available for better seek support
  - Automatically falls back to Kivy `SoundLoader`

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
For Android builds: Buildozer with androidx.media in dependencies
MP3 files placed in a songs/ directory alongside main.py

## Project Structure

```text
project/
├── main.py
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
