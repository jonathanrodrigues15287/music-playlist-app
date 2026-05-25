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
import time
import random


Window.size = (360, 640)

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
        global is_paused
        pygame.mixer.music.play(start=pos)
        if is_paused:
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

current_sound     = None
current_song_name = ""
is_paused         = False
current_volume    = 1.0
paused_pos        = 0.0   
play_start_time   = 0.0
accumulated_time  = 0.0
current_playlist  = []

song_bar = None

SONGS = {

    # songs from random playlist
    " It's My Life\n -Bon Jovi":
        "songs/its_my_life.mp3",
    " They Don't Care About Us\n -Michael Jackson":
        "songs/they_dont_care_about_us.mp3",
    " Can't Help Falling in Love \n -Elvis Presley":
        "songs/cant_help_falling_in_love.mp3",
    " All of Me \n -John Legend":
        "songs/all_of_me.mp3",
    " Hymn For the Weekend \n -Coldplay":
        "songs/hymn_for_the_weekend.mp3",
    " Way Down we go \n -Kaleo":
        "songs/way_down_we_go.mp3",
    " House of Memories \n -Panic! At the Disco":
        "songs/house_of_memories.mp3",
    " Another Love \n -Tom Odell":
        "songs/another_love.mp3",
    " Superbeast \n -Rob Zombie":
        "songs/superbeast.mp3",
    " Ordinary \n -Alex Warren":
        "songs/ordinary.mp3",
    " Bella Ciao \n -Manu Pilas":
        "songs/bella_ciao.mp3",
    " Oh What a Circus \n -Antonio Banderas":
        "songs/oh_what_a_circus.mp3",
    " Numb Little Bug \n -Em Beihold":
        "songs/numb_little_bug.mp3",

    # songs from judas priest
    "Breaking the Law\n -Judas Priest":
        "songs/breaking_the_law.mp3",
    "You've Got Another Thing Coming\n -Judas Priest":
        "songs/youve_got_another_thing_coming.mp3",
    "Living After Midnight\n -Judas Priest":
        "songs/living_after_midnight.mp3",
    "Painkiller\n -Judas Priest":
        "songs/painkiller.mp3",
    "Electric Eye\n -Judas Priest":
        "songs/electric_eye.mp3",
    "The Hellion\n -Judas Priest":
        "songs/the_hellion.mp3",
    "Hell Bent for Leather\n -Judas Priest":
        "songs/hell_bent_for_leather.mp3",
    "Screaming for Vengeance\n -Judas Priest":
        "songs/screaming_for_vengeance.mp3",
    "Turbo Lover\n -Judas Priest":
        "songs/turbo_lover.mp3",
    "Beyond the Realms of Death\n -Judas Priest":
        "songs/beyond_the_realms_of_death.mp3",
    "Victim of Changes\n -Judas Priest":
        "songs/victim_of_changes.mp3",
    "Freewheel Burning\n -Judas Priest":
        "songs/freewheel_burning.mp3",
    "The Sentinel\n -Judas Priest":
        "songs/the_sentinel.mp3",
    "Metal Gods\n -Judas Priest":
        "songs/metal_gods.mp3",
    "Heading Out to the Highway\n -Judas Priest":
        "songs/heading_out_to_the_highway.mp3",
    "Night Crawler\n -Judas Priest":
        "songs/night_crawler.mp3",
    "A Touch of Evil\n -Judas Priest":
        "songs/a_touch_of_evil.mp3",
    "Sinner\n -Judas Priest":
        "songs/sinner.mp3",
    "Exciter\n -Judas Priest":
        "songs/exciter.mp3",
    "Desert Plains\n -Judas Priest":
        "songs/desert_plains.mp3",
    "Dissident Aggressor\n -Judas Priest":
        "songs/dissident_aggressor.mp3",
    "Tyrant\n -Judas Priest":
        "songs/tyrant.mp3",
    "Running Wild\n -Judas Priest":
        "songs/running_wild.mp3",
    "Blood Red Skies\n -Judas Priest":
        "songs/blood_red_skies.mp3",
    "Before the Dawn\n -Judas Priest":
        "songs/before_the_dawn.mp3",
    "Dreamer Deceiver\n -Judas Priest":
        "songs/dreamer_deceiver.mp3",
    "Rock Hard Ride Free\n -Judas Priest":
        "songs/rock_hard_ride_free.mp3",
    "Between the Hammer and the Anvil\n -Judas Priest":
        "songs/between_the_hammer_and_the_anvil.mp3",
    "Hell Patrol\n -Judas Priest":
        "songs/hell_patrol.mp3",
    "Judas Rising\n -Judas Priest":
        "songs/judas_rising.mp3",
    "Firepower\n -Judas Priest":
        "songs/firepower.mp3",
    "Never the Heroes\n -Judas Priest":
        "songs/never_the_heroes.mp3",
    "Halls of Valhalla\n -Judas Priest":
        "songs/halls_of_valhalla.mp3",
    "Traitors Gate\n -Judas Priest":
        "songs/traitors_gate.mp3",
    "Steeler\n -Judas Priest":
        "songs/steeler.mp3",

    # AGAINST THE CURRENT
    "I Like the Way\n -Against The Current":
        "songs/i_like_the_way.mp3",
    "Runaway\n -Against The Current":
        "songs/runaway.mp3",
    "Strangers Again\n -Against The Current":
        "songs/strangers_again.mp3",
    "Demons\n -Against The Current":
        "songs/demons.mp3",
    "Chasing Ghosts\n -Against The Current":
        "songs/chasing_ghosts.mp3",
    "Closer, Faster\n -Against The Current":
        "songs/closer_faster.mp3",
    "Outsiders\n -Against The Current":
        "songs/outsiders.mp3",
    "Blood Like Gasoline\n -Against The Current":
        "songs/blood_like_gasoline.mp3",
    "Roses\n -Against The Current":
        "songs/roses.mp3",
    "One More Weekend\n -Against The Current":
        "songs/one_more_weekend.mp3",
    "Sweet Surrender\n -Against The Current":
        "songs/sweet_surrender.mp3",
    "Come Alive\n -Against The Current":
        "songs/come_alive.mp3",
    "weapon - acoustic\n -Against The Current":
        "songs/weapon_acoustic.mp3",
    "weapon\n -Against The Current":
        "songs/weapon.mp3",
    "that won't save us\n -Against The Current":
        "songs/that_wont_save_us.mp3",
    "Voices\n -Against The Current":
        "songs/voices.mp3",
    "Legends Never Die\n -League of Legends, Against The Current":
        "songs/legends_never_die.mp3",
    "Almost Forgot - Ryan Riback Remix\n -Against The Current, Ryan Riback":
        "songs/almost_forgot_ryan_riback_remix.mp3",
    "Brighter\n -Against The Current":
        "songs/brighter.mp3",
    "Running with the Wild Things\n -Against The Current":
        "songs/running_with_the_wild_things.mp3",
    "Gravity - Acoustic\n -Against The Current":
        "songs/gravity_acoustic.mp3",
    "Forget Me Now\n -Against The Current":
        "songs/forget_me_now.mp3",
    "good guy\n -Against The Current":
        "songs/good_guy.mp3",
    "blindfolded\n -Against The Current":
        "songs/blindfolded.mp3",
    "silent stranger\n -Against The Current":
        "songs/silent_stranger.mp3",
    "Something You Need\n -Against The Current":
        "songs/something_you_need.mp3",
    "Another You (Another Way)\n -Against The Current":
        "songs/another_you_another_way.mp3",
    "The Fuss\n -Against The Current":
        "songs/the_fuss.mp3",
    "In Our Bones\n -Against The Current":
        "songs/in_our_bones.mp3",
    "again&again\n -Against The Current, guardin":
        "songs/again_and_again.mp3",
    "burn it down\n -Against The Current":
        "songs/burn_it_down.mp3",
    "lullaby\n -Against The Current":
        "songs/lullaby.mp3",
    "shatter\n -Against The Current":
        "songs/shatter.mp3",
    "jump\n -Against The Current":
        "songs/jump.mp3",
    "Wildfire\n -Against The Current":
        "songs/wildfire.mp3",
    "Talk\n -Against The Current":
        "songs/talk.mp3",
    "Paralyzed - Acoustic\n -Against The Current":
        "songs/paralyzed_acoustic.mp3",
    "Wasteland\n -Against The Current":
        "songs/wasteland.mp3",
    "See You Again\n -ATC":
        "songs/see_you_again.mp3",
    "One More Night\n -Alex Goot, ATC, Julia Sheer, Luke Conard, Chad Sugg":
        "songs/one_more_night.mp3",
    "P.A.T.T.\n -Against The Current":
        "songs/patt.mp3",
    "Personal\n -Against The Current":
        "songs/personal.mp3",
    "Scream\n -Against The Current":
        "songs/scream.mp3",
    "Young & Relentless\n -Against The Current":
        "songs/young_and_relentless.mp3",
    "Fireproof\n -Against The Current":
        "songs/fireproof.mp3",
    "Friendly Reminder\n -Against The Current":
        "songs/friendly_reminder.mp3",
    "Infinity\n -Against The Current":
        "songs/infinity.mp3",
    "Dreaming Alone\n -Against The Current, Taka":
        "songs/dreaming_alone.mp3",
    "Guessing\n -ATC":
        "songs/guessing.mp3",
    "Heavenly\n -Against The Current":
        "songs/heavenly.mp3",

    # songs from ghost
    "Year Zero\n -Ghost":
        "songs/year_zero.mp3",
    "Mary On A Cross\n -Ghost":
        "songs/mary_on_a_cross.mp3",
    "Square Hammer\n -Ghost":
        "songs/square_hammer.mp3",
    "Dance Macabre\n -Ghost":
        "songs/dance_macabre.mp3",
    "Call Me Little Sunshine\n -Ghost":
        "songs/call_me_little_sunshine.mp3",
    "Spillways\n -Ghost":
        "songs/spillways.mp3",
    "Cirice\n -Ghost":
        "songs/cirice.mp3",
    "The Future Is A Foreign Land\n -Ghost":
        "songs/the_future_is_a_foreign_land.mp3",
    "Life Eternal\n -Ghost":
        "songs/life_eternal.mp3",
    "Kiss The Go-Goat\n -Ghost":
        "songs/kiss_the_go_goat.mp3",
    "Darkness At The Heart Of My Love\n -Ghost":
        "songs/darkness_at_the_heart_of_my_love.mp3",
    "Kaisarion\n -Ghost":
        "songs/kaisarion.mp3",
    "Hunter's Moon\n -Ghost":
        "songs/hunters_moon.mp3",
    "Jesus He Knows Me\n -Ghost":
        "songs/jesus_he_knows_me.mp3",
    "Griftwood\n -Ghost":
        "songs/griftwood.mp3",
    "Watcher In The Sky\n -Ghost":
        "songs/watcher_in_the_sky.mp3",
    "Respite On The Spitalfields\n -Ghost":
        "songs/respite_on_the_spitalfields.mp3",
    "Twenties\n -Ghost":
        "songs/twenties.mp3",
    "Monstrance Clock\n -Ghost":
        "songs/monstrance_clock.mp3",
    "He Is\n -Ghost":
        "songs/he_is.mp3",
    "He Is (feat. Alison Mosshart)\n -Ghost":
        "songs/he_is_feat_alison_mosshart.mp3",
    "See The Light\n -Ghost":
        "songs/see_the_light.mp3",
    "Enter Sandman\n -Ghost":
        "songs/enter_sandman.mp3",
    "Phantom Of The Opera\n -Ghost":
        "songs/phantom_of_the_opera.mp3",
    "Imperium\n -Ghost":
        "songs/imperium.mp3",
    "Miasma\n -Ghost":
        "songs/miasma.mp3",
    "Pro Memoria\n -Ghost":
        "songs/pro_memoria.mp3",
    "Infestissumam\n -Ghost":
        "songs/infestissumam.mp3",
    "Ashes\n -Ghost":
        "songs/ashes.mp3",
    "Helvetesfonster\n -Ghost":
        "songs/helvetesfonster.mp3",
    "Witch Image\n -Ghost":
        "songs/witch_image.mp3",
    "Ritual\n -Ghost":
        "songs/ritual.mp3",
    "Jigolo Har Megiddo\n -Ghost":
        "songs/jigolo_har_megiddo.mp3",
    "Stay [Feat. Patrick Wilson]\n -Ghost, Patrick Wilson":
        "songs/stay.mp3",
    "Faith\n -Ghost":
        "songs/faith.mp3",
    "Lachryma\n -Ghost":
        "songs/lachryma.mp3",
    "Missionary Man\n -Ghost":
        "songs/missionary_man.mp3",
}


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

            print("MediaSession initialised successfully")

        except Exception as e:
            print(f"MediaSession not available (non-Android): {e}")
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
            print(f"MediaSession metadata error: {e}")

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
            print(f"MediaSession state error: {e}")

    def release(self):
        if self.session:
            self.session.setActive(False)
            self.session.release()

media_session = AndroidMediaSession()

class SongBar(FloatLayout):
    BAR_H  = dp(50)  
    PROG_H = dp(3)   
    BTN_W  = dp(45)   
    BTN_H  = dp(45)   

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._dragging = False
        self._drag_pos = 0.0

        self.size_hint = (None, None)
        self.size      = (dp(360), self.BAR_H)
        self.pos       = (0, dp(50))   
        
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            self._bg = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_bg, size=self._update_bg)

        with self.canvas:
            Color(0.25, 0.25, 0.25, 1)
            self._track = Rectangle(pos=self.pos, size=(dp(360), self.PROG_H))

        with self.canvas:
            Color(0, 0.5, 1, 1)
            self._fill = Rectangle(pos=self.pos, size=(0, self.PROG_H))

        self.title_label = Label(
            text="No song playing",
            size_hint=(None, None),
            size=(dp(360) - self.BTN_W - dp(10), self.BAR_H - self.PROG_H),
            pos=(dp(5), dp(50)),
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
            pos=(dp(360) - self.BTN_W - dp(5), dp(50) + self.BAR_H - self.PROG_H - self.BTN_H),
            background_normal="pause_logo.png",   
            background_down="pause_logo.png",
            border=(0, 0, 0, 0),
        )
        self.play_btn.bind(on_press=self._toggle_pause)
        self.add_widget(self.play_btn)

        self.bind(pos=self._reposition_children)
        Clock.schedule_once(lambda dt: self._reposition_children(self, None), 0)

        Clock.schedule_interval(self._tick, 0.05)

    def _update_bg(self, *args):
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def _reposition_children(self, inst, val):
        x, y = self.pos
        self.title_label.pos = (x + dp(5), y)
        self.play_btn.pos    = (x + dp(360) - self.BTN_W - dp(5), y + self.BAR_H - self.PROG_H - self.BTN_H)
        self._track.pos  = (x, y + self.BAR_H - self.PROG_H)
        self._track.size = (self.size[0], self.PROG_H)
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
        global current_sound
        if not current_sound:
            return
        
        local_x = touch.x - self.x
        ratio = max(0.0, min(1.0, local_x / self.width))
        
        duration = current_sound.length
        if not duration or duration <= 0:
            return
            
        self._drag_pos = ratio * duration
        
        x, y = self.pos
        bar_y = y + self.BAR_H - self.PROG_H
        self._fill.pos  = (x, bar_y)
        self._fill.size = (self.size[0] * ratio, self.PROG_H)

    def _apply_seek(self):
        global current_sound, play_start_time, accumulated_time, paused_pos, is_paused
        if not current_sound:
            return
            
        target_pos = self._drag_pos
        
        if USE_PYGAME:
            current_sound.seek(target_pos)
        else:
            if is_paused:
                paused_pos = target_pos
            else:
                current_sound.seek(target_pos)
                
        play_start_time = time.time()
        accumulated_time = target_pos
        if is_paused:
            paused_pos = target_pos

    def _refresh_progress(self):
        global current_sound, is_paused, paused_pos, play_start_time, accumulated_time

        if self._dragging:
            return

        if is_paused:
            position = paused_pos
        elif current_sound:
            pos = current_sound.get_pos()
            if pos > 0:
                position = pos
            else:
                position = accumulated_time + (time.time() - play_start_time)
        else:
            position = 0.0

        duration = current_sound.length if current_sound else 0
        if duration and duration > 0:
            position = min(position, duration)
            ratio = max(0.0, min(1.0, position / duration))
        else:
            ratio = 0.0

        if current_sound and current_sound.state == 'stop' and not is_paused and (time.time() - play_start_time > 0.5):
            if not play_next_song():
                is_paused = False
                paused_pos = 0.0
                accumulated_time = 0.0
                position = 0.0
                ratio = 0.0
                self.play_btn.background_normal = "play_logo.png"
                self.play_btn.background_down   = "play_logo.png"
                media_session.set_playing(False)

        x, y = self.pos
        bar_y = y + self.BAR_H - self.PROG_H
        self._track.pos  = (x, bar_y)
        self._track.size = (self.size[0], self.PROG_H)
        self._fill.pos   = (x, bar_y)
        self._fill.size  = (self.size[0] * ratio, self.PROG_H)

    def _toggle_pause(self, instance):
        global current_sound, is_paused, paused_pos, play_start_time, accumulated_time

        if current_sound is None:
            return

        if is_paused:
            pos_to_seek = paused_pos
            if USE_PYGAME:
                pygame.mixer.music.unpause()
            else:
                current_sound.play()
                Clock.schedule_once(lambda dt: current_sound.seek(pos_to_seek), 0.3)
            is_paused = False
            play_start_time = time.time()
            accumulated_time = pos_to_seek
            self.play_btn.background_normal = "pause_logo.png"
            self.play_btn.background_down   = "pause_logo.png"
            media_session.set_playing(True)
        else:
            pos = current_sound.get_pos()
            if pos <= 0:
                pos = accumulated_time + (time.time() - play_start_time)
            paused_pos = min(pos, current_sound.length if current_sound.length else pos)
            if USE_PYGAME:
                pygame.mixer.music.pause()
            else:
                current_sound.stop()
            is_paused = True
            self.play_btn.background_normal = "play_logo.png"
            self.play_btn.background_down   = "play_logo.png"
            media_session.set_playing(False)

    def on_new_song(self, song_name):
        global is_paused, paused_pos, accumulated_time
        is_paused  = False
        paused_pos = 0.0
        accumulated_time = 0.0
        self.play_btn.background_normal = "pause_logo.png"
        self.play_btn.background_down   = "pause_logo.png"

        title = song_name.split("\n")[0].strip()
        self.title_label.text = title

        self._refresh_progress()

def play_music(song_name):
    global current_sound, current_song_name, is_paused, current_volume, paused_pos, play_start_time, accumulated_time

    song_name = song_name.strip()

    if song_name not in SONGS:
        spaced = " " + song_name
        if spaced in SONGS:
            song_name = spaced
        else:
            print(f"No song file mapped for: {song_name}")
            return

    if current_sound:
        current_sound.stop()
        current_sound = None

    is_paused  = False
    paused_pos = 0.0
    accumulated_time = 0.0

    song_path     = SONGS[song_name]
    if USE_PYGAME:
        current_sound = PygameSoundWrapper(song_path)
    else:
        current_sound = SoundLoader.load(song_path)

    if current_sound is None:
        print(f"Could not load file: {song_path}")
        return

    current_song_name    = song_name
    current_sound.volume = current_volume
    current_sound.play()
    play_start_time = time.time()

    parts  = song_name.split("\n")
    title  = parts[0].strip()
    artist = parts[1].strip().lstrip("-").strip() if len(parts) > 1 else "Unknown"

    media_session.update_metadata(title, artist)
    media_session.set_playing(True)

    if song_bar:
        song_bar.on_new_song(song_name)

    print(f"Now playing: {title} — {artist}")


def play_next_song():
    global current_playlist, current_song_name
    if not current_playlist or not current_song_name:
        return False
    
    try:
        idx = current_playlist.index(current_song_name)
    except ValueError:
        idx = -1
        for i, song in enumerate(current_playlist):
            if song.strip() == current_song_name.strip():
                idx = i
                break
                
    if idx == -1:
        return False
        
    next_idx = idx + 1
    if next_idx >= len(current_playlist):
        next_idx = 0
        
    next_song = current_playlist[next_idx]
    play_music(next_song)
    return True


def play_playlist_sequential(songs):
    """Play the playlist in order, starting from the first song."""
    global current_playlist
    if not songs:
        return
    current_playlist = list(songs)
    play_music(current_playlist[0])


def play_playlist_shuffled(songs):
    """Shuffle the playlist and start playing from the first shuffled song."""
    global current_playlist
    if not songs:
        return
    current_playlist = list(songs)
    random.shuffle(current_playlist)
    play_music(current_playlist[0])



def switch_screen(screen, screen_name):
    if screen.manager:
        screen.manager.current = screen_name


def make_header(text):
    lbl = Label(
        text=text,
        size_hint=(None, None),
        size=(dp(360), dp(50)),
        pos=(dp(0), dp(590)),
        color=(1, 1, 1, 1),
        halign="left",
        valign="middle",
        padding_x=dp(15),
    )
    lbl.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))

    with lbl.canvas.after:
        Color(0, 0, 1, 1)
        lbl.border_line = Line(width=2)

    def update_line(inst, val):
        x, y = inst.pos
        w, _ = inst.size
        inst.border_line.points = [x, y, x + w, y]

    lbl.bind(pos=update_line, size=update_line)
    Clock.schedule_once(lambda dt: update_line(lbl, None), 0)

    return lbl


def make_nav_bar(screen, layout):
    btn_home = Button(
        background_normal="home_logo.png",
        size_hint=(None, None),
        size=(dp(50), dp(50)),
        pos=(dp(0), dp(0))
    )
    btn_home.bind(on_press=lambda inst: switch_screen(screen, 'home'))

    btn_playlist = Button(
        background_normal="playlist_logo.png",
        size_hint=(None, None),
        size=(dp(50), dp(50)),
        pos=(dp(55), dp(0))
    )
    btn_playlist.bind(on_press=lambda inst: switch_screen(screen, 'playlist'))

    btn_settings = Button(
        background_normal="settings_logo.png",
        size_hint=(None, None),
        size=(dp(50), dp(50)),
        pos=(dp(110), dp(0))
    )
    btn_settings.bind(on_press=lambda inst: switch_screen(screen, 'settings'))

    layout.add_widget(btn_home)
    layout.add_widget(btn_playlist)
    layout.add_widget(btn_settings)


def make_scrollable_content(header_text, screen, songs=None):
    layout = FloatLayout()
    layout.add_widget(make_header(header_text))

    # Add playlist play/shuffle buttons in the header area if songs are provided
    if songs is not None:
        btn_play = Button(
            size_hint=(None, None),
            size=(dp(35), dp(35)),
            pos=(dp(260), dp(597)),
            background_normal="playlist_play_logo.png",
            background_down="playlist_play_logo.png",
            border=(0, 0, 0, 0),
        )
        btn_play.bind(on_press=lambda inst: play_playlist_sequential(songs))
        layout.add_widget(btn_play)

        btn_shuffle = Button(
            size_hint=(None, None),
            size=(dp(35), dp(35)),
            pos=(dp(305), dp(597)),
            background_normal="playlist_shuffle_logo.png",
            background_down="playlist_shuffle_logo.png",
            border=(0, 0, 0, 0),
        )
        btn_shuffle.bind(on_press=lambda inst: play_playlist_shuffled(songs))
        layout.add_widget(btn_shuffle)

    scroll = ScrollView(
        size_hint=(None, None),
        size=(dp(360), dp(490)),
        pos=(dp(0), dp(100)),
    )

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


def make_playlist_button(text, callback):
    btn = Button(
        text=text,
        size_hint=(1, None),
        height=dp(50),
        background_normal="",
        background_color=(0, 0, 0, 1),
        color=(0.68, 0.85, 0.90, 1),
        halign="left",
        valign="middle",
        padding_x=dp(15),
    )
    btn.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))
    btn.bind(on_press=callback)

    with btn.canvas.after:
        Color(0.6, 0.6, 0.6, 1)
        btn.divider = Line(width=1)

    def update_divider(inst, val):
        x, y = inst.pos
        w, _ = inst.size
        inst.divider.points = [x, y, x + w, y]

    btn.bind(pos=update_divider, size=update_divider)
    Clock.schedule_once(lambda dt: update_divider(btn, None), 0)

    return btn


#screens
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        btn0 = Button(
            size_hint=(None, None),
            background_normal="welcome_img.png",
            size=(dp(360), dp(490)),
            pos=(dp(0), dp(100))
        )

        btn1 = Button(
            size_hint=(None, None),
            background_normal="home_logo.png",
            size=(dp(50), dp(50)),
            pos=(dp(0), dp(0))
        )

        btn2 = Button(
            background_normal="playlist_logo.png",
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos=(dp(55), dp(0))
        )
        btn2.bind(on_press=lambda inst: switch_screen(self, "playlist"))

        btn3 = Button(
            background_normal="settings_logo.png",
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos=(dp(110), dp(0))
        )
        btn3.bind(on_press=lambda inst: switch_screen(self, "settings"))

        layout.add_widget(btn0)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)

        self.add_widget(layout)


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
        global current_sound, current_volume
        current_volume = value
        if current_sound:
            current_sound.volume = value
        percent = int(value * 100)
        self.volume_label.text = f"Volume: {percent}%"


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

class RandomScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.songs = [
            " It's My Life\n -Bon Jovi",
            " They Don't Care About Us\n -Michael Jackson",
            " Can't Help Falling in Love \n -Elvis Presley",
            " All of Me \n -John Legend",
            " Hymn For the Weekend \n -Coldplay",
            " Way Down we go \n -Kaleo",
            " House of Memories \n -Panic! At the Disco",
            " Another Love \n -Tom Odell",
            " Superbeast \n -Rob Zombie",
            " Ordinary \n -Alex Warren",
            " Bella Ciao \n -Manu Pilas",
            " Oh What a Circus \n -Antonio Banderas",
            " Numb Little Bug \n -Em Beihold",
        ]

        layout, inner = make_scrollable_content(" Random", self, songs=self.songs)

        for song in self.songs:
            btn = make_playlist_button(song, self.play_song)
            inner.add_widget(btn)

        self.add_widget(layout)

    def play_song(self, instance):
        global current_playlist
        current_playlist = self.songs
        play_music(instance.text)

class AtcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.songs = [
            "I Like the Way\n -Against The Current",
            "Runaway\n -Against The Current",
            "Strangers Again\n -Against The Current",
            "Demons\n -Against The Current",
            "Chasing Ghosts\n -Against The Current",
            "Closer, Faster\n -Against The Current",
            "Outsiders\n -Against The Current",
            "Blood Like Gasoline\n -Against The Current",
            "Roses\n -Against The Current",
            "One More Weekend\n -Against The Current",
            "Sweet Surrender\n -Against The Current",
            "Come Alive\n -Against The Current",
            "weapon - acoustic\n -Against The Current",
            "weapon\n -Against The Current",
            "that won't save us\n -Against The Current",
            "Voices\n -Against The Current",
            "Legends Never Die\n -League of Legends, Against The Current",
            "Almost Forgot - Ryan Riback Remix\n -Against The Current, Ryan Riback",
            "Brighter\n -Against The Current",
            "Running with the Wild Things\n -Against The Current",
            "Gravity - Acoustic\n -Against The Current",
            "Forget Me Now\n -Against The Current",
            "good guy\n -Against The Current",
            "blindfolded\n -Against The Current",
            "silent stranger\n -Against The Current",
            "Something You Need\n -Against The Current",
            "Another You (Another Way)\n -Against The Current",
            "The Fuss\n -Against The Current",
            "In Our Bones\n -Against The Current",
            "again&again\n -Against The Current, guardin",
            "burn it down\n -Against The Current",
            "lullaby\n -Against The Current",
            "shatter\n -Against The Current",
            "jump\n -Against The Current",
            "Wildfire\n -Against The Current",
            "Talk\n -Against The Current",
            "Paralyzed - Acoustic\n -Against The Current",
            "Wasteland\n -Against The Current",
            "See You Again\n -ATC",
            "One More Night\n -Alex Goot, ATC, Julia Sheer, Luke Conard, Chad Sugg",
            "P.A.T.T.\n -Against The Current",
            "Personal\n -Against The Current",
            "Scream\n -Against The Current",
            "Young & Relentless\n -Against The Current",
            "Fireproof\n -Against The Current",
            "Friendly Reminder\n -Against The Current",
            "Infinity\n -Against The Current",
            "Dreaming Alone\n -Against The Current, Taka",
            "Guessing\n -ATC",
            "Heavenly\n -Against The Current",
        ]

        layout, inner = make_scrollable_content(" Against the Current", self, songs=self.songs)

        for song in self.songs:
            btn = make_playlist_button(song, self.play_song)
            inner.add_widget(btn)

        self.add_widget(layout)

    def play_song(self, instance):
        global current_playlist
        current_playlist = self.songs
        play_music(instance.text)

class GhostScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.songs = [
            "Year Zero\n -Ghost",
            "Mary On A Cross\n -Ghost",
            "Square Hammer\n -Ghost",
            "Dance Macabre\n -Ghost",
            "Call Me Little Sunshine\n -Ghost",
            "Spillways\n -Ghost",
            "Cirice\n -Ghost",
            "The Future Is A Foreign Land\n -Ghost",
            "Life Eternal\n -Ghost",
            "Kiss The Go-Goat\n -Ghost",
            "Darkness At The Heart Of My Love\n -Ghost",
            "Kaisarion\n -Ghost",
            "Hunter's Moon\n -Ghost",
            "Jesus He Knows Me\n -Ghost",
            "Griftwood\n -Ghost",
            "Watcher In The Sky\n -Ghost",
            "Respite On The Spitalfields\n -Ghost",
            "Twenties\n -Ghost",
            "Monstrance Clock\n -Ghost",
            "He Is\n -Ghost",
            "See The Light\n -Ghost",
            "Enter Sandman\n -Ghost",
            "Phantom Of The Opera\n -Ghost",
            "Imperium\n -Ghost",
            "Miasma\n -Ghost",
            "Pro Memoria\n -Ghost",
            "Infestissumam\n -Ghost",
            "Ashes\n -Ghost",
            "Helvetesfonster\n -Ghost",
            "He Is (feat. Alison Mosshart)\n -Ghost",
            "Witch Image\n -Ghost",
            "Ritual\n -Ghost",
            "Jigolo Har Megiddo\n -Ghost",
            "Stay [Feat. Patrick Wilson]\n -Ghost, Patrick Wilson",
            "Faith\n -Ghost",
            "Lachryma\n -Ghost",
            "Missionary Man\n -Ghost",
        ]

        layout, inner = make_scrollable_content(" Ghost", self, songs=self.songs)

        for song in self.songs:
            btn = make_playlist_button(song, self.play_song)
            inner.add_widget(btn)

        self.add_widget(layout)

    def play_song(self, instance):
        global current_playlist
        current_playlist = self.songs
        play_music(instance.text)

class JPScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.songs = [
            "Breaking the Law\n -Judas Priest",
            "You've Got Another Thing Coming\n -Judas Priest",
            "Living After Midnight\n -Judas Priest",
            "Painkiller\n -Judas Priest",
            "Electric Eye\n -Judas Priest",
            "The Hellion\n -Judas Priest",
            "Hell Bent for Leather\n -Judas Priest",
            "Screaming for Vengeance\n -Judas Priest",
            "Turbo Lover\n -Judas Priest",
            "Beyond the Realms of Death\n -Judas Priest",
            "Victim of Changes\n -Judas Priest",
            "Freewheel Burning\n -Judas Priest",
            "The Sentinel\n -Judas Priest",
            "Metal Gods\n -Judas Priest",
            "Heading Out to the Highway\n -Judas Priest",
            "Night Crawler\n -Judas Priest",
            "A Touch of Evil\n -Judas Priest",
            "Sinner\n -Judas Priest",
            "Exciter\n -Judas Priest",
            "Desert Plains\n -Judas Priest",
            "Dissident Aggressor\n -Judas Priest",
            "Tyrant\n -Judas Priest",
            "Running Wild\n -Judas Priest",
            "Blood Red Skies\n -Judas Priest",
            "Before the Dawn\n -Judas Priest",
            "Dreamer Deceiver\n -Judas Priest",
            "Rock Hard Ride Free\n -Judas Priest",
            "Between the Hammer and the Anvil\n -Judas Priest",
            "Hell Patrol\n -Judas Priest",
            "Judas Rising\n -Judas Priest",
            "Firepower\n -Judas Priest",
            "Never the Heroes\n -Judas Priest",
            "Halls of Valhalla\n -Judas Priest",
            "Traitors Gate\n -Judas Priest",
            "Steeler\n -Judas Priest",
        ]

        layout, inner = make_scrollable_content(" Judas Priest", self, songs=self.songs)

        for song in self.songs:
            btn = make_playlist_button(song, self.play_song)
            inner.add_widget(btn)

        self.add_widget(layout)

    def play_song(self, instance):
        global current_playlist
        current_playlist = self.songs
        play_music(instance.text)

class MyApp(App):
    def build(self):
        global song_bar

        root = FloatLayout(size=(dp(360), dp(640)))

        sm = ScreenManager(size_hint=(1, 1))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PlaylistScreen(name="playlist"))
        sm.add_widget(AtcScreen(name="against"))
        sm.add_widget(GhostScreen(name="ghost"))
        sm.add_widget(JPScreen(name="jp"))
        sm.add_widget(RandomScreen(name="random"))
        sm.add_widget(SettingsScreen(name="settings"))

        song_bar = SongBar()

        root.add_widget(sm)
        root.add_widget(song_bar)

        return root

    def on_pause(self):
        return True

    def on_stop(self):
        global current_sound
        if current_sound:
            current_sound.stop()
        media_session.release()


MyApp().run()
