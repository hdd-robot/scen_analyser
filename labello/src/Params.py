import os

class Params:
    def __init__(self):
        self.base_path = os.path.expanduser('~') + "/labello/dataset/"
        self.image_path = self.base_path + "img/"
        self.point_cloud_path = self.base_path + "pcd/"
        self.spectro_path = self.base_path + "spectro/"
        self.check_paths()

    def get_image_path(self):
        return self.image_path

    def get_cloud_path(self):
        return self.point_cloud_path

    def get_spectro_path(self):
        return self.spectro_path

    def check_paths(self):
        if os.path.exists(self.base_path) is False:
            os.makedirs(self.base_path)

        if os.path.exists(self.image_path) is False:
            os.makedirs(self.image_path)

        if os.path.exists(self.point_cloud_path) is False:
            os.makedirs(self.point_cloud_path)

        if os.path.exists(self.spectro_path) is False:
            os.makedirs(self.spectro_path)
