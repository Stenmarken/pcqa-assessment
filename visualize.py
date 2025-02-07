import numpy as np
import struct
from open3d import *
from pathlib import Path
import os
import rerun as rr
from PIL import Image

def convert_kitti_bin_to_pcd(binFilePath):
    """
    Perhaps this conversion is not entirely correct
    """
    size_float = 4
    list_pcd = []
    with open(binFilePath, "rb") as f:
        byte = f.read(size_float * 4)
        while byte:
            x, y, z, intensity = struct.unpack("ffff", byte)
            list_pcd.append([x, y, z])
            byte = f.read(size_float * 4)
    np_pcd = np.asarray(list_pcd)
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(np_pcd)
    return pcd

def convert_kitti_dir(path, output_path):
    files = [f for f in Path(path).iterdir() if f.is_file()]
    Path(output_path).mkdir(parents=True, exist_ok=True)
    for bin_file in sorted(files):
        file_name = Path(os.path.basename(bin_file))
        print(f"Converting {file_name}")
        pcd_ = convert_kitti_bin_to_pcd(bin_file)
        output_file = f"{os.path.join(output_path, file_name.stem)}.pcd"
        open3d.io.write_point_cloud(output_file, pcd_, write_ascii=False, compressed=False, print_progress=False)

def sorted_files(path):
    return sorted([f for f in Path(path).iterdir() if f.is_file()])

def all_same_length(lists):
    it = iter(lists)
    the_len = len(next(it))
    if not all(len(l) == the_len for l in it):
        return False
    return True
    

def visualize(visualizations):
    rr.init("PCD and image sequence", spawn=True)
    files = [sorted_files(v['path']) for v in visualizations]
    if not all_same_length(files):
        raise ValueError("Directories do not contain the same amount of files")
    n = len(files[0])
    for i in range (n):
        rr.set_time_sequence("frame", i)
        for d_i, d in enumerate(visualizations):
            if d['data_type'] == 'pcd':
                pcd = open3d.io.read_point_cloud(files[d_i][i])
                points = np.asarray(pcd.points)
                colors = np.asarray(pcd.colors)
                rr.log(f"{d['name']}", rr.Points3D(points, colors=colors))
            elif d['data_type'] == 'image':
                image = np.array(Image.open(files[d_i][i]))
                rr.log(f"{d['name']}", rr.Image(image))


if __name__ == "__main__":
    visualizations = [
        {'data_type': 'pcd',
         'name': 'Lidar_Front',
         'path': 'output/RTB_Lidar_Front'},
        {'data_type': 'pcd',
         'name': 'Lidar_Right',
         'path': 'output/RTB_Lidar_Right'},
        {'data_type': 'pcd',
         'name': 'Lidar_Left',
         'path': 'output/RTB_Lidar_Left'},
        {'data_type': 'image',
         'name' : 'Image_Front',
         'path' : '../../data/tmp/avl-snow-day/dgt_2025-01-08-14-37-21_0_s0/RTB_Camera_Front'
        }
    ]
    visualize(visualizations)
    
    #visualize(lidar_path="output/RTB_Lidar_Front",
              #img_path="output/RTB_Lidar_Left")
    #convert_kitti_dir(path="../../data/tmp/avl-snow-day/dgt_2025-01-08-14-37-21_0_s0/RTB_Lidar_Right",
         #output_path="output/RTB_Lidar_Right")