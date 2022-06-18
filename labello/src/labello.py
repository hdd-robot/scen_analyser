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
        self.scan_object.init_to_last_object()
        self.selected_object_prop = self.scan_object.get_current_object_prop()


        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)
        self.init_components()
        self.window = self.builder.get_object('Labello')
        self.window.show_all()


    def init_components(self):
        self.refresh_cmbx_cat_list(None)
        self.refresh_cmbx_subcat_list(None)
        self.refresh_cmbx_object_name_list(None)
        self.upload_all_fildes()
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
        lst = self.scan_object.get_list_categories()
        cmbx = self.builder.get_object('cmbx_cat_list')
        cmbx.clear()
        # the liststore
        liststore = Gtk.ListStore(str, str)
        for elem in lst:
            liststore.append(elem)
        cmbx.set_model(liststore)
        cell = Gtk.CellRendererText()
        cmbx.pack_start(cell, True)
        cmbx.add_attribute(cell, 'text', 0)
        cmbx.set_active(0)
        cmbx.set_entry_text_column(1)

    def refresh_cmbx_subcat_list(self, comb):
        lst = []
        if self.selected_object_prop is not None:
            lst = self.scan_object.get_list_subcategories(self.selected_object_prop["cat_name"])
        cmbx = self.builder.get_object('cmbx_subcat_list')
        cmbx.clear()
        liststore = Gtk.ListStore(str, str)
        for elem in lst:
            liststore.append(elem)
        cmbx.set_model(liststore)
        cell = Gtk.CellRendererText()
        cmbx.pack_start(cell, True)
        cmbx.add_attribute(cell, 'text', 0)
        cmbx.set_active(0)
        cmbx.set_entry_text_column(1)
        pass

    def refresh_cmbx_object_name_list(self, comb):
        lst = []
        if self.selected_object_prop is not None:
            lst = self.scan_object.get_list_object_name(self.selected_object_prop["scat_name"])
        cmbx = self.builder.get_object('cmbx_obj_name_list')
        cmbx.clear()
        liststore = Gtk.ListStore(str, str)
        for elem in lst:
            liststore.append(elem)
        cmbx.set_model(liststore)
        cell = Gtk.CellRendererText()
        cmbx.pack_start(cell, True)
        cmbx.add_attribute(cell, 'text', 0)
        cmbx.set_active(0)
        cmbx.set_entry_text_column(1)
        pass

    def upload_all_fildes(self):
        #RealName
        obj_real_name = self.builder.get_object('obj_real_name')
        obj_real_name.set_text(self.selected_object_prop["obj_real_name"])
        # Description
        obj_description = self.builder.get_object('obj_description')
        obj_description.set_text(self.selected_object_prop["obj_real_description"])
        # size x
        obj_size_x = self.builder.get_object('obj_size_x')
        obj_size_x.set_text(str(self.selected_object_prop["obj_size_length_x"]))
        # size y
        obj_size_y = self.builder.get_object('obj_size_y')
        obj_size_y.set_text(str(self.selected_object_prop["obj_size_width_y"]))
        # size z
        obj_size_z = self.builder.get_object('obj_size_z')
        obj_size_z.set_text(str(self.selected_object_prop["obj_size_height_z"]))
        # obj_weight
        obj_weight = self.builder.get_object('obj_weight')
        obj_weight.set_text(str(self.selected_object_prop["obj_weight"]))

        # load combobox
        self.load_cmbx('cmbx_obj_shine', self.scan_object.get_list_shine(), 'obj_shine')
        self.load_cmbx('cmbx_obj_filling', self.scan_object.get_list_filling(), 'obj_filling')
        self.load_cmbx('cmbx_obj_moveable', self.scan_object.get_list_movable(), 'obj_mov_name')
        self.load_cmbx('cmbx_obj_color_1', self.scan_object.get_list_color(), 'obj_color_name_1')
        self.load_cmbx('cmbx_obj_color_2', self.scan_object.get_list_color(), 'obj_color_name_2')
        self.load_cmbx('cmbx_obj_color_3', self.scan_object.get_list_color(), 'obj_color_name_3')
        self.load_cmbx('cmbx_obj_mat_1', self.scan_object.get_list_material(), 'obj_mat_name_1')
        self.load_cmbx('cmbx_obj_mat_2', self.scan_object.get_list_material(), 'obj_mat_name_2')
        self.load_cmbx('cmbx_obj_mat_3', self.scan_object.get_list_material(), 'obj_mat_name_3')
        self.load_cmbx('cmbx_obj_flx', self.scan_object.get_list_flexible(), 'obj_flx_name')



    def load_cmbx(self, cmbx_name, lst, props):
        cmbx = self.builder.get_object(cmbx_name)
        cmbx.clear()
        liststore = Gtk.ListStore(str, str)
        for elem in lst:
            liststore.append(elem)
        cmbx.set_model(liststore)
        cell = Gtk.CellRendererText()
        cmbx.pack_start(cell, True)
        cmbx.add_attribute(cell, 'text', 0)
        lst2 = [x[0] for x in lst]
        print(lst2)
        cmbx.set_active(lst2.index(self.selected_object_prop[props]))
        cmbx.set_entry_text_column(1)

def main():
    app = GUI()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())

