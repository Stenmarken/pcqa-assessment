from scipy import stats
import json
from pathlib import Path
import copy
import numpy as np


def remove_negative_ones(grouped_scores):
    """
    A score of -1 means that something went wrong with the execution.
    This function removes the dicts where one of the scores are -1
    """
    grouped_copy = copy.deepcopy(grouped_scores)
    for k, v in grouped_scores.items():
        if -1 in v.values():
            del grouped_copy[k]
    return grouped_copy


def group_scores(scores_dict):
    grouped_scores = {}
    for path, score in scores_dict.items():
        path = Path(path)
        file_name = path.name
        if file_name not in grouped_scores:
            grouped_scores[file_name] = {}
        alpha_val = path.parts[-2]
        grouped_scores[file_name][alpha_val] = score
    return grouped_scores

def sorted_scores(grouped_scores):
    return  {
        k: v
        for k, v in sorted(grouped_scores.items(), key=lambda item: item[1], reverse=True)
    }

def main(scores_dict):
    ground_truth = ['alpha_0.005_ply', 'alpha_0.01_ply', 'alpha_0.02_ply', 'alpha_0.03_ply', 'alpha_0.06_ply', 'alpha_0.09_ply', 'alpha_0.12_ply', 'alpha_0.15_ply', 'alpha_0.18_ply', 'alpha_0.21_ply']
    sorted_grouped = remove_negative_ones(group_scores(scores_dict))
    sprc_d = {}
    for k, scores in sorted_grouped.items():
        sorted_scores = {
            k: v
            for k, v in sorted(scores.items(), key=lambda item: item[1])
        }
        sprc_val = stats.spearmanr(a=ground_truth, b=list(sorted_scores.keys()))
        sprc_d[k] = sprc_val
    sroccs = np.array([sprc_d[k].statistic for k in sprc_d.keys()])
    print(f'sroccs[:20]: {list(map(lambda x: float(round(x, 2)), sroccs[:20]))}')
    print(f'len(sroccs): {len(sroccs)}')
    print(f'Mean: {np.mean(sroccs):.2f}')
    print(f'Standard deviation: {np.std(sroccs):.2f}')


if __name__ == "__main__":
    path = "output.json"
    with open(path, "r") as f:
        d = json.load(f)
    main(d)