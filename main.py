from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Line
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

Window.size = (360, 640)


# screen manager
def switch_screen(screen, screen_name):
    if screen.manager:
        screen.manager.current = screen_name


# home screen
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        btn0 = Button(
            size_hint=(None, None),
            background_normal="welcome_img.png",
            size=(dp(360), dp(590)),
            pos=(dp(0), dp(50))
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

        layout.add_widget(btn0)
        layout.add_widget(btn1)
        layout.add_widget(btn2)

        self.add_widget(layout)


# header properties
def make_header(text):
    btn = Button(
        text=text,
        size_hint=(None, None),
        size=(dp(360), dp(50)),
        pos=(dp(0), dp(590)),
        background_normal="",
        background_color=(0, 0, 0, 1),
        color=(1, 1, 1, 1),
        halign="left",
        valign="middle",
        padding_x=dp(15),
    )

    btn.bind(size=lambda inst, val: setattr(inst, 'text_size', inst.size))

    with btn.canvas.after:
        Color(0, 0, 1, 1)
        btn.border_line = Line(width=2)

    def update_line(inst, val):
        x, y = inst.pos
        w, _ = inst.size
        inst.border_line.points = [x, y, x + w, y]

    btn.bind(pos=update_line, size=update_line)
    Clock.schedule_once(lambda dt: update_line(btn, None), 0)

    return btn


# navigation bar properties
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

    layout.add_widget(btn_home)
    layout.add_widget(btn_playlist)


# scrollable properties
def make_scrollable_content(header_text, screen):
    layout = FloatLayout()

    layout.add_widget(make_header(header_text))

    scroll = ScrollView(
        size_hint=(None, None),
        size=(dp(360), dp(540)),
        pos=(dp(0), dp(50)),
    )

    inner = BoxLayout(
        orientation='vertical',
        size_hint_y=None,
    )
    inner.bind(minimum_height=inner.setter('height'))

    scroll.add_widget(inner)
    layout.add_widget(scroll)

    make_nav_bar(screen, layout)

    return layout, inner


# button properties
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


# playlist main screen
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


# random playlist screen
class RandomScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout, inner = make_scrollable_content(" Random", self)

        songs = [
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
            " Numb Little Bug \n -Em Beihold"
        ]

        for song in songs:
            btn = make_playlist_button(song, self.play_song)
            inner.add_widget(btn)

        self.add_widget(layout)

    def play_song(self, instance):
        print(f"Playing: {instance.text}")


# atc playlist screen
class AtcScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout, inner = make_scrollable_content(" Against the Current", self)

        songs = [
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
            "Another You (Another Way)\n -Against The Current",
            "Dreaming Alone\n -Against The Current, Taka",
            "Dreaming Alone\n -Against The Current, Taka",
            "Guessing\n -ATC",
            "Heavenly\n -Against The Current",
        ]

        for song in songs:
            btn = make_playlist_button(song, self.play_song)
            inner.add_widget(btn)

        self.add_widget(layout)

    def play_song(self, instance):
        print(f"Playing: {instance.text}")


#ghost screen
class GhostScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout, inner = make_scrollable_content(" Ghost", self)

        songs = [
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
            "He Is\n -Ghost, Alison Mosshart",
            "Witch Image\n -Ghost",
            "Ritual\n -Ghost",
            "Jigolo Har Megiddo\n -Ghost",
            "Stay [Feat. Patrick Wilson]\n -Ghost, Patrick Wilson",
            "Faith\n -Ghost",
            "Lachryma\n -Ghost",
            "Missionary Man\n -Ghost"    
            ]

        for song in songs:
            btn = make_playlist_button(song, self.play_song)
            inner.add_widget(btn)

        self.add_widget(layout)

    def play_song(self, instance):
        print(f"Playing: {instance.text}")


#judas priest screen
class JPScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout, inner = make_scrollable_content(" Judas Priest", self)

        songs = [
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

        for song in songs:
            btn = make_playlist_button(song, self.play_song)
            inner.add_widget(btn)

        self.add_widget(layout)

    def play_song(self, instance):
        print(f"Playing: {instance.text}")


# default screen
class SimpleScreen(Screen):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)

        layout, inner = make_scrollable_content(title, self)

        btn = make_playlist_button(" Placeholder", self.placeholder_action)
        inner.add_widget(btn)

        self.add_widget(layout)

    def placeholder_action(self, instance):
        print("Placeholder clicked")


# main app
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(PlaylistScreen(name="playlist"))
        sm.add_widget(AtcScreen(name="against"))#
        sm.add_widget(GhostScreen(name="ghost"))
        sm.add_widget(JPScreen(name="jp"))  # FIXED HERE
        sm.add_widget(RandomScreen(name="random"))

        return sm


MyApp().run()