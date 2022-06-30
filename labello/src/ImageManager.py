import pyrealsense2 as rs
import numpy as np
import cv2


class ImageManager:
    def __init__(self):
        self.list_camera = []
        self.camera_connected = False
        self.check_camera_is_connected()

    def check_camera_is_connected(self):
        realsense_ctx = rs.context()
        connected_devices = []
        for i in range(len(realsense_ctx.devices)):
            detected_camera = realsense_ctx.devices[i].get_info(rs.camera_info.serial_number)
            connected_devices.append(detected_camera)

        if (len(connected_devices)) > 0:
            self.camera_connected = True
        else:
            self.camera_connected = False

        self.list_camera = connected_devices
        return self.camera_connected

    def get_next_rgb_image(self):
        pic = cv2.imread("cat.jpg")
        pic = cv2.resize(pic, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        return pic


    def get_next_pc_image(self):
        pic = cv2.imread("cat.jpg")
        pic = cv2.resize(pic, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        return pic

    def get_next_specto_image(self):
        pic = cv2.imread("cat.jpg")
        pic = cv2.resize(pic, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
        return pic