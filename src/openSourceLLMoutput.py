import json
import os
import re
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer
from huggingface_hub import login
from prompts.prompt import prompt
import torch
import pandas as pd
import tqdm
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Log in to Hugging Face Hub
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
if not HUGGINGFACE_TOKEN:
    HUGGINGFACE_TOKEN = input("Hugging Face token not found in environment. Please enter your Hugging Face token: ")
    if not HUGGINGFACE_TOKEN:
        raise ValueError("Hugging Face token is required to proceed.")
    # Save the token to the environment
    os.environ["HUGGINGFACE_TOKEN"] = HUGGINGFACE_TOKEN
login(HUGGINGFACE_TOKEN)

df = pd.read_excel("benchmark_prototype.xlsx")
problem = df.problem_description
start = df.entry_point

def load_model(model_name):
    login("")
    print(f"Loading model: {model_name}...")

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        device_map="auto", 
        trust_remote_code=True, 
        torch_dtype=torch.float16
    )

    return model, tokenizer

model_name = input("Enter the model name (e.g., meta-llama/Llama-3.2-1B): ")

model, tokenizer = load_model("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B" if len(model_name) <= 0 else model_name) 

output = {}

def generate_response(model, tokenizer, prompt, max_length=512):
    """Generates a response from the model given a prompt."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output_ids = model.generate(**inputs, max_length=max_length)
    
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

for i in tqdm.tqdm(range(len(df)), desc="Processing problems"):
    response = generate_response(model, tokenizer, prompt(df.problem_description[i], df.entry_point[i]))
    output["Solution_" + str(i)] = response

with open(f"data/{model_name}", "w") as f:
    json.dump(output, f, indent=4)
