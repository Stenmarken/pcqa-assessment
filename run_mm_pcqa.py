from pathlib import Path
import subprocess


def run_mm_pcqa(path):
    all_files = [file for file in path.rglob("*") if file.is_file()]
    for f in all_files:
        result = subprocess.run(
            [
                "python3",
                "../pcqas/MM-PCQA/test_single_ply.py",
                "--objname",
                str(f),
                "--ckpt_path",
                "../pcqas/MM-PCQA/model_files/WPC.pth",
            ],
            capture_output=True,
            text=True,
        )
        print("Output:", result.stdout)
        print("Error:", result.stderr)
        print("Return Code:", result.returncode)
        print("\n")


if __name__ == "__main__":
    path = Path("output/distorted_ply")
    print(run_mm_pcqa(path))
    # main()
