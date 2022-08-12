import pyrealsense2 as rs
import numpy as np
import cv2


class ImageManager:
    def __init__(self):
        self.list_camera = []
        self.camera_connected = False
        self.check_camera_is_connected()
        self.pipeline = None
        self.config = None
        self.pipeline_wrapper = None
        self.pipeline_profile = None
        self.device = None
        self.device_product_line = None
        self.color_image = None
        self.depth_colormap = None
        self.dist_from_object = 0

        self.image_rgb = None
        self.image_pcd = None
        self.image_spectro = None

        self.init_camera()

    def get_data_of_current_image(self):
        img_data = []
        img_data['img_rgb_type'] = ""
        img_data['img_rgb_size'] = 0
        img_data['img_rgb_file_size'] = 0
        img_data['img_depth_size'] = 0
        img_data['img_depth_type'] = ""
        img_data['img_depth_file_size'] = 0
        img_data['img_depth_intrinsec'] = ""
        img_data['img_depth_extrinsec'] = ""
        img_data['img_depth_turntable_deg'] = 0
        img_data['img_depth_distance'] = ""
        img_data['img_pc_name'] = ""
        img_data['img_pc_size'] = ""
        img_data['img_pc_type'] = ""
        img_data['img_pc_file_size'] = ""
        img_data['img_pc_intrinsec'] = ""
        img_data['img_pc_extrinsec'] = ""
        img_data['img_pc_turntable_deg'] = 0
        img_data['img_pc_distance '] = 0
        img_data['img_specto_data'] = ""
        img_data['img_specto_position'] = 0
        return img_data

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
            # return

        self.list_camera = connected_devices
        return self.camera_connected

    def init_camera(self):
        if (self.check_camera_is_connected() is False):
            return
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        # Get device product line for setting a supporting resolution
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(self.device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in self.device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if self.device_product_line == 'L500':
            self.config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.pipeline.start(self.config)


    def get_next_rgb_image(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        if not depth_frame or not color_frame:
            return
        width = depth_frame.get_width()
        height = depth_frame.get_height()
        self.dist_from_object = depth_frame.get_distance(int(width / 2), int(height / 2))

        # Convert images to numpy arrays

        for i in range (10):
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # # If depth and color resolutions are different, resize color image to match depth image for display
        # if depth_colormap_dim != color_colormap_dim:
        #     resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]),
        #                                      interpolation=cv2.INTER_AREA)
        #     images = np.hstack((resized_color_image, depth_colormap))
        # else:
        #     images = np.hstack((color_image, depth_colormap))

        self.image_rgb = color_image
        self.image_pcd = depth_colormap

        resized_color_image = cv2.resize(color_image,
                                         dsize=(int(depth_colormap_dim[1]/2), int(depth_colormap_dim[0]/2)),
                                         interpolation=cv2.INTER_AREA)

        resized_depth_colormap_image = cv2.resize(depth_colormap,
                                         dsize=(int(depth_colormap_dim[1]/2), int(depth_colormap_dim[0]/2)),
                                         interpolation=cv2.INTER_AREA)

        return resized_color_image, resized_depth_colormap_image


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

    def save_current_image_in_disk(self, path):
        if self.image_rgb is None:
            return
        cv2.imwrite(path, self.image_rgb)

    def save_current_pcd_in_disk(self, path):
        if self.image_pcd is None:
            return
        cv2.imwrite(path, self.image_pcd)

    def save_current_spectro_in_disk(self, path):
        if self.image_spectro is None:
            return
        cv2.imwrite(path, self.image_spectro)