#!/usr/bin/python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-
#
# main.py
# Copyright (C) 2022 Halim Djerroud <hdd@ai.univ-paris8.fr>
#
# imcloudlab is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# imcloudlab is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys
from Scan_object import *



# Comment the first line and uncomment the second before installing
# or making the tarball (alternatively, use project variables)
UI_FILE = "ui/labello.ui"

class GUI:
    def __init__(self):
        self.scan_object = Scan_object()
        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)

        self.init_components()

        self.window = self.builder.get_object('Labello')
        self.window.show_all()


    def init_components(self):
        self.refresh_cmbx_cat_list(None)

    def on_window_destroy(self, window):
        Gtk.main_quit()

    def on_add_categorie(self,widget):
        dialog = self.builder.get_object('cetegorie_dialog_box')
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("OK")
        elif response == Gtk.ResponseType.CANCEL:
            print("CANCEL")
        dialog.destroy()

    def refresh_cmbx_cat_list(self, comb):

        lst = self.scan_object.get_list_color()

        cmbx_cat_list = self.builder.get_object('cmbx_cat_list')
        cmbx_cat_list.clear()
        # the liststore
        liststore = Gtk.ListStore(str, str)

        for elem in lst:
            liststore.append(elem)
        cmbx_cat_list.set_model(liststore)

        cell = Gtk.CellRendererText()
        cmbx_cat_list.pack_start(cell, True)
        cmbx_cat_list.add_attribute(cell, 'text', 0)
        cmbx_cat_list.set_active(0)
        cmbx_cat_list.set_entry_text_column(1)


def main():
    app = GUI()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())

