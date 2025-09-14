import numpy as np
import power_cpp

A = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 4]], dtype=np.float64)
result = power_cpp.power_iteration(A, max_iterations=1000, tolerance=1e-6)
print("Dominant Eigenvector:", result)
