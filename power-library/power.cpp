#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <vector>

namespace py = pybind11;

py::array_t<double> power_iteration(py::array_t<double> matrix, int max_iterations, double tolerance) {
    auto buf = matrix.request();
    int n = buf.shape[0];
    double* ptr = static_cast<double*>(buf.ptr);

    std::vector<double> b_k(n, 1.0); // Start with ones
    std::vector<double> b_k1(n);

    for (int iter = 0; iter < max_iterations; ++iter) {
        // Matrix-vector multiplication
        for (int i = 0; i < n; ++i) {
            b_k1[i] = 0;
            for (int j = 0; j < n; ++j) {
                b_k1[i] += ptr[i * n + j] * b_k[j];
            }
        }

        // Normalize
        double norm = 0;
        for (int i = 0; i < n; ++i) norm += b_k1[i] * b_k1[i];
        norm = std::sqrt(norm);
        for (int i = 0; i < n; ++i) b_k1[i] /= norm;

        // Check convergence
        double diff = 0;
        for (int i = 0; i < n; ++i) diff += std::pow(b_k1[i] - b_k[i], 2);
        if (std::sqrt(diff) < tolerance) break;

        b_k = b_k1;
    }

    return py::array_t<double>(n, b_k.data());
}

PYBIND11_MODULE(power_cpp, m) {
    m.def("power_iteration", &power_iteration, "Power Iteration",
          py::arg("matrix"), py::arg("max_iterations"), py::arg("tolerance"));
}
