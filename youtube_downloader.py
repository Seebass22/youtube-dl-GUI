import youtube_dl
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

ytdl_opts = {}


class GridWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Grid Example")

        # widget grid
        grid = Gtk.Grid()
        self.add(grid)

        # DL button
        button = Gtk.Button(label="click me")
        button.connect("clicked", self.on_button_clicked)

        audio_only_box = Gtk.CheckButton(label="audio only")
        audio_only_box.connect("toggled", self.on_audio_box_toggled)

        # input field
        self.txt = Gtk.Entry()

        grid.add(button)
        grid.attach(self.txt, 1, 0, 2, 1)
        grid.attach(audio_only_box, 0, 1, 1, 1)

    def on_audio_box_toggled(self, checkbox):
        if checkbox.get_active():
            ytdl_opts['format'] = 'bestaudio'
        else:
            ytdl_opts['format'] = 'best'

    def on_button_clicked(self, button):
        url = ['']
        url[0] = self.txt.get_text()
        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            ydl.download(url)


win = GridWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
