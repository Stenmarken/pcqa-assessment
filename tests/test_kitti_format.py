import numpy as np
import unittest
import glob
import os

class TestFileConversions(unittest.TestCase):
    def get_rehearse3d_labeled_path(self):
        try:
            with open("configs/test_configs/rehearse3d-labeled_path.txt", "r") as f:
                path = f.read().strip()
            return path
        except FileNotFoundError:
            raise RuntimeError("Secret path file not found. Please create 'configs/test_configs/rehearse3d-labeled_path.txt'.")

    def test_file_is_kitti_format(self):
        base_dir = self.get_rehearse3d_labeled_path()
        matches = glob.glob(os.path.join(base_dir, '**', '*.bin'), recursive=True)
        bin_files = [f for f in matches if os.path.isfile(f)]

        for file in bin_files:
            point_cloud = np.fromfile(file, dtype=np.float32)

            self.assertEqual(point_cloud.size % 4, 0, f"File size is not divisible by 4: {file}")

            point_cloud = point_cloud.reshape(-1, 4)
            x, y, z, i = point_cloud[:, 0], point_cloud[:, 1], point_cloud[:, 2], point_cloud[:, 3]


            # Check finite numbers
            self.assertTrue(
                np.all(np.isfinite(point_cloud)),
                f"File {file} contains non-finite values (NaN or Inf)."
            )
            # Intensity checks
            if i.min() >= 0:
                print(f"File {file} has intensity values below 0.")

            self.assertTrue(
                (i.max() <= 255),
                f"File {file} has intensity values above 255."
            )

            # Optional sanity: no all-zeros
            self.assertFalse(
                np.all((x == 0) & (y == 0) & (z == 0)),
                f"File {file} has all points at (0,0,0)."
            )

if __name__ == "__main__":
    unittest.main()