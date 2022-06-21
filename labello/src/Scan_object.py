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
        return self.db_manager.get_next_object()

    def previous_object(self):
        """ move to the previous object  """
        return self.db_manager.get_previous_object()

    def move_to_object(self, obj_id):
        """ move to the  object by id  """
        pass

    def get_object_list(self):
        """ get list of all objects"""
        lst = []
        for elem in self.db_manager.get_list_all_object():
            lst.append(list(elem.values()))
        return lst

    def add_color(self, properties):
        """ add color """
        pass

    def get_list_color(self):
        """ get list of colors """
        lst = self.db_manager.get_list_colors()
        return lst

    def add_material(self, properties):
        """ add color """
        pass

    def get_list_material(self):
        """ get list of colors """
        lst = self.db_manager.get_list_material()
        return lst


    def add_categorie(self, properties):
        """ add categorie """
        self.db_manager.add_new_categorie(properties);
        return

    def get_list_categories(self):
        """ get list of colors """
        lst = self.db_manager.get_list_categories()
        return lst

    def add_flexible(self, properties):
        """ add flexible """
        self.db_manager.add_new_flexible(properties);
        return

    def get_list_flexible(self):
        """ get list of flexible """
        lst = self.db_manager.get_list_flexible()
        return lst



    def add_shine(self, properties):
        """ add categorie """
        self.db_manager.add_new_shine(properties);
        return

    def get_list_shine(self):
        """ get list of colors """
        lst = self.db_manager.get_list_shine()
        return lst

    def add_filling(self, properties):
        """ add filling """
        self.db_manager.add_new_filing(properties);
        return

    def get_list_filling(self):
        """ get list of filling """
        lst = self.db_manager.get_list_fillings()
        return lst

    def add_movable(self, properties):
        """ add movable """
        self.db_manager.add_new_filing(properties);
        return

    def get_list_movable(self):
        """ get list of movable """
        lst = self.db_manager.get_list_movable()
        return lst


    def get_list_subcategories(self, id_categorie):
        """ get list of subcategories """
        lst = self.db_manager.get_list_subcategories(id_categorie)
        return lst

    def get_list_object_name(self, id_subcategorie):
        """ get list of name """
        lst = self.db_manager.get_list_objectName(id_subcategorie)
        return lst


    def add_material(self, properties):
        """ add material """
        pass

    def add_object(self, properties):
        """ proprties ar in dictionary  """
        pass

    def get_current_object_prop(self):
        """ return dictionaty with object proprty """
        ## get object
        return self.properties

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



