from pathlib import Path
import subprocess
import yaml
import json
import time
import argparse
import numpy as np

def append_to_dict(path, file_name, score):
    if Path(path).exists():
        with open(path, "r") as f:
            d = json.load(f)
    else:
        d = {}
    d[file_name] = score
    with open(path, "w") as f:
        json.dump(d, f, indent=4)

def read_results_dict(path):
    if Path(path).exists():
        with open(path, "r") as f:
            d = json.load(f)
    else:
        d = {}
    return d

def run_mm_pcqa_ply(data):
    base_ply_dir = Path(data["ply_dir"])
    ply_dirs = [d for d in base_ply_dir.iterdir() if d.is_dir()]
    test_single_ply = data["test_single_ply_path"]
    model_pth = data["model_pth_path"]
    output_path = data["save_results_path"]
    start = time.time()
    for ply_dir in ply_dirs:
        print(f"Running {ply_dir}")
        result = subprocess.run(
                    [
                        "python3",
                        test_single_ply,
                        "--pc_dir",
                        str(ply_dir),
                        "--ckpt_path",
                        model_pth,
                        "--output_path",
                        output_path
                    ],
                    capture_output=True,
                    text=True,
                )
        with open("stdout.txt", "w") as f:
            f.write(result.stdout)
        if result.stderr != "":
            print("Error:", result.stderr)
        if result.returncode != 0:
            print("Return Code:", result.returncode)
        print(f"Time: {time.time() - start} s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MM-PCQA runner")
    parser.add_argument("-c", "--configuration", type=str, required=True)
    arguments = parser.parse_args()
    with open(arguments.configuration, 'r') as file:
        data = yaml.safe_load(file)
    run_mm_pcqa_ply(data)