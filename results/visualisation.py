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
        keys = list(outputs.keys())
        mean_scores = [outputs[key]["mean_score"] for key in keys]
        efficiency_scores = [outputs[key]["efficiency_score"] for key in keys]
        total_scores = [outputs[key]["total_score"] for key in keys]

        x = np.arange(len(keys))  # the label locations
        width = 0.25  # the width of the bars

        fig, ax = plt.subplots(figsize=(10, 6))

        rects1 = ax.bar(x - width, mean_scores, width, label='Mean Score')
        rects2 = ax.bar(x, efficiency_scores, width, label='Efficiency Score')
        rects3 = ax.bar(x + width, total_scores, width, label='Total Score')

        # Add some text for labels, title, and custom x-axis tick labels
        ax.set_xlabel('Files')
        ax.set_ylabel('Scores')
        ax.set_title('Comparison of Scores by File')
        ax.set_xticks(x)
        ax.set_xticklabels(keys, rotation=45, ha="right")
        ax.legend()

        # Display the plot
        plt.tight_layout()
        plt.show()
        
plotG()