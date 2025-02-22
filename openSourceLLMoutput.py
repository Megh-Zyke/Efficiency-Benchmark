from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer
from huggingface_hub import login
from prompt.prompt import prompt
import pandas as pd 
import numpy as np
import torch
import json
import os
import re

# os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

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
# propmt =  "What is the capital of France?"
# def generate_response(model, tokenizer, prompt, max_length=100):
#     """Generates a response from the model given a prompt."""
#     inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

#     with torch.no_grad():
#         output_ids = model.generate(**inputs, max_length=max_length)
    
#     response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
#     return response

# response = generate_response(model, tokenizer, prompt)
# print(response)

# import os
# from transformers import AutoModelForCausalLM, AutoTokenizer
# from huggingface_hub import login

# # Fix OpenMP duplicate runtime issue
# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# # Log in to Hugging Face (if needed)
# def authenticate_huggingface():
#     """Logs into Hugging Face using the access token."""
#     token = input("Enter your Hugging Face token: ").strip()
#     login(token)
#     print("Successfully logged into Hugging Face!")

# # Function to load model and tokenizer
# def load_model(model_name):
#     """Loads a Hugging Face model and tokenizer based on the model type."""
#     print(f"Loading model: {model_name}...")

#     tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

#     model = AutoModelForCausalLM.from_pretrained(
#         model_name, 
#         device_map="auto", 
#         trust_remote_code=True, 
#         torch_dtype=torch.float16
#     )

#     return model, tokenizer

# # Function to generate response
# def generate_response(model, tokenizer, prompt, max_length=100):
#     """Generates a response from the model given a prompt."""
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     inputs = tokenizer(prompt, return_tensors="pt").to(device)

#     with torch.no_grad():
#         output_ids = model.generate(**inputs, max_length=max_length)
    
#     response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
#     return response

# if __name__ == "__main__":
#     model_name = "meta-llama/Llama-3.2-1B"  # Ensure this is a valid Hugging Face model
#     model, tokenizer = load_model(model_name)

#     prompt = "What is the capital of France?"
#     response = generate_response(model, tokenizer, prompt)

#     print("\nGenerated Response:\n", response)
