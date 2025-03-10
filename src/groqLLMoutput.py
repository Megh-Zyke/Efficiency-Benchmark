import sys
import os
import groq
import json
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from prompts.prompt import prompt
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=GROQ_API_KEY)
df = pd.read_excel("benchmark_prototype.xlsx")
problem = df.problem_description
start = df.entry_point

Prompt = prompt(problem, start)

def generate_response(prompt, model="llama3-70b-8192", max_tokens=1024):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature= 0,
    )
    return response.choices[0].message.content

output = {}

for i in range(len(df)):
    response = generate_response(prompt(df.problem_description[i], df.entry_point[i])).split("```python\n")[1].split("```")[0]
    output["Solution_" + str(i)] = response

with open("data/groq_llama.json", "w") as f:
    json.dump(output, f, indent=4)