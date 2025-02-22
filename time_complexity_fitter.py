import json
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define common time complexity functions
def O_1(n, a):          return a * np.ones_like(n)              
def O_log_n(n, a):      return a * np.log(n)                     
def O_n(n, a):          return a * n                             
def O_n_log_n(n, a):    return a * n * np.log(n)                 
def O_n2(n, a):         return a * n**2                          
def O_n2_log_n(n, a):   return a * n**2 * np.log(n)              
def O_n3(n, a):         return a * n**3                          

# List of all complexity functions to test
complexities = {
    "O(1)": O_1,
    "O(log n)": O_log_n,
    "O(n)": O_n,
    "O(n log n)": O_n_log_n,
    "O(n^2)": O_n2,
    "O(n^2 log n)": O_n2_log_n,
    "O(n^3)": O_n3
}

def estimate_complexity(n_values, time_values):
    best_fit = None
    best_error = float("inf")

    for label, func in complexities.items():
        try:
            # Fit the function to the execution time data
            popt, _ = curve_fit(func, n_values, time_values, maxfev=5000)
            predicted = func(n_values, *popt)

            # Compute the error (sum of squared residuals)
            error = np.sum((time_values - predicted) ** 2)

            # Select the best-fitting function with the least error
            if error < best_error:
                best_error = error
                best_fit = label
        except:
            continue  # Skip if fitting fails for a function

    return best_fit

# Example Usage
if __name__ == "__main__":
    with open("testcases_generated/number_of_islands.json") as f:
        data = json.load(f)
    # Sample dataset (Input Size vs. Execution Time)
    
    n_values = np.array([])  # Input sizes
    time_values = np.array([])
    for test in data.values():
        n_values = np.append(n_values, len(test["inputs"]["grid"][0]))
        time_values = np.append(time_values, test["excecution_time"])

    best_complexity = estimate_complexity(n_values, time_values)
    print(f"Estimated Time Complexity: {best_complexity}")

    # Visualization
    plt.scatter(n_values, time_values, label="Measured Data")
    
    # Fit and plot the best complexity curve
    func = complexities[best_complexity]
    popt, _ = curve_fit(func, n_values, time_values, maxfev=5000)
    plt.plot(n_values, func(n_values, *popt), label=f"Best Fit: {best_complexity}", linestyle="--")

    plt.xlabel("Input Size (n)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Time Complexity Estimation")
    plt.legend()
    plt.show()
