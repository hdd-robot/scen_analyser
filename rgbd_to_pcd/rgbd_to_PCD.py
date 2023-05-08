
import open3d  as o3d
import matplotlib.pyplot as plt
import numpy as np
import cv2

if __name__ == "__main__":

    spinholeCamera = o3d.io.read_pinhole_camera_intrinsic('camera_primesense.json')

    color_raw = o3d.io.read_image("/home/hdd/labello/dataset/img/rgb_1_18.jpg")
    depth_raw = o3d.io.read_image("/home/hdd/labello/dataset/pcd/depth_1_18.png")
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth( color_raw, depth_raw, convert_rgb_to_intensity=False )

    camera_intrinsic = o3d.io.read_pinhole_camera_intrinsic("./d415.json")
    print( camera_intrinsic.intrinsic_matrix )

    camera_intrinsic = o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)



    # print(rgbd_image)
    # plt.subplot(1, 2, 1)
    # plt.title('Grayscale image')
    # plt.imshow(rgbd_image.color)
    # plt.subplot(1, 2, 2)
    # plt.title('Depth image')
    # plt.imshow(rgbd_image.depth)
    # plt.show()

    camera_extrinsec = np.array(0.999961, 0.00184501, -0.00861185, -0.00187475, 0.999992, -0.00344586, 0.00860543, 0.00346188, 0.999957)
    camera_extrinsec.reshape(3, 3)

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera_intrinsic, camera_extrinsec)



    # print(np.asarray(pcd.points))
    # print("\n")

    pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

    o3d.visualization.draw_geometries([pcd])
    o3d.io.write_point_cloud( "out.ply", pcd )