import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

# Extended complexity functions
def O_1(n, a):           return a * np.ones_like(n)
def O_log_n(n, a):       return a * np.log(n)
def O_n(n, a):           return a * n
def O_n_log_n(n, a):     return a * n * np.log(n)
def O_n2(n, a):          return a * n**2
def O_n2_log_n(n, a):    return a * n**2 * np.log(n)
def O_n3(n, a):          return a * n**3

complexities = {
    "O(1)": O_1,
    "O(log n)": O_log_n,
    "O(n)": O_n,
    "O(n log n)": O_n_log_n,
    "O(n^2)": O_n2,
    "O(n^2 log n)": O_n2_log_n,
    "O(n^3)": O_n3,

}

def estimate_complexity(n_values, time_values):
    best_fit = None
    best_r2 = -float("inf")

    for label, func in complexities.items():
        try:
            popt, _ = curve_fit(func, (n_values), time_values, maxfev=5000)
            predicted = func(n_values, *popt)
            r2 = r2_score(time_values, predicted)

            if r2 > best_r2:
                best_r2 = r2
                best_fit = label
        except:
            continue

    return best_fit, best_r2

def extract_features(data):
    n_values = []
    time_values = []
    for test in data.values():
        inputs = test["inputs"]
        if "grid" in inputs:
            n_values.append(len(inputs["grid"]))
            m_values.append(len(inputs["grid"][0]))
        elif "nums" in inputs:
            n_values.append(len(inputs["nums"]))
            m_values.append(1)  # Default to 1 if there's no second dimension
        time_values.append(test["excecution_time"])
    return np.array(n_values), np.array(m_values), np.array(time_values)

if __name__ == "__main__":
    with open("kth_largest_element_in_an_array.json") as f:
        data = json.load(f)
    
    n_values, m_values, time_values = extract_features(data)
    
    best_complexity, r2_score = estimate_complexity(n_values, m_values, time_values)
    print(f"Estimated Time Complexity: {best_complexity}")
    print(f"R-squared score: {r2_score}")

    plt.scatter(n_values, time_values, label="Measured Data")
    
    func = complexities[best_complexity]
    popt, _ = curve_fit(func, (n_values, m_values), time_values, maxfev=5000)
    plt.plot(n_values, func(n_values, m_values, *popt), label=f"Best Fit: {best_complexity}", linestyle="--")

    plt.xlabel("Input Size (n)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Time Complexity Estimation")
    plt.legend()
    plt.show()
