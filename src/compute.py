import subprocess
import os
import time
import psutil  

# Configuration
TIME_LIMIT = 5  # seconds
MEMORY_LIMIT_MB = 512  # Maximum memory in MB
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
            text=True
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
                break  # If the process terminated early

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

        if stderr:
            return None, stderr.strip(), peak_memory / 1024 / 1024 , 0

        return stdout.strip(), status, peak_memory / 1024 / 1024, execution_time

    except Exception as e:
        if process:
            kill_process_and_children(process.pid)
        return None, str(e), peak_memory / 1024 / 1024, 0

# Create Python file with test cases
code_template = """class Solution:
    def nth_prime(self, n):
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
def solve():
    solution = Solution()
    return solution.nth_prime({test_case})
print(solve())
"""

file_path = "./tmp/prime_test.py"
os.makedirs("./tmp", exist_ok=True)

# Write the code file
for test_case , test_value in test_cases.items():
    with open(file_path, "w") as f:
        f.write(code_template.format(test_case = test_case))

    # Execute the code
    output, status, memory_usage, execution_time = execute_code_in_isolation(file_path, TIME_LIMIT)

    # Print results
    print("\nExecution Results:")
    if status == "SUCCESS":
        print(output)
        print(str(output) == str(test_value))
        print(f"Execution Time: {execution_time:.4f} sec")
        print(f"Memory Usage: {memory_usage:.2f} MB")
    else:
        print(f"Error: {status}")

# Clean up the temporary file
#os.remove(file_path)