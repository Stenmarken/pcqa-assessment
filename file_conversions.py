import open3d as o3d
from pathlib import Path
import numpy as np
import yaml


def kitti_bin_to_ply(input_dir, file_names, output_dir):
    for idx, f in enumerate(file_names):
        print(f"File: #{idx+1}. Path: {f}")
        path = Path(input_dir)
        file_path = path / f

        # Is it really np.float32?
        bin = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
        xyz = bin[:, :3]
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        f = Path(f).stem
        output_path = output_path / f
        o3d.io.write_point_cloud(f"{output_path}.ply", pcd, print_progress=True)


if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        data = yaml.safe_load(file)

    bin_dirs = data["bin_dirs"]
    ply_dirs = data["ply_dirs"]
    assert len(bin_dirs) == len(ply_dirs)

    for i in range(len(bin_dirs)):
        print(f"Directory: {ply_dirs[i]}")
        input_dir = Path(bin_dirs[i])
        bin_files = [f.name for f in input_dir.glob("*.bin")]
        output_dir = ply_dirs[i]
        kitti_bin_to_ply(input_dir, bin_files, output_dir)
