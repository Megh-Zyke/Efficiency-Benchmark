import torch
import numpy as np
import os

print("NumPy Version:", np.__version__)

# Check for multiple OpenMP libraries
os.system("where libiomp5md.dll")  # Windows

