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
from ImageManager import *
from PlateManage import *

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure
import os.path


import cv2
import numpy as np

# Comment the first line and uncomment the second before installing
# or making the tarball (alternatively, use project variables)
UI_FILE = "ui/labello.ui"


class GUI:
    def __init__(self):

        self.params = Params()

        self.camera_status  = "Unknow"
        self.plate_status   = "Unknow"
        self.spectro_status = "Unknow"

        self.scan_object = Scan_object()
        self.scan_object.init_to_last_object()
        self.selected_object_prop = self.scan_object.get_current_object_prop()



        ### CAMERA
        self.image_manager = ImageManager()

        screen = Gdk.Screen.get_default()
        provider = Gtk.CssProvider()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        css = b"""
                     entry {
                            min-height: 22px;
                     }
                     button.combo {
                            min-height: 0px;
                            margin: 0px;
                            padding: 0px;
                     }
                """
        provider.load_from_data(css)

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_FILE)
        self.builder.connect_signals(self)
        self.refresh_all_components()
        self.window = self.builder.get_object('Labello')
        self.window.maximize()
        self.window.show_all()
        self.check_devices(None)




    def on_window_destroy(self, window):
        Gtk.main_quit()

    def refresh_all_components(self):
        self.selected_object_prop = self.scan_object.get_current_object_prop()
        self.refresh_cmbx_cat_list()
        self.refresh_cmbx_subcat_list()
        self.refresh_cmbx_object_name_list()
        self.refresh_list_objects()
        self.upload_all_fildes()
        self.refresh_image_list()
        self.draw_spectro()

    def on_add_categorie(self, widget):
        dialog = self.builder.get_object('cetegorie_dialog_box')
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("OK")
        elif response == Gtk.ResponseType.CANCEL:
            print("CANCEL")
        dialog.destroy()

    def refresh_cmbx_cat_list(self):
        lst = self.scan_object.get_list_categories()
        cmbx = self.builder.get_object('cmbx_cat_list')
        cmbx.clear()
        # the liststore
        liststore = Gtk.ListStore(str, str)
        lst_cat = []
        for elem in lst:
            liststore.append(elem)
            lst_cat.append(elem[0])
        cmbx.set_model(liststore)
        cell = Gtk.CellRendererText()
        cmbx.pack_start(cell, True)
        cmbx.add_attribute(cell, 'text', 0)
        cmbx.set_active(lst_cat.index(self.selected_object_prop['scat_cat_name']))

        cmbx.set_entry_text_column(1)

    def refresh_cmbx_subcat_list(self):
        lst = []
        if self.selected_object_prop is not None:
            lst = self.scan_object.get_list_subcategories(self.selected_object_prop["cat_name"])
        cmbx = self.builder.get_object('cmbx_subcat_list')
        cmbx.clear()
        liststore = Gtk.ListStore(str, str)
        lst_scat = []
        for elem in lst:
            liststore.append(elem)
            lst_scat.append(elem[0])
        cmbx.set_model(liststore)
        cell = Gtk.CellRendererText()
        cmbx.pack_start(cell, True)
        cmbx.add_attribute(cell, 'text', 0)
        cmbx.set_active(lst_scat.index(self.selected_object_prop['scat_name']))
        cmbx.set_entry_text_column(1)

    def refresh_cmbx_object_name_list(self):
        lst = []
        if self.selected_object_prop is not None:
            lst = self.scan_object.get_list_object_name(self.selected_object_prop["scat_name"])
        cmbx = self.builder.get_object('cmbx_obj_name_list')
        cmbx.clear()
        liststore = Gtk.ListStore(str, str)
        lst_obname = []
        for elem in lst:
            liststore.append(elem)
            lst_obname.append(elem[0])
        cmbx.set_model(liststore)
        cell = Gtk.CellRendererText()
        cmbx.pack_start(cell, True)
        cmbx.add_attribute(cell, 'text', 0)
        cmbx.set_active(lst_obname.index(self.selected_object_prop['obn_name']))

    def cmbx_categorie_changed(self, cmbx):
        obj_cat_index = self.builder.get_object('cmbx_cat_list').get_active()
        obj_cat_model = self.builder.get_object('cmbx_cat_list').get_model()

        if obj_cat_index is None or obj_cat_model is None:
            return

        iter = obj_cat_model.get_iter(obj_cat_index)
        val = obj_cat_model.get_value(iter, 0)

        if (self.selected_object_prop['cat_name'] == val):
            # changed to real value
            self.refresh_cmbx_subcat_list()
            self.refresh_cmbx_object_name_list()
            return

        # changed to new value
        sub_cat_lst = self.scan_object.get_list_subcategories(val)
        cmbx = self.builder.get_object('cmbx_subcat_list')
        cmbx.clear()
        liststore = Gtk.ListStore(str, str)
        lst_scat = []
        for elem in sub_cat_lst:
            liststore.append(elem)
            lst_scat.append(elem[0])
        cmbx.set_model(liststore)
        cell = Gtk.CellRendererText()
        cmbx.pack_start(cell, True)
        cmbx.add_attribute(cell, 'text', 0)
        # cmbx.set_active(lst_scat.index(0))
        cmbx.set_entry_text_column(1)

    def cmbx_subcategorie_changed(self, cmbx):
        obj_subcat_index = self.builder.get_object('cmbx_subcat_list').get_active()
        obj_subcat_model = self.builder.get_object('cmbx_subcat_list').get_model()

        if obj_subcat_index is None or obj_subcat_model is None:
            return

        iter = obj_subcat_model.get_iter(obj_subcat_index)
        val = obj_subcat_model.get_value(iter, 0)

        if (self.selected_object_prop['scat_name'] == val):
            # changed to real value
            self.refresh_cmbx_object_name_list()
            return

        # changed to new value
        obj_name_lst = self.scan_object.get_list_object_name(val)
        cmbx = self.builder.get_object('cmbx_obj_name_list')
        cmbx.clear()
        liststore = Gtk.ListStore(str, str)
        lst_scat = []
        for elem in obj_name_lst:
            liststore.append(elem)
            lst_scat.append(elem[0])
        cmbx.set_model(liststore)
        cell = Gtk.CellRendererText()
        cmbx.pack_start(cell, True)
        cmbx.add_attribute(cell, 'text', 0)
        # cmbx.set_active(lst_scat.index(0))
        cmbx.set_entry_text_column(1)

    def refresh_list_objects(self):
        lst = self.scan_object.get_object_list()
        tv_obj_lst = self.builder.get_object('treeview_object_list')
        list_store = self.builder.get_object('list_store_objects')
        list_store.clear()
        lst_elems = []
        for elem in lst:
            tmp_lst = []
            lst_elems.append(elem[0])
            tmp_lst.append(str(elem[0]))
            tmp_lst.append(elem[1])
            list_store.append(tmp_lst)

        cell = Gtk.CellRendererText()
        tv_obj_lst.set_cursor(lst_elems.index(self.selected_object_prop['obj_id']))



    def upload_all_fildes(self):
        # RealName
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
        obj_shine = self.builder.get_object('obj_size_z')

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
        cmbx.set_active(lst2.index(self.selected_object_prop[props]))
        cmbx.set_entry_text_column(1)

    def go_to_lastest_object(self, btn):
        self.scan_object.init_to_last_object()
        self.selected_object_prop = self.scan_object.get_current_object_prop()
        self.refresh_all_components()

    def go_to_last_object(self, btn):
        self.scan_object.previous_object()
        self.selected_object_prop = self.scan_object.get_current_object_prop()
        self.refresh_all_components()

    def go_to_next_object(self, btn):
        self.scan_object.next_object()
        self.selected_object_prop = self.scan_object.get_current_object_prop()
        self.refresh_all_components()

    def go_to_clicked_object(self, tv, path, col):
        model = tv.get_model()
        tree_iter = model.get_iter(path)
        row = path[0]
        if tree_iter:
            val = model.get_value(tree_iter, 0)
            self.scan_object.move_to_object(val)
            self.selected_object_prop = self.scan_object.get_current_object_prop()
            self.refresh_all_components()

    def update_properties_of_current_object(self):
        obj_real_name = self.builder.get_object('obj_real_name').get_text()
        self.scan_object.set_properties_value('obj_real_name', obj_real_name)

        obj_description = self.builder.get_object('obj_description').get_text()
        self.scan_object.set_properties_value('obj_description', obj_description)

        obj_size_x = self.builder.get_object('obj_size_x').get_text()
        self.scan_object.set_properties_value('obj_size_length_x', obj_size_x)

        obj_size_y = self.builder.get_object('obj_size_y').get_text()
        self.scan_object.set_properties_value('obj_size_width_y', obj_size_y)

        obj_size_z = self.builder.get_object('obj_size_z').get_text()
        self.scan_object.set_properties_value('obj_size_height_z', obj_size_z)

        obj_weight = self.builder.get_object('obj_weight').get_text()
        self.scan_object.set_properties_value('obj_weight', obj_weight)

        obj_shine_index = self.builder.get_object('cmbx_obj_shine').get_active()
        obj_shine_model = self.builder.get_object('cmbx_obj_shine').get_model()
        iter = obj_shine_model.get_iter(obj_shine_index)
        val = obj_shine_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_shine', val)

        obj_filling_index = self.builder.get_object('cmbx_obj_filling').get_active()
        obj_filling_model = self.builder.get_object('cmbx_obj_filling').get_model()
        iter = obj_filling_model.get_iter(obj_filling_index)
        val = obj_filling_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_filling', val)

        obj_mov_name_index = self.builder.get_object('cmbx_obj_moveable').get_active()
        obj_mov_name_model = self.builder.get_object('cmbx_obj_moveable').get_model()
        iter = obj_mov_name_model.get_iter(obj_mov_name_index)
        val = obj_mov_name_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_mov_name', val)

        obj_color_name_1_index = self.builder.get_object('cmbx_obj_color_1').get_active()
        obj_color_name_1_model = self.builder.get_object('cmbx_obj_color_1').get_model()
        iter = obj_color_name_1_model.get_iter(obj_color_name_1_index)
        val = obj_color_name_1_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_color_name_1', val)

        obj_color_name_2_index = self.builder.get_object('cmbx_obj_color_2').get_active()
        obj_color_name_2_model = self.builder.get_object('cmbx_obj_color_2').get_model()
        iter = obj_color_name_2_model.get_iter(obj_color_name_2_index)
        val = obj_color_name_2_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_color_name_2', val)

        obj_color_name_3_index = self.builder.get_object('cmbx_obj_color_3').get_active()
        obj_color_name_3_model = self.builder.get_object('cmbx_obj_color_3').get_model()
        iter = obj_color_name_3_model.get_iter(obj_color_name_3_index)
        val = obj_color_name_3_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_color_name_3', val)

        obj_mat_name_1_index = self.builder.get_object('cmbx_obj_mat_1').get_active()
        obj_mat_name_1_model = self.builder.get_object('cmbx_obj_mat_1').get_model()
        iter = obj_mat_name_1_model.get_iter(obj_mat_name_1_index)
        val = obj_mat_name_1_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_mat_name_1', val)

        obj_mat_name_2_index = self.builder.get_object('cmbx_obj_mat_2').get_active()
        obj_mat_name_2_model = self.builder.get_object('cmbx_obj_mat_2').get_model()
        iter = obj_mat_name_2_model.get_iter(obj_mat_name_2_index)
        val = obj_mat_name_2_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_mat_name_2', val)

        obj_mat_name_3_index = self.builder.get_object('cmbx_obj_mat_3').get_active()
        obj_mat_name_3_model = self.builder.get_object('cmbx_obj_mat_3').get_model()
        iter = obj_mat_name_3_model.get_iter(obj_mat_name_3_index)
        val = obj_mat_name_3_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_mat_name_3', val)

        obj_flx_name_index = self.builder.get_object('cmbx_obj_flx').get_active()
        obj_flx_name_model = self.builder.get_object('cmbx_obj_flx').get_model()
        iter = obj_flx_name_model.get_iter(obj_flx_name_index)
        val = obj_flx_name_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_flx_name', val)

        ### OBJNAME
        obj_name_index = self.builder.get_object('cmbx_obj_name_list').get_active()
        obj_name_model = self.builder.get_object('cmbx_obj_name_list').get_model()
        iter = obj_name_model.get_iter(obj_name_index)
        val = obj_name_model.get_value(iter, 0)
        self.scan_object.set_properties_value('obj_obn_name', val)

    def save_current_object(self, btn):
        self.update_properties_of_current_object()
        self.scan_object.save_curent_object()
        self.refresh_all_components()

    def new_object(self, btn):
        self.update_properties_of_current_object()
        self.scan_object.set_properties_value('obj_size_length_x', 0)
        self.scan_object.set_properties_value('obj_size_width_y', 0)
        self.scan_object.set_properties_value('obj_size_height_z', 0)
        self.scan_object.set_properties_value('obj_weight', 0)
        self.scan_object.add_object()
        self.refresh_all_components()

    def delete_object(self, btn):
        # todo : finish delete action
        dialog = Gtk.MessageDialog(
            title="Delete selected object",
            parent=self.window,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Are you really want de remove this object ? ",
            modal=True)

        response = dialog.run()
        if response == Gtk.ResponseType.NO:
            print("CANCEL")
            dialog.destroy()
            return

        self.scan_object.delete_curent_object()
        self.refresh_all_components()
        dialog.destroy()



    def refresh_image_list(self):
        lst = self.scan_object.get_list_images()
        tv_img_lst = self.builder.get_object('treeview_image_list')
        list_store = self.builder.get_object('list_strore_images')
        list_store.clear()
        lst_elems = []
        for elem in lst:
            tmp_lst = []
            lst_elems.append(elem[0])
            tmp_lst.append(str(elem[0]))
            tmp_lst.append(elem[1])
            list_store.append(tmp_lst)

        cell = Gtk.CellRendererText()
        #tv_img_lst.set_cursor(lst_elems[....])


    def start_image_captur(self, btn):
        if self.image_manager.check_camera_is_connected() is False:
            print("error camera ")
            dialog = Gtk.MessageDialog(
                title="Error camera",
                parent=self.window,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                text="Camera is not connected ! ",
                modal=True)
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                dialog.destroy()
            return

        rgb_image = self.builder.get_object('rgb_image')
        pc_image = self.builder.get_object('pc_image')
        spect_image = self.builder.get_object('spect_image')

        ### SHOW RGB IMAGE
        rgb_img, pc_ima = self.image_manager.get_next_rgb_image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(rgb_img.tobytes(),
                                                GdkPixbuf.Colorspace.RGB,
                                                False,
                                                8,
                                                rgb_img.shape[1],
                                                rgb_img.shape[0],
                                                rgb_img.shape[2] * rgb_img.shape[1])
        rgb_image.set_from_pixbuf(pixbuf.copy())

        ### SHOW PC IMAGE
        #pc_ima = self.image_manager.get_next_pc_image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(pc_ima.tobytes(),
                                                GdkPixbuf.Colorspace.RGB,
                                                False,
                                                8,
                                                pc_ima.shape[1],
                                                pc_ima.shape[0],
                                                pc_ima.shape[2] * rgb_img.shape[1])
        pc_image.set_from_pixbuf(pixbuf.copy())

        ### SHOW SPECTRO IMAGE
        spect_img = self.image_manager.get_next_specto_image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(spect_img.tobytes(),
                                                GdkPixbuf.Colorspace.RGB,
                                                False,
                                                8,
                                                spect_img.shape[1],
                                                spect_img.shape[0],
                                                spect_img.shape[2] * rgb_img.shape[1])
        spect_image.set_from_pixbuf(pixbuf.copy())

    def save_current_image(self, btn):
        rgb_path = self.params.get_image_path()
        pcd_path = self.params.get_cloud_path()
        spectro_path = self.params.get_spectro_path()

        if self.camera_status != 'OK':
            if self.image_manager.check_camera_is_connected() is False:
                print("No image ")
                dialog = Gtk.MessageDialog(
                    title="Error camera",
                    parent=self.window,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.CLOSE,
                    text="No image to save ! ",
                    modal=True)
                response = dialog.run()
                if response == Gtk.ResponseType.CLOSE:
                    dialog.destroy()
                return

        data = self.scan_object.create_new_images("") # todo data

        rgb_path = rgb_path + data['img_rgb_name']
        pcd_path = pcd_path + data['img_depth_name']
        #spectro_path = spectro_path + data['img_rgb_name']

        self.image_manager.save_current_image_in_disk(rgb_path)
        self.image_manager.save_current_pcd_in_disk(pcd_path)
        #self.image_manager.save_current_spectro_in_disk(spectro_path)

        self.refresh_image_list()
        pass

    def show_clicked_image(self, tv, path, col):
        model = tv.get_model()
        tree_iter = model.get_iter(path)
        row = path[0]
        if tree_iter:
            id_image = model.get_value(tree_iter, 0)
            id_object = self.scan_object.get_current_object_prop()['obj_id']

            self.scan_object.load_image(id_object, id_image)

            rgb_path = self.params.get_image_path()
            pcd_path = self.params.get_cloud_path()

            rgb_image = self.builder.get_object('rgb_image')
            depth_image = self.builder.get_object('pc_image')
            spect_image = self.builder.get_object('spect_image')

            rgb_file_path = rgb_path+ self.scan_object.current_image['img_rgb_name']
            depth_file_path = pcd_path+ self.scan_object.current_image['img_depth_name']

            if os.path.exists(rgb_file_path):
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    filename=rgb_file_path,
                    width=400,
                    height=400,
                    preserve_aspect_ratio=True)
                rgb_image.set_from_pixbuf(pixbuf.copy())

        if os.path.exists(depth_file_path):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=depth_file_path,
                width=400,
                height=400,
                preserve_aspect_ratio=True)
            depth_image.set_from_pixbuf(pixbuf.copy())



    def draw_spectro(self):
        rgb_image = self.builder.get_object('specto_graph')
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()
        t = np.arange(0.0, 3.0, 0.01)
        s = np.sin(2 * np.pi * t)
        ax.plot(t, s)
        canvas = FigureCanvas(fig)  # a Gtk.DrawingArea
        canvas.set_size_request(800, 400)
        rgb_image.set_border_width(10)
        rgb_image.add(canvas)

    def check_devices(self, btn):
        self.check_status()
        label_turntable = self.builder.get_object('lab_turn_tab')
        label_camera    = self.builder.get_object('lab_camera')
        label_spectro   = self.builder.get_object('lab_spectro')

        color_turntable = "green" if self.plate_status=='OK' else "red"
        color_camera = "green" if self.camera_status=='OK' else "red"
        color_spectro = "green" if label_spectro=='OK' else "red"

        label_turntable.set_markup("<span color='"+color_turntable+"'>Turntable: " + self.plate_status + "</span>")
        label_camera.set_markup("<span color='"+color_camera+"'>Camera: " + self.camera_status + "</span>")
        label_spectro.set_markup("<span color='"+color_spectro+"'>Spectroscope: " + self.spectro_status + "</span>")



    def check_status(self):
        ## Plate
        PlateManage.init_plate()
        if PlateManage.get_status():
            self.plate_status = "OK"
        else:
            self.plate_status = "Not Respond"

        if self.image_manager.check_camera_is_connected():
            self.camera_status = "OK"
        else:
            self.camera_status = "Not Respond"

        # todo : add check spectro
        self.spectro_status = "NONE"

    def read_from_turntable(self, btn):
        nb_shots_int = 0
        nb_shots = self.builder.get_object('nb_shots').get_text()
        try:
            nb_shots_int = int(nb_shots)
        except ValueError:
            dialog = Gtk.MessageDialog(
                title="Error value",
                parent=self.window,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                text="Shots mast be integer  ! ",
                modal=True)
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                dialog.destroy()
            return

        if (self.plate_status != 'OK' or self.camera_status != 'OK'):
            dialog = Gtk.MessageDialog(
                title="Error Camera or Plate",
                parent=self.window,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.CLOSE,
                text="Camera or plate not respond ! ",
                modal=True)
            response = dialog.run()
            if response == Gtk.ResponseType.CLOSE:
                dialog.destroy()
            return

        if PlateManage.get_status() is False:
            print("error Plafe  status ")
            return

        steps =  200 / nb_shots_int
        for i in range (nb_shots_int):
            self.start_image_captur(None)
            time.sleep(0.1)
            self.save_current_image(None)
            self.refresh_all_components()

            PlateManage.move_plate_steps(steps)
            time.sleep(2)


def main():
    app = GUI()
    Gtk.main()


if __name__ == "__main__":
    sys.exit(main())
