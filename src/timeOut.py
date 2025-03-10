import threading
import time

time_limits = {
    "easy": 2,
    "medium": 5,
    "hard": 10
}

def run_with_timeout(method, inputs, level):
    result = None
    exception_error = ""

    def target():
        nonlocal result, exception_error
        try:
            result = method(*inputs)
        except Exception as e:
            exception_error = str(e)

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(time_limits[level])

    if thread.is_alive():
        exception_error = "Timeout"
        thread.join(0)

    return result, exception_error

# Sample function to test
def sample_function(x, y):
    time.sleep(x)
    return x + y

# Test it
result, error = run_with_timeout(sample_function, (3, 5), "hard")
print("Result:", result)
print("Error:", error)
