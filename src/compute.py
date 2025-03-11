import subprocess
import json
import os
import time
import psutil  # For memory tracking
import pandas as pd
from tqdm import tqdm

# Configuration
TIME_LIMIT = 5  # seconds
MEMORY_LIMIT_MB = 512  # Maximum memory in MB

# Paths
data_path = "./benchmark_prototype.xlsx"
results_path = "./results"
os.makedirs(results_path, exist_ok=True)

# Read the questions
data = pd.read_excel(data_path)
questions = data["question"]

# Utility function to convert MB to bytes
MEMORY_LIMIT_BYTES = MEMORY_LIMIT_MB * 1024 * 1024

# Expected test cases
test_cases = {
    5: 41,
    7: 17,
    10: 29
}

# Function to forcefully kill a process and its children (Windows)
def kill_process_and_children(pid):
    try:
        process = psutil.Process(pid)
        for child in process.children(recursive=True):
            child.kill()
        process.kill()
    except psutil.NoSuchProcess:
        pass  # Ignore if the process already terminated

# Function to execute code in an isolated process
def execute_code_in_isolation(file_path, timeout):
    process = None
    peak_memory = 0
    status = "SUCCESS"

    try:
        # Launch the Python code as a subprocess
        process = subprocess.Popen(
            ['python', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Ensure text mode output
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )

        # Monitor the process in real-time
        start_time = time.time()
        while process.poll() is None:
            current_time = time.time()

            # Track memory usage in real-time
            try:
                mem_info = psutil.Process(process.pid).memory_info().rss
                peak_memory = max(peak_memory, mem_info)
            except psutil.NoSuchProcess:
                # If the process terminated early, break
                break

            # Handle timeouts
            if current_time - start_time > timeout:
                kill_process_and_children(process.pid)
                status = "TIME_LIMIT_EXCEEDED"
                return None, status, peak_memory / 1024 / 1024

            # Handle memory limits
            if peak_memory > MEMORY_LIMIT_BYTES:
                kill_process_and_children(process.pid)
                status = "MEMORY_LIMIT_EXCEEDED"
                return None, status, peak_memory / 1024 / 1024

        # Capture output and error
        stdout, stderr = process.communicate()
        execution_time = time.time() - start_time

        # Handle runtime errors
        if stderr:
            return None, stderr.strip(), peak_memory / 1024 / 1024

        return stdout.strip(), status, peak_memory / 1024 / 1024

    except Exception as e:
        if process:
            kill_process_and_children(process.pid)
        return None, str(e), peak_memory / 1024 / 1024


# Function to benchmark all completions
def benchmark_completions(dataset_file):
    with open("data/" + dataset_file, "r") as f:
        dataset = json.load(f)

    results = []

    for question, solution in tqdm(dataset.items()):
        question_id = int(question.split("_")[1])
        question_filename = questions[question_id].lower().replace(" ", "_") + ".py"

        # Generate code for multiple test cases
        sol = """def nth_prime(n):
    if n < 6:
        limit = 15
    else:
        limit = int(n * (1.2 * (n**0.5)))
    
    sieve = [True] * (limit+1)
    sieve[0], sieve[1] = False, False
    
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit+1, i):
                sieve[j] = False
    
    primes = [i for i in range(len(sieve)) if sieve[i]]
    
    return primes[n-1]
"""

        # Create Python file with completion code
        file_path = f"./tmp/{question_filename}"
        os.makedirs("./tmp", exist_ok=True)

        with open(file_path, "w") as f:
            f.write(sol)

        # Execute the code in isolation
        output, status, memory_usage = execute_code_in_isolation(file_path, TIME_LIMIT)

        # Parse output
        assertions = {}
        if status == "SUCCESS" and output:
            output_lines = output.split("\n")
            for line in output_lines:
                try:
                    n, prime = map(int, line.split(":"))
                    assertions[n] = prime == test_cases[n]
                except:
                    pass

        # Capture results
        result = {
            "question_id": question_id,
            "file_name": question_filename,
            "status": status,
            "memory_usage_mb": round(memory_usage, 2),
            "error": output if status != "SUCCESS" else "",
            "assertions": assertions
        }
        results.append(result)

    # Save results as CSV
    df = pd.DataFrame(results)
    df.to_csv(f"{results_path}/benchmark_results.csv", index=False)

# Run the benchmark
benchmark_completions("groq_llama.json")
