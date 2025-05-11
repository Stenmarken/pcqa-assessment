import open3d as o3d
from pathlib import Path
import numpy as np
import yaml
import shutil
import argparse

def kitti_bin_to_ply(file_path):
    # Is it really np.float32?
    bin = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    xyz = bin[:, :3]
    intensities = bin[:, 3]
    intensity_normalized = np.clip(intensities / 255.0, 0.0, 1.0)
    colors = np.stack([intensity_normalized, intensity_normalized, intensity_normalized], axis = 1)

    ply = o3d.geometry.PointCloud()
    ply.points = o3d.utility.Vector3dVector(xyz)
    ply.colors = o3d.utility.Vector3dVector(colors)
    return ply

def kitti_bin_to_ply_directory(input_dir, output_dir):
    input_dir = Path(input_dir)
    bin_files = [file for file in input_dir.rglob("*") if file.is_file() and file.suffix in {".bin"}]
    remaining_files = [file for file in input_dir.rglob("*") if file.is_file() and file.suffix not in {".bin"}]
    for idx, f in enumerate(bin_files):
        print(f"File: #{idx+1}. Path: {f}")
        path = Path(input_dir)
        file_path = path / f
        ply = kitti_bin_to_ply(file_path)

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        f = Path(f).stem
        output_path = output_path / f
        o3d.io.write_point_cloud(f"{output_path}.ply", ply, print_progress=True)
    for file in remaining_files:
        if file.is_file():
            shutil.copy(file, output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Converts KITTI bin files to PLY files"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        required=True,
        help='Path to the configuration file'
    )
    args = parser.parse_args()
    print(args)
    with open(args.config, 'r') as f:
        data = yaml.safe_load(f)

    base_bin_dir = Path(data["bin_dir"])
    base_ply_dir = Path(data["ply_dir"])

    bin_dirs = [d for d in base_bin_dir.iterdir() if d.is_dir()]

    for bin_dir in bin_dirs:
        ply_dir = base_ply_dir / bin_dir.name
        ply_dir.mkdir(parents=True, exist_ok=True)

        kitti_bin_to_ply_directory(bin_dir, ply_dir)
