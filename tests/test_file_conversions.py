import unittest
from file_conversions import kitti_bin_to_ply
from pathlib import Path
import shutil
import numpy as np
import open3d as o3d
import os

class TestFileConversions(unittest.TestCase):

    def get_rehearse3d_labeled_path(self):
        try:
            with open("configs/test_configs/rehearse3d-labeled_path.txt", "r") as f:
                path = f.read().strip()
            return path
        except FileNotFoundError:
            raise RuntimeError("Secret path file not found. Please create 'configs/test_configs/rehearse3d-labeled_path.txt'.")
    
    def test_kitti_bin_to_ply(self):
        base_dir = Path(self.get_rehearse3d_labeled_path())
        bin_dirs = [d for d in base_dir.iterdir() if d.is_dir()]
        for bin_dir in bin_dirs:

            bin_files = [file for file in bin_dir.rglob("*") if file.is_file() and file.suffix in {".bin"}]
            for file in bin_files:
                kitti_pc = np.fromfile(file, dtype=np.float32).reshape(
                    -1, 4
                )[:, :3]

                ply = kitti_bin_to_ply(file)

                ply_points = np.asarray(ply.points)

                self.assertTrue(np.array_equal(kitti_pc, ply_points))


if __name__ == "__main__":
    unittest.main()
