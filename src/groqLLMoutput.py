import sys
import os
import groq
import json
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from prompts.prompt import prompt
from dotenv import load_dotenv # type: ignore
import tqdm

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=GROQ_API_KEY)
df = pd.read_excel("benchmark_prototype.xlsx")
problem = df.problem_description
start = df.entry_point

Prompt = prompt(problem, start)

not_present = [6,8,9,10,11,13,14,15,16,18,19,20,23,26,27,29,30,31,34,36,37,39,40,41,42,43,44,45]

def generate_response(prompt, model="qwen-qwq-32b", max_tokens=58250):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature= 0,
    )
    return response.choices[0].message.content

output = {}

for i in tqdm.tqdm(range(len(df)), desc="Processing problems"):
 if i in not_present:
        
    try:
        response = generate_response(prompt(df.problem_description[i], df.entry_point[i])).split("```python\n")[1].split("```")[0]
        output["Solution_" + str(i)] = response
    except Exception as e:
        continue

with open("data/qwen-qwq-32b2.json", "w") as f:
    json.dump(output, f, indent=4)