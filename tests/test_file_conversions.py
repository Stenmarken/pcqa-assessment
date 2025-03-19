import unittest
from file_conversions import kitti_bin_to_ply
from pathlib import Path
import shutil
import numpy as np
import open3d as o3d


class TestFileConversions(unittest.TestCase):
    output_dir = Path("output/distorted/heavy/velodyne/tmp/")

    def tearDown(self):
        if self.output_dir.exists() and self.output_dir.is_dir():
            shutil.rmtree(self.output_dir)
        else:
            print(f"Directory {self.output_dir} does not exist")

    def test_kitti_bin_to_ply(self):
        input_dir = "output/distorted/heavy/velodyne/"
        input_dir = "output/distorted/heavy/velodyne/"
        file_name = "000001.bin"
        kitti_bin_to_ply(input_dir, [file_name], self.output_dir)

        bin_points = np.fromfile(f"{input_dir}/{file_name}", dtype=np.float32).reshape(
            -1, 4
        )[:, :3]

        ply = o3d.io.read_point_cloud(f"{self.output_dir}/000001.ply")

        ply_points = np.asarray(ply.points)

        self.assertTrue(np.array_equal(bin_points, ply_points))


if __name__ == "__main__":
    unittest.main()
