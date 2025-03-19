import json
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
            #print(f"Monotonic: {lst}")
            print_list_two_decimals("Monotonic", lst)
            num_monotonic += 1
        else:
            #print(f"Not monotonic: {lst}")
            print_list_two_decimals("Not monotonic", lst)
        n += 1
    print(f"Number of monotonic: {num_monotonic}")
    print(f"In total: {n}")

if __name__ == "__main__":
    main("output/output.json")