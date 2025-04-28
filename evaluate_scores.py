import json
from pathlib import Path
import matplotlib.pyplot as plt

def is_monotonic(lst):
    increasing = all(x <= y for x, y in zip(lst, lst[1:]))
    decreasing = all(x >= y for x, y in zip(lst, lst[1:]))
    return increasing or decreasing

def print_list_two_decimals(prefix, lst):
    formatted_numbers = [f"{number:.2f}" for number in lst]
    number_string = " ".join(formatted_numbers)
    print(prefix, number_string)

def main(path):
    filenames = {f"{i:06d}.ply" for i in range(1, 101)}

    with open(path, "r") as f:
        d = json.load(f)
    grouped_scores = {f : {} for f in filenames}
    for k, v in d.items():
        k_split = k.split('/')
        distortion, filename = k_split[-2], k_split[-1]
        if float(filename[:-3]) > 100:
            continue
        grouped_scores[filename][distortion] = v
    num_monotonic = 0
    n = 0
    for k, v in grouped_scores.items():
        lst = [v["light_ply"], v["moderate_ply"], v["heavy_ply"]]
        if is_monotonic(lst):
            print_list_two_decimals("Monotonic", lst)
            num_monotonic += 1
        else:
            print_list_two_decimals("Not monotonic", lst)
        n += 1
    print(f"Number of monotonic: {num_monotonic}")
    print(f"In total: {n}")

def plot_scores(path):
    def trim_path(k):
        k_path = Path(k)
        return Path(f"{k_path.parent.name}/{k_path.name}")

    with open(path, "r") as f:
        d = json.load(f)
    transformed_d = {trim_path(k) : v for k, v in d.items()}

    points = []
    color_dict = {"light_ply": "green", "moderate_ply": "yellow", "heavy_ply": "red"}
    for k, v in transformed_d.items():
        points.append((int(k.stem), v, color_dict[str(k.parent)]))
    x_values = [p[0] for p in points]
    y_values = [p[1] for p in points]
    colors = [p[2] for p in points]
    plt.scatter(x_values, y_values, c=colors)
    plt.xlabel("X Axis")
    plt.ylabel("Y Axis")
    plt.title("Colored Points Plot")
    plt.grid(True)

    plt.show()

if __name__ == "__main__":
    main("output.json")
    #plot_scores("output/output.json")