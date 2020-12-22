#!/usr/bin/python3
import youtube_dl

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, GObject

import threading


class GridWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Grid Example")

        # widget grid
        grid = Gtk.Grid()
        self.add(grid)

        # DL button
        self.button = Gtk.Button(label="DL")
        self.button.connect("clicked", self.on_dl_button_clicked)

        # metadata button
        metabutton = Gtk.Button(label="meta")
        metabutton.connect("clicked", self.on_meta_button_clicked)

        # audio only tickbox
        audio_only_box = Gtk.CheckButton(label="audio only")
        audio_only_box.connect("toggled", self.on_audio_box_toggled)

        # input field
        self.txt = Gtk.Entry()
        self.txt.set_width_chars(50)

        # spinner
        self.spinner = Gtk.Spinner()
        ytdl_opts['progress_hooks'] = [self.ytdl_progress_hook]

        # metadata output
        self.metadata = Gtk.Label()

        # download status
        self.download_status = Gtk.Label()

        # grid layout
        grid.add(self.button)
        grid.attach(metabutton, 1, 0, 1, 1)
        grid.attach(self.txt, 2, 0, 2, 1)

        grid.attach(audio_only_box, 0, 1, 1, 1)
        grid.attach(self.metadata, 1, 1, 2, 1)
        grid.attach(self.spinner, 3, 1, 1, 1)

        grid.attach(self.download_status, 0, 2, 3, 1)

    def on_audio_box_toggled(self, checkbox):
        if checkbox.get_active():
            ytdl_opts['format'] = 'bestaudio'
        else:
            ytdl_opts['format'] = 'best'

    def on_meta_button_clicked(self, metabutton):
        url = self.txt.get_text()
        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            self.metadata.set_text('uploader: {}\ntitle: {}'.format(meta['uploader'], meta['title']))

    def on_dl_button_clicked(self, button):
        url = ['']
        url[0] = self.txt.get_text()

        self.ydl = youtube_dl.YoutubeDL(ytdl_opts)

        self.thread = threading.Thread(
                target=self.ydl.download,
                args=(url,)
                )
        self.thread.start()

    def update_dl_status_ui(self, d):
        if d['status'] == 'downloading':
            self.button.set_sensitive(False)
            self.spinner.start()
            self.download_status.set_text('Downloading: {}\nprogress: {}\ntime remaining: {}'.format(d['filename'], d['_percent_str'], d['_eta_str']))
        if d['status'] == 'finished':
            self.button.set_sensitive(True)
            self.spinner.stop()
            self.download_status.set_text('')

    def ytdl_progress_hook(self, d):
        GLib.idle_add(self.update_dl_status_ui, d)

ytdl_opts = {}
win = GridWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
