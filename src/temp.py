import numpy as np
import pandas as pd 
import time 
import json
import os 

data_path = "./benchmark_prototype.xlsx"
data = pd.read_excel(data_path)
questions = data["question"]

def compute_score(filename):
    """Computes the score of the generated code."""
    # Load the generated code
    path = "data/" + filename
    try:
        with open(path, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("File is not a valid JSON")

    for question , solution in data.items():
        question_id = int(question.split("_")[1])
        print(questions[question_id])
       
        
    
compute_score("demo.json")