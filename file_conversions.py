import open3d as o3d
from pathlib import Path
import numpy as np


def kitti_bin_to_ply(input_dir, file_names, output_dir):
    for f in file_names:
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
    for severity in ["light", "moderate", "heavy"]:
        input_dir = Path(f"output/distorted/{severity}/velodyne/")
        bin_files = [f.name for f in input_dir.glob("*.bin")]
        output_dir = f"output/distorted_ply/{severity}/velodyne/"
        kitti_bin_to_ply(input_dir, bin_files, output_dir)
