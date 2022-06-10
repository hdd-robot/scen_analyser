from db_manager import *


class Scan_object:

    def __init__(self):
        self.db_manager = db_manager()
        self.current_object = 0
        self.object_proprties = None
        self.properties = {}

    def init_to_last_object(self):
        last_id = self.db_manager.get_last_object()
        if last_id is None:
            self.properties = {}
            return
        self.properties = self.db_manager.get_object_by_id(last_id)


    def next_object(self):
        """ move to the next object  """
        pass

    def previous_object(self):
        """ move to the previous object  """
        pass

    def move_to_object(self, obj_id):
        """ move to the previous object  """
        pass

    def get_object_list(self):
        """ get list of all objects"""
        pass

    def add_color(self, properties):
        """ add color """
        pass

    def get_list_color(self):
        """ get list of colors """
        lst = self.db_manager.get_colors()
        return lst

    def add_material(self, properties):
        """ add material """
        pass

    def add_object(self, properties):
        """ proprties ar in dictionary  """
        pass

    def get_current_object(self):
        """ return dictionaty with object proprty """
        ## get object
        return None

    def get_list_images(self):
        """ get list of images of curent object
            return py list of list  with featurs of images
            [
              [rgb images],
              [depth images],
              [spectroscop data]
            ]
        """
        return None



