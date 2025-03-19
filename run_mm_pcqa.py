from pathlib import Path
import subprocess
import yaml
import json
import time

def append_to_dict(path, file_name, score):
    with open(path, "r") as f:
        d = json.load(f)
    d[file_name] = score
    with open(path, "w") as f:
        json.dump(d, f, indent=4)

def read_results_dict(path):
    with open(path, "r") as f:
        d = json.load(f)
    return d

def run_mm_pcqa(data):
    ply_dirs = data["ply_dirs"]
    test_single_ply = data["test_single_ply_path"]
    model_pth = data["model_pth_path"]
    output_path = data["save_results_path"]
    start = time.time()
    for ply_dir in ply_dirs:
        print(f"Running dir: {ply_dir}")
        ply_dir = Path(ply_dir)
        all_files = sorted([file for file in ply_dir.rglob("*") if file.is_file()])

        for idx, f in enumerate(all_files):
            d = read_results_dict(output_path)
            string_file_path = str(f)
            if string_file_path in d:
                print(f"Already calculated score for {f}. Skipping")
                continue
            print(f"Running file #{idx+1}. File path: {f}")
            result = subprocess.run(
                [
                    "python3",
                    test_single_ply,
                    "--objname",
                    string_file_path,
                    "--ckpt_path",
                    model_pth,
                ],
                capture_output=True,
                text=True,
            )
            if result.stderr != "":
                print("Error:", result.stderr)
            if result.returncode != 0:
                print("Return Code:", result.returncode)

            predicted_score_line = result.stdout.splitlines()[-1]
            score = float(predicted_score_line.split(':')[1].strip())
            append_to_dict(output_path, string_file_path, score)
            print(f"Time: {time.time() - start} s")


if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        data = yaml.safe_load(file)
    run_mm_pcqa(data)