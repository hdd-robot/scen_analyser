class Scan_object:

    def __init__(self):
        self.current_object = 0
        self.object_proprties = None
        pass

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
        pass

    
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


    
