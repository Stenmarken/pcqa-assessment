from open3d import *
import open3d as o3d
from pathlib import Path
import rerun as rr
import yaml


def visualize(data_dict):
    severities = data_dict["severities"]
    file_names = data_dict["file_names"]
    rr.init("Point cloud sequence", spawn=True)
    for i in range(len(file_names)):
        print(f"Timestamp: {i}")
        rr.set_time_sequence("frame", i)
        for sev in severities:
            ply_path = f"{data_dict[sev]}/{file_names[i]}"

            ply_pc = o3d.io.read_point_cloud(ply_path)
            rr.log(f"{sev}", rr.Points3D(ply_pc.points))


if __name__ == "__main__":
    file_names = [f"{i:06}.ply" for i in range(1, 598)]
    with open("config.yaml", "r") as file:
        data_dict = yaml.safe_load(file)

    data_dict["file_names"] = file_names
    visualize(data_dict)
