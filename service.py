import os
import sys
import json
import time
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

# Ensure Kivy doesn't try to open a window
os.environ["KIVY_AUDIO"] = "sdl2"
os.environ["KIVY_NO_ARGS"] = "1"

# Initialize Pygame Mixer directly for background audio
import pygame
if not pygame.mixer.get_init():
    pygame.mixer.init()

from db import increment_play_count

from jnius import autoclass, cast
from android.broadcast import BroadcastReceiver

PythonService = autoclass('org.kivy.android.PythonService')
mService = PythonService.mService
Context = autoclass('android.content.Context')
Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
NotificationCompat = autoclass('androidx.core.app.NotificationCompat')
NotificationManager = autoclass('android.app.NotificationManager')
NotificationChannel = autoclass('android.app.NotificationChannel')
MediaSessionCompat = autoclass('androidx.media.session.MediaSessionCompat')
PlaybackStateCompat = autoclass('androidx.media.session.PlaybackStateCompat')
MediaMetadataCompat = autoclass('androidx.media.MediaMetadataCompat')
IconCompat = autoclass('androidx.core.graphics.drawable.IconCompat')
RDrawable = autoclass('android.R$drawable')
String = autoclass('java.lang.String')
System = autoclass('java.lang.System')
MediaStyle = autoclass('androidx.media.app.NotificationCompat$MediaStyle')

CLIENT_PORT = 3001
SERVER_PORT = 3000

osc = OSCThreadServer()
osc.listen(address='127.0.0.1', port=SERVER_PORT, default=True)
client = OSCClient('127.0.0.1', CLIENT_PORT)

class AudioPlayerService:
    def __init__(self):
        self.is_playing = False
        self.is_paused = False
        self.current_song_path = ""
        self.current_song_name = ""
        self.current_song_title = "No Song Playing"
        self.current_song_artist = "Unknown"
        self.paused_pos = 0.0
        self.play_start_time = 0.0
        self.accumulated_time = 0.0
        self.playlist = []
        self.current_index = -1
        self.sound = None
        self.volume = 1.0

        self.session = MediaSessionCompat(mService, "KivyMusicService")
        self.session.setActive(True)

        self._setup_notification_channel()
        self._setup_broadcast_receiver()

    def _setup_notification_channel(self):
        if System.getProperty("os.version") >= "8.0.0":
            channel = NotificationChannel("music_channel", "Music Playback", NotificationManager.IMPORTANCE_LOW)
            channel.setDescription("Music playback controls")
            notification_manager = cast('android.app.NotificationManager', mService.getSystemService(Context.NOTIFICATION_SERVICE))
            notification_manager.createNotificationChannel(channel)

    def _setup_broadcast_receiver(self):
        self.br = BroadcastReceiver(self.on_broadcast, actions=['org.music.PLAY', 'org.music.PAUSE', 'org.music.NEXT', 'org.music.PREV'])
        self.br.start()

    def on_broadcast(self, context, intent):
        action = intent.getAction()
        if action == 'org.music.PLAY':
            self.unpause()
        elif action == 'org.music.PAUSE':
            self.pause()
        elif action == 'org.music.NEXT':
            self.play_next()
        elif action == 'org.music.PREV':
            self.play_prev()

    def get_pending_intent(self, action_string):
        intent = Intent(action_string)
        intent.setPackage(mService.getPackageName())
        flags = PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        return PendingIntent.getBroadcast(mService, 0, intent, flags)

    def update_notification(self):
        builder = NotificationCompat.Builder(mService, "music_channel")
        builder.setContentTitle(self.current_song_title)
        builder.setContentText(self.current_song_artist)
        builder.setSmallIcon(RDrawable.ic_media_play)
        builder.setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
        builder.setOnlyAlertOnce(True)
        builder.setOngoing(self.is_playing)

        # Prev Action
        prev_intent = self.get_pending_intent('org.music.PREV')
        builder.addAction(RDrawable.ic_media_previous, "Previous", prev_intent)

        # Play/Pause Action
        if self.is_playing:
            pause_intent = self.get_pending_intent('org.music.PAUSE')
            builder.addAction(RDrawable.ic_media_pause, "Pause", pause_intent)
        else:
            play_intent = self.get_pending_intent('org.music.PLAY')
            builder.addAction(RDrawable.ic_media_play, "Play", play_intent)

        # Next Action
        next_intent = self.get_pending_intent('org.music.NEXT')
        builder.addAction(RDrawable.ic_media_next, "Next", next_intent)

        # MediaStyle
        style = MediaStyle()
        style.setMediaSession(self.session.getSessionToken())
        style.setShowActionsInCompactView(0, 1, 2)
        builder.setStyle(style)

        notification = builder.build()
        mService.startForeground(1, notification)

    def play_song(self, path, song_name, title, artist):
        self.current_song_path = path
        self.current_song_name = song_name
        self.current_song_title = title
        self.current_song_artist = artist

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            pygame.mixer.music.set_volume(self.volume)
            snd = pygame.mixer.Sound(path)
            self.length = snd.get_length()
        except Exception as e:
            self.length = 0.0

        self.is_playing = True
        self.is_paused = False
        self.paused_pos = 0.0
        self.accumulated_time = 0.0
        self.play_start_time = time.time()
        
        self.update_metadata(title, artist)
        self.update_playback_state()
        self.update_notification()
        self.send_status()

    def update_metadata(self, title, artist):
        metadata = (MediaMetadataCompat.Builder()
                    .putString(MediaMetadataCompat.METADATA_KEY_TITLE, title)
                    .putString(MediaMetadataCompat.METADATA_KEY_ARTIST, artist)
                    .build())
        self.session.setMetadata(metadata)

    def update_playback_state(self):
        state_val = PlaybackStateCompat.STATE_PLAYING if self.is_playing else PlaybackStateCompat.STATE_PAUSED
        state = (PlaybackStateCompat.Builder()
                 .setActions(PlaybackStateCompat.ACTION_PLAY | PlaybackStateCompat.ACTION_PAUSE | PlaybackStateCompat.ACTION_SKIP_TO_NEXT | PlaybackStateCompat.ACTION_SKIP_TO_PREVIOUS)
                 .setState(state_val, int(self.get_pos() * 1000), 1.0)
                 .build())
        self.session.setPlaybackState(state)

    def pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.paused_pos = self.get_pos()
            self.is_playing = False
            self.is_paused = True
            self.update_playback_state()
            self.update_notification()
            self.send_status()

    def unpause(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.is_paused = False
            self.accumulated_time = self.paused_pos
            self.play_start_time = time.time()
            self.update_playback_state()
            self.update_notification()
            self.send_status()

    def seek(self, pos):
        pygame.mixer.music.play(start=pos)
        if self.is_paused:
            pygame.mixer.music.pause()
            self.paused_pos = pos
        self.accumulated_time = pos
        self.play_start_time = time.time()
        self.send_status()

    def set_volume(self, vol):
        self.volume = vol
        pygame.mixer.music.set_volume(vol)

    def get_pos(self):
        if self.is_paused:
            return self.paused_pos
        elif self.is_playing:
            return self.accumulated_time + (time.time() - self.play_start_time)
        return 0.0

    def play_song_dict(self, song_dict):
        song_name = song_dict["name"]
        path = song_dict["path"]
        parts  = song_name.split("\n")
        title  = parts[0].strip()
        artist = parts[1].strip().lstrip("-").strip() if len(parts) > 1 else "Unknown"
        increment_play_count(song_name)
        self.play_song(path, song_name, title, artist)

    def play_next(self):
        if self.playlist:
            idx = -1
            for i, p in enumerate(self.playlist):
                if p["name"] == self.current_song_name:
                    idx = i
                    break
            if idx != -1:
                next_idx = (idx + 1) % len(self.playlist)
                self.play_song_dict(self.playlist[next_idx])
            else:
                self.play_song_dict(self.playlist[0])

    def play_prev(self):
        if self.playlist:
            idx = -1
            for i, p in enumerate(self.playlist):
                if p["name"] == self.current_song_name:
                    idx = i
                    break
            if idx != -1:
                prev_idx = (idx - 1) % len(self.playlist)
                self.play_song_dict(self.playlist[prev_idx])
            else:
                self.play_song_dict(self.playlist[-1])

    def send_status(self):
        status = {
            'is_playing': self.is_playing,
            'is_paused': self.is_paused,
            'pos': self.get_pos(),
            'length': getattr(self, 'length', 0.0),
            'song_name': self.current_song_name,
            'title': self.current_song_title,
            'artist': self.current_song_artist
        }
        client.send_message(b'/status', [json.dumps(status).encode('utf-8')])

    def tick(self):
        if self.is_playing and not pygame.mixer.music.get_busy() and (time.time() - self.play_start_time > 1.0):
            self.play_next()

player = AudioPlayerService()

@osc.address(b'/play')
def on_play(path, song_name, title, artist, playlist_json):
    path = path.decode('utf-8')
    song_name = song_name.decode('utf-8')
    title = title.decode('utf-8')
    artist = artist.decode('utf-8')
    playlist = json.loads(playlist_json.decode('utf-8'))
    player.playlist = playlist
    player.play_song(path, song_name, title, artist)

@osc.address(b'/pause')
def on_pause():
    player.pause()

@osc.address(b'/unpause')
def on_unpause():
    player.unpause()

@osc.address(b'/seek')
def on_seek(pos):
    player.seek(pos)

@osc.address(b'/volume')
def on_volume(vol):
    player.set_volume(vol)

@osc.address(b'/sync')
def on_sync():
    player.send_status()

if __name__ == '__main__':
    while True:
        player.tick()
        time.sleep(0.1)
