import os
from pathlib import Path


class Params:

    base_path = "~/labello/dataset/"
    image_path = base_path + "img"
    point_cloud_path = base_path + "pcd"


    def __init__(self):
        self.path_img = "~"
        self.pc_img = "~"
        pass

    @classmethod
    def create_paths(cls):
        # basePath = Path(cls.base_path)
        # imagePath = Path(cls.image_path)
        # pointCloudPath = Path(cls.point_cloud_path)
        # path = Path(imagePath)
        # path.mkdir(parents=True, exist_ok=True)
        # path = Path(pointCloudPath)
        # path.mkdir(parents=True, exist_ok=True)
        pass
