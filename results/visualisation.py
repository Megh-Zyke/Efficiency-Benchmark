import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def computeScore(filename):
    efficiency_score = filename.groupby("question")["score"].mean().mean()
    scores = []
    pass_scores = filename.groupby("question")["pass"].apply(list).reset_index()
    for i in range(len(pass_scores)):
        count = 0
        pass_val = 0
        for val in pass_scores["pass"][i]:
            if val:
                pass_val += 1
            count += 1
        scores.append(pass_val/count)

    return np.mean(scores) , efficiency_score


# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# List all files in the directory
files = os.listdir(current_directory)

outputs = {}

for file in files:
    if file.endswith(".csv"):
        # Read the CSV file into a DataFrame
        df = pd.read_csv("results/"+file)
        # Compute the score
        mean_score, efficiency_score = computeScore(df)

        if file == "demo.csv":
             efficiency_score = efficiency_score / 100
        # Store the scores in the dictionary
        outputs[file] = {
            "mean_score": mean_score,
            "efficiency_score": efficiency_score,
            "total_score" : mean_score * efficiency_score
        }
def plotG():
    # Ensure demo.csv is always first
    keys = sorted(outputs.keys(), key=lambda x: (x != "optimal_human_code.csv", x))
    mean_scores = [outputs[key]["mean_score"] for key in keys]
    efficiency_scores = [outputs[key]["efficiency_score"] for key in keys]
    total_scores = [outputs[key]["total_score"] for key in keys]

    x = np.arange(len(keys))  # the label locations
    width = 0.5  # the width of the bars

    # Plot Mean Score
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x, mean_scores, width, label='Mean Score', color='blue')
    ax.set_xlabel('Files')
    ax.set_ylabel('Pass @ 1 Score')
    ax.set_title('Pass@1 Score by File')
    ax.set_xticks(x)
    ax.set_xticklabels(keys, rotation=45, ha="right")
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

    # Plot Efficiency Score
    fig, ax = plt.subplots(figsize=(10, 6))
    rects2 = ax.bar(x, efficiency_scores, width, label='Efficiency Score', color='green')
    ax.set_xlabel('Files')
    ax.set_ylabel('Efficiency Score')
    ax.set_title('Efficiency Score by File')
    ax.set_xticks(x)
    ax.set_xticklabels(keys, rotation=45, ha="right")
    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

    # Plot Total Score
    fig, ax = plt.subplots(figsize=(10, 6))
    rects3 = ax.bar(x, total_scores, width, label='Total Score', color='red')
    ax.set_xlabel('Files')
    ax.set_ylabel('Total Score')
    ax.set_title('Total Score by File')
    ax.set_xticks(x)
    ax.set_xticklabels(keys, rotation=45, ha="right")
    for rect in rects3:
        height = rect.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

plotG()
