import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler
import numpy as np

ms_pcqe_0000_0_ply = [1.35, 1.32, 1.33, 1.32, 1.31, 1.29, 1.35, 1.33, 1.33, 1.51]
mm_pcqa_0000_0_ply = [-40.6688232421875, 
           -50.334129333496094, 
           -52.41478729248047,
           -53.45233917236328,
           -41.28671646118164,
           -47.16729736328125,
           -38.43882751464844,
           -58.071502685546875,
           -54.25508117675781,
           -27.960275650024414]

def visualize_one_fig():
    scaler = StandardScaler()
    colors = ["red", "blue"]
    metrics = ['ms_pcqe', 'mm_pcqa']
    scores_dict = {'mm_pcqa': [-40.6688232421875, 
                                -50.334129333496094, 
                                -52.41478729248047,
                                -53.45233917236328,
                                -41.28671646118164,
                                -47.16729736328125,
                                -38.43882751464844,
                                -58.071502685546875,
                                -54.25508117675781,
                                -27.960275650024414],
                    'ms_pcqe': [1.35, 1.32, 1.33, 1.32, 1.31, 1.29, 1.35, 1.33, 1.33, 1.51]
                }
    plt.figure(figsize=(10, 8))
    for i in range(2):
        xs = []
        ys = []
        scores = scores_dict[metrics[i]]
        print(scores)
        metric_name = metrics[i]
        image_names = [i for i in range(10)]
        for img in image_names:
            xs.append(img)
            ys.append(scores[img])
            ys_norm = scaler.fit_transform(np.array(ys).reshape(-1, 1))
        plt.scatter(xs, ys_norm, color=colors[i % len(colors)], s=10, label=metric_name)
    plt.xlabel("Noise severity")
    plt.ylabel("Normalized")
    plt.title(f"Normalized scores for NR-PCQA metrics at different severities")
    plt.legend(title="Metrics", loc="upper right")
    file_name = "_".join(map(str, metrics))
    full_path = os.path.join('.', file_name)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    plt.savefig(full_path, bbox_inches="tight")
    print(f"Plot saved as {full_path}")

if __name__ == "__main__":
    plt.rcParams.update(
        {
            "font.size": 14,  # Default text size
            "axes.titlesize": 16,  # Title size
            "axes.labelsize": 14,  # X and Y label size
            "xtick.labelsize": 12,  # X tick size
            "ytick.labelsize": 12,  # Y tick size
            "legend.fontsize": 12,  # Legend text size
        }
    )
    visualize_one_fig()