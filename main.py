from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Line, Rectangle
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
import time
import random
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def resource_path(path):
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, *path.split('/'))


from kivy.utils import platform
if platform not in ('android', 'ios'):
    Window.size = (360, 640)

#initialisation of pygame on user device
USE_PYGAME = False
try:
    import pygame
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    USE_PYGAME = True
except ImportError:
    USE_PYGAME = False

class PygameSoundWrapper:
    def __init__(self, path):
        self.path = path
        try:
            snd = pygame.mixer.Sound(path)
            self.length = snd.get_length()
        except Exception:
            self.length = 0.0
        pygame.mixer.music.load(path)
        self._volume = 1.0

    def play(self):
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def seek(self, pos):
        pygame.mixer.music.play(start=pos)
        if player.is_paused:
            pygame.mixer.music.pause()

    def get_pos(self):
        return 0.0

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, val):
        self._volume = val
        pygame.mixer.music.set_volume(val)

    @property
    def state(self):
        if pygame.mixer.music.get_busy():
            return 'play'
        return 'stop'

#global state object
class PlayerState:
    def __init__(self):
        self.sound = None
        self.song_name = ""
        self.is_paused = False
        self.volume = 1.0
        self.paused_pos = 0.0
        self.song_bar = None
        self.play_start_time = 0.0
        self.accumulated_time = 0.0
        self.current_playlist = []
        self.is_search_looping = False

player = PlayerState() 

#random songs playlist
RANDOM_SONGS = {
    "It's My Life\n -Bon Jovi": "songs/its_my_life.mp3",
    "They Don't Care About Us\n -Michael Jackson": "songs/they_dont_care_about_us.mp3",
    "Can't Help Falling in Love\n -Elvis Presley": "songs/cant_help_falling_in_love.mp3",
    "All of Me\n -John Legend": "songs/all_of_me.mp3",
    "Hymn For the Weekend\n -Coldplay": "songs/hymn_for_the_weekend.mp3",
    "Way Down we go\n -Kaleo": "songs/way_down_we_go.mp3",
    "House of Memories\n -Panic! At the Disco": "songs/house_of_memories.mp3",
    "Another Love\n -Tom Odell": "songs/another_love.mp3",
    "Superbeast\n -Rob Zombie": "songs/superbeast.mp3",
    "Ordinary\n -Alex Warren": "songs/ordinary.mp3",
    "Bella Ciao\n -Manu Pilas": "songs/bella_ciao.mp3",
    "Oh What a Circus\n -Antonio Banderas": "songs/oh_what_a_circus.mp3",
    "Numb Little Bug\n -Em Beihold": "songs/numb_little_bug.mp3",
}

#judas priest playlist
JP_SONGS = {
    "Breaking the Law\n -Judas Priest": "songs/breaking_the_law.mp3",
    "You've Got Another Thing Coming\n -Judas Priest": "songs/youve_got_another_thing_coming.mp3",
    "Living After Midnight\n -Judas Priest": "songs/living_after_midnight.mp3",
    "Painkiller\n -Judas Priest": "songs/painkiller.mp3",
    "Electric Eye\n -Judas Priest": "songs/electric_eye.mp3",
    "The Hellion\n -Judas Priest": "songs/the_hellion.mp3",
    "Hell Bent for Leather\n -Judas Priest": "songs/hell_bent_for_leather.mp3",
    "Screaming for Vengeance\n -Judas Priest": "songs/screaming_for_vengeance.mp3",
    "Turbo Lover\n -Judas Priest": "songs/turbo_lover.mp3",
    "Beyond the Realms of Death\n -Judas Priest": "songs/beyond_the_realms_of_death.mp3",
    "Victim of Changes\n -Judas Priest": "songs/victim_of_changes.mp3",
    "Freewheel Burning\n -Judas Priest": "songs/freewheel_burning.mp3",
    "The Sentinel\n -Judas Priest": "songs/the_sentinel.mp3",
    "Metal Gods\n -Judas Priest": "songs/metal_gods.mp3",
    "Heading Out to the Highway\n -Judas Priest": "songs/heading_out_to_the_highway.mp3",
    "Night Crawler\n -Judas Priest": "songs/night_crawler.mp3",
    "A Touch of Evil\n -Judas Priest": "songs/a_touch_of_evil.mp3",
    "Sinner\n -Judas Priest": "songs/sinner.mp3",
    "Exciter\n -Judas Priest": "songs/exciter.mp3",
    "Desert Plains\n -Judas Priest": "songs/desert_plains.mp3",
    "Dissident Aggressor\n -Judas Priest": "songs/dissident_aggressor.mp3",
    "Tyrant\n -Judas Priest": "songs/tyrant.mp3",
    "Running Wild\n -Judas Priest": "songs/running_wild.mp3",
    "Blood Red Skies\n -Judas Priest": "songs/blood_red_skies.mp3",
    "Before the Dawn\n -Judas Priest": "songs/before_the_dawn.mp3",
    "Dreamer Deceiver\n -Judas Priest": "songs/dreamer_deceiver.mp3",
    "Rock Hard Ride Free\n -Judas Priest": "songs/rock_hard_ride_free.mp3",
    "Between the Hammer and the Anvil\n -Judas Priest": "songs/between_the_hammer_and_the_anvil.mp3",
    "Hell Patrol\n -Judas Priest": "songs/hell_patrol.mp3",
    "Judas Rising\n -Judas Priest": "songs/judas_rising.mp3",
    "Firepower\n -Judas Priest": "songs/firepower.mp3",
    "Never the Heroes\n -Judas Priest": "songs/never_the_heroes.mp3",
    "Halls of Valhalla\n -Judas Priest": "songs/halls_of_valhalla.mp3",
    "Traitors Gate\n -Judas Priest": "songs/traitors_gate.mp3",
    "Steeler\n -Judas Priest": "songs/steeler.mp3",
}

#against the current playlist
ATC_SONGS = {
    "I Like the Way\n -Against The Current": "songs/i_like_the_way.mp3",
    "Runaway\n -Against The Current": "songs/runaway.mp3",
    "Strangers Again\n -Against The Current": "songs/strangers_again.mp3",
    "Demons\n -Against The Current": "songs/demons.mp3",
    "Chasing Ghosts\n -Against The Current": "songs/chasing_ghosts.mp3",
    "Closer, Faster\n -Against The Current": "songs/closer_faster.mp3",
    "Outsiders\n -Against The Current": "songs/outsiders.mp3",
    "Blood Like Gasoline\n -Against The Current": "songs/blood_like_gasoline.mp3",
    "Roses\n -Against The Current": "songs/roses.mp3",
    "One More Weekend\n -Against The Current": "songs/one_more_weekend.mp3",
    "Sweet Surrender\n -Against The Current": "songs/sweet_surrender.mp3",
    "Come Alive\n -Against The Current": "songs/come_alive.mp3",
    "weapon - acoustic\n -Against The Current": "songs/weapon_acoustic.mp3",
    "weapon\n -Against The Current": "songs/weapon.mp3",
    "that won't save us\n -Against The Current": "songs/that_wont_save_us.mp3",
    "Voices\n -Against The Current": "songs/voices.mp3",
    "Legends Never Die\n -League of Legends, Against The Current": "songs/legends_never_die.mp3",
    "Almost Forgot - Ryan Riback Remix\n -Against The Current, Ryan Riback": "songs/almost_forgot_ryan_riback_remix.mp3",
    "Brighter\n -Against The Current": "songs/brighter.mp3",
    "Running with the Wild Things\n -Against The Current": "songs/running_with_the_wild_things.mp3",
    "Gravity - Acoustic\n -Against The Current": "songs/gravity_acoustic.mp3",
    "Forget Me Now\n -Against The Current": "songs/forget_me_now.mp3",
    "good guy\n -Against The Current": "songs/good_guy.mp3",
    "blindfolded\n -Against The Current": "songs/blindfolded.mp3",
    "silent stranger\n -Against The Current": "songs/silent_stranger.mp3",
    "Something You Need\n -Against The Current": "songs/something_you_need.mp3",
    "Another You (Another Way)\n -Against The Current": "songs/another_you_another_way.mp3",
    "The Fuss\n -Against The Current": "songs/the_fuss.mp3",
    "In Our Bones\n -Against The Current": "songs/in_our_bones.mp3",
    "again&again\n -Against The Current, guardin": "songs/again_and_again.mp3",
    "burn it down\n -Against The Current": "songs/burn_it_down.mp3",
    "lullaby\n -Against The Current": "songs/lullaby.mp3",
    "shatter\n -Against The Current": "songs/shatter.mp3",
    "jump\n -Against The Current": "songs/jump.mp3",
    "Wildfire\n -Against The Current": "songs/wildfire.mp3",
    "Talk\n -Against The Current": "songs/talk.mp3",
    "Paralyzed - Acoustic\n -Against The Current": "songs/paralyzed_acoustic.mp3",
    "Wasteland\n -Against The Current": "songs/wasteland.mp3",
    "See You Again\n -ATC": "songs/see_you_again.mp3",
    "One More Night\n -Alex Goot, ATC, Julia Sheer, Luke Conard, Chad Sugg": "songs/one_more_night.mp3",
    "P.A.T.T.\n -Against The Current": "songs/patt.mp3",
    "Personal\n -Against The Current": "songs/personal.mp3",
    "Scream\n -Against The Current": "songs/scream.mp3",
    "Young & Relentless\n -Against The Current": "songs/young_and_relentless.mp3",
    "Fireproof\n -Against The Current": "songs/fireproof.mp3",
    "Friendly Reminder\n -Against The Current": "songs/friendly_reminder.mp3",
    "Infinity\n -Against The Current": "songs/infinity.mp3",
    "Dreaming Alone\n -Against The Current, Taka": "songs/dreaming_alone.mp3",
    "Guessing\n -ATC": "songs/guessing.mp3",
    "Heavenly\n -Against The Current": "songs/heavenly.mp3",
    "Dead Man Walking\n -Against The Current": "songs/dead_man_walking.mp3",
}

#ghost playlist
GHOST_SONGS = {
    "Year Zero\n -Ghost": "songs/year_zero.mp3",
    "Mary On A Cross\n -Ghost": "songs/mary_on_a_cross.mp3",
    "Square Hammer\n -Ghost": "songs/square_hammer.mp3",
    "Dance Macabre\n -Ghost": "songs/dance_macabre.mp3",
    "Call Me Little Sunshine\n -Ghost": "songs/call_me_little_sunshine.mp3",
    "Spillways\n -Ghost": "songs/spillways.mp3",
    "Cirice\n -Ghost": "songs/cirice.mp3",
    "The Future Is A Foreign Land\n -Ghost": "songs/the_future_is_a_foreign_land.mp3",
    "Life Eternal\n -Ghost": "songs/life_eternal.mp3",
    "Kiss The Go-Goat\n -Ghost": "songs/kiss_the_go_goat.mp3",
    "Darkness At The Heart Of My Love\n -Ghost": "songs/darkness_at_the_heart_of_my_love.mp3",
    "Kaisarion\n -Ghost": "songs/kaisarion.mp3",
    "Hunter's Moon\n -Ghost": "songs/hunters_moon.mp3",
    "Jesus He Knows Me\n -Ghost": "songs/jesus_he_knows_me.mp3",
    "Griftwood\n -Ghost": "songs/griftwood.mp3",
    "Watcher In The Sky\n -Ghost": "songs/watcher_in_the_sky.mp3",
    "Respite On The Spitalfields\n -Ghost": "songs/respite_on_the_spitalfields.mp3",
    "Twenties\n -Ghost": "songs/twenties.mp3",
    "Monstrance Clock\n -Ghost": "songs/monstrance_clock.mp3",
    "He Is\n -Ghost": "songs/he_is.mp3",
    "He Is (feat. Alison Mosshart)\n -Ghost": "songs/he_is_feat_alison_mosshart.mp3",
    "See The Light\n -Ghost": "songs/see_the_light.mp3",
    "Enter Sandman\n -Ghost": "songs/enter_sandman.mp3",
    "Phantom Of The Opera\n -Ghost": "songs/phantom_of_the_opera.mp3",
    "Imperium\n -Ghost": "songs/imperium.mp3",
    "Miasma\n -Ghost": "songs/miasma.mp3",
    "Pro Memoria\n -Ghost": "songs/pro_memoria.mp3",
    "Infestissumam\n -Ghost": "songs/infestissumam.mp3",
    "Ashes\n -Ghost": "songs/ashes.mp3",
    "Helvetesfonster\n -Ghost": "songs/helvetesfonster.mp3",
    "Witch Image\n -Ghost": "songs/witch_image.mp3",
    "Ritual\n -Ghost": "songs/ritual.mp3",
    "Jigolo Har Megiddo\n -Ghost": "songs/jigolo_har_megiddo.mp3",
    "Stay [Feat. Patrick Wilson]\n -Ghost, Patrick Wilson": "songs/stay.mp3",
    "Faith\n -Ghost": "songs/faith.mp3",
    "Lachryma\n -Ghost": "songs/lachryma.mp3",
    "Missionary Man\n -Ghost": "songs/missionary_man.mp3",
}

SONGS = {**RANDOM_SONGS, **JP_SONGS, **ATC_SONGS, **GHOST_SONGS}


#bridge between app and android media controls
class AndroidMediaSession:
    def __init__(self):
        self.session = None
        self._PlaybackStateCompat = None
        self._MediaMetadataCompat = None
        self._setup()

    def _setup(self):
        try:
            from jnius import autoclass

            PythonActivity      = autoclass('org.kivy.android.PythonActivity')
            MediaSessionCompat  = autoclass('androidx.media.session.MediaSessionCompat')
            PlaybackStateCompat = autoclass('androidx.media.session.PlaybackStateCompat')
            MediaMetadataCompat = autoclass('androidx.media.MediaMetadataCompat')

            self._PlaybackStateCompat = PlaybackStateCompat
            self._MediaMetadataCompat = MediaMetadataCompat

            activity = PythonActivity.mActivity
            context  = activity.getApplicationContext()

            self.session = MediaSessionCompat(context, "KivyMusicPlayer")

            actions = (
                PlaybackStateCompat.ACTION_PLAY |
                PlaybackStateCompat.ACTION_PAUSE |
                PlaybackStateCompat.ACTION_STOP |
                PlaybackStateCompat.ACTION_SKIP_TO_NEXT |
                PlaybackStateCompat.ACTION_SKIP_TO_PREVIOUS
            )

            state = (PlaybackStateCompat.Builder()
                     .setActions(actions)
                     .setState(PlaybackStateCompat.STATE_STOPPED, 0, 1.0)
                     .build())

            self.session.setPlaybackState(state)
            self.session.setActive(True)

            logging.info("MediaSession initialised successfully")

        except Exception as e:
            logging.warning(f"MediaSession not available (non-Android): {e}")
            self.session = None

    def update_metadata(self, title, artist):
        if not self.session:
            return
        try:
            metadata = (self._MediaMetadataCompat.Builder()
                        .putString(self._MediaMetadataCompat.METADATA_KEY_TITLE, title)
                        .putString(self._MediaMetadataCompat.METADATA_KEY_ARTIST, artist)
                        .build())
            self.session.setMetadata(metadata)
        except Exception as e:
            logging.error(f"MediaSession metadata error: {e}")

    def set_playing(self, is_playing):
        if not self.session:
            return
        try:
            state_val = (self._PlaybackStateCompat.STATE_PLAYING
                         if is_playing
                         else self._PlaybackStateCompat.STATE_PAUSED)
            state = (self._PlaybackStateCompat.Builder()
                     .setState(state_val, 0, 1.0)
                     .build())
            self.session.setPlaybackState(state)
        except Exception as e:
            logging.error(f"MediaSession state error: {e}")

    def release(self):
        if self.session:
            self.session.setActive(False)
            self.session.release()

media_session = AndroidMediaSession()

#song bar controls and ui design 
class SongBar(FloatLayout):
    BAR_H  = dp(50)  
    PROG_H = dp(3)   
    BTN_W  = dp(45)   
    BTN_H  = dp(45)   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dragging = False
        self._drag_pos = 0.0

        self.size_hint = (1, None)
        self.height = self.BAR_H
        self.pos_hint = {'x': 0, 'y': 0.078125}
        
        with self.canvas.before:
            Color(0.05, 0.05, 0.05, 1)
            self._bg = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_bg, size=self._update_bg)

        with self.canvas:
            Color(0.2, 0.2, 0.2, 1)
            self._track = Rectangle(pos=self.pos, size=(self.width, self.PROG_H))

        with self.canvas:
            Color(0.0, 0.9, 1.0, 1)
            self._fill = Rectangle(pos=self.pos, size=(0, self.PROG_H))

        self.title_label = Label(
            text="No song playing",
            size_hint=(None, None),
            size=(0, self.BAR_H - self.PROG_H),
            pos=(dp(5), self.y),
            color=(1, 1, 1, 1),
            halign="left",
            valign="middle",
            font_size=dp(12),
            shorten=True,
            shorten_from="right",
        )
        self.title_label.bind(
            size=lambda inst, val: setattr(inst, 'text_size', inst.size)
        )
        self.add_widget(self.title_label)

        self.play_btn = Button(
            text="",
            size_hint=(None, None),
            size=(self.BTN_W, self.BTN_H),
            background_normal=resource_path("pause_logo.png"),   
            background_down=resource_path("pause_logo.png"),
            border=(0, 0, 0, 0),
        )
        self.play_btn.bind(on_press=self._toggle_pause)
        self.add_widget(self.play_btn)

        self.bind(pos=self._reposition_children, size=self._reposition_children)
        Clock.schedule_once(lambda dt: self._reposition_children(self, None), 0)

        Clock.schedule_interval(self._tick, 0.05)

    def _update_bg(self, *args):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def _reposition_children(self, inst, val):
        x, y = self.pos
        self.title_label.size = (self.width - self.BTN_W - dp(10), self.BAR_H - self.PROG_H)
        self.title_label.pos = (x + dp(5), y)
        self.play_btn.pos    = (x + self.width - self.BTN_W - dp(5), y + self.BAR_H - self.PROG_H - self.BTN_H)
        self._track.pos  = (x, y + self.BAR_H - self.PROG_H)
        self._track.size = (self.width, self.PROG_H)
        self._fill.pos   = (x, y + self.BAR_H - self.PROG_H)

    def _tick(self, dt):
        self._refresh_progress()

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        
        if self.collide_point(*touch.pos):
            if touch.y >= self.y + self.BAR_H - dp(25):
                self._dragging = True
                self._update_drag(touch)
                touch.grab(self)
                return True
        return False

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self._update_drag(touch)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self._apply_seek()
            self._dragging = False
            return True
        return super().on_touch_up(touch)

    def _update_drag(self, touch):
        if not player.sound:
            return
        
        local_x = touch.x - self.x
        ratio = max(0.0, min(1.0, local_x / self.width))
        
        duration = player.sound.length
        if not duration or duration <= 0:
            return
            
        self._drag_pos = ratio * duration
        
        x, y = self.pos
        bar_y = y + self.BAR_H - self.PROG_H
        self._fill.pos  = (x, bar_y)
        self._fill.size = (self.size[0] * ratio, self.PROG_H)

    def _apply_seek(self):
        if not player.sound:
            return
            
        target_pos = self._drag_pos
        
        if USE_PYGAME:
            player.sound.seek(target_pos)
        else:
            if player.is_paused:
                player.paused_pos = target_pos
            else:
                player.sound.seek(target_pos)
                
        player.play_start_time = time.time()
        player.accumulated_time = target_pos
        if player.is_paused:
            player.paused_pos = target_pos

    def _refresh_progress(self):
        if self._dragging:
            return

        if player.is_paused:
            position = player.paused_pos
        elif player.sound:
            pos = player.sound.get_pos()
            if pos > 0:
                position = pos
            else:
                position = player.accumulated_time + (time.time() - player.play_start_time)
        else:
            position = 0.0

        duration = player.sound.length if player.sound else 0
        if duration and duration > 0:
            position = min(position, duration)
            ratio = max(0.0, min(1.0, position / duration))
        else:
            ratio = 0.0

        if player.sound and player.sound.state == 'stop' and not player.is_paused and (time.time() - player.play_start_time > 0.5):
            if not play_next_song():
                player.is_paused = False
                player.paused_pos = 0.0
                player.accumulated_time = 0.0
                position = 0.0
                ratio = 0.0
                self.play_btn.background_normal = resource_path("play_logo.png")
                self.play_btn.background_down   = resource_path("play_logo.png")
                media_session.set_playing(False)

        x, y = self.pos
        bar_y = y + self.BAR_H - self.PROG_H
        self._track.pos  = (x, bar_y)
        self._track.size = (self.size[0], self.PROG_H)
        self._fill.pos   = (x, bar_y)
        self._fill.size  = (self.size[0] * ratio, self.PROG_H)

    def _toggle_pause(self, instance):
        if player.sound is None:
            return

        if player.is_paused:
            pos_to_seek = player.paused_pos
            if USE_PYGAME:
                pygame.mixer.music.unpause()
            else:
                player.sound.play()
                Clock.schedule_once(lambda dt: player.sound.seek(pos_to_seek), 0.3)
            player.is_paused = False
            player.play_start_time = time.time()
            player.accumulated_time = pos_to_seek
            self.play_btn.background_normal = resource_path("pause_logo.png")
            self.play_btn.background_down   = resource_path("pause_logo.png")
            media_session.set_playing(True)
        else:
            pos = player.sound.get_pos()
            if pos <= 0:
                pos = player.accumulated_time + (time.time() - player.play_start_time)
            player.paused_pos = min(pos, player.sound.length if player.sound.length else pos)
            if USE_PYGAME:
                pygame.mixer.music.pause()
            else:
                player.sound.stop()
            player.is_paused = True
            self.play_btn.background_normal = resource_path("play_logo.png")
            self.play_btn.background_down   = resource_path("play_logo.png")
            media_session.set_playing(False)

    def on_new_song(self, song_name):
        player.is_paused  = False
        player.paused_pos = 0.0
        player.accumulated_time = 0.0
        self.play_btn.background_normal = resource_path("pause_logo.png")
        self.play_btn.background_down   = resource_path("pause_logo.png")

        title = song_name.split("\n")[0].strip()
        self.title_label.text = title

        self._refresh_progress()

#plays song after selection
def play_music(song_name, from_search=False):
    player.is_search_looping = from_search
    song_name = song_name.strip()

    if song_name not in SONGS:
        spaced = " " + song_name
        if spaced in SONGS:
            song_name = spaced
        else:
            logging.warning(f"No song file mapped for: {song_name}")
            return

    if player.sound:
        player.sound.stop()
        player.sound = None

    player.is_paused  = False
    player.paused_pos = 0.0
    player.accumulated_time = 0.0

    song_path     = SONGS[song_name]
    song_path = resource_path(song_path)
    if USE_PYGAME:
        player.sound = PygameSoundWrapper(song_path)
    else:
        player.sound = SoundLoader.load(song_path)

    if player.sound is None:
        logging.error(f"Could not load file: {song_path}")
        return

    player.song_name    = song_name
    player.sound.volume = player.volume
    player.sound.play()
    player.play_start_time = time.time()

    parts  = song_name.split("\n")
    title  = parts[0].strip()
    artist = parts[1].strip().lstrip("-").strip() if len(parts) > 1 else "Unknown"

    media_session.update_metadata(title, artist)
    media_session.set_playing(True)

    if player.song_bar:
        player.song_bar.on_new_song(song_name)

    logging.info(f"Now playing: {title} — {artist}")


#plays next song in current playlist
def play_next_song():
    if player.is_search_looping and player.song_name:
        play_music(player.song_name, from_search=True)
        return True

    if not player.current_playlist or not player.song_name:
        return False
    
    try:
        idx = player.current_playlist.index(player.song_name)
    except ValueError:
        idx = -1
        for i, song in enumerate(player.current_playlist):
            if song.strip() == player.song_name.strip():
                idx = i
                break
                
    if idx == -1:
        return False
        
    next_idx = idx + 1
    if next_idx >= len(player.current_playlist):
        next_idx = 0
        
    next_song = player.current_playlist[next_idx]
    play_music(next_song)
    return True


#play playlist in sequential order
def play_playlist_sequential(songs):
    if not songs:
        return
    player.is_search_looping = False
    player.current_playlist = list(songs)
    play_music(player.current_playlist[0])


#plays the playlist in a shuffled order 
def play_playlist_shuffled(songs):
    if not songs:
        return
    player.is_search_looping = False
    player.current_playlist = list(songs)
    random.shuffle(player.current_playlist)
    play_music(player.current_playlist[0])


#switches the current screen
def switch_screen(screen, screen_name):
    if screen.manager:
        screen.manager.current = screen_name


#creates the header for each screen
def make_header(text):
    lbl = Label(
        text=text,
        size_hint=(1, 0.0781),
        pos_hint={'x': 0, 'top': 1},
        color=(1, 1, 1, 1),
        halign="left",
        valign="middle",
        padding_x=dp(15),
        bold=True,
        font_size=dp(18)
    )
    lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))

    with lbl.canvas.before:
        Color(0.07, 0.07, 0.07, 1)
        lbl.bg = Rectangle(pos=lbl.pos, size=lbl.size)

    with lbl.canvas.after:
        Color(0.0, 0.9, 1.0, 1)
        lbl.border_line = Line(width=1.5)

    def update_line(inst, val):
        x, y = inst.pos
        w, _ = inst.size
        inst.bg.pos = inst.pos
        inst.bg.size = inst.size
        inst.border_line.points = [x, y, x + w, y]

    lbl.bind(pos=update_line, size=update_line)
    Clock.schedule_once(lambda dt: update_line(lbl, None), 0)

    return lbl


#creates the navigation bar for each screen
def make_nav_bar(screen, layout):
    nav_bg = Label(size_hint=(1, 0.0781), pos_hint={'x': 0, 'y': 0})
    with nav_bg.canvas.before:
        Color(0.07, 0.07, 0.07, 1)
        nav_bg.rect = Rectangle(pos=nav_bg.pos, size=nav_bg.size)
        Color(0.0, 0.9, 1.0, 1)
        nav_bg.line = Line(points=[nav_bg.x, nav_bg.y+nav_bg.height, nav_bg.right, nav_bg.y+nav_bg.height], width=1)
        
    def update_nav(inst, val):
        inst.rect.pos = inst.pos
        inst.rect.size = inst.size
        inst.line.points = [inst.x, inst.y+inst.height, inst.right, inst.y+inst.height]

    nav_bg.bind(pos=update_nav, size=update_nav)
    layout.add_widget(nav_bg)

    btn_home = Button(
        background_normal=resource_path("home_logo.png"),
        size_hint=(0.1388, 0.0781),
        pos_hint={'x': 0, 'y': 0}
    )
    btn_home.bind(on_press=lambda inst: switch_screen(screen, 'home'))

    btn_playlist = Button(
        background_normal=resource_path("playlist_logo.png"),
        size_hint=(0.1388, 0.0781),
        pos_hint={'x': 0.1527, 'y': 0}
    )
    btn_playlist.bind(on_press=lambda inst: switch_screen(screen, 'playlist'))

    btn_settings = Button(
        background_normal=resource_path("settings_logo.png"),
        size_hint=(0.1388, 0.0781),
        pos_hint={'x': 0.3056, 'y': 0}
    )
    btn_settings.bind(on_press=lambda inst: switch_screen(screen, 'settings'))

    layout.add_widget(btn_home)
    layout.add_widget(btn_playlist)
    layout.add_widget(btn_settings)


#makes a scrollable list of songs
def make_scrollable_content(header_text, screen, songs=None):
    layout = FloatLayout(size_hint=(1, 1))
    layout.add_widget(make_header(header_text))

    # Add playlist play/shuffle buttons in the header area if songs are provided
    if songs is not None:
        btn_play = Button(
            size_hint=(0.0972, 0.0546),
            pos_hint={'right': 0.9, 'top': 1},
            background_normal=resource_path("playlist_play_logo.png"),
            background_down=resource_path("playlist_play_logo.png"),
            border=(0, 0, 0, 0),
        )
        btn_play.bind(on_press=lambda inst: play_playlist_sequential(songs))
        layout.add_widget(btn_play)

        btn_shuffle = Button(
            size_hint=(0.0972, 0.0546),
            pos_hint={'right': 0.98, 'top': 1},
            background_normal=resource_path("playlist_shuffle_logo.png"),
            background_down=resource_path("playlist_shuffle_logo.png"),
            border=(0, 0, 0, 0),
        )
        btn_shuffle.bind(on_press=lambda inst: play_playlist_shuffled(songs))
        layout.add_widget(btn_shuffle)

    #scrollable list of songs 
    scroll = ScrollView(
        size_hint=(1, 0.765625),
        pos_hint={'x': 0, 'y': 0.15625},
    )

    #creates the inner layout for the scrollable list of songs 
    inner = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
        spacing=dp(2),
        padding=dp(2)
    )
    inner.bind(minimum_height=inner.setter('height'))

    scroll.add_widget(inner)
    layout.add_widget(scroll)
    make_nav_bar(screen, layout)

    return layout, inner


#makes a button for each playlist
def make_playlist_button(text, callback):
    btn = Button(
        text=text,
        size_hint=(1, None),
        height=dp(60),
        background_normal="",
        background_color=(0.08, 0.08, 0.08, 1),
        background_down="",
        color=(0.9, 0.9, 0.9, 1),
        halign="left",
        valign="middle",
        padding_x=dp(20),
        font_size=dp(15),
    )
    
    def on_state(instance, value):
        if value == 'down':
            instance.background_color = (0.2, 0.2, 0.2, 1)
        else:
            instance.background_color = (0.08, 0.08, 0.08, 1)
            
    btn.bind(state=on_state)
    btn.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
    btn.bind(on_press=callback)

    with btn.canvas.after:
        Color(0.2, 0.2, 0.2, 1)
        btn.divider = Line(width=1)

    def update_divider(inst, val):
        x, y = inst.pos
        w, _ = inst.size
        inst.divider.points = [x, y, x + w, y]

    btn.bind(pos=update_divider, size=update_divider)
    Clock.schedule_once(lambda dt: update_divider(btn, None), 0)

    return btn


#home screen
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()

        # Welcome image (default home view)
        self.welcome_btn = Button(
            size_hint=(1, 0.765625),
            background_normal=resource_path("welcome_img.png"),
            pos_hint={'x': 0, 'y': 0.15625}
        )

        # Search results ScrollView (hidden by default)
        self.results_scroll = ScrollView(
            size_hint=(1, 0.765625),
            pos_hint={'x': 0, 'y': 0.15625},
            opacity=0,
            disabled=True
        )

        self.results_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(2),
            padding=dp(2)
        )
        self.results_box.bind(minimum_height=self.results_box.setter('height'))
        self.results_scroll.add_widget(self.results_box)

        # Bottom navigation buttons
        self.nav_bg = Label(size_hint=(1, 0.0781), pos_hint={'x': 0, 'y': 0})
        with self.nav_bg.canvas.before:
            Color(0.07, 0.07, 0.07, 1)
            self.nav_bg.rect = Rectangle(pos=self.nav_bg.pos, size=self.nav_bg.size)
            Color(0.0, 0.9, 1.0, 1)
            self.nav_bg.line = Line(points=[self.nav_bg.x, self.nav_bg.y+self.nav_bg.height, self.nav_bg.right, self.nav_bg.y+self.nav_bg.height], width=1)
            
        def update_home_nav(inst, val):
            inst.rect.pos = inst.pos
            inst.rect.size = inst.size
            inst.line.points = [inst.x, inst.y+inst.height, inst.right, inst.y+inst.height]

        self.nav_bg.bind(pos=update_home_nav, size=update_home_nav)

        btn1 = Button(
            size_hint=(0.1388, 0.0781),
            background_normal=resource_path("home_logo.png"),
            pos_hint={'x': 0, 'y': 0}
        )

        btn2 = Button(
            background_normal=resource_path("playlist_logo.png"),
            size_hint=(0.1388, 0.0781),
            pos_hint={'x': 0.1527, 'y': 0}
        )
        btn2.bind(on_press=lambda inst: switch_screen(self, "playlist"))

        btn3 = Button(
            background_normal=resource_path("settings_logo.png"),
            size_hint=(0.1388, 0.0781),
            pos_hint={'x': 0.3056, 'y': 0}
        )
        btn3.bind(on_press=lambda inst: switch_screen(self, "settings"))

        # Search Header
        self.header_layout = FloatLayout(
            size_hint=(1, 0.0781),
            pos_hint={'x': 0, 'top': 1}
        )

        # Draw a line at the bottom of the header to match other screens
        with self.header_layout.canvas.before:
            Color(0.07, 0.07, 0.07, 1)
            self.header_layout.bg = Rectangle(pos=self.header_layout.pos, size=self.header_layout.size)
            
        with self.header_layout.canvas.after:
            Color(0.0, 0.9, 1.0, 1)  # Cyan line
            self.header_layout.header_line = Line(width=1.5)

        def update_header_line(inst, val):
            x, y = inst.pos
            w, _ = inst.size
            inst.bg.pos = inst.pos
            inst.bg.size = inst.size
            inst.header_line.points = [x, y, x + w, y]

        self.header_layout.bind(pos=update_header_line, size=update_header_line)
        Clock.schedule_once(lambda dt: update_header_line(self.header_layout, None), 0)

        # Search logo button/icon
        self.search_icon = Button(
            size_hint=(0.0833, 0.0468),
            pos_hint={'x': 0.028, 'top': 1},
            background_normal=resource_path("search_logo.png"),
            background_down=resource_path("search_logo.png"),
            border=(0, 0, 0, 0)
        )
        self.search_icon.bind(on_press=lambda inst: setattr(self.search_input, 'focus', True))

        # Search text input
        self.search_input = TextInput(
            hint_text="Search songs...",
            multiline=False,
            size_hint=(0.82, 0.0562),
            pos_hint={'x': 0.14, 'top': 1},
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.6, 0.6, 0.6, 1),
            font_size=dp(14),
            padding=(dp(10), dp(8), dp(10), dp(8)),
            border=(1, 1, 1, 1)
        )
        self.search_input.bind(text=self.on_search_text)

        self.header_layout.add_widget(self.search_icon)
        self.header_layout.add_widget(self.search_input)

        # Add all widgets to the main screen layout
        self.layout.add_widget(self.welcome_btn)
        self.layout.add_widget(self.results_scroll)
        self.layout.add_widget(self.nav_bg)
        self.layout.add_widget(btn1)
        self.layout.add_widget(btn2)
        self.layout.add_widget(btn3)
        self.layout.add_widget(self.header_layout)

        self.add_widget(self.layout)

    def on_enter(self, *args):
        # Clear search input when returning to home screen
        self.search_input.text = ""

    def on_search_text(self, instance, value):
        query = value.strip().lower()
        self.results_box.clear_widgets()

        if not query:
            self.results_scroll.opacity = 0
            self.results_scroll.disabled = True
            self.welcome_btn.opacity = 1
            self.welcome_btn.disabled = False
            return

        self.results_scroll.opacity = 1
        self.results_scroll.disabled = False
        self.welcome_btn.opacity = 0
        self.welcome_btn.disabled = True

        matching_songs = []
        for song in SONGS.keys():
            if query in song.lower():
                matching_songs.append(song)

        if not matching_songs:
            no_results_label = Label(
                text="No songs found",
                size_hint_y=None,
                height=dp(50),
                color=(0.6, 0.6, 0.6, 1)
            )
            self.results_box.add_widget(no_results_label)
        else:
            self.current_results = matching_songs
            for song in matching_songs:
                btn = make_playlist_button(song, self.play_song)
                self.results_box.add_widget(btn)

    def play_song(self, instance):
        player.current_playlist = getattr(self, 'current_results', [instance.text])
        play_music(instance.text, from_search=True)


#settings screen
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout, inner = make_scrollable_content("  Settings", self)

        self.volume_label = Label(
            text="Volume: 100%",
            size_hint_y=None,
            height=dp(40),
            color=(1, 1, 1, 1)
        )

        slider = Slider(min=0, max=1, value=1.0, size_hint_y=None, height=dp(50))
        slider.bind(value=self.change_volume)

        inner.add_widget(self.volume_label)
        inner.add_widget(slider)

        self.add_widget(layout)

    def change_volume(self, instance, value):
        player.volume = value
        if player.sound:
            player.sound.volume = value
        percent = int(value * 100)
        self.volume_label.text = f"Volume: {percent}%"


#playlist tab screen
class PlaylistScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout, inner = make_scrollable_content("  Playlists", self)

        playlists = [
            ("Against The Current", "against"),
            ("Ghost", "ghost"),
            ("Judas Priest", "jp"),
            ("Random", "random"),
        ]

        for name, screen_name in playlists:
            btn = make_playlist_button(
                f" {name}",
                lambda inst, s=screen_name: switch_screen(self, s)
            )
            inner.add_widget(btn)

        self.add_widget(layout)






class PlaylistDetailScreen(Screen):
    def __init__(self, title, songs, **kwargs):
        super().__init__(**kwargs)
        self.songs = songs

        layout, inner = make_scrollable_content(f" {title}", self, songs=self.songs)

        for song in self.songs:
            btn = make_playlist_button(song, self.play_song)
            inner.add_widget(btn)

        self.add_widget(layout)

    def play_song(self, instance):
        player.current_playlist = self.songs
        play_music(instance.text)

#main application
class MyApp(App):
    def build(self):
        root = FloatLayout(size_hint=(1, 1))

        sm = ScreenManager(size_hint=(1, 1))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PlaylistScreen(name="playlist"))
        sm.add_widget(PlaylistDetailScreen(name="against", title="Against the Current", songs=list(ATC_SONGS.keys())))
        sm.add_widget(PlaylistDetailScreen(name="ghost", title="Ghost", songs=list(GHOST_SONGS.keys())))
        sm.add_widget(PlaylistDetailScreen(name="jp", title="Judas Priest", songs=list(JP_SONGS.keys())))
        sm.add_widget(PlaylistDetailScreen(name="random", title="Random", songs=list(RANDOM_SONGS.keys())))
        sm.add_widget(SettingsScreen(name="settings"))

        player.song_bar = SongBar()

        root.add_widget(sm)
        root.add_widget(player.song_bar)

        return root

    def on_pause(self):
        return True

    def on_stop(self):
        if player.sound:
            player.sound.stop()
        media_session.release()


MyApp().run()
