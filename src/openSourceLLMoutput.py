from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer
from huggingface_hub import login
from prompt.prompt import prompt
import pandas as pd 
import numpy as np
import torch
import json
import os
import re

def load_model(model_name):
    login("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")
    print(f"Loading model: {model_name}...")

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        device_map="auto", 
        trust_remote_code=True, 
        torch_dtype=torch.float16
    )

    return model, tokenizer

model, tokenizer = load_model("meta-llama/Llama-3.2-1B")

prompt =  "give me a python code snippet that reads a csv file and prints the first 5 rows of the dataframe"
def generate_response(model, tokenizer, prompt, max_length=512):
    """Generates a response from the model given a prompt."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        output_ids = model.generate(**inputs, max_length=max_length)
    
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response

response = generate_response(model, tokenizer, prompt)
print(response)

